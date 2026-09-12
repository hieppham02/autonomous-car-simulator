# Mô phỏng điều khiển xe tự động bằng BFS, Dijkstra và A*

Bài tập lớn môn Trí tuệ nhân tạo: mô phỏng xe di chuyển trên bản đồ dạng lưới, lập kế hoạch đường đi bằng BFS, Dijkstra hoặc A*, sau đó trực quan hóa và so sánh kết quả.

## Trạng thái

Đã khởi tạo khung tệp cho dự án. Mã triển khai các thành phần sẽ được thực hiện ở các bước tiếp theo.

## Cấu trúc

- `docs/`: đặc tả bài toán, kiến trúc và kế hoạch thực hiện.
- `src/`: nơi đặt mã nguồn sau khi chốt thiết kế.
- `data/maps/`: bản đồ mẫu và bản đồ thực nghiệm.
- `tests/`: kiểm thử thuật toán và mô phỏng.
- `reports/`: kết quả đo và tài liệu báo cáo.

## Phạm vi phiên bản đầu

- Bản đồ ô vuông 2D, di chuyển 4 hướng.
- Vật cản và chi phí di chuyển không âm.
- Ba thuật toán: BFS, Dijkstra, A*.
- Xe chạy theo đường đã tìm; phần nhận diện cảm biến/vật lý thực không thuộc phiên bản đầu.
## Thư viện và cài đặt môi trường

Dự án sử dụng Python 3.11 trở lên và Pygame để tạo cửa sổ mô phỏng, vẽ bản đồ, nhận thao tác chuột/bàn phím và chạy hoạt ảnh. Các thuật toán BFS, Dijkstra và A* sẽ dùng thư viện chuẩn của Python, nên chưa cần thêm gói bên ngoài.

Danh sách phiên bản được lưu trong `requirements.txt`. Cài đặt bằng:

```powershell
py -m pip install -r requirements.txt
```

Kiểm tra Pygame sau khi cài đặt:

```powershell
py -c "import pygame; print(pygame.version.ver)"
```
