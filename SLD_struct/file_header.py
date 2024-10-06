from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint16, uint32, FixedLenStr


class SLD_Header(BaseStruct):
    file_descriptor: str    = Retriever(FixedLenStr[4], default="SLDX")
    version: int            = Retriever(uint16, default=4)
    num_frames: int         = Retriever(uint16, default=1)
    unknown1: int           = Retriever(uint16, default=0)
    unknown2: int           = Retriever(uint16, default=0)
    unknown3: int           = Retriever(uint32, default=255)
