from .abstractevent import Event
import struct


class LocalizationTransition(Event):
    def build(self):
        pack_format = "<BBfBBHbBBBBB"

        (
            self.roadPieceId,  # uint8  2bytes
            self.preRoadPieceId,  # 3
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
        return f"[LT] PieceID={self.preRoadPieceId}>>{self.roadPieceId} Offset={self.offsetFromRoadCenter}mm L={self.leftWheelDist} R={self.rightWheelDist} followDrift={self.followDriftPixels}"

    def __repr__(self):
        return self.__str__()
