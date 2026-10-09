# 🚦 Collision Warning System

Hệ thống **cảnh báo va chạm giao thông** (thuộc mảng ITS, hệ thống giao thông thông minh). Hệ thống nhận dữ liệu từ camera và phương tiện, phát hiện tình huống có nguy cơ va chạm rồi gửi **cảnh báo realtime** lên giao diện web.

---

## 📌 Mục lục
1. [Tổng quan](#-tổng-quan)
2. [Công nghệ sử dụng](#-công-nghệ-sử-dụng)
3. [Kiến trúc MVC](#-kiến-trúc-mvc)
4. [Cấu trúc thư mục](#-cấu-trúc-thư-mục)
5. [Cài đặt & chạy dự án](#-cài-đặt--chạy-dự-án)
6. [Database (MySQL)](#-database-mysql)
7. [CI/CD](#️-cicd)
8. [Quy trình làm việc nhóm (Git)](#-quy-trình-làm-việc-nhóm-git)
9. [Quy ước code](#-quy-ước-code)

---

## 🔭 Tổng quan

```
 Camera / Xe ──► Backend (FastAPI) ──► Phát hiện & tính nguy cơ va chạm
                     │        ▲
                     ▼        │ REST API + WebSocket
                  MySQL    Frontend (React) ──► Dashboard, bản đồ, popup cảnh báo
```

**Chức năng chính dự kiến:**
- 🔐 Đăng nhập / phân quyền người dùng
- 🚗 Quản lý phương tiện (vehicle)
- 📷 Quản lý camera và xem luồng hình ảnh, có vẽ khung nhận diện
- ⚠️ Phát hiện nguy cơ va chạm (collision event)
- 🔔 Gửi cảnh báo realtime qua WebSocket
- 🗺️ Hiển thị phương tiện và cảnh báo trên bản đồ

---

## 🛠 Công nghệ sử dụng

| Thành phần | Công nghệ |
|---|---|
| Backend | Python 3.12, **FastAPI**, SQLAlchemy, Alembic, Pydantic |
| Frontend | **React 18 + TypeScript + Vite**, React Router, Axios, Leaflet |
| Database | **MySQL 8.0** |
| Realtime | WebSocket |
| Triển khai | Docker, Docker Compose, Nginx |
| CI/CD | GitHub Actions, GitHub Container Registry (GHCR) |

---

## 🧱 Kiến trúc MVC

| Lớp | Vị trí | Vai trò |
|---|---|---|
| **Model** | `BE/app/models/` và MySQL | Định nghĩa bảng dữ liệu, thao tác với DB |
| **View** | `FE/` (React), `BE/app/schemas/` | Giao diện người dùng; schema quy định dữ liệu vào/ra API |
| **Controller** | `BE/app/routes/` và `BE/app/controllers/` | `routes` nhận request; `controllers` xử lý nghiệp vụ |

**Luồng xử lý một request:**
```
FE (services/*.ts) ─► routes ─► controllers ─► services (logic phức tạp) ─► models ─► MySQL
                    ◄──────────────────── schemas (response) ◄──────────────────────
```

---

## 📁 Cấu trúc thư mục

```
Collision-warning-system/
├── BE/                          # Backend (FastAPI)
│   ├── app/
│   │   ├── main.py              # Điểm khởi chạy app
│   │   ├── core/                # config, kết nối DB, bảo mật (JWT), logger
│   │   ├── models/              # MODEL: user, vehicle, camera, alert, collision_event
│   │   ├── schemas/             # Pydantic schema (request/response)
│   │   ├── controllers/         # CONTROLLER: xử lý nghiệp vụ
│   │   ├── routes/              # Định nghĩa API endpoint + WebSocket
│   │   ├── services/            # Phát hiện, tracking, tính va chạm, gửi thông báo
│   │   ├── middlewares/         # Xác thực, xử lý lỗi
│   │   └── utils/               # Hàm tiện ích (geo, time, validate)
│   ├── tests/                   # unit/ và integration/
│   ├── alembic/                 # Migration database
│   ├── requirements.txt         # Thư viện chạy
│   ├── requirements-dev.txt     # Thư viện dev/test (pytest, ruff)
│   └── Dockerfile
│
├── FE/                          # Frontend (React + TS) - VIEW
│   ├── src/
│   │   ├── components/          # common, layout, map, camera, alert
│   │   ├── pages/               # Dashboard, Login, Cameras, Vehicles, Alerts, NotFound
│   │   ├── services/            # Gọi API & WebSocket
│   │   ├── hooks/               # useAuth, useWebSocket, useAlerts
│   │   ├── store/               # State toàn cục
│   │   ├── types/               # Kiểu dữ liệu TypeScript
│   │   ├── routes/              # Điều hướng trang
│   │   └── styles/              # CSS
│   ├── nginx/default.conf       # Cấu hình Nginx khi chạy Docker
│   └── Dockerfile
│
├── database/
│   ├── init/01_schema.sql       # Tạo bảng
│   ├── init/02_seed.sql         # Dữ liệu mẫu
│   └── backups/                 # Bản backup (không push lên Git)
│
├── .github/workflows/           # ci.yml, cd.yml
├── docker-compose.yml           # Chạy MySQL + BE + FE cùng lúc
└── .env.example                 # Mẫu biến môi trường
```

---

## 🚀 Cài đặt & chạy dự án

### Yêu cầu
- Git
- Docker Desktop (cách 1), **hoặc** Python 3.12, Node.js 20 và MySQL 8 (cách 2)

### Cách 1: Chạy bằng Docker (khuyên dùng)
```bash
git clone https://github.com/NayuD06/collision-warning-system.git
cd collision-warning-system
cp .env.example .env          # rồi sửa mật khẩu nếu cần
docker compose up -d --build
```

| Dịch vụ | Địa chỉ |
|---|---|
| Frontend | http://localhost |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| MySQL | localhost:3306 |

Dừng toàn bộ: `docker compose down`

### Cách 2: Chạy thủ công từng phần

**Backend**
```bash
cd BE
python -m venv .venv
# Windows: .venv\Scripts\activate   |   macOS/Linux: source .venv/bin/activate
pip install -r requirements-dev.txt
cp .env.example .env          # sửa thông tin MySQL
uvicorn app.main:app --reload
```

**Frontend**
```bash
cd FE
npm install
cp .env.example .env
npm run dev                   # http://localhost:5173
```

---

## 🗄 Database (MySQL)

- **Tên DB:** `collision_warning`
- **Các bảng dự kiến:** `users`, `vehicles`, `cameras`, `alerts`, `collision_events`
- Các file trong `database/init/` **tự động chạy** khi container MySQL khởi động lần đầu.
- Khi thay đổi cấu trúc bảng, dùng **Alembic**:
  ```bash
  cd BE
  alembic revision --autogenerate -m "mo ta thay doi"
  alembic upgrade head
  ```
- Muốn reset DB khi chạy Docker: `docker compose down -v` (⚠️ lệnh này **xóa toàn bộ dữ liệu**).

---

## ⚙️ CI/CD

### CI ([.github/workflows/ci.yml](.github/workflows/ci.yml))
Chạy khi **push lên bất kỳ nhánh nào** hoặc khi **tạo PR vào `main`**:
1. **Backend:** kiểm tra code bằng `ruff`, tạo bảng trên MySQL test, chạy `pytest`
2. **Frontend:** `npm install`, sau đó `npm run build`
3. **Docker:** build thử image BE và FE

👉 Nếu CI báo ❌ (đỏ) thì **sửa trước khi merge**.

### CD ([.github/workflows/cd.yml](.github/workflows/cd.yml))
Chạy khi code được merge vào **`main`**:
1. Build và đẩy Docker image lên `ghcr.io`
2. Deploy lên server qua SSH. Bước này mặc định **tắt**; muốn bật thì vào Settings của repo, thêm biến `DEPLOY_ENABLED=true` và các secret `SERVER_HOST`, `SERVER_USER`, `SERVER_SSH_KEY`, `SERVER_APP_DIR`.

---

## 👥 Quy trình làm việc nhóm (Git)

> Mỗi người làm xong sẽ push lên **branch riêng**, mỗi chức năng là **1 file** trong nhánh đó.
> Mỗi lần push tiếp vẫn cập nhật lên **nhánh cũ** đã tạo lúc đầu.

```bash
# 1. Lấy code mới nhất
git checkout main
git pull origin main

# 2. Tạo nhánh của mình (chỉ làm 1 lần)
git checkout -b feature/ten-chuc-nang

# 3. Code xong thì commit & push
git add .
git commit -m "feat: them API tao canh bao"
git push origin feature/ten-chuc-nang

# 4. Lên GitHub tạo Pull Request vào main, chờ CI xanh và review
```

**Đặt tên nhánh:** `feature/...` (tính năng mới), `fix/...` (sửa lỗi), `docs/...` (tài liệu)

**Commit message:** `feat:` tính năng · `fix:` sửa lỗi · `docs:` tài liệu · `refactor:` tái cấu trúc · `test:` test

⚠️ **Không push thẳng lên `main`. Không push file `.env`** (file này chứa mật khẩu).

---

## 📝 Quy ước code

**Backend (Python)**
- Tên file và hàm: `snake_case`; tên class: `PascalCase`
- Mỗi thực thể có đủ 4 file: `models/x.py`, `schemas/x_schema.py`, `controllers/x_controller.py`, `routes/x_routes.py`
- Chạy `ruff check .` trước khi push

**Frontend (React/TS)**
- Component/Page: `PascalCase.tsx`; hook: `useXxx.ts`; service: `xxxService.ts`
- Không gọi API trực tiếp trong component; luôn gọi qua `src/services/`
- Khai báo kiểu dữ liệu trong `src/types/`

### Thêm một chức năng mới (ví dụ: "Alert")
1. `BE/app/models/alert.py`: định nghĩa bảng
2. `BE/app/schemas/alert_schema.py`: dữ liệu vào/ra
3. `BE/app/controllers/alert_controller.py`: xử lý logic
4. `BE/app/routes/alert_routes.py`: khai báo API
5. `FE/src/types/alert.ts`, rồi `FE/src/services/alertService.ts`, rồi `FE/src/pages/Alerts/AlertsPage.tsx`
6. Viết test trong `BE/tests/`
