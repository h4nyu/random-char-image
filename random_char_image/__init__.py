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


class BackgroundRepo:
    def __init__(self) -> None:
        self.backgrounds: t.List[Image] = []

    def with_file(self, path: str) -> "BackgroundRepo":
        self.backgrounds.append(Image.open(path))
        return self

    def get(self) -> Image:
        return random.choice(self.backgrounds)


Direction = t.Literal["column", "row"]
Box = t.Tuple[int, int, int, int]


class RandomImage:
    def __init__(self, size:t.Tuple[int, int]=(512, 512)) -> None:
        self.size = size
        self.direction = "row"
        self.line_space = 4
        self.fontsize = 24
        self.text = TextRepo()
        self.font_paths: t.Dict[str, t.Tuple[int, bool]] = dict()
        self.font_space = 4
        self.background = Image.new("RGB", size=self.size, color=(255, 255, 255))

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

    def with_background(self, img: Image) -> "RandomImage":
        self.background = img
        self.size = img.size
        return self

    def with_label_font(
        self, path: str, label: int = 0, is_random: bool = True
    ) -> "RandomImage":
        self.font_paths[path] = (label, is_random)
        return self

    def with_text(self, text: TextRepo) -> "RandomImage":
        self.text = text
        return self

    def get(self) -> t.Tuple[t.Any, t.List[Box], t.List[int], t.List[str]]:
        img = (
            self.background.copy()
            if self.background is not None
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
        chars = []
        char_count = int(limit_y * limit_y // self.fontsize ** 2)
        font_paths = list(self.font_paths.keys())
        for c in self.text.get(char_count):
            fpath = random.choice(font_paths)
            label, is_random = self.font_paths[fpath]
            n_font = 1.0
            if is_random:
                n_font = np.random.uniform(low=0.7, high=1.3)
            font = ImageFont.truetype(fpath, int(self.fontsize * n_font),)
            w, h = font.getsize(c)
            n_x = 0.0
            n_y = 0.0
            if is_random:
                n_x, n_y = (
                    np.random.uniform(low=-0.5, high=0.5),
                    np.random.uniform(low=-0.5, high=0.5),
                )
            x0 = x + w * n_x
            y0 = y + h * n_y
            x1 = x0 + w
            y1 = y0 + h

            if (x0 < limit_y) & (y0 < limit_y) & (x1 < limit_x) & (y1 < limit_y):
                draw.text((x0, y0), c, font=font, fill="black")
                boxes.append((x0, y0, x1, y1))
                labels.append(label)
                chars.append(c)

            if self.direction == "row":
                x += self.font_space + w
                if x >= limit_x:
                    x = self.fontsize
                    y += line_height

                if y >= limit_y:
                    break
            else:
                y += self.font_space + h
                if y >= limit_y:
                    y = self.fontsize
                    x += line_height
                if x >= limit_x:
                    break

        return img, boxes, labels, chars
