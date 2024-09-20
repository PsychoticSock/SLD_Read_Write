from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, FixedLenStr, Bytes, Array16

from block_contruction import DXT4_Block, DXT1_Block


class CommandArray(BaseStruct):
    skipped_blocks_count: int = Retriever(uint8)
    draw_blocks_count: int = Retriever(uint8)



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

class ShortGraphicsHeader(BaseStruct):
    @staticmethod
    def no_flag_allowed(retriever: Retriever, instance: 'SLD'):
        if getattr(instance, retriever.s_name) & 1:
            raise ValueError('Not supported yet!')

    Flag1: int = Retriever(uint8, default=0)
    Unknown: int = Retriever(uint8, default=0)

class MainLayer(BaseStruct):
    @staticmethod
    def set_padded_content_length(_, instance: MainLayer):
        content_length = (getattr(instance, _.p_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        print(f"{_.p_name} actual_length {actual_length}, content_length {content_length}, Difference:", actual_length-content_length)
        Retriever.set_repeat(MainLayer.null_bytes, instance, (actual_length-content_length))

    @staticmethod
    def set_layer_blocks_repeat(_, instance: MainLayer):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count

        Retriever.set_repeat(MainLayer.layer_blocks, instance, count)

    main_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[set_layer_blocks_repeat])
    layer_blocks: list[DXT1_Block] = Retriever(DXT1_Block, default_factory=DXT1_Block)
    null_bytes: bytes = Retriever(Bytes[1], repeat=-1, default=b"\x00")

class ShadowLayer(BaseStruct):
    @staticmethod
    def set_shadow_padded_content_length(_, instance: ShadowLayer):
        content_length = (getattr(instance, _.p_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        print(f"{_.p_name} actual_length {actual_length}, content_length {content_length}, Difference:", actual_length-content_length)
        if actual_length-content_length > 0:
            Retriever.set_repeat(ShadowLayer.null_bytes, instance, (actual_length-content_length))

    @staticmethod
    def shadow_set_layer_blocks_repeat(_, instance: ShadowLayer):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count
        Retriever.set_repeat(ShadowLayer.shadow_layer_blocks, instance, count)
        print(ShadowLayer.shadow_layer_blocks)

    shadow_content_length: int = Retriever(uint32, default=0, on_set=[set_shadow_padded_content_length])
    shadow_graphics_header: GraphicsHeader = Retriever(GraphicsHeader, default_factory=GraphicsHeader)
    shadow_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[shadow_set_layer_blocks_repeat])
    shadow_layer_blocks: list[DXT4_Block] = Retriever(DXT4_Block, default_factory=DXT4_Block)
    null_bytes: bytes = Retriever(Bytes[1], repeat=-1, default=b"\x00")

class UnknownLayer(BaseStruct):
    @staticmethod
    def set_unknown_content_length(_, instance: UnknownLayer()):
        content_length = (getattr(instance, _.p_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        print(f"{_.p_name} actual_length {actual_length}, content_length {content_length}, Difference:", actual_length-content_length)
        if actual_length-content_length > 0:
            Retriever.set_repeat(UnknownLayer.unknown_graphics_data, instance, actual_length - 4)

    unknown_content_length: int = Retriever(uint32, default=0, on_set=[set_unknown_content_length])
    unknown_graphics_data: bytes = Retriever(Bytes[1], repeat=-1,                         default=b"\x00")


class DamageLayer(BaseStruct):
    @staticmethod
    def set_padded_content_length(_, instance: DamageLayer):
        content_length = (getattr(instance, _.p_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        print(f"{_.p_name} actual_length {actual_length}, content_length {content_length}, Difference:", actual_length-content_length)
        Retriever.set_repeat(DamageLayer.null_bytes, instance, (actual_length-content_length))

    @staticmethod
    def set_damage_layer_blocks_repeat(_, instance: DamageLayer):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count
        Retriever.set_repeat(DamageLayer.damage_layer_blocks, instance, count)

    damage_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    damage_graphics_header: ShortGraphicsHeader = Retriever(ShortGraphicsHeader, default_factory=ShortGraphicsHeader)
    damage_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[set_damage_layer_blocks_repeat])
    damage_layer_blocks: list[DXT1_Block] = Retriever(DXT1_Block, default_factory=DXT1_Block)
    null_bytes: bytes = Retriever(Bytes[1], repeat=-1, default=b"\x00")

class PlayerColourLayer(BaseStruct):
    @staticmethod
    def set_padded_content_length(_, instance: PlayerColourLayer):
        content_length = (getattr(instance, _.s_name))
        actual_length = content_length + ((4 - content_length) % 4)
        setattr(instance, _.s_name, actual_length)
        print(f"{_.p_name} actual_length {actual_length}, content_length {content_length}, Difference:", actual_length-content_length)
        Retriever.set_repeat(PlayerColourLayer.null_bytes, instance, (actual_length-content_length))

    @staticmethod
    def player_colour_set_layer_blocks_repeat(_, instance: PlayerColourLayer):
        command_array: list[CommandArray] = getattr(instance, _.s_name)
        count = 0
        for item in command_array:
            count += item.draw_blocks_count
        Retriever.set_repeat(PlayerColourLayer.player_colour_layer_blocks, instance, count)

    player_colour_content_length: int = Retriever(uint32, default=0, on_set=[set_padded_content_length])
    player_colour_graphics_header: ShortGraphicsHeader = Retriever(ShortGraphicsHeader, default_factory=ShortGraphicsHeader)
    player_colour_command_array: list[CommandArray] = Retriever(Array16[CommandArray], on_set=[player_colour_set_layer_blocks_repeat])
    player_colour_layer_blocks: list[DXT4_Block] = Retriever(DXT4_Block, default_factory=DXT4_Block)
    null_bytes: bytes = Retriever(Bytes[1], repeat=-1, default=b"\x00")

class LayerData(BaseStruct):
    pass