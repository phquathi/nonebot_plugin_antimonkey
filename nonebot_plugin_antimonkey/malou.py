from nonebot import on_message, logger
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, MessageSegment
from nonebot.adapters.onebot.v11.message import Message
from nonebot.plugin import require
from nonebot.adapters.onebot.v11 import GroupMessageEvent
import cv2
import aiohttp
import numpy as np

from .image_recognition import check_image

scheduler = require("nonebot_plugin_apscheduler").scheduler


async def download_image(url: str) -> np.ndarray:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                image_array = np.asarray(bytearray(image_data), dtype="uint8")
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                return image


revoke_plugin = on_message()


@revoke_plugin.handle()
async def handle_message(bot: Bot, event: MessageEvent):
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id
        member_info = await bot.get_group_member_info(group_id=group_id, user_id=event.self_id)  # 管理员检测，节省系统资源
        if member_info['role'] != 'admin':
            return

    msg: Message = event.message
    for seg in msg:
        if seg.type == 'image':
            try:
                image_url = seg.data['url']
                image = await download_image(image_url)
                if check_image(image):
                    await bot.delete_msg(message_id=event.message_id)
                    await bot.send(event, "请不要发猴子图片")
                    logger.info(f"撤回了包含猴子的图片并发送警告：{image_url}")
            except Exception as e:
                logger.error(f"处理图片时出错：{e}")