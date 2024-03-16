import time as t
from typing import Self
import struct
import bleak
from loguru import logger
from .controller import Controller
from .car_interface import ICar
from typing import List

from .exceptions import NotConnected
from .protocol import Protocol
from .events import (
    LocalizationTransition,
    LocalizationPosition,
    Event,
    IObserver,
    OffTrack,
    BatteryResponse,
    VersionResponse,
)


class Car(IObserver, ICar):
    # Args:
    #    car_address (str): vehicle MAC-address
    #    cat_name (str): name
    def __init__(self, car_address: str, car_name: str, debug: bool = False):
        self.address: str = car_address
        self.name = car_name

        self.client: bleak.BleakClient = bleak.BleakClient(self.address)

        # connection status
        self.connected: bool = False

        self.ble_notify_started: bool = False

        # tmp var
        self.debug = debug
        self.before = ""
        self.start_ping_time = None

    def get_name(self) -> str:
        return self.name

    def get_address(self)-> str:
        return self.address

    # Get object as string
    def __str__(self):
        return f"Anki Overdrive car {self.name} | {self.address}"

    def __repr__(self) -> str:
        return self.__str__()

    # Send BLE command to car
    async def send_command(self, command: bytes):
        """Send BLE command to car

        Args:
            command (bytes): Command that should get send.
        """
        if self.connected:
            command = struct.pack("B", len(command)) + command
            await self.client.write_gatt_char(Protocol.UUID.WRITE_UUID, command)
        else:
            raise NotConnected("Not connected to vehicle")

    async def get_controller(self):
        await self.connect()
        ctrl = Controller(self)

        return ctrl

    async def connect(self):
        if not self.connected:
            await self.client.connect()
            self.connected: bool = True
            await self.send_command(b"\x90\x01\x01")

        if not self.ble_notify_started:
            logger.info("Starting BLE event notifications")
            await self.client.start_notify(Protocol.UUID.READ_UUID, self._ble_notify)
            self.ble_notify_started = True

        return self.name

    async def ping(self):
        """Get the ping to vehicle

        Returns:
            ping (int): Ping in ms.
        """
        command = struct.pack("<BBB", Protocol.CommandList.PING_REQUEST, 0x01, 0x01)
        await self.send_command(command)
        self.ping_time: int = t.time_ns()
        # self.wait_ping: bool = True
        # while self.wait_ping:
        #     t.sleep(0)
        # return self.start_ping_time

    async def version(self):
        command = struct.pack("<BBB", Protocol.CommandList.VERSION_REQUEST, 0x01, 0x01)
        await self.send_command(command)

    async def battery(self):
        command = struct.pack("<BBB", Protocol.CommandList.BATTERY_REQUEST, 0x01, 0x01)
        await self.send_command(command)

    # disconnect and slow down the car
    async def disconnect(self, stop_car: bool = True):
        try:
            if self.client.is_connected:
                if stop_car:
                    command = struct.pack(
                        "<BHHB", Protocol.CommandList.SET_SPEED, 0, 1000, 0x01
                    )
                    await self.send_command(command)

                t.sleep(0.5)
                await self.send_command(
                    struct.pack("<BB", Protocol.CommandList.DISCONNECT, 0x01)
                )
                self.connected = False
                
                await self.client.disconnect()
                self.ble_notify_started = False
                return True
        except KeyboardInterrupt:
            return False

    def build_message(self, data):
        evt = None

        match data[1]:
            case 0x29:
                evt = LocalizationTransition(
                    data[0], data[1], data[2:], self.name
                ).build()
            case 0x27:
                evt = LocalizationPosition(
                    data[0], data[1], data[2:], self.name
                ).build()
            case 0x2B:
                evt = OffTrack().build()
            case Protocol.CommandList.PING_RESPONSE:
                self.ping_time = t.time_ns() - self.ping_time
                logger.info(
                    "Ping time {}  response {}", self.ping_time, self._log(data)
                )
            case Protocol.CommandList.VERSION_RESPONSE:
                evt = VersionResponse(data[0], data[1], data[2:], self.name).build()
                logger.info(evt)

            case Protocol.CommandList.BATTERY_RESPONSE:
                evt = BatteryResponse(data[0], data[1], data[2:], self.name).build()
                logger.info(evt)
            case _:
                evt = Event(data[0], data[1], data[2:], self.name).build()
                logger.info(evt)

        return evt

    # Start to receive notify
    async def start_notify(self, observer):
        self._attach(observer)

    #
    async def stop_notify(self, observer):
        self._detach(observer)

    def _log(self, data) -> str:
        text = "["
        for v in list(data):
            text += f"{v:02X} "

        text = text.strip()
        text += "]"
        return text

    # BLE callback
    async def _ble_notify(self, sender, data: bytearray):
        logger.debug(f"BLE - {sender} {self._log(data)}")
        if data == self.before:
            return

        self.before = data

        msg = self.build_message(data)
        if msg:
            await self._notify(msg)

    def _get_car_name(advertised):
        data_table: list = advertised.manufacturer_data[61374]
        value = bytearray(data_table)
        car_name = Car._decodeCarname(value)
        return car_name

    def _decodeCarname(manufacturerData):
        carId = manufacturerData[1]
        carnames = {
            0: "x52",
            8: "Groundshock",
            9: "Skull",
            10: "Thermo",
            11: "Nuke",
            12: "Guardian",
            14: "Bigbang",
            15: "Free Wheel",
            16: "x52",
            17: "x52 Ice",
            18: "MXT",
            19: "Ice Charger",
        }

        if carId in carnames:
            return carnames[carId]
        else:
            return "Unknown"

    async def update(self, event) -> None:
        logger.info(f"{event}")

    @staticmethod
    async def scanner(active: bool = True) -> List[Self]:
        device_list = await bleak.BleakScanner.discover(return_adv=True)
        result: list = []
        if len(device_list) == 0:
            return list

        for n, data in device_list.items():
            address = n
            (device, advertised) = data

            if device.name is not None:
                if "Drive" in device.name:
                    if active:
                        if "P" not in device.name:
                            c = Car(address, Car._get_car_name(advertised))
                            result.append(c)
                    else:
                        c = Car(address, Car._get_car_name(advertised))
                        result.append(c)

        return result

    _observers: List[IObserver] = []

    def _attach(self, observer: IObserver) -> None:
        self._observers.append(observer)

    def _detach(self, observer: IObserver) -> None:
        self._observers.remove(observer)

    async def _notify(self, event) -> None:
        for observer in self._observers:
            await observer.update(event)
