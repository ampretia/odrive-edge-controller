
import sys
import asyncio

from loguru import logger

from anki_support import SimpleGame, TrackScanner, CarScanner
        
async def main():
    try:
        logger.info("Scanning for cars")
        cs = CarScanner()
        car_list = await cs.main_loop()
        logger.info(car_list)

        ts = TrackScanner(car_list)
        logger.info("Scanning track....")
        track = await ts.get_track()
        for t in track:
            logger.info(t)

        s = SimpleGame(car_list)
        await s.play()

    finally:
        await ts.shutdown()

if __name__ == "__main__":
    import asyncio
    import sys

    try:
        asyncio.run(main())
    except KeyboardInterrupt:       
        sys.exit(0)
    except Exception:
        sys.exit(0)


