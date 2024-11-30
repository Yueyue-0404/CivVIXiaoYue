# -*- coding: utf-8 -*-
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.manage import GroupManageEvent
from botpy.message import GroupMessage, Message
from .settings import *
from .controller import Controller
from . import accessor

test_config = read(CONFIG_DIR.joinpath("config.yaml"))
_log = logging.get_logger()


class CivVIBot(botpy.Client):
    def __init__(self):
        intents = botpy.Intents(public_messages=True)
        super().__init__(intents=intents)
        self.ctrl = Controller()

    async def on_group_add_robot(self, event: GroupManageEvent):
        _log.info("机器人被添加到了群聊：" + str(event))
        await self.api.post_group_message(
            group_openid=event.group_openid,
            msg_type=0,
            event_id=event.event_id,
            content="你好，我是小钥。\n小钥能够为您便捷快速地查询文明6原版数据，快来@我试试吧！",
        )

    async def on_group_at_message_create(self, message: GroupMessage):
        print(message.content)
        command = self.ctrl.parseMSG(message.content)  # 解析命令
        result = self.ctrl.assignQueryMission(*command)  # 执行命令返回查询结果
        result = self.ctrl.defendSQLInjectionAttack(result)  # qq官方拒绝处理sql注入攻击，需要自己手写防御脚本
        messageResult = await message._api.post_group_message(
            group_openid=message.group_openid,
            msg_type=0,
            msg_id=message.id,
            content=result,
        )
        _log.info(messageResult)

    # async def on_group_at_file_create(self, message: GroupMessage):
    #     file_url = ""  # 这里需要填写上传的资源Url
    #     uploadMedia = await message._api.post_group_file(
    #         group_openid=message.group_openid,
    #         file_type=1, # 文件类型要对应上，具体支持的类型见方法说明
    #         url=file_url # 文件Url
    #     )
