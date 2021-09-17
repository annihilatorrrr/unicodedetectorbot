from os import environ


HERUKO = bool(environ.get("HERUKO", False))


if not HERUKO:
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"  # api hash
    APP_ID = int(6)  # api id
    BOT_USERNAME = ""  # without @
    BOT_TOKEN = ""  # token
    REDIS_URL = "" # redis db for storage
else:
    API_HASH = str(environ.get("API_HASH",
                               "eb06d4abfb49dc3eeb1aeb98ae0f581e"))  # api hash
    APP_ID = int(environ.get("APP_ID", 6))  # api id
    BOT_USERNAME = str(environ.get("BOT_USERNAME", "sex"))  # without @
    BOT_TOKEN = str(environ.get("BOT_TOKEN",
                                "123456789:ertyuioghjtrytr"))  # token
    REDIS_URL = str(environ.get("REDIS_URL", "")) # redis db for storage
