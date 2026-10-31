import sys

from telethon.network.connection.tcpabridged import ConnectionTcpAbridged
from telethon.sessions import StringSession

from ..Config import Config
from .client import CatUserBotClient
from .string_session import to_telethon_string

__version__ = "3.3.0"

loop = None

if Config.STRING_SESSION:
    try:
        session_string, source_api_id = to_telethon_string(str(Config.STRING_SESSION))
    except ValueError as error:
        print(f"STRING_SESSION - {error}")
        sys.exit(1)
    if source_api_id and int(source_api_id) != int(Config.APP_ID):
        print(
            "STRING_SESSION - this Pyrogram session was created with "
            f"APP_ID {source_api_id}, but APP_ID is {Config.APP_ID}. "
            "Set APP_ID to that value and use the API_HASH from the same my.telegram.org app."
        )
        sys.exit(1)
    session = StringSession(session_string)
else:
    session = "catuserbot"

try:
    catub = CatUserBotClient(
        session=session,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH,
        loop=loop,
        app_version=__version__,
        connection=ConnectionTcpAbridged,
        auto_reconnect=True,
        connection_retries=None,
    )
except Exception as e:
    print(f"STRING_SESSION - {e}")
    sys.exit()


catub.tgbot = tgbot = CatUserBotClient(
    session="CatTgbot",
    api_id=Config.APP_ID,
    api_hash=Config.API_HASH,
    loop=loop,
    app_version=__version__,
    connection=ConnectionTcpAbridged,
    auto_reconnect=True,
    connection_retries=None,
).start(bot_token=Config.TG_BOT_TOKEN)
