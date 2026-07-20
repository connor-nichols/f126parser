import ctypes

from ..constants import MAX_CARS, MAX_PARTICIPANT_NAME_LEN
from ..header import PacketHeader


class LobbyInfoData(ctypes.LittleEndianStructure):
    _pack_ = 1
    _fields_ = [
        ("m_aiControlled", ctypes.c_uint8),
        ("m_teamId", ctypes.c_uint16),                       # 65535 if no team currently selected
        ("m_nationality", ctypes.c_uint8),
        ("m_platform", ctypes.c_uint8),
        ("m_name", ctypes.c_char * MAX_PARTICIPANT_NAME_LEN),
        ("m_carNumber", ctypes.c_uint8),
        ("m_yourTelemetry", ctypes.c_uint8),
        ("m_showOnlineNames", ctypes.c_uint8),
        ("m_techLevel", ctypes.c_uint16),
        ("m_readyStatus", ctypes.c_uint8),                   # 0 = not ready, 1 = ready, 2 = spectating
    ]


class PacketLobbyInfoData(ctypes.LittleEndianStructure):
    """1062 bytes."""

    _pack_ = 1
    _fields_ = [
        ("m_header", PacketHeader),
        ("m_numPlayers", ctypes.c_uint8),
        ("m_lobbyPlayers", LobbyInfoData * MAX_CARS),
    ]
