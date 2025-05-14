# -*- coding: utf-8 -*-
from PIL import Image
import requests
from io import BytesIO 

def merge(im1: Image.Image, im2: Image.Image) -> Image.Image:
    w = im1.size[0] + im2.size[0]
    h = max(im1.size[1], im2.size[1])
    im = Image.new("RGBA", (w, h))

    im.paste(im1)
    im.paste(im2, (im1.size[0], 0))

    return im

i = Image.open(BytesIO(requests.get("https://mmbiz.qpic.cn/sz_mmbiz_png/ZFU5JMP7wK6pdFRh6xQiaAnT0RFG7dNYq1mpEoQ3qV1PPz272Kaj1ibjoiczBkSIgfwakzT61jaictibDcfPXQgAejg/640?wx_fmt=png").content))

i.save("1.png")