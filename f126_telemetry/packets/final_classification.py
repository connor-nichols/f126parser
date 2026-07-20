import ctypes

from ..constants import MAX_CARS, MAX_TYRE_STINTS
from ..header import PacketHeader


class FinalClassificationData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_position", ctypes.c_uint8),
        ("m_numLaps", ctypes.c_uint8),
        ("m_gridPosition", ctypes.c_uint8),
        ("m_points", ctypes.c_uint8),
        ("m_numPitStops", ctypes.c_uint8),
        ("m_resultStatus", ctypes.c_uint8),
        ("m_resultReason", ctypes.c_uint8),
        ("m_bestLapTimeInMS", ctypes.c_uint32),
        ("m_totalRaceTime", ctypes.c_double),
        ("m_penaltiesTime", ctypes.c_uint8),
        ("m_numPenalties", ctypes.c_uint8),
        ("m_numTyreStints", ctypes.c_uint8),
        ("m_tyreStintsActual", ctypes.c_uint8 * MAX_TYRE_STINTS),
        ("m_tyreStintsVisual", ctypes.c_uint8 * MAX_TYRE_STINTS),
        ("m_tyreStintsEndLaps", ctypes.c_uint8 * MAX_TYRE_STINTS),
    ]


class PacketFinalClassificationData(ctypes.LittleEndianStructure):
    """1134 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numCars", ctypes.c_uint8),
        ("m_classificationData", FinalClassificationData * MAX_CARS),
    ]
