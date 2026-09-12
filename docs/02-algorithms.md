# Đặc tả thuật toán

## BFS

Hàng đợi FIFO, ưu tiên độ sâu nhỏ nhất. Tối ưu số bước khi mọi cạnh có cùng chi phí; không tối ưu tổng chi phí trong bản đồ có trọng số khác nhau.

## Dijkstra

Hàng đợi ưu tiên theo chi phí tích lũy `g(n)`. Tối ưu tổng chi phí khi chi phí cạnh không âm.

## A*

Hàng đợi ưu tiên theo `f(n) = g(n) + h(n)`. Với lưới 4 hướng, heuristic mặc định là khoảng cách Manhattan nhân chi phí bước nhỏ nhất. Heuristic phải không vượt chi phí thật.

## Kết quả chung

Mỗi thuật toán trả về đường đi, chi phí, số bước, số nút mở rộng, trạng thái thành công/thất bại và nhật ký các nút đã xét để trực quan hóa.
