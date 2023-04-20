from typing import Union

import requests
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group, Friend
from graia.ariadne.message.element import Image

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import numpy as np
from PIL import Image as pimg

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend], message: MessageChain):
    if str(message) in ['/图片镜像','/pic_mirror']:
        await app.send_message(
            sender,
            MessageChain('请附带图片发送\n'
                         '/左镜像[图片]\n'
                         '/右镜像[图片]\n'
                         '/上镜像[图片]\n'
                         '/下镜像[图片]')
        )



@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend], message: MessageChain = DetectPrefix(['/镜像','/镜像图片','/mirror','/图片镜像'])):
        await app.send_message(
            sender,
            MessageChain('/左镜像[图片]\n'
                         '/右镜像[图片]\n'
                         '/上镜像[图片]\n'
                         '/下镜像[图片]')
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend],
               message: MessageChain = DetectPrefix(['/左镜像', '/左镜像图片', '/lmirror'])):
    # 判断消息中有没有图片
    if 'gchat.qpic.cn' not in message.as_persistent_string():
        await app.send_message(
            sender,
            MessageChain('byd不发图片镜像你妈呢'),
        )
    else:
        # 获取图片链接
        img_url = message.as_persistent_string().split('url":"')[1]
        img_url = img_url.split('","')[0]
        url = img_url
        r = requests.get(url)
        # 把图片下载到本地
        with open("./img/src.jpg", "wb") as f:
            f.write(r.content)
        # PIL打开图片
        img = pimg.open('./img/src.jpg')
        size = img.size
        # 框定裁剪范围
        box = (0, 0, int(size[0] / 2), size[1])
        img_crop = img.crop(box)
        # 镜像
        img_crop2 = img_crop.transpose(pimg.FLIP_LEFT_RIGHT)
        # 拼接
        img_raw = np.concatenate((img_crop, img_crop2), axis=1)
        img_output = pimg.fromarray(img_raw)
        img_output.save('./img/img_output.jpg')
        await app.send_message(
            sender,
            MessageChain('byd你图片镜像好了' + Image(path='./img/img_output.jpg')),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend],
               message: MessageChain = DetectPrefix(['/右镜像', '/右镜像图片', '/rmirror'])):
    if 'gchat.qpic.cn' not in message.as_persistent_string():
        await app.send_message(
            sender,
            MessageChain('byd不发图片镜像你妈呢'),
        )
    else:
        img_url = message.as_persistent_string().split('url":"')[1]
        img_url = img_url.split('","')[0]
        url = img_url
        r = requests.get(url)
        with open("./img/src.jpg", "wb") as f:
            f.write(r.content)
        img = pimg.open('./img/src.jpg')
        size = img.size
        box = (int(size[0] / 2), 0, size[0], size[1])
        img_crop = img.crop(box)
        img_crop2 = img_crop.transpose(pimg.FLIP_LEFT_RIGHT)
        img_raw = np.concatenate((img_crop2, img_crop), axis=1)
        img_output = pimg.fromarray(img_raw)
        img_output.save('./img/img_output.jpg')
        await app.send_message(
            sender,
            MessageChain('byd你图片镜像好了' + Image(path='./img/img_output.jpg')),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend],
               message: MessageChain = DetectPrefix(['/上镜像', '/上镜像图片', '/umirror'])):
    if 'gchat.qpic.cn' not in message.as_persistent_string():
        await app.send_message(
            sender,
            MessageChain('byd不发图片镜像你妈呢'),
        )
    else:
        img_url = message.as_persistent_string().split('url":"')[1]
        img_url = img_url.split('","')[0]
        url = img_url
        r = requests.get(url)
        with open("./img/src.jpg", "wb") as f:
            f.write(r.content)
        img = pimg.open('./img/src.jpg')
        size = img.size
        box = (0, 0, size[0],int(size[1]/2))
        img_crop = img.crop(box)
        img_crop2 = img_crop.transpose(pimg.FLIP_TOP_BOTTOM)
        img_raw = np.concatenate((img_crop, img_crop2), axis=0)
        img_output = pimg.fromarray(img_raw)
        img_output.save('./img/img_output.jpg')
        await app.send_message(
            sender,
            MessageChain('byd你图片镜像好了' + Image(path='./img/img_output.jpg')),
        )


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, sender: Union[Group, Friend],
               message: MessageChain = DetectPrefix(['/下镜像', '/下镜像图片', '/dmirror'])):
    if 'gchat.qpic.cn' not in message.as_persistent_string():
        await app.send_message(
            sender,
            MessageChain('byd不发图片镜像你妈呢'),
        )
    else:
        img_url = message.as_persistent_string().split('url":"')[1]
        img_url = img_url.split('","')[0]
        url = img_url
        r = requests.get(url)
        with open("./img/src.jpg", "wb") as f:
            f.write(r.content)
        img = pimg.open('./img/src.jpg')
        size = img.size
        box = (0,int(size[1]/2), size[0],size[1])
        img_crop = img.crop(box)
        img_crop2 = img_crop.transpose(pimg.FLIP_TOP_BOTTOM)
        img_raw = np.concatenate((img_crop2, img_crop), axis=0)
        img_output = pimg.fromarray(img_raw)
        img_output.save('./img/img_output.jpg')
        await app.send_message(
            sender,
            MessageChain('byd你图片镜像好了' + Image(path='./img/img_output.jpg')),
        )

