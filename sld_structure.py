from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import uint32, ByteStream, Array16

from block_contruction import DXT1_Block, DXT4_Block
from file_header import SLD_Header
from frame_header import Frame_Header
from frames import Frame
from layer_data import GraphicsHeader, CommandArray


class SLD(BaseStruct):
    @staticmethod
    def set_frames_repeat(_: Retriever, instance: SLD):
        Retriever.set_repeat(SLD.frames, instance, instance.header.num_frames)


    header: SLD_Header                       = Retriever(SLD_Header,     default_factory=SLD_Header, on_read=[set_frames_repeat])
    frame_header: Frame_Header               = Retriever(Frame_Header,   default_factory=Frame_Header)
    frames: list[Frame] = Retriever(Frame, default_factory=Frame)

    #layers: LayerData           = Retriever(LayerData,      default=LayerData())

    @classmethod
    def get_version(
            cls,
            stream: ByteStream,
            struct_ver: Version = Version((0,)),
            parent: BaseStruct = None,
    ) -> Version:
        ver_str = str(stream.peek(6)[-2])
        return Version(tuple(map(int, ver_str.split("."))))