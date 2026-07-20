import ctypes

from ..constants import MAX_NUM_TYRE_SETS
from ..header import PacketHeader


class TyreSetData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_actualTyreCompound", ctypes.c_uint8),
        ("m_visualTyreCompound", ctypes.c_uint8),
        ("m_wear", ctypes.c_uint8),
        ("m_available", ctypes.c_uint8),
        ("m_recommendedSession", ctypes.c_uint8),
        ("m_lifeSpan", ctypes.c_uint8),
        ("m_usableLife", ctypes.c_uint8),
        ("m_lapDeltaTime", ctypes.c_int16),
        ("m_fitted", ctypes.c_uint8),
    ]


class PacketTyreSetsData(ctypes.LittleEndianStructure):
    """231 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_carIdx", ctypes.c_uint8),
        ("m_tyreSetData", TyreSetData * MAX_NUM_TYRE_SETS),   # 13 dry + 7 wet
        ("m_fittedIdx", ctypes.c_uint8),
    ]
