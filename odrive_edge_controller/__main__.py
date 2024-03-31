# https://www.freecodecamp.org/news/how-to-build-and-publish-python-packages-with-poetry/
# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
from loguru import logger
import traceback
import websockets


from .drive_server import handler


async def main():
    try:
        logger.info("Starting websocket server..")
        async with websockets.serve(handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    except Exception as e:
        logger.error(e)
        traceback.print_exc(file=sys.stdout)


if __name__ == "__main__":
    import asyncio
    import sys

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)
