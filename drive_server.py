from loguru import logger
import traceback
import websockets
from anki_support import CarScanner, SimpleGame
from anki_support.anki_sdk import Controller, Car
from anki_support.anki_sdk.i_netransport import ITransport
from anki_support.game_support import TrackLighting, TrackScanner
import json


def carJson(car: Car):
    cj = {
        "name": car.get_name(),
        "battery": 0,
        "version": 0,
        "address": car.get_address(),
    }
    return cj


class WebSocketTransport(ITransport):
    def __init__(self, websocket):
        self.socket = websocket

    async def send_position(self, data):
        await self.socket.send(json.dumps(data))
        logger.info("Sent position.....")


async def handler(websocket):
    allcars: list[Car] = None
    track = None

    wst = WebSocketTransport(websocket)

    async for message in websocket:
        event = json.loads(message)
        if event["action"] == "scancars":
            logger.info("Scanning for cars...")
            cs = CarScanner()
            allcars: list[Car] = await cs.scan()

            logger.info(allcars)
            data = {"response": "cars", "cars": [carJson(c) for c in allcars]}

            await websocket.send(json.dumps(data))
            logger.info(json.dumps(data))

        elif event["action"] == "scantrack":
            if not allcars or len(allcars) == 0:
                logger.warning("No cars")
                data = {"response": "error", "error": "no cars"}
                await websocket.send(json.dumps(data))
            else:
                logger.info("Scanning track...")
                ts = TrackScanner(allcars)
                track = await ts.get_track()
                logger.info(track)

                data = {"response": "layout", "layout": track.to_dict()}
                await websocket.send(json.dumps(data))
                logger.info(json.dumps(data))

        elif event["action"] == "movestart":
            logger.info("Moving to start")

            for c in allcars:
                ctrl = await c.get_controller()
                ctrl.set_layout(track)
                await ctrl.move_start()

            data = {"response": "movestart", "movestart": True}
            await websocket.send(json.dumps(data))

        elif event["action"] == "freedrive":
            simpleGame = SimpleGame(allcars)
            simpleGame.play()

        elif event["action"] == "wander":
            for c in allcars:
                ctrl = await c.get_controller()
                ctrl.set_layout(track)
                await ctrl.set_speed(400, 400)
                await ctrl.live_tracking(wst)

        else:
            logger.error("unsupported event: {}", event)


async def main():
    try:
        logger.info("Starting websocket server..")
        async with websockets.serve(handler, "0.0.0.0", 8765):
            await asyncio.Future()  # run forever

    except Exception as e:
        logger.error(e)
        traceback.print_exc(file=sys.stdout)

        # logger.info("Got to the start line")

        # await ctrl.set_speed(400, 400)
        # logger.info("Good to run.....")

        # await ctrl.live_tracking()

        # s = SimpleGame(car_list)

        # await s.play()

        # TrackLighting.Control.all_off()
        # await asyncio.sleep(30)

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
