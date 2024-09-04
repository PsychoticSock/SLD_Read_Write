from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32


class DXT1_Block(BaseStruct):
    color0: int  = Retriever(uint16)
    color1: int = Retriever(uint16)
    pixel_indices: int = Retriever(uint32)

class CommandArray(BaseStruct):
    skipped_blocks_count: int   = Retriever(uint8)
    draw_blocks_count: int      = Retriever(uint8)


class GraphicsHeader(BaseStruct):
    offset_x1: int      = Retriever(uint16, default=0)
    offset_y1: int      = Retriever(uint16, default=0)
    offset_x2: int      = Retriever(uint16, default=0)
    offset_y2: int      = Retriever(uint16, default=0)
    flag1: int          = Retriever(uint8, default=0)
    unknown1: int       = Retriever(uint8, default=0)


class LayerData(BaseStruct):
    pass
