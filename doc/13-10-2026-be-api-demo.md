# BE API demo: cảnh báo (alerts) và kiểm tra va chạm

- **Ngày:** 13/10/2026
- **Nhánh:** `feature/demo-api`
- **Phạm vi:** chỉ Backend. Frontend chưa làm.

## Đã làm gì

Skeleton BE ban đầu toàn file rỗng. Lần này viết một lát cắt chạy được từ đầu đến cuối
theo đúng quy ước MVC trong README (model → schema → controller → route), đủ để CI có thứ để kiểm tra.

| File | Nội dung |
|---|---|
| `BE/app/main.py` | Khởi tạo FastAPI, CORS, gắn router dưới `/api`, endpoint `/health` |
| `BE/app/core/config.py` | Đọc cấu hình từ biến môi trường / `.env` (pydantic-settings) |
| `BE/app/core/database.py` | Engine MySQL (pymysql), `SessionLocal`, dependency `get_db` |
| `BE/app/models/base.py`, `alert.py` | Bảng `alerts` |
| `BE/app/schemas/alert_schema.py` | `AlertCreate`, `AlertResponse`, enum `AlertLevel` |
| `BE/app/schemas/collision_event_schema.py` | Dữ liệu vào/ra của API kiểm tra va chạm |
| `BE/app/controllers/alert_controller.py` | CRUD cảnh báo |
| `BE/app/controllers/collision_event_controller.py` | Gọi service tính nguy cơ, có nguy cơ thì lưu cảnh báo |
| `BE/app/routes/alert_routes.py`, `collision_event_routes.py`, `__init__.py` | Khai báo endpoint |
| `BE/app/services/collision_service.py` | Thuật toán tính nguy cơ va chạm |
| `BE/app/utils/geo_utils.py` | Đổi tốc độ + hướng thành vector vận tốc |
| `database/init/01_schema.sql` | Lệnh tạo bảng `alerts` cho MySQL |
| `BE/tests/` | `conftest.py`, 6 unit test, 9 integration test |

## Danh sách API

| Method | Đường dẫn | Mô tả |
|---|---|---|
| GET | `/health` | Kiểm tra server còn sống |
| GET | `/api/alerts` | Danh sách cảnh báo, mới nhất trước. Lọc: `level`, `is_resolved`; phân trang: `skip`, `limit` |
| POST | `/api/alerts` | Tạo cảnh báo (201) |
| GET | `/api/alerts/{id}` | Xem một cảnh báo (404 nếu không có) |
| PATCH | `/api/alerts/{id}/resolve` | Đánh dấu đã xử lý |
| DELETE | `/api/alerts/{id}` | Xoá (204) |
| POST | `/api/collision-events/check` | Nhận trạng thái 2 xe, trả mức nguy cơ; nếu có nguy cơ thì tự tạo cảnh báo |

Ví dụ gọi API kiểm tra va chạm:

```json
POST /api/collision-events/check
{
  "vehicle_a": { "plate": "29A-123.45", "x": -15, "y": 0, "speed_kmh": 36, "heading_deg": 90 },
  "vehicle_b": { "plate": "51G-678.90", "x": 0, "y": -15, "speed_kmh": 36, "heading_deg": 0 }
}
```

Kết quả: `level = "danger"`, `ttc_seconds = 1.5`, kèm bản ghi `alert` vừa được lưu.

## Cách tính nguy cơ va chạm

Dùng phương pháp điểm tiếp cận gần nhất (CPA), giả định hai xe giữ nguyên vận tốc:

1. Toạ độ tính bằng mét; hướng theo la bàn (0 = bắc, 90 = đông).
2. Tính thời điểm hai xe gần nhau nhất (`ttc_seconds`) và khoảng cách lúc đó (`min_distance_m`).
3. Phân loại:
   - `safe`: đang rời xa nhau, hoặc khoảng cách gần nhất ≥ 3 m, hoặc TTC ≥ 4 giây
   - `warning`: khoảng cách gần nhất < 3 m và 2 ≤ TTC < 4 giây
   - `danger`: khoảng cách gần nhất < 3 m và TTC < 2 giây

Các ngưỡng là hằng số ở đầu `collision_service.py`, đang là giá trị demo, chưa hiệu chỉnh theo thực tế.

## Kiểm tra theo CI

Chạy đúng các bước của job `backend` trong `.github/workflows/ci.yml`, trên Python 3.12:

```bash
cd BE
pip install -r requirements-dev.txt
ruff check .
pytest --cov=app --cov-report=term
```

Kết quả trên máy: `ruff` không lỗi, `pytest` 15/15 qua, độ phủ 98%.

## Lưu ý

- Test dùng **SQLite trong bộ nhớ** (xem `conftest.py`) nên chạy được mà không cần MySQL.
  Vì vậy `01_schema.sql` chưa được chạy thử trên MySQL thật ở máy (Docker Desktop đang tắt);
  CI sẽ nạp file này vào MySQL ở bước "Load database schema".
- Bảng `alerts` trong `01_schema.sql` phải sửa cùng lúc với `models/alert.py`.
- Chưa làm: đăng nhập / JWT, các thực thể `users`, `vehicles`, `cameras`, `collision_events`,
  WebSocket, Alembic (`alembic.ini` và `env.py` còn rỗng).
- API chưa có xác thực, ai gọi cũng được.

## Chạy thử

```bash
cd BE
cp .env.example .env
uvicorn app.main:app --reload
```

Mở http://localhost:8000/docs để thử API (cần MySQL đang chạy và đã có bảng `alerts`).
