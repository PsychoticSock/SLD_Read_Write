from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import ByteStream, FixedLenStr, uint16, uint32, uint8

def convert_pixel_array_to_lookup(pixel_array):
    output_array = []
    for x in range(0, len(pixel_array), 5):

        palette_sections = pixel_array[x + 4]
        palette_section_pixel0 = palette_sections & 0b00000011
        palette_section_pixel1 = palette_sections >> 2 & 0b00000011
        palette_section_pixel2 = palette_sections >> 4 & 0b00000011
        palette_section_pixel3 = palette_sections >> 6 & 0b00000011

        output_array.append([pixel_array[x], palette_section_pixel0])
        output_array.append([pixel_array[x+1], palette_section_pixel1])
        output_array.append([pixel_array[x+2], palette_section_pixel2])
        output_array.append([pixel_array[x+3], palette_section_pixel3])

    return output_array

class SMX_Layer_Header(BaseStruct):
    # @formatter:off
    width: int                  = Retriever(uint16,         default=0)
    height: int                 = Retriever(uint16,         default=0)
    hotspot_x: int              = Retriever(uint16,         default=0)
    hotspot_y: int              = Retriever(uint16,         default=0)
    layer_len: int              = Retriever(uint32,         default=0)
    Unknown: int                = Retriever(uint32,         default=0)
    # @formatter:on

class SMXOutlineLayer(BaseStruct):
    @staticmethod
    def set_combined_array_repeat(_, instance: SMX_MainLayer):
        # print("instance.layer_header.height", instance.layer_header.layer_len)
        Retriever.set_repeat(SMX_MainLayer.command_array, instance, instance.layer_header.layer_len)

    # @formatter:off
    layer_header: SMX_Layer_Header      = Retriever(SMX_Layer_Header,                   default_factory=SMX_Layer_Header,   on_read=[set_combined_array_repeat])
    command_array: list[int]            = Retriever(uint8,              repeat=-1,      default=0)
    # @formatter:on

class SMXShadowLayer(BaseStruct):
    @staticmethod
    def set_combined_array_repeat(_, instance: SMX_MainLayer):
        #print("instance.layer_header.height", instance.layer_header.layer_len)
        Retriever.set_repeat(SMX_MainLayer.command_array, instance, instance.layer_header.layer_len)

    # @formatter:off
    layer_header: SMX_Layer_Header      = Retriever(SMX_Layer_Header,                   default_factory=SMX_Layer_Header,   on_read=[set_combined_array_repeat])
    command_array: list[int]            = Retriever(uint8,              repeat=-1,      default=0)
    # @formatter:on

class SMP_Layer_Row_Edge(BaseStruct):
    # @formatter:off
    left_space: int             = Retriever(uint16, default=0)
    right_space: int            = Retriever(uint16, default=0)
    # @formatter:on

class SMX_MainLayer(BaseStruct):
    @staticmethod
    def set_row_edge_repeat(_, instance: SMX_MainLayer):
        # print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SMX_MainLayer.smp_layer_row_edge, instance, instance.layer_header.height)
    @staticmethod
    def set_command_array_repeat(_, instance: SMX_MainLayer):
        # print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SMX_MainLayer.command_array, instance, instance.command_array_length)
    @staticmethod
    def set_pixel_array_repeat(_, instance: SMX_MainLayer):
        # print("instance.layer_header.height", instance.layer_header.height)
        Retriever.set_repeat(SMX_MainLayer.pixel_data_array, instance, instance.pixel_data_array_length)

    # @formatter:off
    layer_header: SMX_Layer_Header          = Retriever(SMX_Layer_Header,                       default_factory=SMX_Layer_Header,   on_read=[set_row_edge_repeat])
    smp_layer_row_edge: SMP_Layer_Row_Edge  = Retriever(SMP_Layer_Row_Edge,     repeat=-1)
    command_array_length: int               = Retriever(uint32,                                 default=0,                          on_read=[set_command_array_repeat])
    pixel_data_array_length: int            = Retriever(uint32,                                 default=0,                          on_read=[set_pixel_array_repeat])
    command_array: list[int]                = Retriever(uint8,                  repeat=-1,      default=0)
    pixel_data_array: list[int]             = Retriever(uint8,                  repeat=-1,      default=0)
    # @formatter:on

class SMX_Frame_Header(BaseStruct):
    # @formatter:off
    frame_type: int         = Retriever(uint8,      default=3)  #, on_read=[])
    palette_number: int     = Retriever(uint8,      default=21)
    uncomp_size: int        = Retriever(uint32,     default=0)
    # @formatter:on

class SMX_Frame(BaseStruct):
    compression_8_to_5 = False
    shadows_on_top = False
    @staticmethod
    def set_layer_repeats(_, instance: SMX_Frame):

        frame_type = (instance.smx_frame_header.frame_type)
        # print(frame_type)

        main_bitmask = 0b00000001
        shadow_bitmask = 0b00000010
        outline_bitmask = 0b00000100
        bitmask_8to5 = 0b00001000
        animations_shadows_on_top = 0b00010000

        # print("main", frame_type & main_bitmask)
        # print("shadow", frame_type & shadow_bitmask)
        # print("outline", frame_type & outline_bitmask)
        # print("8_to_5 compression_8_to_5", frame_type & bitmask_8to5)
        # print("animations_shadows_on_top", frame_type & animations_shadows_on_top)

        if frame_type & main_bitmask:
            pass
            #    print("main")

        if frame_type & shadow_bitmask:
            Retriever.set_repeat(SMX_Frame.smx_shadow, instance, 1)
        if frame_type & outline_bitmask:
            Retriever.set_repeat(SMX_Frame.smx_outline, instance, 1)
        if frame_type & bitmask_8to5:
            SMX_Frame.compression_8_to_5 = True
        if frame_type & animations_shadows_on_top:
            SMX_Frame.shadows_on_top = True
        # print("compression_8_to_5", Frame.compression_8_to_5)
        # print("shadows_on_top", Frame.shadows_on_top)

    @staticmethod
    def set_flags(_, instance: SMX_Frame):
        SMX_Frame.flags = instance.smx_frame_header.frame_type

    # @formatter:off
    smx_frame_header: SMX_Frame_Header        = Retriever(SMX_Frame_Header,                                   default_factory=SMX_Frame_Header,   on_read = [set_layer_repeats])
    smx_main: SMX_MainLayer                   = Retriever(SMX_MainLayer,                                      default_factory=SMX_MainLayer)
    smx_shadow: SMXShadowLayer                = Retriever(SMXShadowLayer,                repeat=-1,           default_factory=SMXShadowLayer)
    smx_outline: SMXOutlineLayer              = Retriever(SMXOutlineLayer,               repeat=-1,           default_factory=SMXOutlineLayer)
    # @formatter:on

class SMX_Header(BaseStruct):
    # @formatter:off
    file_descriptor: str            = Retriever(FixedLenStr[4],         default="SMPX")
    version: int                    = Retriever(uint16,                 default=2)
    num_frames: int                 = Retriever(uint16,                 default=1)
    file_size_comp: int             = Retriever(uint32,                 default=0)
    file_size_uncomp: int           = Retriever(uint32,                 default=0)
    comment: int                    = Retriever(FixedLenStr[16])
    # @formatter:on

class SMX(BaseStruct):
    @staticmethod
    def set_frames_repeat(_: Retriever, instance: SMX):
        Retriever.set_repeat(SMX.smx_frames, instance, instance.smx_header.num_frames)
        #print(f"Frames: {instance.header.num_frames}")

    # @formatter:off
    smx_header: SMX_Header           = Retriever(SMX_Header,            default_factory=SMX_Header,     on_read=[set_frames_repeat])
    smx_frames: list[SMX_Frame]          = Retriever(SMX_Frame,             default_factory=SMX_Frame)
    # @formatter:on

    @classmethod
    def get_version(
            cls,
            stream: ByteStream,
            struct_ver: Version = Version((0,)),
            parent: BaseStruct = None,
    ) -> Version:
        ver_str = str(stream.peek(6)[-2])
        return Version(tuple(map(int, ver_str.split("."))))