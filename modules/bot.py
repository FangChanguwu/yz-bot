import textwrap
from typing import Union

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import At, Image
from graia.ariadne.model import Group, Friend

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from PIL import Image as pimg
from PIL import ImageDraw, ImageFont

channel = Channel.current()


def help():
    width = 600
    height = 1000
    color = "#FDF4F3"
    img = pimg.new("RGB", (width, height), color)

    text_color = "#DD7E81"
    text = "/旅行伙伴\n" \
           "生成maimai旅行伙伴的图片\n\n" \
           "/图片镜像\n" \
           "对图片进行镜像操作\n\n" \
           "/[来张、随机、空]草图\n" \
           "发送一张来自网络的草图\n" \
           "\n\n\n\n\n\n\n\n\n\n\n/xxx为指令部分\n[]内以顿号分隔\n为可选的指令部分\n如果有“空”则代表[]内容可以不填\n" \
           "伊兹Bot v1.0.0 by Fcuwu"
    font_path = "./src/font/SmileySans-Oblique.ttf"
    font_size = 40
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)

    # 将文本按照手动添加的换行符进行分割
    text_lines = text.split("\n")

    # 逐行绘制除最后一行外的文本
    x, y = 0, 0
    line_height = font.getsize("A")[1]  # 获取字体的高度
    for i in range(len(text_lines) - 1):
        line = text_lines[i]
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    # 自动换行最后一行文本
    last_line = text_lines[-1]
    last_line_wrapped = textwrap.wrap(last_line, width=30)

    # 在最后一行之前添加一些空白行
    for i in range(10):
        y += line_height

    # 绘制最后一行自动换行后的文本
    last_line_height = font.getsize(last_line_wrapped[0])[1]
    y = height - last_line_height
    for line in last_line_wrapped:
        draw.text((x, y), line, fill=text_color, font=font)
        y += line_height

    img.save('./src/img/help.png')
    return Image(path="./src/img/help.png")


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def nihao(app: Ariadne, group: Group, message: MessageChain):
    if str(message) in ["伊兹", 'ez', '@3446560564']:
        await app.send_message(
            group,
            MessageChain(f"不在"),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def nihao(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    if str(message) in ['@3446560564 help', '/yz', '!yz', '/ez', '!ez']:
        await app.send_message(sender, help())
