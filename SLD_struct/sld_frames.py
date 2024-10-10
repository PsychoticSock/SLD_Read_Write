from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import Bytes, void

from SLD_struct import sld_structure
from SLD_struct.sld_frame_header import Frame_Header
from SLD_struct.sld_layer_data import PlayerColourLayer, DamageLayer, ShadowLayer, \
    MainLayer, UnknownLayer


class SLD_Frame(BaseStruct):
    flags = -1
    @staticmethod
    def set_layer_repeats(_, instance: SLD_Frame):
        flags = sld_structure.lookup_layers(SLD_Frame.flags)
        if not flags['07 main']:
            Retriever.set_repeat(SLD_Frame.sld_main, instance, -1)
        if not flags['06 shadow']:
            Retriever.set_repeat(SLD_Frame.sld_shadow, instance, -1)
        if not flags['05 ???']:
            Retriever.set_repeat(SLD_Frame.sld_unused_outline, instance, -1)
        if not flags['04 damage']:
            Retriever.set_repeat(SLD_Frame.sld_damage, instance, -1)
        if not flags['03 player_colour']:
            Retriever.set_repeat(SLD_Frame.sld_player_colour, instance, -1)

    @staticmethod
    def set_flags(_, instance: SLD_Frame):
        SLD_Frame.flags = instance.sld_frame_header.frame_type

    # @ formatter: off
    sld_frame_header: Frame_Header          = Retriever(Frame_Header,           default_factory=Frame_Header,       on_read=[set_flags])
    sld_main: MainLayer                     = Retriever(MainLayer,              default_factory=MainLayer,          on_read = [set_layer_repeats])
    sld_shadow: ShadowLayer                 = Retriever(ShadowLayer,            default_factory=ShadowLayer)
    sld_unused_outline: UnknownLayer        = Retriever(UnknownLayer,           default_factory=UnknownLayer)
    sld_damage: DamageLayer                 = Retriever(DamageLayer,            default_factory=DamageLayer)
    sld_player_colour: PlayerColourLayer    = Retriever(PlayerColourLayer,      default_factory=PlayerColourLayer)
    # @formatter:on