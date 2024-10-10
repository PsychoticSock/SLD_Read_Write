from __future__ import annotations

import math

from binary_file_parser import BaseStruct, Retriever
from binary_file_parser.types import uint32, FixedLenStr

from block_contruction import DXT1_Block, NVTT_DXT4_Block, DrawDXT1Graphic, FillDXT1_PixelBlocks, DrawDXT4Graphic, \
    Fill_DXT4_PixelBlocks


def DetermineBlockSize(dds_data):
    image_width = dds_data.dwWidth
    image_height = dds_data.dwHeight

    block_width_remainder = image_width % 4
    block_height_remainder = image_height % 4

    if block_width_remainder != 0:
        image_width_in_blocks = int(math.floor(image_width / 4) + 1)
    else:
        image_width_in_blocks = int(image_width / 4)
    if block_height_remainder != 0:
        image_height_in_blocks = int(math.floor(image_height / 4) + 1)
    else:
        image_height_in_blocks = int(image_height / 4)

    layer_blocks_length = image_width_in_blocks * image_height_in_blocks

    return layer_blocks_length

class DDS_PIXEL_FORMAT(BaseStruct):
    # @formatter:off
    dwSize: int             = Retriever(uint32,             default=0)
    dwFlags: int            = Retriever(uint32,             default=0)
    dwFourCC: str           = Retriever(FixedLenStr[4],     default=0)
    dwRGBBitCount: int      = Retriever(uint32,             default=0)
    dwRBitMask: int         = Retriever(uint32,             default=0)
    dwGBitMask: int         = Retriever(uint32,             default=0)
    dwBBitMask: int         = Retriever(uint32,             default=0)
    dwABitMask: int         = Retriever(uint32,             default=0)
    # @formatter:on


class DDS_DXT1(BaseStruct):
    @staticmethod
    def set_layer_blocks_repeat(_: Retriever, instance: DDS_DXT1):
        layer_blocks_length = DetermineBlockSize(instance)
        Retriever.set_repeat(DDS_DXT1.layer_blocks, instance, layer_blocks_length)

    # @formatter:off
    dwMagic: str                            = Retriever(FixedLenStr[4],                     default="DDS ")
    dwSize: int                             = Retriever(uint32,                             default=124)
    dwFlags: int                            = Retriever(uint32,                             default=0)
    dwHeight: int                           = Retriever(uint32,                             default=1)
    dwWidth: int                            = Retriever(uint32,                             default=1,      on_read=[set_layer_blocks_repeat])
    dwPitchOrLinearSize: int                = Retriever(uint32,                             default=0)
    dwDepth: int                            = Retriever(uint32,                             default=0)
    dwMipMapCount: int                      = Retriever(uint32,                             default=1)
    dwReserved1: int                        = Retriever(uint32,             repeat=11,      default=0)
    dds_pixel_format: DDS_PIXEL_FORMAT      = Retriever(DDS_PIXEL_FORMAT,                   default_factory=DDS_PIXEL_FORMAT)
    dwCaps: int                             = Retriever(uint32,                             default=0)
    dwCaps2: int                            = Retriever(uint32,                             default=0)
    dwCaps3: int                            = Retriever(uint32,                             default=0)
    dwCaps4: int                            = Retriever(uint32,                             default=0)
    dwReserved2: int                        = Retriever(uint32,                             default=0)
    layer_blocks: list[DXT1_Block]          = Retriever(DXT1_Block,                         default_factory=DXT1_Block)
    # @formatter:on

class DDS_DXT4(BaseStruct):
    @staticmethod
    def set_layer_blocks_repeat(_: Retriever, instance: DDS_DXT4):
        layer_blocks_length = DetermineBlockSize(instance)
        Retriever.set_repeat(DDS_DXT4.layer_blocks, instance, layer_blocks_length)

    # @formatter:off
    dwMagic: str                            = Retriever(FixedLenStr[4],                     default="DDS ")
    dwSize: int                             = Retriever(uint32,                             default=124)
    dwFlags: int                            = Retriever(uint32,                             default=0)
    dwHeight: int                           = Retriever(uint32,                             default=1)
    dwWidth: int                            = Retriever(uint32,                             default=1,      on_read=[set_layer_blocks_repeat])
    dwPitchOrLinearSize: int                = Retriever(uint32,                             default=0)
    dwDepth: int                            = Retriever(uint32,                             default=0)
    dwMipMapCount: int                      = Retriever(uint32,                             default=1)
    dwReserved1: int                        = Retriever(uint32,             repeat=11,      default=0)
    dds_pixel_format: DDS_PIXEL_FORMAT      = Retriever(DDS_PIXEL_FORMAT,                   default_factory=DDS_PIXEL_FORMAT)
    dwCaps: int                             = Retriever(uint32,                             default=0)
    dwCaps2: int                            = Retriever(uint32,                             default=0)
    dwCaps3: int                            = Retriever(uint32,                             default=0)
    dwCaps4: int                            = Retriever(uint32,                             default=0)
    dwReserved2: int                        = Retriever(uint32,                             default=0)
    layer_blocks: list[NVTT_DXT4_Block]     = Retriever(NVTT_DXT4_Block,                    default_factory=NVTT_DXT4_Block)
    # @formatter:on

dds_main_data = DDS_DXT1._from_file("nvtt_output/rainbow_bc1a.dds", strict=True)
dds_shadow_data = DDS_DXT4._from_file("nvtt_output/rainbow_alpha_bc3.dds", strict=False)

pixel_blocks = []
for block_index in range(len(dds_main_data.layer_blocks)):
    lookup_table = dds_main_data.layer_blocks[block_index].create_lookup_table()
    pixel_blocks.append(FillDXT1_PixelBlocks(lookup_table, dds_main_data.layer_blocks[block_index].pixel_indices))

MainImage = DrawDXT1Graphic(dds_main_data.dwWidth, dds_main_data.dwHeight, pixel_blocks, from_dds_file=True)

MainImage.show()
MainImage.save(f"dds_main_test.png")

shadow_pixel_blocks = []
for block_index in range(len(dds_shadow_data.layer_blocks)):
    lookup_table = dds_shadow_data.layer_blocks[block_index].create_lookup_table()
    shadow_pixel_blocks.append(Fill_DXT4_PixelBlocks(lookup_table, dds_shadow_data.layer_blocks[block_index].pixel_indices))

ShadowImage = DrawDXT4Graphic(dds_shadow_data.dwWidth, dds_shadow_data.dwHeight, shadow_pixel_blocks, from_dds_file=True)
ShadowImage.show()
ShadowImage.save(f"dds_shadow_test.png")