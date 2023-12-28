from loguru import logger
import asyncio
import sys
from ..anki_sdk import LocalalizationPosition, LocalalizationTransition
from ..anki_sdk import Controller, Car
from ..anki_sdk.events import IObserver

from ..anki_sdk.track import Curve, Straight, Start, Finish


class TrackScanner(IObserver):
    # private _callback: Function
    # private _locations: LocalizationPositionUpdate[]
    # private _pieces: IPiece[]
    # private _round: number
    # private _scanning: boolean
    # private _vehicle: IVehicle

    def __init__(self,car_list):
        self.scanning = False
        self.locations = []
        self.pieces = []
        self.round = 0
        self.car_list = car_list

    async def update(self, event) -> None:
        if type(event) is LocalalizationTransition and len(self.locations) > 0:
            position = self.locations[0]
            transition = event
            piece = self.createPiece(position, transition)

            if self.round == 2:               
                await self.controller.set_speed(0, 200)
                await self.scan_car.stop_notify(self)
                await self.scan_car.disconnect()
                async with self.condition:
                    self.condition.notify()
            elif self.isStart(position.roadPieceId):
                self.round += 1
            elif self.round == 1 and piece:
                self.pieces.append(piece)

            self.locations = []
        elif type(event) is LocalalizationPosition:
            
            logger.info(f"Appending  {event}")
            self.locations.append(event)

    async def shutdown(self):
        await self.scan_car.disconnect()


    async def get_track(self):
        self.condition = asyncio.Condition()
        async with self.condition:
            _ = asyncio.create_task(self.main_loop())
            await self.condition.wait()

            return self.pieces

    async def main_loop(self):

        # start scanner and add event listener
        self.scan_car = self.car_list[0]
        await self.scan_car.connect()

        self.controller = Controller(self.scan_car)
        await self.scan_car.start_notify(self)

        await self.controller.set_speed(400, 200)

        logger.info("Scannig...")

    def createPiece(
        self, position: LocalalizationPosition, transition: LocalalizationTransition
    ):
        logger.info(f"Create Track Piece {position} {transition}")

        if self.isCurve(transition):
            logger.info("..curve")
            return Curve(position.get_road_piece_id())

        if self.isStraight(position, transition):
            logger.info("..straight")
            return Straight(position.get_road_piece_id())
        
        if self.isStart(position.get_road_piece_id()):
            logger.info("..start")

        if self.isStart(position.get_road_piece_id()):
            logger.info("..finish")


    def isStart(self, roadPieceId: int) -> bool:
        return roadPieceId == Start.ID

    def isFinish(self, roadPieceId: int) -> bool:
        return roadPieceId == Finish.ID

    def isStraight(
        self,
        position: LocalalizationPosition,
        transition: LocalalizationTransition,
    ) -> bool:
        
        lr_diff = abs(transition.get_right_wheel_dist() - transition.get_left_wheel_dist())

        return (
            not self.isStart(position.get_road_piece_id())
            and not self.isFinish(position.get_road_piece_id())
            and (lr_diff == 0 or lr_diff == 1)
        )

    def isCurve(self, transition: LocalalizationTransition) -> bool:
        return abs(transition.get_right_wheel_dist() - transition.get_left_wheel_dist()) > 1


# }

# export{TrackScanner}
