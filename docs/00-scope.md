# Đặc tả phạm vi bước 1

## Mục tiêu

Xây dựng nền tảng cho chương trình mô phỏng xe tự động đi từ điểm xuất phát đến đích trong bản đồ dạng lưới có vật cản và các mức chi phí di chuyển khác nhau.

## Mô hình bài toán

- Trạng thái cơ bản: tọa độ ô `(x, y)`.
- Hành động: đi lên, xuống, trái, phải.
- Ô vật cản: không thể đi vào.
- Cạnh: một bước di chuyển giữa hai ô kề nhau.
- Chi phí cạnh: chi phí của ô đích; mọi chi phí phải không âm.
- Mục tiêu: đạt ô đích với đường hợp lệ.

## Ranh giới

Phiên bản đầu mô phỏng lập kế hoạch đường đi trên bản đồ đã biết. Không mô phỏng camera, nhận dạng vật thể, động lực học xe, điều khiển vô-lăng liên tục hoặc giao thông nhiều xe.

## Tiêu chí đầu ra

Mỗi lần chạy cần có đường đi hoặc trạng thái không tìm thấy đường, số bước, tổng chi phí, số nút đã mở rộng và thời gian tìm kiếm.
