import tkinter as tk
from typing import List, Tuple
import Configs as cf


def _concat_colors(curr_c: Tuple[int, int, int], draw_c: Tuple[int, int, int]) -> Tuple[int, int, int]:
    new_c = tuple()
    for curr, draw in zip(curr_c, draw_c):
        new_c += (min(curr, (curr + draw)//2),)
    return new_c


def _RGB_2_HEX(RGB: Tuple[int, int, int]) -> str:
    return "#{:04x}{:04x}{:04x}".format(*[num if 0 <= num <= 65535 else 0 if num < 0 else 65535 for num in RGB])


def _len_between_points(f_p: Tuple[int,int], s_p: Tuple[int, int]) -> float:
    return pow(((f_p[0] - s_p[0])**2 + (f_p[1] - s_p[1])**2), 0.5)


class ColorGridCanvas(tk.Tk):

    def __init__(self, n:int=50, cell:int=5, color:str="red", brush_size:int=1) -> None:
        super().__init__()
        self.title(f"Предсказание цифр")
        self.n = n
        self.cell = cell
        self.color = color

        self.canvas: tk.Canvas = tk.Canvas(self, width=n*cell, height=n*cell)
        self.canvas.pack()
        self.rects: List[List[int]] = [[0 for _ in range(n)] for _ in range(n)]

        self._create_grid()
        self.canvas.bind("<B1-Motion>", self._on_click_hover)
        self.canvas.bind("<Button-1>", self._on_click_hover)
        self.canvas.bind("<Button-3>", self._clear_canvas)

    def _create_grid(self) -> None:
        for i in range(self.n):
            for j in range(self.n):
                x0 = j * self.cell + 2
                y0 = i * self.cell + 2
                x1 = x0 + self.cell
                y1 = y0 + self.cell
                rect = self.canvas.create_rectangle(x0, y0, x1, y1,
                                                    fill=cf.BASE_COLOR,
                                                    outline="black",
                                                    tags="rect")
                self.rects[i][j] = rect

    def _clear_canvas(self, event) -> None:
        self.canvas.itemconfig("rect", fill=cf.BASE_COLOR)

    def _on_click_hover(self, event) -> None:
        col = event.x // self.cell
        row = event.y // self.cell
        self._draw_circle(col, row, 5)

    def _draw_circle(self, x: int, y: int, radius: int) -> None:
        for row in range(y - radius, y + radius + 1):
            for col in range(x - radius, x + radius + 1):
                dot_len = _len_between_points((col, row), (x, y))
                if 0 <= row < self.n and 0 <= col < self.n and dot_len < radius:
                    rect = self.rects[row][col]

                    # use pow(..., 2) for smoother color gradient with brighter color in the center
                    color_grad = pow(_len_between_points((col, row), (x, y)), 2) / pow(radius, 2)
                    draw_color_int = round(color_grad * cf.COLOR_MAX)
                    draw_color = (draw_color_int,) * 3
                    curr_color = self.canvas.winfo_rgb(self.canvas.itemcget(rect, "fill"))

                    new_color = _concat_colors(curr_color, draw_color)
                    color_str = _RGB_2_HEX(new_color)

                    self.canvas.itemconfig(rect, fill=color_str)


if __name__ == "__main__":
    app = ColorGridCanvas()
    app.mainloop()
