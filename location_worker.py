#!/usr/bin/env python3
"""
Persistent GPS location worker for Windows — zero administrator privileges.
Supports:
  1. iOS 17+ in-process Userspace RSD Tunnel (PyTCP - no TAP/TUN driver, no root/admin)
  2. iOS <= 16 Lockdown DtSimulateLocation fallback (via usbmux)
  3. Legacy host:port connection
"""
import sys
import json
import asyncio
import threading
import inspect
import os


WAS_READY = False


def conn_type():
    return 'Network' if os.environ.get('GPS_CONN_TYPE', '').lower() in ('wifi', 'network') else None


def is_admin() -> bool:
    try:
        import ctypes
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def emit(obj):
    try:
        sys.stdout.write(json.dumps(obj) + '\n')
        sys.stdout.flush()
    except Exception:
        pass


async def do_set(loc, lat: float, lng: float):
    if inspect.iscoroutinefunction(loc.set):
        await loc.set(lat, lng)
    else:
        await asyncio.to_thread(loc.set, lat, lng)


async def do_clear(loc):
    if hasattr(loc, 'clear'):
        if inspect.iscoroutinefunction(loc.clear):
            await loc.clear()
        else:
            await asyncio.to_thread(loc.clear)


async def message_loop(loc, mode_name: str):
    global WAS_READY
    WAS_READY = True
    emit({'status': 'ready', 'mode': mode_name})

    loop = asyncio.get_event_loop()
    cmd_queue: asyncio.Queue = asyncio.Queue()

    def stdin_reader():
        while True:
            try:
                line = sys.stdin.readline()
            except Exception:
                break
            if not line:
                loop.call_soon_threadsafe(cmd_queue.put_nowait, None)
                break
            stripped = line.strip()
            if stripped:
                loop.call_soon_threadsafe(cmd_queue.put_nowait, stripped)

    t = threading.Thread(target=stdin_reader, daemon=True)
    t.start()

    while True:
        try:
            cmd = await asyncio.wait_for(cmd_queue.get(), timeout=30.0)
        except asyncio.TimeoutError:
            continue

        if cmd is None or cmd == 'quit':
            try:
                await do_clear(loc)
            except Exception:
                pass
            break

        if cmd == 'ping':
            emit({'pong': True})
            continue

        if cmd == 'clear':
            try:
                await do_clear(loc)
                emit({'ok': True, 'action': 'clear'})
            except Exception as e:
                emit({'error': str(e)})
            continue

        if cmd == 'get-location':
            try:
                if hasattr(loc, 'get') and inspect.iscoroutinefunction(loc.get):
                    pos = await loc.get()
                    if pos and 'latitude' in pos:
                        emit({'ok': True, 'action': 'get-location', 'lat': pos['latitude'], 'lng': pos['longitude']})
                    else:
                        emit({'ok': False, 'action': 'get-location', 'error': 'No location data'})
                else:
                    emit({'ok': False, 'action': 'get-location', 'error': 'get-location not supported by engine'})
            except Exception as e:
                emit({'ok': False, 'action': 'get-location', 'error': str(e)})
            continue

        # Expected format: "lat,lng" or "set:lat,lng"
        if cmd.startswith('set:'):
            cmd = cmd[4:]

        try:
            lat_s, lng_s = cmd.split(',', 1)
            lat = float(lat_s.strip())
            lng = float(lng_s.strip())
        except Exception as e:
            emit({'error': f'Bad command: {e}'})
            continue
        try:
            await asyncio.wait_for(do_set(loc, lat, lng), timeout=5.0)
            emit({'ok': True, 'lat': lat, 'lng': lng})
        except Exception as e:
            # Device link is most likely gone (cable pulled / WiFi lost): report and exit so the app reconnects.
            emit({'error': f'Set location failed: {e!r}', 'fatal': True})
            sys.exit(2)


async def run_userspace_rsd(udid: str | None):
    """iOS 17+ WITHOUT admin (pymobiledevice3 >= 10): in-process PyTCP tunnel.
    Honors USB vs WiFi (usbmux 'Network') and falls back to RemotePairing over Bonjour on WiFi."""
    try:
        from pymobiledevice3.remote.userspace_tunnel import UserspaceRsdTunnel, TunnelProvider
    except ImportError:
        raise RuntimeError('NEED_UPGRADE: pymobiledevice3 qua cu (can >= 10), chay: pip install -U pymobiledevice3')
    from pymobiledevice3.lockdown import create_using_usbmux
    from pymobiledevice3.remote import tunnel_service
    from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider
    from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation

    ctype = conn_type()

    async def provider_factory():
        last_err = None
        lockdown = None
        try:
            lockdown = await create_using_usbmux(serial=udid, connection_type=ctype, autopair=True)
            return TunnelProvider(await tunnel_service.CoreDeviceTunnelProxy.create(lockdown), lockdown)
        except Exception as e:
            last_err = e
            if lockdown is not None:
                try:
                    await lockdown.close()
                except Exception:
                    pass
        # WiFi fallback: RemotePairing over Bonjour (needs the phone awake on the same network)
        try:
            services = await tunnel_service.get_remote_pairing_tunnel_services(udid=udid, first_address_only=True)
        except Exception:
            services = []
        if services:
            return TunnelProvider(services[0])
        raise last_err or RuntimeError('Khong tim thay iPhone qua WiFi')

    async with UserspaceRsdTunnel(serial=udid, provider_factory=provider_factory) as rsd:
        async with DvtProvider(rsd) as dvt:
            async with LocationSimulation(dvt) as loc:
                await message_loop(loc, 'userspace-rsd')


async def run_tunnel_rsd(udid: str | None):
    """iOS 17+: CoreDeviceProxy tunnel -> RSD -> DVT LocationSimulation.
    pymobiledevice3 >= 9 needs a TUN adapter, so this requires Administrator on Windows."""
    from pymobiledevice3.lockdown import create_using_usbmux
    from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
    from pymobiledevice3.remote.tunnel_service import CoreDeviceTunnelProxy
    from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider
    from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation

    lockdown = await create_using_usbmux(serial=udid, connection_type=conn_type())
    proxy = await CoreDeviceTunnelProxy.create(lockdown)
    try:
        async with proxy.start_tcp_tunnel() as tunnel:
            async with RemoteServiceDiscoveryService((tunnel.address, tunnel.port)) as rsd:
                async with DvtProvider(rsd) as dvt:
                    async with LocationSimulation(dvt) as loc:
                        await message_loop(loc, 'tunnel-rsd')
    finally:
        try:
            await proxy.close()
        except Exception:
            pass


async def run_lockdown(udid: str | None):
    """iOS <= 16: DtSimulateLocation through lockdown (create_using_usbmux is async in v9)."""
    from pymobiledevice3.lockdown import create_using_usbmux
    from pymobiledevice3.services.simulate_location import DtSimulateLocation

    lockdown = await create_using_usbmux(serial=udid, connection_type=conn_type())
    try:
        major = int(str(lockdown.product_version).split('.')[0])
    except Exception:
        major = 0
    if major >= 17:
        raise RuntimeError(f'iOS {lockdown.product_version} requires the RSD tunnel (lockdown simulation unsupported)')
    loc = DtSimulateLocation(lockdown)
    try:
        await message_loop(loc, 'lockdown')
    finally:
        try:
            r = loc.close()
            if inspect.isawaitable(r):
                await r
        except Exception:
            pass


async def run_host_port(host: str, port: int):
    from pymobiledevice3.remote.remote_service_discovery import RemoteServiceDiscoveryService
    from pymobiledevice3.services.dvt.instruments.dvt_provider import DvtProvider
    from pymobiledevice3.services.dvt.instruments.location_simulation import LocationSimulation

    async with RemoteServiceDiscoveryService((host, port)) as rsd:
        async with DvtProvider(rsd) as dvt:
            async with LocationSimulation(dvt) as loc:
                await message_loop(loc, 'host-port')


async def main_async():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    second = sys.argv[2] if len(sys.argv) > 2 else None

    # Check if host and port were provided: e.g. python location_worker.py 127.0.0.1 5555
    if target and second and second.isdigit():
        await run_host_port(target, int(second))
        return

    udid = None if (not target or target.lower() in ('auto', 'none', 'default')) else target

    # iOS 17+ first (tunnel -> RSD -> DVT), then iOS <= 16 lockdown fallback
    e_user = None
    try:
        await run_userspace_rsd(udid)
        return
    except Exception as e:
        e_user = e
        if WAS_READY:
            # Connection dropped after it was working (cable pulled / WiFi lost): exit so the app reconnects.
            emit({'error': f'Mất kết nối iPhone: {e!r}'})
            sys.exit(1)
        if 'NEED_UPGRADE' in str(e):
            emit({'error': str(e), 'need_upgrade': True})
            sys.exit(1)

    try:
        await run_tunnel_rsd(udid)
        return
    except Exception as e_rsd:
        try:
            await run_lockdown(udid)
            return
        except Exception as e_lock:
            hint = ''
            if sys.platform == 'win32' and not is_admin():
                hint = ' (iOS 17+ cần chạy app bằng quyền Administrator)'
            emit({'error': f'Failed connecting to device{hint}: Userspace={e_user!r} | RSD={e_rsd!r} | Lockdown={e_lock!r}'})
            sys.exit(1)


def main():
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        emit({'error': str(e)})
        sys.exit(1)


if __name__ == '__main__':
    main()
