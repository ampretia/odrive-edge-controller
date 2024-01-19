from loguru import logger
import sys
from ..anki_sdk import Car


class CarScanner:
    # private _callback: Function
    # private _locations: LocalizationPositionUpdate[]
    # private _pieces: IPiece[]
    # private _round: number
    # private _scanning: boolean
    # private _vehicle: IVehicle

    def __init__(self):
        pass

    async def scan(self) -> list[Car]:
        logger.info("Looking for cars....")
        car_list = await Car.scanner()
        if len(car_list) == 0:
            logger.error("No cars found..")
            sys.exit(-1)

        return car_list
    
