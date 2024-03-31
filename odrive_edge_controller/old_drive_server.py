# from loguru import logger
# import traceback
# import websockets
# from anki_support import CarScanner, SimpleGame
# from anki_support.anki_sdk import Controller, Car
# from anki_support.anki_sdk.i_netransport import ITransport
# from anki_support.game_support import TrackLighting, TrackScanner
# import json
# import flatbuffers

# import odrive_wsprotocol.adts.odrive.CarScan as CarScan
# import odrive_wsprotocol.adts.odrive.Message as Message
# import odrive_wsprotocol.adts.odrive.Events as Events

# from .game_support.car_scanner import CarScanner


# def carJson(car: Car):
#     cj = {
#         "name": car.get_name(),
#         "battery": 0,
#         "version": 0,
#         "address": car.get_address(),
#     }
#     return cj


# class WebSocketTransport(ITransport):
#     def __init__(self, websocket):
#         self.socket = websocket

#     async def send_position(self, data):
#         await self.socket.send(json.dumps(data))
#         logger.info("Sent position.....")


# async def handler(websocket):
#     allcars: list[Car] = None
#     track = None

#     wst = WebSocketTransport(websocket)

#     async for message in websocket:
#         event = json.loads(message)
#         if event["action"] == "scancars":
#             logger.info("Scanning for cars...")
#             cs = CarScanner()
#             allcars: list[Car] = await cs.scan()

#             logger.info(allcars)
#             data = {"response": "cars", "cars": [carJson(c) for c in allcars]}

#             await websocket.send(json.dumps(data))
#             logger.info(json.dumps(data))

#         elif event["action"] == "scantrack":
#             if not allcars or len(allcars) == 0:
#                 logger.warning("No cars")
#                 data = {"response": "error", "error": "no cars"}
#                 await websocket.send(json.dumps(data))
#             else:
#                 logger.info("Scanning track...")
#                 ts = TrackScanner(allcars)
#                 track = await ts.get_track()
#                 logger.info(track)

#                 data = {"response": "layout", "layout": track.to_dict()}
#                 await websocket.send(json.dumps(data))
#                 logger.info(json.dumps(data))

#         elif event["action"] == "movestart":
#             logger.info("Moving to start")

#             for c in allcars:
#                 ctrl = await c.get_controller()
#                 ctrl.set_layout(track)
#                 await ctrl.move_start()

#             data = {"response": "movestart", "movestart": True}
#             await websocket.send(json.dumps(data))

#         elif event["action"] == "freedrive":
#             simpleGame = SimpleGame(allcars)
#             simpleGame.play()

#         elif event["action"] == "wander":
#             for c in allcars:
#                 ctrl = await c.get_controller()
#                 ctrl.set_layout(track)
#                 await ctrl.set_speed(400, 400)
#                 await ctrl.live_tracking(wst)

#         else:
#             logger.error("unsupported event: {}", event)


