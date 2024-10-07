from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import ByteStream, FixedLenStr, uint16, uint32, uint8

from SLD_struct.file_header import SLD_Header
from SLD_struct.frames import Frame

def lookup_layers(frame_type):
    frames = bin(frame_type)[2:].zfill(8)
    result = {}
    result['03 player_colour'] = int(frames[3])
    result['04 damage'] = int(frames[4])
    result['05 ???'] = int(frames[5])
    result['06 shadow'] = int(frames[6])
    result['07 main'] = int(frames[7])
    print("Layers present in file: ", list(reversed(sorted(result.keys()))))
    return result

class Frame(BaseStruct):
    flags = -1
    pass
    @staticmethod
    def set_layer_repeats(_, instance: Frame):
        flags = lookup_layers(Frame.flags)
        if not flags['07 main']:
            # Retriever.set_repeat(Frame.main_content_length, instance, -1)
            Retriever.set_repeat(Frame.main, instance, -1)
        if not flags['06 shadow']:
            # Retriever.set_repeat(Frame.shadow_content_length, instance, -1)
            Retriever.set_repeat(Frame.shadow, instance, -1)
        if not flags['05 outline ']:
            Retriever.set_repeat(Frame.outline, instance, -1)
        if not flags['04 compression']:
            Retriever.set_repeat(Frame.compression, instance, -1)
        if not flags['03 other_animation_shadows']:
            Retriever.set_repeat(Frame.player_colour, instance, -1)

    @staticmethod
    def set_flags(_, instance: Frame):
        Frame.flags = instance.frame_header.frame_type


    # frame_header: Frame_Header                    = Retriever(Frame_Header,               default_factory=Frame_Header,                   on_read=[set_flags])
    # void: void                                    = Retriever(Bytes[0],                                                                   on_read = [set_layer_repeats])
    # main: MainLayer                               = Retriever(MainLayer,                  default_factory=MainLayer)
    # shadow: ShadowLayer                           = Retriever(ShadowLayer,                default_factory=ShadowLayer)
    # outline: UnknownLayer                         = Retriever(UnknownLayer,               default_factory=UnknownLayer)
    # compression: DamageLayer                      = Retriever(DamageLayer,                default_factory=DamageLayer)
    # other_animation_shadows: PlayerColourLayer    = Retriever(PlayerColourLayer,          default_factory=PlayerColourLayer)

class SMX_Frame_Header(BaseStruct):
    # @formatter:off
    frame_type: int         = Retriever(uint8,      default=3, on_read=[])
    palette_number: int     = Retriever(uint8,      default=21)
    uncomp_size: int        = Retriever(uint32,     default=0)
    # @formatter:on

7 	If set to 1, the frame contains a main graphic layer
6 	If set to 1, the frame contains a shadow layer
5 	If set to 1, the frame contains an outline layer
4 	Determines the compression algorithm for the main graphic layer. 0 = 4plus1; 1 = 8to5 (see the Compression Algorithms section)
3 	If set to 1, other animations' shadows will be cast over the animation.
0-2 	Unused

class SMX_Header(BaseStruct):
    # @formatter:off
    file_descriptor: str    = Retriever(FixedLenStr[4], default="SMPX")
    version: int            = Retriever(uint16, default=2)
    num_frames: int         = Retriever(uint16, default=1)
    file_size_comp: int     = Retriever(uint32, default=0)
    file_size_uncomp: int   = Retriever(uint32, default=0)
    comment: int            = Retriever(FixedLenStr[16])
    # @formatter:on

class SMX(BaseStruct):
    @staticmethod
    def set_frames_repeat(_: Retriever, instance: SMX):
        Retriever.set_repeat(SMX.frames, instance, instance.header.num_frames)
        print(f"Frames: {instance.header.num_frames}")

    header: SMX_Header                       = Retriever(SMX_Header,     default_factory=SMX_Header, on_read=[set_frames_repeat])
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