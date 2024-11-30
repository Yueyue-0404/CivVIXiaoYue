# -*- coding: utf-8 -*-
import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.manage import GroupManageEvent
from botpy.message import GroupMessage

from .controller import Controller
from .settings import *

# from . import accessor

test_config = read(CONFIG_DIR.joinpath("config.yaml"))
log_config = read(CONFIG_DIR.joinpath("log_config.yaml"))
_log = logging.get_logger()
logging.configure_logging(config=log_config)


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
            content="你好，我是Civ‌Ⅵ小钥。\n小钥能够为您便捷快速地查询文明6原版数据，快来@我试试吧！",
        )

    async def on_group_at_message_create(self, message: GroupMessage):
        print(message.content)
        command = self.ctrl.parseMSG(message.content)  # 解析命令
        result, context = self.ctrl.assignQueryMission(*command)  # 执行命令返回查询结果
        if context.get("type") == 0:
            result = self.ctrl.defendSQLInjectionAttack(result)  # qq官方拒绝处理sql注入攻击，需要自己手写防御脚本
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content=result,
            )
        elif context.get("type") == 1:
            file_url = context.get("file_url")
            uploadMedia = await message._api.post_group_file(
                group_openid=message.group_openid,
                file_type=1,
                url=file_url
            )
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=7,  # 7表示富媒体类型
                msg_id=message.id,
                media=uploadMedia
            )
        else:
            messageResult = await message._api.post_group_message(
                group_openid=message.group_openid,
                msg_type=0,
                msg_id=message.id,
                content="未知错误",
            )
        _log.info(messageResult)
