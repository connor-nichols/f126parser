# f126_telemetry

A small, dependency-free Python receiver for F1 25's 2026 Season Pack UDP telemetry
(packet format `2026`). Every packet type in the spec is parsed via `ctypes` structs
that mirror the official C++ layout field-for-field, so there's no manual byte
offset math anywhere.

## Setup

No dependencies — just Python 3.

In-game: **Settings > Telemetry Settings**
- UDP Telemetry: On
- UDP IP Address: the IP of the machine running this script (`127.0.0.1` if it's the same machine)
- UDP Port: `20777`
- UDP Format: `2026`
- UDP Send Rate: whatever you want (up to 60 Hz)

Then run:

```bash
python3 main.py
```

## How it's organized

- `f126_telemetry/header.py` — `PacketHeader`, present at the start of every packet.
- `f126_telemetry/constants.py` — `PacketID` enum and the array-size constants from the spec.
- `f126_telemetry/packets/` — one module per packet family (motion, session, lap data,
  event, participants, car setups, car telemetry, car status, final classification,
  lobby info, car damage, session history, tyre sets, motion ex, time trial, lap
  positions, car telemetry 2). Each defines the `ctypes.Structure`(s) for that packet.
  `packets/__init__.py` holds `PACKET_REGISTRY`, the single dict mapping `PacketID` to
  its top-level struct class.
- `f126_telemetry/listener.py` — `TelemetryListener`: binds the UDP socket, peeks the
  header of every datagram to find its `PacketID`, looks up the matching struct in
  `PACKET_REGISTRY`, parses it with `from_buffer_copy`, and dispatches it to whatever
  handlers you've registered.
- `f126_telemetry/utils.py` — `struct_to_dict()`, recursively turns any parsed packet
  into plain dicts/lists (handy for `json.dumps`, logging, etc.).
- `main.py` — example usage.

## Adding a handler for a packet type

```python
from f126_telemetry import PacketID, TelemetryListener

listener = TelemetryListener(port=20777)

@listener.on(PacketID.CAR_STATUS)
def on_car_status(packet, addr):
    car = packet.m_carStatusData[packet.m_header.m_playerCarIndex]
    print(car.m_fuelInTank, car.m_actualTyreCompound)

listener.run()
```

You can register multiple handlers for the same `PacketID`, and mix in
`@listener.on_raw` if you want to see every datagram's raw bytes regardless of type
(e.g. to log/replay a session).

## Adding support for a new packet type

If EA adds a new packet type in a future patch:

1. Add a module under `f126_telemetry/packets/` with a `ctypes.LittleEndianStructure`
   (`_pack_ = 1`) that mirrors the new C++ struct field-for-field — copy the pattern
   from an existing module like `car_status.py`.
2. Register it in `f126_telemetry/packets/__init__.py`'s `PACKET_REGISTRY`.

That's it — `listener.py` and everything else works unchanged.

## Notes

- All structs are packed, little-endian, matching how the game sends them.
- The listener checks each datagram's length against the expected struct size before
  parsing, so a version/size mismatch (e.g. a future patch changing a packet) is
  skipped rather than crashing.
- `f126_telemetry/packets/event.py` also has `describe_event(packet)`, which reads
  `m_eventStringCode` and picks the right member out of the `EventDataDetails` union
  for you (e.g. `{"code": "SPTP", "label": "Speed Trap", "details": {...}}`).
