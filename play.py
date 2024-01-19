from loguru import logger
import traceback
from anki_support import CarScanner, SimpleGame
from anki_support.anki_sdk import Controller, Car
from anki_support.game_support import TrackLighting, TrackScanner


async def main():
    try:
        TrackLighting.Control.all_on()

        logger.info("Scanning for cars...")
        cs = CarScanner()
        car_list: list[Car] = await cs.scan()
        logger.info(car_list)
               
        logger.info("Scanning track...")
        ts = TrackScanner(car_list)
        track = await ts.get_track()
        logger.info(track)
        await asyncio.sleep(3)
        logger.info("Scan complete")

        finish = track.get_finish()
        logger.info(finish)
        logger.info(finish.get_next())

        ctrl = await car_list[0].get_controller()
        ctrl.set_layout(track)

        await ctrl.move_start()
        logger.info("Got to the start line")

        await ctrl.set_speed(400, 400)
        logger.info("Good to run.....")
        
        await ctrl.live_tracking()

        # s = SimpleGame(car_list)

        # await s.play()

        TrackLighting.Control.all_off()
        await asyncio.sleep(30)

    except Exception as e:
        logger.error(e)
        traceback.print_exc(file=sys.stdout)
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
