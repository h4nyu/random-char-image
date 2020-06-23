from PIL import ImageFont, ImageDraw, Image
import typing as t
from collections import defaultdict
import numpy as np
import random


class TextRepo:
    def __init__(self) -> None:
        self.text = ""

    def __len__(self) -> int:
        return len(self.text)

    def with_file(self, path: str) -> "TextRepo":
        with open(path, "r") as f:
            self.text += "".join(f.read().splitlines())
        return self

    def get(self, lenght: int) -> str:
        high = len(self) - lenght
        start = np.random.randint(low=0, high=high)
        return self.text[start : start + lenght]


class BackgrandRepo:
    def __init__(self) -> None:
        self.backgrands: t.List[Image] = []

    def with_file(self, path: str) -> "BackgrandRepo":
        self.backgrands.append(Image.open(path))
        return self

    def get(self) -> Image:
        return random.choice(self.backgrands)


Direction = t.Literal["column", "row"]
Box = t.Tuple[int, int, int, int]


class RandomImage:
    def __init__(self,) -> None:
        self.size = (512, 512)
        self.direction = "row"
        self.line_space = 4
        self.fontsize = 24
        self.text = TextRepo()
        self.font_paths: t.Dict[str, int] = dict()
        self.font_space = 4

    def with_config(
        self,
        fontsize: int = 8,
        line_space: int = 4,
        char_space: int = 4,
        direction: Direction = "row",
    ) -> "RandomImage":
        self.fontsize = fontsize
        self.line_space = line_space
        self.char_space = char_space
        self.direction = direction
        return self

    def with_backgrand(self, img: Image) -> "RandomImage":
        self.blackgrand = img
        self.size = img.size
        return self

    def with_label_font(self, path: str, label: int = 0,) -> "RandomImage":
        self.font_paths[path] = label
        return self

    def with_text(self, text: TextRepo) -> "RandomImage":
        self.text = text
        return self

    def get(self) -> t.Tuple[t.Any, t.List[Box], t.List[int]]:
        img = (
            self.blackgrand.copy()
            if self.blackgrand is not None
            else Image.new("RGB", self.size)
        )
        draw = ImageDraw.Draw(img)
        x = self.fontsize
        y = self.fontsize
        limit_x = self.size[0] - self.fontsize - self.font_space
        limit_y = self.size[1] - self.fontsize - self.font_space
        line_height = self.fontsize + self.line_space
        boxes = []
        labels = []
        char_count = int(limit_y * limit_y // self.fontsize ** 2)
        font_paths = list(self.font_paths.keys())
        for c in self.text.get(char_count):
            fpath = random.choice(font_paths)
            label = self.font_paths[fpath]
            font = ImageFont.truetype(
                fpath, int(self.fontsize * np.random.uniform(low=0.7, high=1.3)),
            )
            w, h = font.getsize(c)
            n_x, n_y = 0.2 * (np.random.rand(2) - 0.5)
            char_x: int = x + w * n_x
            char_y: int = y + h * n_y
            draw.text((char_x, char_y), c, font=font, fill="black")
            boxes.append((char_x, char_y, w, h))
            labels.append(label)

            if self.direction == "row":
                x += self.font_space + w
                if x > limit_x:
                    x = self.fontsize
                    y += line_height

                if y > limit_y:
                    break
            else:
                y += self.font_space + h
                if y > limit_y:
                    y = self.fontsize
                    x += line_height
                if x > limit_x:
                    break
        return img, boxes, labels
