from typing import Union


from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage, FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, Voice
from graia.ariadne.message.parser.base import ContainKeyword, DetectPrefix
from graia.ariadne.model import Friend
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graiax import silkcoder

channel = Channel.current()


@channel.use(
    ListenerSchema(
        listening_events=[GroupMessage, FriendMessage],
    )
)
async def oiias(app: Ariadne, sender: Union[Group, Friend], message: MessageChain = DetectPrefix(['/51121'])):
    voice_bytes = await silkcoder.async_encode("./src/audio/51121.m4a", ios_adaptive=True)
    await app.send_message(sender, MessageChain(Voice(data_bytes=voice_bytes)))
