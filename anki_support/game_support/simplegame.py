from ..anki_sdk import Car, Controller
from loguru import logger
import sys
import asyncio 


from .game import Game
from .player import Player


class SimpleGame:

    def __init__(self,car_list):
        self.players = []
        self.car_list = car_list

    def shutdown(self):
        for p in self.players:
            p.disconnect()

    async def play(self):
        logger.info("Play")
        self.condition = asyncio.Condition()
        async with self.condition:
            logger.info("mainloop")
            _ = asyncio.create_task(self.main_loop())
            logger.info("wait")
            await self.condition.wait()


    async def main_loop(self):
        logger.info("Finding gamepads")
        gamepad_list = Game.setup_gamepads()
        if len(gamepad_list) == 0:
            logger.error("No gamepads found")
            sys.exit(-2)

        logger.info(self.car_list)
        logger.info(gamepad_list)
        players = [
            Player(name=f"Player {i}", car=c, device=g)
            for i, (c, g) in enumerate(zip(self.car_list, gamepad_list))
        ]

        logger.info(players)

        for p in players:
            await p.connect()
            asyncio.ensure_future(p.handle_events())

        logger.info("PLAY...")
