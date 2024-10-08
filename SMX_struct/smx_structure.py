from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import ByteStream, FixedLenStr, uint16, uint32, uint8

from SLD_struct.file_header import SLD_Header
from SLD_struct.frames import Frame

def lookup_layers(frame_type):
    print("lookup_layers frame type:", frame_type)

class SMX_Layer_Header(BaseStruct):
    width: int                  = Retriever(uint16,     default=0)
    height: int                 = Retriever(uint16,     default=0)
    hotspot_x: int              = Retriever(uint16,     default=0)
    hotspot_y: int              = Retriever(uint16,     default=0)
    layer_len: int              = Retriever(uint32,     default=0)
    Unknown: int                = Retriever(uint32,     default=0)

class SMXOutlineLayer(BaseStruct):
    @staticmethod
    def set_combined_array_repeat(_, instance: SLXMainLayer):
        #print("instance.layer_header.height", instance.layer_header.layer_len)
        Retriever.set_repeat(SLXMainLayer.command_array, instance, instance.layer_header.layer_len)

    # @formatter:off
    layer_header: SMX_Layer_Header  = Retriever(SMX_Layer_Header, default_factory=SMX_Layer_Header, on_read=[set_combined_array_repeat])
    command_array: list[int]                = Retriever(uint8, repeat=-1, default=0)

class SMXShadowLayer(BaseStruct):
    @staticmethod
    def set_combined_array_repeat(_, instance: SLXMainLayer):
        #print("instance.layer_header.height", instance.layer_header.layer_len)
        Retriever.set_repeat(SLXMainLayer.command_array, instance, instance.layer_header.layer_len)

    # @formatter:off
    layer_header: SMX_Layer_Header  = Retriever(SMX_Layer_Header, default_factory=SMX_Layer_Header, on_read=[set_combined_array_repeat])
    command_array: list[int]                = Retriever(uint8, repeat=-1, default=0)

class SMP_Layer_Row_Edge(BaseStruct):
    left_space: int             = Retriever(uint16, default=0)
    right_space: int            = Retriever(uint16, default=0)

class SLXMainLayer(BaseStruct):
    @staticmethod
    def set_row_edge_repeat(_, instance: SLXMainLayer):
        #print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SLXMainLayer.smp_layer_row_edge, instance, instance.layer_header.height)
    @staticmethod
    def set_command_array_repeat(_, instance: SLXMainLayer):
        #print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SLXMainLayer.command_array, instance, instance.command_array_length)
    @staticmethod
    def set_pixel_array_repeat(_, instance: SLXMainLayer):
        #print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SLXMainLayer.pixel_data_array, instance, instance.pixel_data_array_length)

    # @formatter:off
    layer_header: SMX_Layer_Header          = Retriever(SMX_Layer_Header, default_factory=SMX_Layer_Header, on_read=[set_row_edge_repeat])
    smp_layer_row_edge: SMP_Layer_Row_Edge  = Retriever(SMP_Layer_Row_Edge, repeat=-1)
    command_array_length: int               = Retriever(uint32, default=0, on_read=[set_command_array_repeat])
    pixel_data_array_length: int                = Retriever(uint32, default=0, on_read=[set_pixel_array_repeat])
    command_array: list[int]                = Retriever(uint8, repeat=-1, default=0)
    pixel_data_array: list[int]             = Retriever(uint8, repeat=-1, default=0)
    # @formatter:on

class SMX_Frame_Header(BaseStruct):
    # @formatter:off
    frame_type: int         = Retriever(uint8,      default=3)  #, on_read=[])
    palette_number: int     = Retriever(uint8,      default=21)
    uncomp_size: int        = Retriever(uint32,     default=0)
    # @formatter:on

class Frame(BaseStruct):
    compression_8_to_5 = False
    shadows_on_top = False
    @staticmethod
    def set_layer_repeats(_, instance: Frame):

        frame_type = (instance.frame_header.frame_type)
        #print(frame_type)

        main_bitmask = 0b00000001
        shadow_bitmask = 0b00000010
        outline_bitmask = 0b00000100
        bitmask_8to5 = 0b00001000
        animations_shadows_on_top = 0b00010000

        #print("main", frame_type & main_bitmask)
        #print("shadow", frame_type & shadow_bitmask)
        #print("outline", frame_type & outline_bitmask)
        #print("8_to_5 compression_8_to_5", frame_type & bitmask_8to5)
        #print("animations_shadows_on_top", frame_type & animations_shadows_on_top)

        if frame_type & main_bitmask:
            pass
            #    print("main")

        if frame_type & shadow_bitmask:
            Retriever.set_repeat(Frame.shadow, instance, 1)
        if frame_type & outline_bitmask:
            Retriever.set_repeat(Frame.outline, instance, 1)
        if frame_type & bitmask_8to5:
            Frame.compression_8_to_5 = True
        if frame_type & animations_shadows_on_top:
            Frame.shadows_on_top = True
        #print("compression_8_to_5", Frame.compression_8_to_5)
        #print("shadows_on_top", Frame.shadows_on_top)

    @staticmethod
    def set_flags(_, instance: Frame):
        Frame.flags = instance.frame_header.frame_type

    # frame_header: Frame_Header                    = Retriever(Frame_Header,               default_factory=Frame_Header,                   on_read=[set_flags])
    # void: void                                    = Retriever(Bytes[0],                                                                   on_read = [set_layer_repeats])
    frame_header: SMX_Frame_Header                  = Retriever(SMX_Frame_Header,                                   default_factory=SMX_Frame_Header,   on_read = [set_layer_repeats])
    main: SLXMainLayer                              = Retriever(SLXMainLayer,                                       default_factory=SLXMainLayer)
    shadow: SMXShadowLayer                          = Retriever(SMXShadowLayer,                repeat=-1,            default_factory=SMXShadowLayer)
    outline: SMXOutlineLayer                        = Retriever(SMXOutlineLayer,               repeat=-1,            default_factory=SMXOutlineLayer)
    # compression: DamageLayer                      = Retriever(DamageLayer,                default_factory=DamageLayer)
    # other_animation_shadows: PlayerColourLayer    = Retriever(PlayerColourLayer,          default_factory=PlayerColourLayer)


# 7 	If set to 1, the frame contains a main graphic layer
# 6 	If set to 1, the frame contains a shadow layer
# 5 	If set to 1, the frame contains an outline layer
# 4 	Determines the compression algorithm for the main graphic layer. 0 = 4plus1; 1 = 8to5 (see the Compression Algorithms section)
# 3 	If set to 1, other animations' shadows will be cast over the animation.
# 0-2 	Unused

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
        #print(f"Frames: {instance.header.num_frames}")

    header: SMX_Header                          = Retriever(SMX_Header,             default_factory=SMX_Header, on_read=[set_frames_repeat])
    frames: list[Frame]                         = Retriever(Frame,                  default_factory=Frame)

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