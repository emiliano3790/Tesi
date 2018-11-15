import os
import rasterio
from rasterio.merge import merge

resampled_images_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/3_resampled_images/'
mosaiced_image_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/4_mosaiced_image/'

band_list = ['B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'B07', 'B08', 'B8A', 'B09', 'B11', 'B12']


def mosaic_images():
    for band in band_list:
        merging_image_list = []
        for spec_resampled_dir in os.listdir(resampled_images_dir):
            for filenames in os.listdir(resampled_images_dir + spec_resampled_dir):
                if band in filenames:
                    print resampled_images_dir + spec_resampled_dir + filenames
                    merging_image_list.append(rasterio.open(resampled_images_dir + spec_resampled_dir + '/' + filenames, 'r'))
                    continue
        merged_array, output_transform = merge(merging_image_list)
        example_dataset_meta = merging_image_list[0].meta.copy()
        print example_dataset_meta
        example_dataset_meta.update({"driver": "GTiff",
                                     "height": merged_array.shape[1],
                                     "width": merged_array.shape[2],
                                     "transform": output_transform
                                     })
        print example_dataset_meta
        print "Mosaicatura effettuata"
        mosaiced_image = rasterio.open(mosaiced_image_dir + 'mosaic_image_' + band + '.tif', "w", **example_dataset_meta)
        mosaiced_image.write(merged_array)
        merging_image_list[0].close()
        merging_image_list[1].close()
        mosaiced_image.close()