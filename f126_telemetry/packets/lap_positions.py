import ctypes

from ..constants import MAX_CARS, MAX_LAPS_IN_LAP_POSITIONS_HISTORY
from ..header import PacketHeader


class PacketLapPositionsData(ctypes.LittleEndianStructure):
    """1231 bytes. Details the positions of all drivers at the start of each lap."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numLaps", ctypes.c_uint8),
        ("m_lapStart", ctypes.c_uint8),   # index of the lap where the data starts, 0-indexed
        # [lap][vehicleIdx] -> position, 0 if no record
        ("m_positionForVehicleIdx", (ctypes.c_uint8 * MAX_CARS) * MAX_LAPS_IN_LAP_POSITIONS_HISTORY),
    ]
