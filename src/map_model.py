class GridMap:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.start = None
        self.goal = None
        self.obstacles = set()

    # Kiểm tra xem một vị trí có nằm trong bản đồ hay không
    def is_inside(self, position):
        row, column = position
        return (
            0 <= row < self.rows
            and 0 <= column < self.columns
        )

    # Kiểm tra xem một vị trí có phải là vật cản hay không
    def is_obstacle(self, position):
        return position in self.obstacles

    # Lấy các ô hàng xóm có thể đi đến theo 4 hướng
    def get_neighbors(self, position):
        row, column = position
        directions = [
            (-1, 0),  # Lên
            (1, 0),   # Xuống
            (0, -1),  # Trái
            (0, 1)    # Phải
        ]
        neighbors = []
        for delta_row, delta_column in directions:
            next_position = (
                row + delta_row,
                column + delta_column
            )
            if (
                self.is_inside(next_position)
                and not self.is_obstacle(next_position)
            ):
                neighbors.append(next_position)

        return neighbors
