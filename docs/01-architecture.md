# Kiến trúc dự kiến

## Các thành phần

1. **Map model**: đã triển khai trong `src/map_model.py`; quản lý lưới, vật cản, chi phí, điểm đầu, điểm đích và láng giềng 4 hướng.
2. **Search algorithms**: giao diện chung cho BFS, Dijkstra và A*.
3. **Simulation**: xe thực hiện từng bước theo đường đi, dừng khi lỗi hoặc đến đích.
4. **Renderer/UI**: vẽ bản đồ, trạng thái tìm kiếm, xe và bảng điều khiển.
5. **Experiment runner**: chạy cùng một cấu hình cho nhiều thuật toán và ghi số liệu.
6. **Persistence**: lưu và tải bản đồ, cấu hình thực nghiệm.

## Nguyên tắc kết nối

- Thuật toán không phụ thuộc giao diện.
- Giao diện chỉ tiêu thụ trạng thái và kết quả tìm kiếm.
- Cùng một bản đồ, điểm đầu, điểm đích, thứ tự xét hàng xóm và quy tắc chi phí được dùng khi so sánh.
- Hoạt ảnh không được tính vào thời gian chạy thuật toán.

## Công nghệ dự kiến

Python và Pygame cho bản thử nghiệm trực quan. Có thể thay đổi nếu giảng viên yêu cầu nền tảng khác.
