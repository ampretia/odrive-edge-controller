from .abstractevent import Event
import struct


class LocalalizationTransition(Event):
    def build(self):
        pack_format = "<BBfBBHBBBBBB"

        #[11 29 00 00 A4 70 6B C2 00 81 46 00 F9 00 49 00 1E 25 ]
        # 2 2 4 2 2 4 2 2 2 2 2 2 

        (
            self.roadPieceId,           # uint8  2bytes
            self.preRoadPieceId,         # 3
            self.offsetFromRoadCenter,
            self.lastRecvLaneChangeCmdId,
            self.lastrExecLaneChangeCmdId,
            self.lastLaneChangeSpeed,
            self.followDriftPixels,
            self.hadLaneChange,
            self.uphill,
            self.downhilll,
            self.leftWheelDist,
            self.rightWheelDist,
        ) = struct.unpack(pack_format, self.payload)

        return self

    def get_left_wheel_dist(self):
        return self.leftWheelDist

    def get_right_wheel_dist(self):
        return self.rightWheelDist

    def __str__(self):
        return f"Transition {self.roadPieceId}/{self.preRoadPieceId} Offset={self.offsetFromRoadCenter}mm L={self.leftWheelDist} R={self.rightWheelDist} {self.log()}"

    def __repr__(self):
        return self.__str__()