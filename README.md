# Mô phỏng điều khiển xe tự động bằng BFS, Dijkstra và A*

Bài tập lớn môn Trí tuệ nhân tạo: mô phỏng xe di chuyển trên bản đồ dạng lưới, lập kế hoạch đường đi bằng BFS, Dijkstra hoặc A*, sau đó trực quan hóa và so sánh kết quả.

## Trạng thái

Đã có mô phỏng Pygame với BFS, Dijkstra và A*: quét node, tìm đường rồi cho xe di chuyển. Giao diện gồm panel điều khiển bên trái, bản đồ ở giữa và kết quả/benchmark bên phải.

## Chạy và sử dụng

```powershell
py src/main.py
```

- Bấm BFS, Dijkstra hoặc A* để chạy lại mô phỏng từ điểm đầu.
- Giao diện dùng light theme; panel trái thu gọn, bản đồ ở giữa và kết quả/benchmark ở panel phải.
- Nhập số hàng (5–50) và số cột (5–80), sau đó bấm `Tạo grid map` hoặc Enter. Khi nhấp vào ô nhập, giá trị cũ được chọn toàn bộ để số mới thay thế ngay; sau khi nhập có con trỏ nhấp nháy. Map mới đặt start ở góc trên trái và goal ở góc dưới phải; cell luôn giữ hình vuông. Panel giữa tự lấy kích thước grid cộng 10 px đệm mỗi cạnh nên không còn khoảng trống bên trong panel.
- Bấm `Đặt Start` hoặc `Đặt Goal`, sau đó chọn một ô trên grid. Điểm mới không thể trùng điểm còn lại; obstacle tại ô được chọn sẽ tự xóa.
- `Reset bản đồ` chỉ xóa obstacle, đường quét và animation; vị trí Start và Goal được giữ nguyên.
- Giữ chuột trái để tô vật cản, chuột phải để xóa. Start và goal được bảo vệ.
- Quét node màu xanh nhạt, đường xe đã đi màu vàng, obstacle liền khối màu đen.
- Xe dùng ảnh `assets/car-topdown.png`, xoay theo hướng di chuyển.
- Nút `− / ms / +` chỉnh thời gian mỗi bước trong khoảng 10–500 ms, bước điều chỉnh 10 ms.
- Benchmark lần lượt mô phỏng BFS → Dijkstra → A*: về trạng thái chờ, quét node rồi cho xe di chuyển. Chỉ khi cả ba lượt mô phỏng hoàn tất mới hiện bảng so sánh; lượt không có đường kết thúc sau khi quét.
- Benchmark đo trên bản sao của map hiện tại, mỗi thuật toán 20 lượt. Bảng hiển thị thời gian trung bình (ms), số node được xét (bao gồm start/goal khi tới đích), số bước và chi phí. Thời gian đo không tính vẽ giao diện hoặc chờ animation.
- Bản đồ hiện không có trọng số: chi phí bằng số bước; không có đường được hiển thị bằng `—`.
- Thay đổi map sẽ hủy animation, hủy benchmark đang chạy và xóa kết quả cũ. Chọn riêng một thuật toán cũng hủy benchmark đang chạy. Bấm benchmark lần nữa sau khi hoàn tất để đo và mô phỏng lại.
- Có thể thay đổi kích thước cửa sổ; giao diện và vị trí chuột được quy đổi theo cùng tỉ lệ.

Kiểm tra tự động (bao gồm Pygame headless):

```powershell
py -m unittest discover -s tests -p "test_*.py" -v
```

## Cấu trúc chương trình

- `docs/`: đặc tả bài toán, kiến trúc và kế hoạch thực hiện.
- `src/main.py`: xử lý sự kiện và vòng lặp ứng dụng.
- `src/renderer.py`: bố cục, vẽ bản đồ, xe và bảng kết quả.
- `src/simulation.py`: quản lý pha quét và di chuyển.
- `src/benchmark.py`: đo ba thuật toán, mỗi frame một lượt đo.
- `src/algorithms.py`, `src/map_model.py`: thuật toán và dữ liệu lưới.
- `assets/`: ảnh xe.
- `data/maps/`: bản đồ mẫu và bản đồ thực nghiệm.
- `tests/`: kiểm thử thuật toán và mô phỏng.
- `reports/`: kết quả đo và tài liệu báo cáo.

## Phạm vi chương trình

- Bản đồ ô vuông 2D, di chuyển 4 hướng.
- Vật cản; mỗi bước di chuyển có chi phí bằng 1.
- Ba thuật toán: BFS, Dijkstra, A*.
- Xe chạy theo đường đã tìm; phần nhận diện cảm biến/vật lý thực không thuộc phiên bản đầu.
- 
## Thư viện và cài đặt môi trường

Dự án sử dụng Python 3.11 trở lên và Pygame để tạo cửa sổ mô phỏng, vẽ bản đồ, nhận thao tác chuột/bàn phím và chạy hoạt ảnh. Các thuật toán BFS, Dijkstra và A* sẽ dùng thư viện chuẩn của Python, nên chưa cần thêm gói bên ngoài.

Danh sách thư viện được lưu trong `requirements.txt`. Cài đặt bằng:

```powershell
py -m pip install -r requirements.txt
```

Kiểm tra Pygame sau khi cài đặt:

```powershell
py -c "import pygame; print(pygame.version.ver)"
```
