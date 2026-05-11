import json
import logging
import random
from pathlib import Path

from astrbot.api.star import Context, Star, register
from astrbot.api.event import AstrMessageEvent, MessageEventResult
from astrbot.api.event.filter import event_message_type, EventMessageType
from astrbot.api.all import *

logger = logging.getLogger(__name__)

# =========================
# 路径配置
# =========================

BASE_DIR = Path(__file__).parent

CHARACTER_DIR = BASE_DIR / "character"
CHARACTER_MAP_FILE = BASE_DIR / "character_map.json"


# =========================
# 加载关键词映射
# =========================

def load_character_map():

    if not CHARACTER_MAP_FILE.exists():
        logger.warning("character_map.json 不存在")
        return {}

    try:
        with open(CHARACTER_MAP_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        logger.info("角色关键词映射加载成功")
        return data

    except Exception as e:
        logger.error(f"加载 character_map.json 失败: {e}")
        return {}


CHARACTER_MAP = load_character_map()


# =========================
# 动态读取角色文本
# =========================

def get_random_dialog(character_name: str):


    file_path = CHARACTER_DIR / f"{character_name}.json"

    if not file_path.exists():
        logger.warning(f"角色文件不存在: {file_path.name}")
        return None

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        dialogs = data.get("dialogs", [])

        if not dialogs:
            logger.warning(f"{character_name}.json 中 dialogs 为空")
            return None

        return random.choice(dialogs)

    except Exception as e:
        logger.error(f"读取角色文件失败 {character_name}: {e}")
        return None


# =========================
# 主插件
# =========================

@register("PGR", "KurisuRee7", "战双文本插件", "2.0", "https://github.com/KurisuRee7/astrBot_PGR_Dialogue")
class PGR_Plugin(Star):

    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        self.config = config

    @event_message_type(EventMessageType.ALL)
    async def on_message(self, event: AstrMessageEvent) -> MessageEventResult:

        msg_obj = event.message_obj
        text = msg_obj.message_str or ""

        # 转小写（兼容 Nanami / nanami）
        text_lower = text.lower()

        probability = float(self.config.get("probability", 0.3))

        # 概率判定
        if random.random() >= probability:
            return

        # 遍历角色关键词映射
        for character_name, keywords in CHARACTER_MAP.items():

            # 命中任意关键词
            if any(keyword.lower() in text_lower for keyword in keywords):

                reply = get_random_dialog(character_name)

                if reply:
                    yield event.plain_result(reply)

                return
