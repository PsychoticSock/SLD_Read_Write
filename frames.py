from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, Array16, Bytes

import frames
from block_contruction import DXT1_Block, DXT4_Block
from layer_data import GraphicsHeader, CommandArray, ShortGraphicsHeader

class Frame(BaseStruct):
    @staticmethod
    def set_padded_content_length(_, instance: Frame):
        content_length = (getattr(instance, _.s_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)

    @staticmethod
    def set_unknown_content_length(_, instance: Frame):
        content_length = (getattr(instance, _.s_name))
        frames.unknown_content_initial_length = content_length
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        Retriever.set_repeat(Frame.unknown_graphics_data, instance, actual_length -4)

    @staticmethod
    def set_layer_blocks_repeat(_, instance: Frame):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count

        Retriever.set_repeat(Frame.layer_blocks, instance, count)

    @staticmethod
    def set_damage_layer_blocks_repeat(_, instance: Frame):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count

        Retriever.set_repeat(Frame.damage_layer_blocks, instance, count)

    @staticmethod
    def shadow_set_layer_blocks_repeat(_, instance: Frame):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count
        Retriever.set_repeat(Frame.shadow_layer_blocks, instance, count)

    @staticmethod
    def player_colour_set_layer_blocks_repeat(_, instance: Frame):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count
        Retriever.set_repeat(Frame.player_colour_layer_blocks, instance, count)

    content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[set_layer_blocks_repeat])
    layer_blocks: list[DXT1_Block] = Retriever(DXT1_Block, default_factory=DXT1_Block)
    shadow_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    shadow_graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    shadow_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[shadow_set_layer_blocks_repeat])
    shadow_layer_blocks: list[DXT4_Block] = Retriever(DXT4_Block, default_factory=DXT4_Block)

    unknown_content_length: int = Retriever(uint32, default=0, on_set=[set_unknown_content_length])
    #unknown_graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    unknown_graphics_data: bytes = Retriever(Bytes[1], repeat=0,                          default=b"\x00")
    damage_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    damage_graphics_header: ShortGraphicsHeader = Retriever(ShortGraphicsHeader, default_factory=ShortGraphicsHeader)
    damage_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[set_damage_layer_blocks_repeat])
    damage_layer_blocks: list[DXT1_Block] = Retriever(DXT1_Block, default_factory=DXT1_Block)
    player_colour_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    player_colour_graphics_header: ShortGraphicsHeader = Retriever(ShortGraphicsHeader, default_factory=ShortGraphicsHeader)
    player_colour_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[player_colour_set_layer_blocks_repeat])
    player_colour_layer_blocks: list[DXT4_Block] = Retriever(DXT4_Block, default_factory=DXT4_Block)