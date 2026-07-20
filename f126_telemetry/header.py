import ctypes


class PacketHeader(ctypes.LittleEndianStructure):
    """29 bytes. Present at the start of every packet type."""

    _pack_ = 1
    _fields_ = [
        ("m_packetFormat", ctypes.c_uint16),            # 2026
        ("m_gameYear", ctypes.c_uint8),                  # Game year - last two digits e.g. 26
        ("m_gameMajorVersion", ctypes.c_uint8),          # Game major version - "X.00"
        ("m_gameMinorVersion", ctypes.c_uint8),          # Game minor version - "1.XX"
        ("m_packetVersion", ctypes.c_uint8),             # Version of this packet type
        ("m_packetId", ctypes.c_uint8),                  # Identifier for the packet type
        ("m_sessionUID", ctypes.c_uint64),               # Unique identifier for the session
        ("m_sessionTime", ctypes.c_float),               # Session timestamp
        ("m_frameIdentifier", ctypes.c_uint32),          # Identifier for the frame the data was retrieved on
        ("m_overallFrameIdentifier", ctypes.c_uint32),   # Doesn't go back after flashbacks
        ("m_playerCarIndex", ctypes.c_uint8),            # Index of player's car in the array
        ("m_secondaryPlayerCarIndex", ctypes.c_uint8),   # Splitscreen secondary player, 255 if none
    ]
