import re
from typing import Union

import imageio
import requests
from PIL import Image as pimg, ImageOps, ImageSequence
from PIL import ImageDraw
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, At
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group, Friend
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema


def squar(img_path):
    image = pimg.open(img_path)
    width, height = image.size
    if height > width:
        # 计算正方形大小
        square_size = width
        # 计算裁剪坐标
        left = 0
        top = (height - square_size) / 2
        right = square_size
        bottom = top + square_size
        square_image = image.crop((left, top, right, bottom))
        square_image.save(img_path)
    else:
        # 计算正方形大小
        square_size = height
        # 计算裁剪坐标
        left = (width - square_size) / 2
        top = 0
        right = left + square_size
        bottom = square_size
        # 裁剪图片并保存
        square_image = image.crop((left, top, right, bottom))
        square_image.save(img_path)

def extract_qq_and_picurl(text):
    qq_pattern = r'"target":(\d+)'
    picurl_pattern = r'"url":"(.*?)"'

    qq_match = re.search(qq_pattern, text)
    picurl_match = re.search(picurl_pattern, text)

    if qq_match:
        qq = qq_match.group(1)
        return f'https://q.qlogo.cn/g?b=qq&nk={qq}&s=640'
    elif picurl_match:
        picurl = picurl_match.group(1)
        return picurl
    else:
        return None

def hbjr(image_url):
    img_url = extract_qq_and_picurl(image_url)
    if not img_url:
        return '没有@人/无效@/未发送图片，请重试'
    else:
        url = img_url
        r = requests.get(url)
        with open("./img/maimai_img/lx_pic.jpg", "wb") as f:
            f.write(r.content)
        squar("./img/maimai_img/lx_pic.jpg")
        img = pimg.open('./img/maimai_img/lx_pic.jpg')
        # 创建一个新图像和一个画布
        output = pimg.new('RGBA', img.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(output)
        # 在画布上绘制一个圆形掩码
        mask = pimg.new('L', img.size, 0)
        draw_mask = ImageDraw.Draw(mask)
        draw_mask.ellipse((0, 0) + img.size, fill=255)
        # 将掩码应用到图像上
        output.paste(img, (0, 0), mask=mask)
        # 将圆形外的区域设置为透明
        output.putalpha(mask)
        # 保存结果图像
        output.save('./img/maimai_img/lx_qq_circle.png')
        # 计算源图像在目标图像中的位置
        source_image = pimg.open("./img/maimai_img/lx_qq_circle.png").convert("RGBA")
        destination_image = pimg.open("./img/maimai_img/lx_base.jpg").convert("RGBA")
        new_size = (860, 860)  # 新的大小，这里设为200x200
        source_image = source_image.resize(new_size)
        # 处理源图像的透明度通道
        alpha_mask = source_image.getchannel("A")
        if not alpha_mask:
            alpha_mask = pimg.new("L", source_image.size, 255)
        source_image = source_image.convert("RGBa")
        source_image.putalpha(alpha_mask)
        # 计算源图像在目标图像中的位置
        source_size = source_image.size
        destination_size = destination_image.size
        position = ((destination_size[0] - source_size[0]) // 2, (destination_size[1] - source_size[1]) // 2 + 43)
        # 将源图像粘贴到目标图像中间
        destination_image.alpha_composite(source_image, dest=(position[0], position[1]))
        # 保存结果图像
        destination_image.save("./img/maimai_img/lxhb_img.png")
        return Image(path='./img/maimai_img/lxhb_img.png')


def hbjx(image_url):
    img_url = extract_qq_and_picurl(image_url)
    if not img_url:
        return '没有@人/无效@/未发送图片，请重试'
    else:
        url = img_url
        r = requests.get(url)
        with open("./img/maimai_img/jx_pic.png", "wb") as f:
            f.write(r.content)
        canvas = pimg.new('RGBA', (640, 640), (255, 255, 255, 255))
        # 打开需要贴上去的图片，缩放
        squar("./img/maimai_img/jx_pic.png")
        qq_image = pimg.open('./img/maimai_img/jx_pic.png')
        qq_image = ImageOps.fit(qq_image, (460, 460))
        # 计算在画布中的位置
        canvas_size = canvas.size
        qq_size = qq_image.size
        position = ((canvas_size[0] - qq_size[0]) // 2, (canvas_size[1] - qq_size[1]) // 2)
        # 将 qq.png 粘贴到画布中心
        canvas.paste(qq_image, position)
        # 打开 jx.png，并将其粘贴到画布上，保留透明部分
        jx_image = pimg.open('./img/maimai_img/jx_base.png')
        canvas = pimg.alpha_composite(canvas, jx_image)
        # 保存结果图像
        canvas.save('./img/maimai_img/hbjx_img.png')
        return Image(path='./img/maimai_img/hbjx_img.png')




channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def lxhb_img(app: Ariadne, sender: Union[Group, Friend],
                   message: MessageChain = DetectPrefix(['/旅行伙伴', '/lxhb'])):
    await app.send_message(sender, MessageChain("/伙伴加入@xxx\n"
                                                "/伙伴觉醒@xxx\n\n"
                                                "可以将@他人替换为附带图片发送"))


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def lxhb_img(app: Ariadne, sender: Union[Group, Friend],
                   message: MessageChain = DetectPrefix(['/伙伴加入', '/hbjr'])):
    msg = message.as_persistent_string()
    await app.send_message(sender, hbjr(msg))

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def lxhb_img(app: Ariadne, sender: Union[Group, Friend],
                   message: MessageChain = DetectPrefix(['/伙伴觉醒', '/hbjx'])):
    msg = message.as_persistent_string()
    await app.send_message(sender, hbjx(msg))

