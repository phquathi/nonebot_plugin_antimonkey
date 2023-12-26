from nonebot import get_driver
from nonebot.plugin import PluginMetadata

from .config import Config

global_config = get_driver().config
config = Config.parse_obj(global_config)

__plugin_meta__ = PluginMetadata(
    name="AntiMonkey",
    description="自动检测和撤回包含恶心吗喽的图片",
    usage="",
    type="application",
    homepage="https://github.com/phquathi/nonebot_plugin_antimonkey",
    config=None,
    supported_adapters={"~onebot.v11"}
)
