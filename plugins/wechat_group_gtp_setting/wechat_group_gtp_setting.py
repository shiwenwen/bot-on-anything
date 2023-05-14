# encoding:utf-8

import os
import plugins
from plugins import *
from common import log
from common import functions


@plugins.register(name="WeChatGroupGPTSetting", desire_priority=80, hidden=True, desc="微信群聊高级设置", version="0.1",
                  author="ShiWenwen")
class WeChatGroupGPTSetting(Plugin):
    def __init__(self):
        super().__init__()
        self.handlers[Event.ON_HANDLE_CONTEXT] = self.select_model
        self.handlers[Event.ON_BRIDGE_HANDLE_STREAM_CONTEXT] = self.select_model
        log.info("[WeChatGroupGPTSetting] inited")

    def get_events(self):
        return self.handlers

    def select_model(self, e_context: EventContext):
        e_context.action = EventAction.CONTINUE  # 事件继续，交付给下个插件或默认逻辑
        return e_context
