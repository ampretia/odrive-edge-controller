from loguru import logger

from anki_support import CarScanner, SimpleGame
from anki_support.game_support import TrackLighting


async def main():
    try:
        TrackLighting.Control.all_on()

        logger.info("Scanning for cars")
        cs = CarScanner()
        car_list = await cs.main_loop()
        logger.info(car_list)

        # logger.info("Scanning track....")
        # ts = TrackScanner(car_list)

        # track = await ts.get_track()
        # logger.info(track)

        s = SimpleGame(car_list)

        await s.play()
        TrackLighting.Control.all_off()

    except Exception as e:
        logger.error(e)
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
