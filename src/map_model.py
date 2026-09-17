import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")


class GridMap:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.start = None
        self.goal = None
        self.obstacles = set()
        self.weights = {}

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

    def weight_at(self, position):
        """Return traversal cost for a cell; normal cells cost one."""
        return max(1, self.weights.get(position, 1))

    def set_weight(self, position, weight):
        if not self.is_inside(position) or position in self.obstacles:
            return
        weight = max(1, int(weight))
        if weight == 1:
            self.weights.pop(position, None)
        else:
            self.weights[position] = weight

    def clear_weights(self):
        self.weights.clear()

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
