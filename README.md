# 📍 iOS GPS Pro by BraveHoang (v1.0.4)

> Ứng dụng Desktop (Electron) giả lập và điều khiển định vị GPS cho iPhone/iPad kết nối máy tính qua **cáp USB** hoặc **Wi-Fi**.
> Bản đồ vệ tinh Google Maps có tên đường tiếng Việt, nhận diện tọa độ DMS, mô phỏng lộ trình thực tế chống phát hiện.
>
> ⚠️ **Lưu ý quan trọng (v1.0.4):** iPhone chạy **iOS 17 trở lên** (kể cả iOS 26) cần tạo kênh tunnel ảo nên **bắt buộc chạy app bằng quyền Administrator** trên Windows. Bản cũ ghi "Zero-Admin" không còn đúng với `pymobiledevice3` 9.x.

---

## 🌟 1. Các tính năng nổi bật (Features)

1. **🔌📶 Hai giao thức kết nối: Cáp USB và Wi-Fi**:
   - Công tắc **🔌 Cáp USB | 📶 WiFi** ngay trong mục *Thiết bị*, lựa chọn được ghi nhớ cho lần mở sau.
   - Chế độ USB: cắm cáp là dùng, ổn định nhất.
   - Chế độ WiFi: dùng được sau khi bật *Sync qua Wi-Fi* (xem mục 6).
   - Bản đồ hiển thị ngay khi mở app, việc kết nối iPhone chạy nền (không còn phải chờ).

2. **🌍 Bản đồ vệ tinh Google Maps Hybrid chuẩn tiếng Việt**:
   - Sử dụng lớp vệ tinh độ nét cao của Google Maps tích hợp lớp phủ tên đường, phường/xã, quận/huyện, tỉnh/thành phố và địa danh (POI) sắc nét bằng tiếng Việt.
   - Hỗ trợ chuyển đổi nhanh 3 chế độ xem: `🌍 Vệ tinh (Google)`, `🗺️ Đường phố (Google)`, `🌐 OpenStreetMap`.

3. **🧭 Nhận diện & Dịch chuyển tọa độ thông minh (DMS & Thập phân)**:
   - Dán trực tiếp tọa độ định dạng Độ - Phút - Giây (DMS): ví dụ `21°01'56.3"N 105°50'08.4"E`.
   - Dán tọa độ thập phân: `21.032306, 105.835667` hoặc link chia sẻ từ Google Maps (`https://maps.google.com/?q=...`).
   - Có thể dán tại **Thanh tìm kiếm trên cùng** hoặc ô **Nhập tọa độ nhanh** ở Sidebar bên trái.

4. **📍 Xem trước vị trí trước khi dịch chuyển (Preview Confirmation)**:
   - Khi click lên bản đồ hoặc dán tọa độ: Ứng dụng cắm cọc ghim (Marker) và mở bảng Popup hiển thị chi tiết tên địa chỉ tiếng Việt + tọa độ Lat/Lng.
   - **Chỉ dịch chuyển khi bạn bấm nút xác nhận**: Bấm `🚀 Dịch chuyển tới đây` trên bảng Popup hoặc `🚀 Dịch chuyển vị trí` ở thanh Sidebar. Tránh tình trạng dịch chuyển nhầm vị trí.

5. **🔤 Gõ tiếng Việt có dấu mượt mà (Unikey / EVKey / Telex)**:
   - Xử lý bắt trọn sự kiện IME (`compositionstart` / `compositionend`), khắc phục triệt để lỗi nuốt dấu, mất chữ hay gián đoạn con trỏ khi gõ tiếng Việt.
   - Nâng cấp bộ máy tìm kiếm với **Photon Geocoder** (hỗ trợ tìm kiếm mờ tiếng Việt theo bán kính vị trí bản đồ hiện tại) và fallback OpenStreetMap Nominatim.

6. **🛣️ Mô phỏng lộ trình di chuyển (Route Navigation A → B)**:
   - Chọn điểm A (xuất phát) và B (đích đến) trực tiếp trên bản đồ.
   - Tự động vẽ lộ trình thực tế bám theo đường bộ bằng thuật toán **OSRM**.
   - Điều chỉnh tốc độ tùy thích (Đi bộ `3.6 km/h`, Xe đạp `15 km/h`, Xe máy `45 km/h`, Ô tô `80 km/h`...).
   - **Tính năng Anti-ban (Speed Jitter)**: Tự động biến thiên vận tốc ngẫu nhiên (±10%) như người lái xe thực tế để chống thuật toán phát hiện gian lận của game/ứng dụng.

7. **🕹️ Joystick điều khiển ảo (WASD & Phím mũi tên)**:
   - Di chuyển GPS theo thời gian thực bằng các phím `W`, `A`, `S`, `D` hoặc các phím mũi tên trên bàn phím.
   - Phù hợp chơi game AR (Pokémon GO, Monster Hunter Now...) hoặc test ứng dụng giao hàng/đặt xe.

8. **🔄 Khôi phục GPS thật (Reset Location)**:
   - Bấm nút `🔄 Khôi phục GPS thật` ở đầu thanh bên để xóa session giả lập và trả lại định vị vệ tinh GPS gốc của iPhone ngay lập tức.

9. **⏱️ Bộ tính thời gian chờ an toàn (Cooldown Calculator)**:
   - Tự động đo khoảng cách đường chim bay giữa điểm fake trước và điểm fake mới.
   - Đưa ra thời gian chờ khuyến cáo (từ 1 phút đến 120 phút) nhằm đảm bảo an toàn tuyệt đối cho tài khoản.

10. **⭐ Địa điểm Yêu thích & Lịch sử**:
    - Lưu các tọa độ thường dùng vào mục Yêu thích và quản lý lịch sử 25 lần dịch chuyển gần nhất.

---

## 🏗️ 2. Kiến trúc kỹ thuật (Technical Architecture)

```
┌─────────────────────────────────────────────────────────────┐
│                     Electron Renderer UI                    │
│   (index.html + style.css + app.js + Leaflet Google Maps)   │
└──────────────────────────────┬──────────────────────────────┘
                               │ IPC (preload.js)
┌──────────────────────────────▼──────────────────────────────┐
│                    Electron Main Process                    │
│        (main.js – tự nâng quyền Admin trên Windows)         │
└──────────────────────────────┬──────────────────────────────┘
                               │ stdin / stdout (JSON protocol)
┌──────────────────────────────▼──────────────────────────────┐
│              Python Worker (location_worker.py)             │
│  iOS 17+: CoreDeviceProxy tunnel → RSD → DVT LocationSim    │
│  iOS ≤ 16: Lockdown DtSimulateLocation                      │
└──────────────────────────────┬──────────────────────────────┘
                               │ usbmuxd (USB hoặc Network/Wi-Fi)
┌──────────────────────────────▼──────────────────────────────┐
│                    Thiết bị Apple iPhone                    │
└─────────────────────────────────────────────────────────────┘
```

### Cách hoạt động
- `main.js` khởi chạy `location_worker.py` một lần và giữ tiến trình nền, biến môi trường `GPS_CONN_TYPE` (`usb` / `wifi`) quyết định kết nối qua cáp hay mạng.
- Khi cần đổi vị trí, `main.js` ghi `lat,lng
` vào `stdin` của worker, worker trả JSON kết quả. Lỗi thật được hiển thị trên giao diện.
- **iOS 17+** cần một card mạng ảo (TUN) để mở tunnel → trên Windows phải có quyền Administrator. Khi chạy bản đã đóng gói, app tự hiện hộp thoại UAC để nâng quyền.
- **iOS ≤ 16** dùng dịch vụ `com.apple.dt.simulatelocation` qua lockdown, không cần Admin.

---

## 📁 3. Cấu trúc thư mục (Project Structure)

```
fake-gps-mobile/
├── main.js                  # Electron Main Process (quản lý cửa sổ, worker process, IPC)
├── preload.js               # ContextBridge an toàn giữa Electron và Renderer
├── location_worker.py       # Python daemon xử lý tunnel RSD (iOS 17+) / lockdown (iOS ≤ 16) & set location
├── package.json             # Cấu hình dự án & electron-builder
├── build/                   # Thư mục xuất file cài đặt (.exe portable & setup)
│   ├── IOS GPS by BraveHoang-1.0.4-portable.exe
│   └── IOS GPS by BraveHoang Setup 1.0.4.exe
├── renderer/                # Giao diện người dùng
│   ├── index.html           # HTML cấu trúc UI (Sidebar, Map container, Modals)
│   ├── style.css            # CSS giao diện Dark Modern Glassmorphism
│   ├── app.js               # Logic điều khiển Leaflet, tìm kiếm, OSRM, Joystick
│   └── vendor/leaflet/      # Leaflet đóng gói sẵn (không tải từ CDN, load nhanh hơn)
├── iconapp.png              # Icon ứng dụng (PNG)
├── iconapp.ico              # Icon ứng dụng định dạng Windows ICO
└── README.md                # Tài liệu hướng dẫn sử dụng và phát triển
```

---

## 💻 4. Yêu cầu môi trường & Cài đặt phát triển

### A. Yêu cầu hệ thống:
1. **Hệ điều hành**: Windows 10 hoặc Windows 11 (64-bit).
2. **Node.js**: Phiên bản 18+ trở lên (khuyên dùng LTS).
3. **Python**: Phiên bản 3.10 - 3.14 (đã tích chọn `Add Python to PATH` khi cài đặt).
4. **Apple Driver**: Đã cài iTunes bản desktop hoặc Apple Devices app (để máy tính nhận diện được driver `usbmuxd`).
5. **pymobiledevice3**: Thư viện giao tiếp iOS:
   ```bash
   pip install -U pymobiledevice3
   ```
6. **Quyền Administrator**: bắt buộc với iPhone iOS 17 trở lên (xem mục 6).

### B. Các bước chạy Development:
```bash
# 1. Clone mã nguồn
git clone https://github.com/huydung2002/fake-gps-mobile.git
cd fake-gps-mobile

# 2. Cài đặt các gói phụ thuộc Node.js
npm install

# 3. Khởi chạy ứng dụng
npm start
```

> Với iOS 17+, hãy mở **PowerShell / CMD bằng "Run as administrator"** rồi `cd` vào thư mục dự án trước khi chạy `npm start` (chế độ dev không tự nâng quyền).

---

## 📦 5. Hướng dẫn Đóng gói (Build) & Phát hành (Release)

### A. Đóng gói file chạy cho Windows:
Lệnh sau sẽ tự động đóng gói ứng dụng bằng `electron-builder`:
```bash
npm run dist
```
Sau khi build xong, thư mục `build/` sẽ chứa:
- **`IOS GPS by BraveHoang-1.0.4-portable.exe`**: Bản Portable mở lên chạy ngay không cần cài đặt.
- **`IOS GPS by BraveHoang Setup 1.0.4.exe`**: Bộ cài đặt chuẩn Windows tạo shortcut Desktop và Start Menu.

> **Lưu ý kỹ thuật khi đóng gói**:
> File `location_worker.py` được cấu hình trong `package.json` với `asarUnpack` và `extraResources`. Hàm `getLocationWorkerScriptPath()` trong [main.js](file:///f:/github/fake-gps-mobile/main.js) sẽ tự động dò tìm vị trí file script ở cả chế độ dev lẫn khi đã nén vào thư mục cài đặt `resources/`.

### B. Phát hành phiên bản mới lên GitHub Releases:
1. Tăng version trong `package.json` (ví dụ `1.0.4`).
2. Commit và gắn tag:
   ```bash
   git add -A
   git commit -m "release: v1.0.4"
   git push origin main
   git tag -a v1.0.4 -m "Release v1.0.4"
   git push origin v1.0.4
   ```
3. Đẩy file build lên GitHub Releases bằng `electron-builder`:
   ```powershell
   $env:GH_TOKEN = "your_personal_access_token_here"
   npm run dist -- --publish always
   ```

---

## 📱 6. Hướng dẫn sử dụng cho người dùng cuối

### Bước chuẩn bị (làm một lần)
1. **Tin cậy**: Cắm cáp USB, mở khóa iPhone và bấm **Tin cậy (Trust)** khi có thông báo.
2. **Developer Mode (iOS 16+)**: **Cài đặt** → **Quyền riêng tư & Bảo mật** → **Chế độ nhà phát triển** → Bật, rồi khởi động lại máy theo yêu cầu.
3. **Chạy app bằng Administrator** (bắt buộc với iOS 17+). Bản cài đặt sẽ tự hiện hộp thoại UAC, bấm **Yes**.

### Cách 1 – Kết nối bằng cáp USB (khuyên dùng)
1. Trong mục **Thiết bị**, chọn tab **🔌 Cáp USB**.
2. Giữ iPhone mở khóa, cắm cáp. App tự phát hiện và kết nối. Huy hiệu chuyển sang **● Đã kết nối ⚡**.

### Cách 2 – Kết nối qua Wi-Fi
1. Cắm cáp **một lần**, mở **iTunes / Apple Devices / Finder** → chọn iPhone → bật **Hiện iPhone này khi có Wi-Fi** (Show this iPhone when on Wi-Fi) → Áp dụng.
2. Rút cáp. Đảm bảo iPhone và máy tính **cùng một mạng Wi-Fi**, iPhone đang sáng màn hình.
3. Trong app chọn tab **📶 WiFi**, bấm **↻** để làm mới, chọn thiết bị trong danh sách.
4. Nếu không thấy, thử nút quét 📡 hoặc quay lại cáp USB.

### Dịch chuyển vị trí
1. Dán tọa độ vào thanh tìm kiếm / ô *Nhập tọa độ nhanh*, hoặc nhấp lên bản đồ.
2. Xem trước địa chỉ và bấm **🚀 Dịch chuyển tới đây**.
3. Kiểm tra bằng app Bản đồ trên iPhone. Nếu vẫn hiện vị trí cũ, thử mở lại app Bản đồ.
4. **Khôi phục**: bấm **🔄 Đặt lại vị trí thật (Reset GPS)** khi dùng xong.

---

## 🛠️ 7. Xử lý sự cố thường gặp (Troubleshooting)

| Lỗi | Nguyên nhân | Cách khắc phục |
| :--- | :--- | :--- |
| **Chưa thấy iPhone** | Cáp lỏng, chưa có driver, hoặc sai tab kết nối | Rút cắm lại cáp, mở khóa iPhone và bấm **Tin cậy**, cài iTunes/Apple Devices. Kiểm tra đang ở đúng tab USB / WiFi. |
| **Báo thành công nhưng vị trí không đổi / `Access is denied`** | iOS 17+ cần quyền Administrator để tạo tunnel | Đóng app, mở lại bằng **Run as administrator** (dev: mở terminal Admin rồi `npm start`). |
| **Không thấy iPhone ở tab WiFi** | Chưa bật Sync qua Wi-Fi, khác mạng, hoặc iPhone đang khóa | Làm lại mục "Cách 2" ở trên, đảm bảo cùng mạng và mở khóa iPhone. |
| **Lỗi ghép cặp Mux 183** | Bản ghi Trust cũ bị lỗi hoặc bị đổi máy | Mở khóa iPhone, chọn Trust lại. Nếu cần: Cài đặt → Cài đặt chung → Đặt lại vị trí & quyền riêng tư. |
| **Developer Mode required** | iOS 16+ yêu cầu bật chế độ nhà phát triển | Cài đặt → Quyền riêng tư & Bảo mật → Chế độ nhà phát triển → Bật. |
| **`'electron' is not recognized`** | Chưa cài thư viện Node | Chạy `npm install` trong thư mục dự án. |
| **Bản đồ không tải được** | Mất Internet hoặc bị chặn tile server | Kiểm tra mạng. Có thể chuyển sang lớp `🌐 OpenStreetMap`. |
| **File log chi tiết** | Cần xem log để sửa lỗi | Xem file `gps_debug.log` tại thư mục cài đặt hoặc `%APPDATA%/ios-gps-by-bravehoang/gps_debug.log`. |

---

## 📄 Bản quyền & Tác giả
- **Tác giả:** BraveHoang ([huydung2002](https://github.com/huydung2002))
- **Mã nguồn:** [https://github.com/huydung2002/fake-gps-mobile](https://github.com/huydung2002/fake-gps-mobile)
- **Giấy phép:** ISC License