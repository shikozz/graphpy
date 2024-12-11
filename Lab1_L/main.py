import tkinter as tk
from tkinter import Canvas, simpledialog

class Shape:
    """Базовый класс для всех фигур."""
    def draw(self, canvas):
        raise NotImplementedError("Метод draw() должен быть реализован в подклассе.")

class Point(Shape):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, canvas):
        canvas.create_oval(self.x - 2, self.y - 2, self.x + 2, self.y + 2, fill="black")

class Line(Shape):
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, canvas):
        canvas.create_line(self.x1, self.y1, self.x2, self.y2, fill="black")

class Circle(Shape):
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius

    def draw(self, canvas):
        canvas.create_oval(self.x - self.radius, self.y - self.radius,
                           self.x + self.radius, self.y + self.radius, outline="black")

class Square(Shape):
    def __init__(self, x, y, side):
        self.x = x
        self.y = y
        self.side = side

    def draw(self, canvas):
        half_side = self.side / 2
        canvas.create_rectangle(self.x - half_side, self.y - half_side,
                                self.x + half_side, self.y + half_side, outline="black")

class GraphicalEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Графический редактор")

        self.canvas = Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.btn_draw_point = tk.Button(self.root, text="Нарисовать точку", command=self.enable_point_drawing)
        self.btn_draw_point.pack(side=tk.LEFT)

        self.btn_connect_points = tk.Button(self.root, text="Соединить линиями", command=self.connect_points)
        self.btn_connect_points.pack(side=tk.LEFT)

        self.btn_draw_circle = tk.Button(self.root, text="Построить круг", command=self.draw_circle)
        self.btn_draw_circle.pack(side=tk.LEFT)

        self.btn_draw_square = tk.Button(self.root, text="Построить квадрат", command=self.draw_square)
        self.btn_draw_square.pack(side=tk.LEFT)

        self.btn_free_draw = tk.Button(self.root, text="Свободное рисование", command=self.enable_free_drawing)
        self.btn_free_draw.pack(side=tk.LEFT)

        self.btn_clear = tk.Button(self.root, text="Очистить окно", command=self.clear_canvas)
        self.btn_clear.pack(side=tk.LEFT)

        self.shapes = []
        self.points = []

        self.drawing_points = False
        self.free_drawing = False

        self.canvas.bind("<Button-1>", self.add_point)
        self.canvas.bind("<B1-Motion>", self.free_draw)

    def enable_point_drawing(self):
        self.drawing_points = True
        self.free_drawing = False

    def enable_free_drawing(self):
        self.free_drawing = True
        self.drawing_points = False

    def add_point(self, event):
        if self.drawing_points:
            point = Point(event.x, event.y)
            point.draw(self.canvas)
            self.points.append(point)

    def connect_points(self):
        if len(self.points) < 2:
            return
        for i in range(len(self.points) - 1):
            line = Line(self.points[i].x, self.points[i].y,
                        self.points[i + 1].x, self.points[i + 1].y)
            line.draw(self.canvas)
            self.shapes.append(line)
        # Соединяем последнюю точку с первой
        line = Line(self.points[-1].x, self.points[-1].y,
                    self.points[0].x, self.points[0].y)
        line.draw(self.canvas)
        self.shapes.append(line)
        self.drawing_points = False

    def free_draw(self, event):
        if self.free_drawing:
            x, y = event.x, event.y
            point = Point(x, y)
            if self.shapes and isinstance(self.shapes[-1], Line):
                last_line = self.shapes[-1]
                line = Line(last_line.x2, last_line.y2, x, y)
            else:
                line = Line(x, y, x, y)
            line.draw(self.canvas)
            self.shapes.append(line)

    def draw_circle(self):
        radius = simpledialog.askinteger("Параметры круга", "Введите радиус:")
        if radius is not None:
            circle = Circle(400, 300, radius)
            circle.draw(self.canvas)
            self.shapes.append(circle)

    def draw_square(self):
        side = simpledialog.askinteger("Параметры квадрата", "Введите длину стороны:")
        if side is not None:
            square = Square(400, 300, side)
            square.draw(self.canvas)
            self.shapes.append(square)

    def clear_canvas(self):
        self.canvas.delete("all")
        self.shapes.clear()
        self.points.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphicalEditor(root)
    root.mainloop()
