import datetime
import random
import re
import sqlite3
from datetime import date

from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.message.element import Image, At, Plain
from graia.ariadne.message.parser.base import DetectPrefix
from graia.ariadne.model import Group, Friend, MemberInfo, Member
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from typing import Union


def istable(name):
    conn = sqlite3.connect('./database/day_lucky.db')
    c = conn.cursor()
    table_name = name
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    result = c.fetchone()
    if result:
        conn.close()
        return True
    else:
        conn.execute('''CREATE TABLE lucky
                     (qq INT PRIMARY KEY NOT NULL,
                      today TEXT NOT NULL,
                      luck_num INT NOT NULL);''')
        conn.close()
        return False


def lucky_num(qq, today=None):
    table_name = 'lucky'
    table = istable(table_name)
    conn = sqlite3.connect('./database/day_lucky.db')
    c = conn.cursor()
    if today is None:
        today = date.today().strftime('%Y%m%d')
    else:
        today = datetime.strptime(today, '%Y%m%d').strftime('%Y%m%d')
    c.execute("SELECT luck_num FROM " + table_name + " WHERE qq=? AND today=?", (qq, today))
    result = c.fetchone()
    if result:
        # 如果记录已经存在，则不更新运势值
        luck_num = result[0]
    else:
        luck_num = random.randint(1, 100)
        c.execute("INSERT INTO " + table_name + " (qq, today, luck_num) VALUES (?, ?, ?)", (qq, today, luck_num))
        conn.commit()
    conn.close()
    return MessageChain(At(qq), Plain('你今天的运势是：' + str(luck_num)))


channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def lxhb_img(app: Ariadne,
                   sender: Union[Group, Friend],
                   member: Member,
                   message: MessageChain = DetectPrefix(['/dbtest'])):
    qq = member.id
    today = date.today().strftime('%Y%m%d')
    await app.send_message(sender, lucky_num(qq, today))