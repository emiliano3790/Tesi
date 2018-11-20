import rasterio
import os


def stack_bands(masked_images_dir, stacked_bands_dir):
    stack_file_name = stacked_bands_dir + 'stacked_image.tif'
    tif_file_path_list = []
    for masked_tif in os.listdir(masked_images_dir):
        tif_file_path_list.append(masked_images_dir + masked_tif)
    masked = rasterio.open(tif_file_path_list[0])
    stack_meta = masked.meta.copy()
    masked.close()
    stack_meta.update(count=len(tif_file_path_list))
    stack_file = rasterio.open(stack_file_name, 'w+', **stack_meta)
    i = 1
    for tif_file in tif_file_path_list:
        with rasterio.open(tif_file) as src_tif:
            stack_file.write_band(i, src_tif.read(1))
            stack_file.update_tags(band=src_tif.descriptions[0])
            stack_file.set_band_description(i, src_tif.descriptions[0])
        i += 1
    stack_file.close()
    print 'Stack operation ok!!!'




