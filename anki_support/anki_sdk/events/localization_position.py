from .abstractevent import Event
import struct


class LocalalizationPosition(Event):
    def build(self):
        pack_format = "<BBfHBBBHH"

        #[11 29 00 00 A4 70 6B C2 00 81 46 00 F9 00 49 00 1E 25 ]
        # 2 2 4 2 2 4 2 2 2 2 2 2 

        (
            self.locationId,           # uint8  2bytes
            self.roadPieceId,         # 3
            self.offsetFromRoadCenter,
            self.speed,
            self.parsingFlags,
            self.lastRecvLaneChangeCmdId,
            self.lastExecLaneChangeCmdId,
            self.lastDesiredLaneChangeSpeedMmPerSec,
            self.lastDesiredSpeedMmPerSec,
        ) = struct.unpack(pack_format, self.payload)

        return self

    def get_road_piece_id(self):
        return self.roadPieceId

    def get_location_id(self):
        return self.locationId

    def __str__(self):
        return f"Position {self.roadPieceId}::{self.locationId} Offset={self.offsetFromRoadCenter}mm  Speed={self.speed}mm/s {self.log()}"

    def __repr__(self):
        return self.__str__()