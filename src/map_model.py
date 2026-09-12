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
        self.costs = {}

    # Hàm kiểm tra xem một vị trí có nằm trong bản đồ hay không
    def is_inside(self, position: tuple[int, int]):
        row, column = position
        return (
            0 <= row and row < self.rows
            and
            0 <= column and column < self.columns
        )

    # Hàm kiểm tra xem một vị trí có phải là chướng ngại vật hay không
    def is_obstacle(self, position: tuple[int, int]):
        # Kiểm tra xem vị trí có nằm trong tập hợp các vị trí chướng ngại vật hay không
        return position in self.obstacles

    # Hàm lấy chi phí cho một vị trí trên bản đồ
    def get_cost(self, position):
        return self.costs.get(position, 1)

    # Hàm đặt chi phí cho một vị trí trên bản đồ
    def set_cost(self, position, cost):
        try:
            if cost <= 0:
                raise ValueError("Chi phí phải lớn hơn 0")
            self.costs[position] = cost
        except ValueError as e:
            print(f"Lỗi: {e}")
            

def main():
    grid = GridMap(5, 6)

    print(grid.is_inside((2, 3)))
    print(grid.is_inside((8, 3)))

    grid.obstacles.add((1, 2))

    print(grid.is_obstacle((1, 2)))
    print(grid.is_obstacle((0, 0)))

    # Tại node n = (2, 3) có cost c(n) = 5
    grid.set_cost((2, 3), 5)
    print(grid.get_cost((2, 3)))
    print(grid.get_cost((0, 0)))


if __name__ == "__main__":
    main()
