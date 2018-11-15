import rasterio
import os

masked_images_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/5_masked_image/'
stacked_bands_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/6_stacked_bands/'


def stack_bands():
    stack_file_name = stacked_bands_dir + 'stacked_image.tif'
    tif_file_path_list = []
    for masked_tif in os.listdir(masked_images_dir):
        tif_file_path_list.append(masked_images_dir + masked_tif)
        print masked_images_dir + masked_tif
    masked = rasterio.open(tif_file_path_list[0])
    stack_meta = masked.meta.copy()
    masked.close()
    stack_meta.update(count=len(tif_file_path_list))
    stack_file = rasterio.open(stack_file_name, 'w+', **stack_meta)
    i = 1
    for tif_file in tif_file_path_list:
        src_tif = rasterio.open(tif_file)
        stack_file.write_band(i, src_tif.read(1))
        src_tif.close()
        i += 1
    dst_array = stack_file.read(1)
    print dst_array.shape
    stack_file.close()



