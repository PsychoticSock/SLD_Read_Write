from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16


class Frame_Header(BaseStruct):
    canvas_width: int          = Retriever(uint16, default=200)
    canvas_height: int         = Retriever(uint16, default=200)
    canvas_hotspot_x: int      = Retriever(uint16, default=100)
    canvas_hotspot_y: int      = Retriever(uint16, default=100)
    frame_type: int            = Retriever(uint8, default=0)        # This is a bitfield:
    unknown5: int              = Retriever(uint8, default=1)
    frame_index: int           = Retriever(uint16, default=5)
