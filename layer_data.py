from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, FixedLenStr, Bytes


class CommandArray(BaseStruct):
    skipped_blocks_count: int = Retriever(uint8)
    draw_blocks_count: int = Retriever(uint8)


class GraphicsHeader(BaseStruct):
    offset_x1: int = Retriever(uint16, default=0)
    offset_y1: int = Retriever(uint16, default=0)
    offset_x2: int = Retriever(uint16, default=0)
    offset_y2: int = Retriever(uint16, default=0)
    flag1: int = Retriever(uint8, default=0)
    unknown1: int = Retriever(uint8, default=0)

class GraphicsHeader(BaseStruct):
    @staticmethod
    def no_flag_allowed(retriever: Retriever, instance: 'SLD'):
        if getattr(instance, retriever.s_name) & 1:
            raise ValueError('Not supported yet!')

    offset_x1: int = Retriever(uint16, default=0)
    offset_y1: int = Retriever(uint16, default=0)
    offset_x2: int = Retriever(uint16, default=0)
    offset_y2: int = Retriever(uint16, default=0)
    flag1: int = Retriever(uint8, default=0) #0, on_read=[no_flag_allowed])
    unknown1: int = Retriever(uint8, default=0)

class LayerData(BaseStruct):
    pass