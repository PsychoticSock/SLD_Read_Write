from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint8, uint16, uint32, Array16, Bytes, void

import frames
import sld_structure
from block_contruction import DXT1_Block, DXT4_Block
from frame_header import Frame_Header
from layer_data import GraphicsHeader, CommandArray, ShortGraphicsHeader, PlayerColourLayer, DamageLayer, ShadowLayer, \
    MainLayer, UnknownLayer


class Frame(BaseStruct):

    flags = -1

    @staticmethod
    def set_layer_repeats(_, instance: Frame):
        flags = sld_structure.lookup_layers(Frame.flags)
        if not flags['07 main']:
            #Retriever.set_repeat(Frame.main_content_length, instance, -1)
            Retriever.set_repeat(Frame.main, instance, -1)
        if not flags['06 shadow']:
            #Retriever.set_repeat(Frame.shadow_content_length, instance, -1)
            Retriever.set_repeat(Frame.shadow, instance, -1)
        if not flags['05 ???']:
            Retriever.set_repeat(Frame.unknown, instance, -1)
        if not flags['04 damage']:
            Retriever.set_repeat(Frame.damage, instance, -1)
        if not flags['03 player_colour']:
            Retriever.set_repeat(Frame.player_colour, instance, -1)

        #if layer NOT present: # fix this
        #    Retriever.set_repeat(Frame.layer, instance, -1)



    @staticmethod
    def set_flags(_, instance: Frame):
        #print(f"Layers present in file: {sld_structure.lookup_layers(instance.frame_header.frame_type)}")
        #print(instance.frame_header)
        Frame.flags = instance.frame_header.frame_type


    frame_header: Frame_Header               = Retriever(Frame_Header,   default_factory=Frame_Header, on_read=[set_flags])
    void: void = Retriever(Bytes[0], on_read = [set_layer_repeats])
    main: MainLayer = Retriever(MainLayer, default_factory=MainLayer)
    shadow: ShadowLayer = Retriever(ShadowLayer, default_factory=ShadowLayer)
    unknown: UnknownLayer = Retriever(UnknownLayer, default_factory=UnknownLayer)
    damage: DamageLayer = Retriever(DamageLayer, default_factory=DamageLayer)
    player_colour: PlayerColourLayer = Retriever(PlayerColourLayer, default_factory=PlayerColourLayer)