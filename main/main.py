from bot.client import get_client
from core.handler.events import register_events
from core.redis.conection import ConnectionSupplier
import settings as settings
from bot.loop import get_loop


# это мать его маейн, не забудь API_KEY прописать в settings

async def main():
    if settings.DEBUG_MODE:
        await ConnectionSupplier.clear_all()
    client = get_client()
    register_events(client)
    await client.start(settings.API_KEY)


if __name__ == '__main__':
    loop = get_loop()
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        loop.run_until_complete(get_client().logout())
    finally:
        loop.run_until_complete(get_client().close())
