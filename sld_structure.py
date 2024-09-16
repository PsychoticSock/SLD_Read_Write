from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import uint32, ByteStream, Array16

from block_contruction import DXT1_Block, DXT4_Block
from file_header import SLD_Header
from frame_header import Frame_Header
from layer_data import GraphicsHeader, CommandArray


class SLD(BaseStruct):
    @staticmethod
    def set_actual_content_length(_, instance: SLD):
        content_length = (getattr(instance, _.s_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)

    @staticmethod
    def set_layer_blocks_repeat(_, instance: SLD):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count

        Retriever.set_repeat(SLD.layer_blocks, instance, count)

    @staticmethod
    def shadow_set_layer_blocks_repeat(_, instance: SLD):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count

        Retriever.set_repeat(SLD.shadow_layer_blocks, instance, count)

    header: SLD_Header                       = Retriever(SLD_Header,     default_factory=SLD_Header)
    frame_header: Frame_Header               = Retriever(Frame_Header,   default_factory=Frame_Header)

    content_length: int                      = Retriever(uint32,         default=0, on_set=[set_actual_content_length])
    graphics_header: GraphicsHeader          = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    command_array: list[CommandArray]        = Retriever(Array16[CommandArray], on_set=[set_layer_blocks_repeat])
    layer_blocks: list[DXT1_Block]           = Retriever(DXT1_Block, default_factory=DXT1_Block)
    shadow_content_length: int = Retriever(uint32, default=0, on_set=[set_actual_content_length])
    shadow_graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    shadow_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[shadow_set_layer_blocks_repeat])
    shadow_layer_blocks: list[DXT4_Block] = Retriever(DXT4_Block, default_factory=DXT4_Block)
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