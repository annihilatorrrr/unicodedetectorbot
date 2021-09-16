import re
from logging import INFO, basicConfig, getLogger
from time import time

from pyrogram import Client, __version__, filters
from pyrogram.errors import ChatAdminRequired, RPCError
from pyrogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from redis import StrictRedis

from config import *

basicConfig(
    format="%(asctime)s - [DETECTOR] - %(levelname)s - %(message)s",
    level=INFO,
)
LOGGER = getLogger(__name__)
bot = Client(
    "detector",
    bot_token=BOT_TOKEN,
    api_id=APP_ID,
    api_hash=API_HASH,
    sleep_threshold=15,
)
BOT_ID = int(BOT_TOKEN.split(":")[0])

print(f"Started detector with pyrogram version {__version__}")

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)
try:
    REDIS.ping()
except BaseException:
    raise Exception("Your redis server is not alive, please check again.")

finally:
    REDIS.ping()
    LOGGER.info("Your redis server is alive!")


@bot.on_message(filters.command("start") & ~filters.bot)
async def start(_, m: Message):
    if m.chat.type != "private":
        return await m.reply_text("I'm alive!")
    kb = InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                text="Add me to your chat!",
                url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
            )
        ],
    ])
    return await m.reply_text(
        "Hi there! i'm the one who removes all unicode user from ur chat if u give me a chance!\nCheck /help !",
        reply_markup=kb,
    )


@bot.on_message(filters.command("help") & ~filters.bot)
async def help(_, m: Message):
    return await m.reply_text(
        "Just add me to your chat with ban user permission and toggle /detector on | off !"
    )


@bot.on_message(filters.command("ping") & ~filters.bot)
async def ping(_, m: Message):
    start = time()
    reply = await m.reply_text("Pinging ...")
    delta_ping = time() - start
    return await reply.edit_text(f"<b>Pong!</b>\n{delta_ping * 1000:.3f} ms")


# thanks to hamkercat for this shortcut
async def member_permissions(chat_id: int, user_id: int):
    perms = []
    try:
        member = await bot.get_chat_member(chat_id, user_id)
    except Exception:
        return []
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_change_info:
        perms.append("can_change_info")
    return perms


@bot.on_message(filters.command("detector") & ~filters.bot)
async def power(_, m: Message):
    if m and not m.from_user:
        return
    if m.chat.type == "private":
        return await m.reply_text("This command works only on supergroups.")

    permissions = await member_permissions(int(m.chat.id), int(m.from_user.id))
    if "can_change_info" not in permissions:
        return await m.reply_text("You don't have enough permissions!")
    args = m.text.split()
    status = REDIS.get(f"Chat_{m.chat.id}")

    if len(args) < 2:
        return await m.reply_text(
            f"This group's current setting is: `{status}`\nTry with on and off to toggle!"
        )
    option = args[1].lower()
    if option in ("yes", "on", "true"):
        REDIS.set(f"Chat_{m.chat.id}", str("True"))
        await m.reply_text(
            "Turned on.",
            quote=True,
        )
    elif option in ("no", "off", "false"):
        REDIS.set(f"Chat_{m.chat.id}", str("False"))
        await m.reply_text(
            "Turned off.",
            quote=True,
        )
    return


bot.run()
