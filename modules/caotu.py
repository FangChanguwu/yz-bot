from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, At
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def caotu(app: Ariadne, group: Group, message: MessageChain):
    if message.display in ["/来张草图",'/草图','/随机草图']:
        session = Ariadne.service.client_session
        async with session.get("https://oss.grass.starxw.com/service/image") as resp:
            img_bytes = await resp.read()
        await app.send_message(group, MessageChain(Image(data_bytes=img_bytes)))
