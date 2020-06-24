import typing as t
from PIL import ImageDraw
from glob import glob
from random_char_image import TextRepo, BackgroundRepo, RandomImage


def test_image() -> None:
    br = BackgroundRepo().with_file("templates/shiyoukyokashinnseisho09.jpg")
    text = TextRepo().with_file("texts/hvt.txt")

    ri = (
        RandomImage()
        .with_config(fontsize=24, line_space=20, char_space=10, direction="column")
        .with_background(br.get())
        .with_text(text)
    )
    for i, p in enumerate(glob("fonts/*.ttf")):
        if i % 2 == 0:
            ri.with_label_font(p, label=0, is_random=True)
        else:
            ri.with_label_font(p, label=1, is_random=False)

    img, boxes, labels, _ = ri.get()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for box, label in zip(boxes, labels):
        x0, y0, x1, y1 = box
        assert x1 < w
        assert y1 < h
        assert x0 < w
        assert y0 < h
        if label == 0:
            draw.rectangle(box, outline="red")
        else:
            draw.rectangle(box, outline="blue")
    img.save("/store/test.png")


def test_image_without_background() -> None:
    text = TextRepo().with_file("texts/hvt.txt")

    ri = (
        RandomImage()
        .with_config(fontsize=24, line_space=20, char_space=10, direction="column")
        .with_text(text)
    )
    for i, p in enumerate(glob("fonts/*.ttf")):
        if i % 2 == 0:
            ri.with_label_font(p, label=0, is_random=True)
        else:
            ri.with_label_font(p, label=1, is_random=False)

    img, boxes, labels, _ = ri.get()
    draw = ImageDraw.Draw(img)
    w, h = img.size
    for box, label in zip(boxes, labels):
        x0, y0, x1, y1 = box
        assert x1 < w
        assert y1 < h
        assert x0 < w
        assert y0 < h
        if label == 0:
            draw.rectangle(box, outline="red")
        else:
            draw.rectangle(box, outline="blue")
    img.save("/store/without-background.png")
