from loguru import logger

import flatbuffers

from odrive_wsprotocol.Events import Events
import odrive_wsprotocol.CarScanEvent as CarScanEvent

import odrive_wsprotocol.Message as Message
import odrive_wsprotocol.Requests as Requests

import odrive_wsprotocol.TrackPiece as TrackPiece
import odrive_wsprotocol.TrackType as TrackType
import odrive_wsprotocol.TrackTurn as TrackTurn
import odrive_wsprotocol.TrackScanEvent as TrackScanEvent

from odrive_edge_controller.anki_sdk.car import Car
from odrive_edge_controller.anki_sdk.track.piece import Type
from odrive_edge_controller.game_support.car_scanner import CarScanner
from odrive_edge_controller.game_support.track_scanner import TrackScanner

# class WebSocketTransport(ITransport):
#     def __init__(self, websocket):
#         self.socket = websocket

#     async def send_position(self, data):
#         await self.socket.send(json.dumps(data))
#         logger.info("Sent position.....")
# ----

scancar = []


def mapType(t: Type):
    if t == Type.STRAIGHT:
        return TrackType.TrackType.straight
    elif t == Type.CURVE:
        return TrackType.TrackType.curve
    elif t == Type.FINISH:
        return TrackType.TrackType.finish
    elif t == Type.START:
        return TrackType.TrackType.start
    else:
        return TrackType.TrackType.undefined


def mapTurn(t: str):
    if t == "left":
        return TrackTurn.TrackTurn.left
    elif t == "right":
        return TrackTurn.TrackTurn.right
    else:
        return TrackTurn.TrackTurn.none


async def sendTrackScan(allcars):
    builder = flatbuffers.Builder(1027)

    logger.info("Scanning track...")
    ts = TrackScanner(allcars)
    layout = (await ts.get_track()).to_dict()
    logger.info(layout)
    piececount = len(layout["track"])
    #                 data = {"response": "layout", "layout": track.to_dict()}
    #                 await websocket.send(json.dumps(data))
    #                 logger.info(json.dumps(data))

    TrackScanEvent.TrackScanEventStartTrackVector(builder, piececount)
    for t in layout["track"]:
        if "turn" in t:
            turn = t["turn"]
        else:
            turn = "none"

        logger.info(f'{t["lid"]} {t["type"]} {turn}')

        TrackPiece.CreateTrackPiece(
            builder, t["lid"], mapType(t["type"]), mapTurn(turn)
        )
        
    trackscanvector = builder.EndVector()

    TrackScanEvent.Start(builder)
    TrackScanEvent.AddTrack(builder, trackscanvector)
    lse = TrackScanEvent.End(builder)

    Message.Start(builder)
    Message.AddEvent(builder, lse)
    Message.AddEventType(builder, Events.TrackScanEvent)

    msg = Message.End(builder)

    builder.Finish(msg)
    buffer = builder.Output()
    logger.info(buffer)
    return buffer


async def sendCarScan():
    global scancar
    builder = flatbuffers.Builder(1027)

    logger.info("Scanning for cars...")
    cs = CarScanner()
    cars = []
    allcars: list[Car] = await cs.scan()
    scancar = allcars
    for a in allcars:
        cse = a.get_scan_event(builder)
        cars.append(cse)

    # fakeCarCount = 4

    # for x in range(fakeCarCount):
    #     ca = builder.CreateString(f"CarAddress#{x}")
    #     cn = builder.CreateString("Skull")
    #     CarScan.Start(builder)
    #     CarScan.AddAddress(builder, ca)
    #     CarScan.AddName(builder, cn)
    #     cc = CarScan.End(builder)
    #     cars.append(cc)

    CarScanEvent.StartScansVector(builder, len(cars))
    for c in cars:
        builder.PrependSOffsetTRelative(c)
        # CarScanEvent.CarScanEventAddScans(builder, c)
    carscanvector = builder.EndVector()

    CarScanEvent.Start(builder)
    CarScanEvent.AddScans(builder, carscanvector)
    cse = CarScanEvent.End(builder)

    Message.Start(builder)
    Message.AddEvent(builder, cse)
    Message.AddEventType(builder, Events.CarScanEvent)

    msg = Message.End(builder)

    builder.Finish(msg)
    buffer = builder.Output()

    return buffer


async def handler(websocket):
    # allcars: list[Car] = None
    # track = None

    # wst = WebSocketTransport(websocket)

    async for msgdata in websocket:
        logger.info(msgdata)
        backMsg = Message.Message.GetRootAs(msgdata, 0)

        reqType = backMsg.RequestType()
        logger.info(reqType)
        if reqType == Requests.Requests.CarScanReq:
            logger.info("Car scan request")
            carscan = await sendCarScan()
            await websocket.send(carscan)
            logger.info("Sent car scan event")
            # logger.info("Scanning track...")
            # ts = TrackScanner(scancar)
            # track = await ts.get_track()
            # logger.info(track.to_dict())
        elif reqType == Requests.Requests.TrackScanReq:
            logger.info("Scanning track")
            layout = await sendTrackScan(scancar)
            await websocket.send(layout)
            logger.info("send track scan event")
        # evtType = backMsg.EventType()
        # if evtType == Events.CarScanEvent:
        #     evt = backMsg.Event()
        #     scanEvent = CarScanEvent.CarScanEvent()
        #     scanEvent.Init(evt.Bytes, evt.Pos)

        #     print(scanEvent.Name().decode("utf-8"))
        #     print(scanEvent.Address().decode("utf-8"))
