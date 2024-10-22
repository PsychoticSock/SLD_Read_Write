from __future__ import annotations

from binary_file_parser import BaseStruct, Retriever, Version
from binary_file_parser.types import ByteStream

from SLD_struct.sld_file_header import SLD_Header
from SLD_struct.sld_frames import SLD_Frame



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

class SLD(BaseStruct):
    @staticmethod
    def set_frames_repeat(_: Retriever, instance: SLD):
        Retriever.set_repeat(SLD.sld_frames, instance, instance.sld_header.num_frames)
        print(f"Frames: {instance.sld_header.num_frames}")

    sld_header: SLD_Header                       = Retriever(SLD_Header, default_factory=SLD_Header, on_read=[set_frames_repeat])
    sld_frames: list[SLD_Frame] = Retriever(SLD_Frame, default_factory=SLD_Frame)

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