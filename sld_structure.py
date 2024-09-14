from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import uint32, ByteStream, Array16, Bytes

from file_header import SLD_Header
from frame_header import Frame_Header
from layer_data import GraphicsHeader, CommandArray, DXT1_Block, DXT4_Block


class SLD(BaseStruct):
    @staticmethod
    def set_actual_content_length(_, instance: SLD):
        content_length = (getattr(instance, _.s_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)

    @staticmethod
    def find_block_count(_, instance: SLD):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        for item in command_array:
            draw_blocks_count = item.draw_blocks_count
            SLD.block_count += draw_blocks_count

    @staticmethod
    def set_layer_blocks_repeat(_, instance: SLD):
        Retriever.set_repeat(SLD.layer_blocks, instance, instance.block_count)

    @staticmethod
    def set_shadow_layer_blocks_repeat(_, instance: SLD):
        Retriever.set_repeat(SLD.shadow_layer_blocks, instance, instance.block_count)

    header: SLD_Header                = Retriever(SLD_Header,     default_factory=SLD_Header)
    frame_header: Frame_Header        = Retriever(Frame_Header,   default_factory=Frame_Header)

    content_length: int               = Retriever(uint32,         default=0, on_set=[set_actual_content_length])
    graphics_header: GraphicsHeader   = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[find_block_count])
    block_count: int = 0
    fake_value: int                   = Retriever(Bytes[0], on_set=[set_layer_blocks_repeat])
    layer_blocks: list[DXT1_Block]    = Retriever(DXT1_Block, default_factory=DXT1_Block)
    fake_value2: int                   = Retriever(Bytes[0], on_set=[set_shadow_layer_blocks_repeat])
    shadow_layer_blocks: list[DXT4_Block]    = Retriever(DXT4_Block, default_factory=DXT4_Block)
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