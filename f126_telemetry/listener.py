import ctypes
import socket

from .constants import PacketID
from .header import PacketHeader
from .packets import PACKET_REGISTRY

HEADER_SIZE = ctypes.sizeof(PacketHeader)


class TelemetryListener:
    """Binds a UDP socket and dispatches parsed F1 26 telemetry packets to
    registered handlers.

    Usage:
        listener = TelemetryListener(port=20777)

        @listener.on(PacketID.CAR_TELEMETRY)
        def handle_telemetry(packet, addr):
            ...

        listener.run()
    """

    def __init__(self, host="", port=20777, buffer_size=2048):
        self.host = host
        self.port = port
        self.buffer_size = buffer_size
        self._handlers = {}
        self._raw_handlers = []
        self._sock = None

    def on(self, packet_id: PacketID):
        """Decorator: register fn(packet, addr) for a given PacketID."""

        def decorator(fn):
            self._handlers.setdefault(packet_id, []).append(fn)
            return fn

        return decorator

    def on_raw(self, fn):
        """Decorator: register fn(data: bytes, header: PacketHeader, addr) for every datagram."""

        self._raw_handlers.append(fn)
        return fn

    def _dispatch(self, data: bytes, addr):
        if len(data) < HEADER_SIZE:
            return

        header = PacketHeader.from_buffer_copy(data, 0)

        for fn in self._raw_handlers:
            fn(data, header, addr)

        try:
            packet_id = PacketID(header.m_packetId)
        except ValueError:
            return  # Unknown/future packet id - ignore for forward compatibility

        struct_cls = PACKET_REGISTRY.get(packet_id)
        if struct_cls is None or packet_id not in self._handlers:
            return

        if len(data) < ctypes.sizeof(struct_cls):
            return  # Packet smaller than expected for this struct/version - skip safely

        packet = struct_cls.from_buffer_copy(data, 0)

        for fn in self._handlers[packet_id]:
            fn(packet, addr)

    def run(self):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind((self.host, self.port))
        print(f"Listening for F1 26 telemetry on {self.host or '*'}:{self.port}")
        try:
            while True:
                data, addr = self._sock.recvfrom(self.buffer_size)
                self._dispatch(data, addr)
        except KeyboardInterrupt:
            pass
        finally:
            self.stop()

    def stop(self):
        if self._sock is not None:
            self._sock.close()
            self._sock = None
