import logging
import tensorflow as tf
from keras.applications.mobilenet_v2 import MobileNetV2, preprocess_input
from keras.preprocessing.image import img_to_array
import numpy as np
import cv2
from keras.src.applications import imagenet_utils
from nonebot import on_message, require
from nonebot.rule import Rule
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
import aiohttp

# 配置日志记录
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.info("Loading MobileNetV2 model...")
# MobileNetV2模型
model = MobileNetV2(weights="imagenet")


def check_image(image: np.ndarray) -> bool:
    """
    检查图像中是否有猴子。
    :param image: OpenCV图像数组。
    :return: 如果图像中有猴子，返回True；否则返回False。
    """
    logger.debug("Resizing image...")
    image = cv2.resize(image, (224, 224))

    logger.debug("Converting image to array...")
    image = img_to_array(image)
    image = np.expand_dims(image, axis=0)
    image = preprocess_input(image)

    logger.debug("Predicting image...")
    predictions = model.predict(image)
    results = imagenet_utils.decode_predictions(predictions)

    monkey_labels = {
        "guenon", "guenon monkey",
        "patas", "hussar monkey", "Erythrocebus patas",
        "baboon",
        "macaque",
        "langur",
        "colobus", "colobus monkey",
        "proboscis monkey", "Nasalis larvatus",
        "marmoset",
        "capuchin", "ringtail", "Cebus capucinus",
        "howler monkey", "howler",
        "titi", "titi monkey",
        "spider monkey", "Ateles geoffroyi",
        "squirrel monkey", "Saimiri sciureus"
    }

    logger.debug("Checking predictions...")
    for _, label, probability in results[0]:
        if label in monkey_labels and probability > 0.1:  # 阈值
            logger.info(f"Detected monkey with probability {probability:.2f}")
            return True
    logger.info(f"No monkey detected, highest probability: {probability:.2f}")
    return False


scheduler = require("nonebot_plugin_apscheduler").scheduler


async def download_image(url: str) -> np.ndarray:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                image_data = await resp.read()
                image_array = np.asarray(bytearray(image_data), dtype="uint8")
                image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
                return image


async def group_message_contains_image(event: MessageEvent) -> bool:
    if isinstance(event, GroupMessageEvent) and any(seg.type == 'image' for seg in event.message):
        logger.debug("Message contains image.")
        return True
    logger.debug("Message does not contain image.")
    return False


revoke_plugin = on_message(rule=Rule(group_message_contains_image))


@revoke_plugin.handle()
async def handle_image_message(bot: Bot, event: GroupMessageEvent):
    group_id = event.group_id
    logger.debug(f"Received image message in group {group_id}")
    member_info = await bot.get_group_member_info(group_id=group_id, user_id=event.self_id)  # 管理员检测
    logger.debug(f"Bot role in group: {member_info['role']}")
    if member_info['role'] != 'admin':
        logger.debug("Bot is not admin. Exiting.")
        return

    for seg in event.message:
        if seg.type == 'image':
            try:
                image_url = seg.data['url']
                logger.debug(f"Downloading image from {image_url}")
                image = await download_image(image_url)
                if check_image(image):
                    await bot.call_api('delete_msg', message_id=event.message_id)
                    await bot.send(event, "请不要发猴子图片")
                    logger.info(f"撤回了包含猴子的图片并发送警告：{image_url}")
                else:
                    logger.debug("Image does not contain monkey.")
            except Exception as e:
                logger.error(f"处理图片时出错：{e}")
