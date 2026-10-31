import base64
import ipaddress
import struct

# Pyrogram 2 stores dc_id, api_id, test_mode, auth_key, user_id, is_bot.
_PYROGRAM_V2 = ">BI?256sQ?"
# Older Pyrogram strings omit api_id from the front of the struct.
_PYROGRAM_V1 = ">B?256sI?"
# Telethon StringSession: version byte "1" plus dc_id, ipv4, port, auth_key.
_TELETHON_STRUCT = ">B4sH256s"
_DC_IPV4 = {
    1: "149.154.175.53",
    2: "149.154.167.51",
    3: "149.154.175.100",
    4: "149.154.167.91",
    5: "91.108.56.130",
}


def _unquote(value: str) -> str:
    value = str(value).strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1].strip()
    return value


def _b64decode(value: str) -> bytes:
    return base64.urlsafe_b64decode(value + "=" * (-len(value) % 4))


def to_telethon_string(raw: str) -> tuple[str, int | None]:
    """Return a Telethon string session and the Pyrogram api_id, if any.

    Strings that already start with Telethon's version marker are returned
    unchanged. Pyrogram session strings are repacked into Telethon's format
    so the rest of the userbot can keep using Telethon.
    """
    value = _unquote(raw)
    if not value:
        raise ValueError("STRING_SESSION is empty")
    if value.startswith("1"):
        return value, None

    data = _b64decode(value)
    api_id = None
    if len(data) == struct.calcsize(_PYROGRAM_V2):
        dc_id, api_id, test_mode, auth_key, _user_id, is_bot = struct.unpack(_PYROGRAM_V2, data)
    elif len(data) == struct.calcsize(_PYROGRAM_V1):
        dc_id, test_mode, auth_key, _user_id, is_bot = struct.unpack(_PYROGRAM_V1, data)
    else:
        raise ValueError("STRING_SESSION is not a Telethon or Pyrogram session string")

    if is_bot:
        raise ValueError("STRING_SESSION is a Pyrogram bot session. CatUserbot needs the user account session.")
    if test_mode:
        raise ValueError("STRING_SESSION is a Telegram test-mode session, which this converter does not load.")
    ip = _DC_IPV4.get(int(dc_id))
    if ip is None or not any(auth_key):
        raise ValueError("STRING_SESSION could not be converted to a Telethon session")

    packed = struct.pack(_TELETHON_STRUCT, int(dc_id), ipaddress.ip_address(ip).packed, 443, auth_key)
    return "1" + base64.urlsafe_b64encode(packed).decode("ascii"), (int(api_id) if api_id else None)
