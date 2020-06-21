
```py
from PIL import ImageDraw
from glob import glob
from random_char_image import TextRepo, BackgrandRepo, RandomImage

br = BackgrandRepo().with_file("templates/shiyoukyokashinnseisho09.jpg")
text = TextRepo().with_file("texts/hvt.txt")

ri = (
    RandomImage()
    .with_config(fontsize=24, line_space=10, char_space=10, direction="column")
    .with_backgrand(br.get())
    .with_text(text)
)
for i, p in enumerate(glob("fonts/*.ttf")):
    ri.with_label_font(p, i % 2)

img, boxes, labels = ri.get()
draw = ImageDraw.Draw(img)
for box, label in zip(boxes, labels):
    if label == 0:
        draw.rectangle(box, outline="red")
    else:
        draw.rectangle(box, outline="blue")
img.save("test.png")
```

![example](./test.png)
