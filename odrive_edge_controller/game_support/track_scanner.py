from loguru import logger
import asyncio

from ..anki_sdk import Controller, Car
from ..anki_sdk.events import (
    IObserver,
    LocalizationPosition,
    LocalizationTransition,
)

from ..anki_sdk.track import Curve, Straight, Start, Finish, Layout


class TrackScanner(IObserver):

    def __init__(self, car_list: list[Car]):
        self.scanning = False
        self.locations = []
        self.pieces = []
        self.round = 0
        self.car_list = car_list

    async def update(self, event) -> None:
        if type(event) is LocalizationTransition and len(self.locations) > 0:
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
            
            if self.round == 1 and piece:
                self.pieces.append(piece)

            self.locations = []
        elif type(event) is LocalizationPosition:
            logger.info(f"Appending  {event}")
            self.locations.append(event)

    async def shutdown(self):
        await self.scan_car.disconnect()

    async def get_track(self):
        self.condition = asyncio.Condition()
        async with self.condition:
            _ = asyncio.create_task(self.main_loop())
            await self.condition.wait()
            await self.scan_car.disconnect()
            return Layout(self.pieces)

    async def main_loop(self):
        # start scanner and add event listener
        self.scan_car = self.car_list[0]
        await self.scan_car.connect()

        self.controller = Controller(self.scan_car)
        await self.scan_car.start_notify(self)

        await self.controller.set_speed(400, 200)

        logger.info("Scanning...")

    def createPiece(
        self, position: LocalizationPosition, transition: LocalizationTransition
    ):
        logger.info(f"Create Track Piece p={position} tr={transition}")

        if self.isCurve(transition):
            logger.info("..curve")
            return Curve(position.get_road_piece_id(), self.turn(transition))

        if self.isStraight(position, transition):
            logger.info("..straight")
            return Straight(position.get_road_piece_id())

        if self.isStart(position.get_road_piece_id()):
            logger.info("..start")
            return Start()

        if self.isFinish(position.get_road_piece_id()):
            logger.info("..finish")
            return Finish()

    def isStart(self, roadPieceId: int) -> bool:
        return roadPieceId == Start.ID

    def isFinish(self, roadPieceId: int) -> bool:
        return roadPieceId == Finish.ID

    def isStraight(
        self,
        position: LocalizationPosition,
        transition: LocalizationTransition,
    ) -> bool:
        lr_diff = abs(
            transition.get_right_wheel_dist() - transition.get_left_wheel_dist()
        )

        return (
            not self.isStart(position.get_road_piece_id())
            and not self.isFinish(position.get_road_piece_id())
            and (lr_diff == 0 or lr_diff == 1)
        )

    def turn(self, transition: LocalizationTransition) -> str:
        logger.info("right {} left {}",transition.get_right_wheel_dist(),transition.get_left_wheel_dist())
        if (transition.get_right_wheel_dist() - transition.get_left_wheel_dist()) > 0:
            return 'left'
        else:
            return 'right'

    def isCurve(self, transition: LocalizationTransition) -> bool:
        return (
            abs(transition.get_right_wheel_dist() - transition.get_left_wheel_dist())
            > 1
        )
