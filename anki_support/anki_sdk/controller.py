import struct
import asyncio
from anki_support.anki_sdk.car_position import CarPosition
from anki_support.anki_sdk.i_netransport import ITransport
from .events import IObserver, LocalizationPosition, LocalizationTransition
from .track import Layout
from .car_interface import ICar
from .protocol import Protocol
from loguru import logger


class Controller:
    """Controller class object

    Args:
        carClass (carClass): Car to be controlled
    """

    def __init__(self, car: ICar):
        self.car: ICar = car
        self.speed = 0
        self.accel = 0
        self.light = (0, 0, 0)

    def set_layout(self, layout: Layout):
        self.position = CarPosition(layout, self.car)
        self.position.set_finish()

    async def live_tracking(self, transport: ITransport) -> None:
        class LiveProxy(IObserver):
            def __init__(self, ctrl):
                self.ctrl = ctrl

            async def run(self):
                await self.ctrl.car.start_notify(self)

            async def update(self, event):
                if type(event) is LocalizationPosition:
                    self.ctrl.position.position(event)
                elif type(event) is LocalizationTransition:
                    self.ctrl.position.transistion(event)

                # logger.info(self.ctrl.position.to_dict())
                await transport.send_position(self.ctrl.position.to_dict())

        await LiveProxy(self).run()

    async def move_start(self) -> None:
        moved = asyncio.Condition()

        class proxy(IObserver):
            def __init__(self, ctrl):
                self.ctrl = ctrl

            async def run(self):
                await self.ctrl.set_speed(400)
                await self.ctrl.car.start_notify(self)

            async def update(self, event):
                if type(event) is LocalizationPosition:
                    if event.get_road_piece_id() == 34:
                        logger.info("Got to what I think is the finish")
                        await self.ctrl.set_speed(0, 2000)
                        self.ctrl.position.set_finish()
                        logger.info(self.ctrl.position)
                        await self.ctrl.car.stop_notify(self)
                        async with moved:
                            moved.notify()

        _ = asyncio.create_task(proxy(self).run())
        async with moved:
            await moved.wait()

    # async def update(self, event) -> None:
    #     logger.info(event)

    async def set_speed(self, speed: int, accel: int | None = 1000, limit: bool = True):
        """Set the vehicle speed

        Args:
            speed (int): Speed to set.
            accel (int): Accelration. Defaults to 1000.
        """
        if accel is None:
            accel = 1000

        speed_limit = 0x01 if limit else 0x0

        command = struct.pack(
            "<BHHB", Protocol.CommandList.SET_SPEED, speed, accel, speed_limit
        )
        self.speed = speed
        self.accel = accel
        await self.car.send_command(command)

    async def turn(self, type, trigger):
        command = struct.pack("<BBB", Protocol.CommandList.TURN, type, trigger)
        await self.car.send_command(command)

    async def set_lane(self, offset: float = 0.0):
        """Set the current lane for the vehicle (doesn't move the car)

        Args:
            offset (float): Offset from lane. Defaults to 0.0.
        """
        command = struct.pack("<Bf", Protocol.CommandList.RESET_LANE, offset)
        await self.car.send_command(command)

    async def change_lane(self, offset: float):
        """Change current lane

        -44.5 left
        44.5 right

        Args:
            offset (float): How much the car should move.
        """
        command = struct.pack(
            "<BHHf", Protocol.CommandList.CHANGE_LANE, self.speed, self.accel, offset
        )
        await self.car.send_command(command)

    async def left_lane(self, lanes: float = 1.0):
        """Change the lane to left

        Args:
            lanes (float): How many lanes to left. Default 1.0
        """
        lane = lanes * -44.5
        await self.change_lane(lane)

    async def right_lane(self, lanes: float = 1.0):
        """Change the lane to right

        Args:
            lanes (float): How many lanes to right. Default 1.0
        """
        lane = lanes * 44.5
        await self.change_lane(lane)

    def __encodeLightChange(self, val: int):
        if val == "l":
            message = bytearray(3)
            struct.pack_into("BBB", message, 0, 0x02, 0x1D, 140)
        elif val == "lp":
            message = bytearray(9)
            struct.pack_into("BBBBBHB", message, 0, 0x07, 0x33, 5, 1, 1, 5, 0)
        else:
            message = None
        return message

    async def set_light(self, value: str | int):
        """_summary_

        Args:
            value (int):
                LIGHT_HEADLIGHTS:    0
                LIGHT_BRAKELIGHTS:   1
                LIGHT_FRONTLIGHTS:   2
                LIGHT_ENGINE:        3
        """
        message = self.__encodeLightChange(value)
        logger.info("sending light command")
        await self.car.send_command(bytes(message))

    def __encodeEngineLightChange(self, r, g, b):
        message = bytearray(18)
        struct.pack_into(
            "BBBBBBBBBBBBBBBBBB",
            message,
            0,
            17,
            51,
            3,
            0,
            0,
            r,
            r,
            0,
            3,
            0,
            g,
            g,
            0,
            2,
            0,
            b,
            b,
            0,
        )
        return message

    async def set_engine_light(self, red: int, green: int, blue: int):
        """Set vehicle light

        Args:
            red (float): Red
            green (float): Green
            blue (float): Blue
            pattern (float): Pattern type
        """
        r, g, b = red, green, blue

        r = 0 if (r < 0) else r
        r = 255 if (r > 255) else r
        g = 0 if (g < 0) else g
        g = 255 if (g > 255) else g
        b = 0 if (b < 0) else b
        b = 255 if (b > 255) else b

        command = self.__encodeEngineLightChange(red, green, blue)
        self.light = (red, green, blue)
        print(command)
        await self.car.send_command(command)
