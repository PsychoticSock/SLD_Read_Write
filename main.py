from pathlib import Path


from SLD_drawing import DrawGraphicsLayers
from SLD_struct.sld_structure import SLD
from SMX_struct.smx_structure import SMX

if __name__ == "__main__":

    current_sld = (Path(__file__).parent / 'sld_source/u_sie_cobra_car_idleA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/a_alfred_attackA_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_rubble_1x1_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_scen_hut_a_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/s_campfire_x1.sld').absolute()
    current_sld = (Path(__file__).parent / 'sld_source/b_medi_castle_age3_x1.sld').absolute()


    current_smx = (Path(__file__).parent / 'smx_source/b_medi_castle_age3_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/u_sie_cobra_car_idleA_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/s_rubble_1x1_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/b_scen_hut_a_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/a_alfred_attackA_x1.smx').absolute()
    current_smx = (Path(__file__).parent / 'smx_source/s_campfire_x1.smx').absolute()

SLD_test = False
if SLD_test:
    print(f"Using file {current_sld}:")
    sld_file: SLD = SLD._from_file(str(current_sld), strict=False)

    for frame in range(sld_file.header.num_frames):
        #print(frame)
        images = DrawGraphicsLayers(sld_file, frame, show_images=False)


SMX_test = True
if SMX_test:
    print(f"Using file {current_smx}:")
    smx_file: SLD = SMX._from_file(str(current_smx), strict=False)
    print(smx_file)