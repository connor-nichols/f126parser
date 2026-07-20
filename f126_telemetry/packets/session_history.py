import ctypes

from ..constants import MAX_LAPS_IN_HISTORY, MAX_TYRE_STINTS
from ..header import PacketHeader


class LapHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_lapTimeInMS", ctypes.c_uint32),
        ("m_sector1TimeMSPart", ctypes.c_uint16),
        ("m_sector1TimeMinutesPart", ctypes.c_uint8),
        ("m_sector2TimeMSPart", ctypes.c_uint16),
        ("m_sector2TimeMinutesPart", ctypes.c_uint8),
        ("m_sector3TimeMSPart", ctypes.c_uint16),
        ("m_sector3TimeMinutesPart", ctypes.c_uint8),
        ("m_lapValidBitFlags", ctypes.c_uint8),   # 0x01 lap, 0x02 s1, 0x04 s2, 0x08 s3
    ]


class TyreStintHistoryData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_endLap", ctypes.c_uint8),             # 255 if current tyre
        ("m_tyreActualCompound", ctypes.c_uint8),
        ("m_tyreVisualCompound", ctypes.c_uint8),
    ]


class PacketSessionHistoryData(ctypes.LittleEndianStructure):
    """1460 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carIdx", ctypes.c_uint8),
        ("m_numLaps", ctypes.c_uint8),                    # includes current partial lap
        ("m_numTyreStints", ctypes.c_uint8),
        ("m_bestLapTimeLapNum", ctypes.c_uint8),
        ("m_bestSector1LapNum", ctypes.c_uint8),
        ("m_bestSector2LapNum", ctypes.c_uint8),
        ("m_bestSector3LapNum", ctypes.c_uint8),
        ("m_lapHistoryData", LapHistoryData * MAX_LAPS_IN_HISTORY),
        ("m_tyreStintsHistoryData", TyreStintHistoryData * MAX_TYRE_STINTS),
    ]
