from loguru import logger

from anki_support import CarScanner
from anki_support.anki_sdk import Controller
from anki_support.game_support import TrackLighting

import traceback


def log(payload) -> str:
    text = "["
    for v in list(payload):
        text += f"{v:02X} "

    text = text.strip()
    text += "]"
    return text


async def main():
    try:
        TrackLighting.Control.all_on()

        logger.info("Scanning for cars")
        cs = CarScanner()
        car_list = await cs.scan()
        logger.info(car_list)

        for car in car_list:
            await car.connect()

            ctrl = Controller(car)
            # await ctrl.set_speed(400)
            await ctrl.set_engine_light(127, 0, 0)

        await asyncio.sleep(20)

    except Exception as e:
        print(traceback.format_exc())
        logger.error(e)
        logger.catch(e)
    # finally:
    # await ts.shutdown()


if __name__ == "__main__":
    import asyncio
    import sys

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        sys.exit(0)
