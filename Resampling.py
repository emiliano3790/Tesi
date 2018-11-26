import os
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
from affine import Affine
import Tool as tl

resizing_band_list = ['B01', 'B09', 'B11', 'B8A', 'B05', 'B06', 'B07', 'B12']


def resampling(jp2_images_dir, resampled_images_dir, zip_path_list):
    tl.extract_zip(jp2_images_dir, zip_path_list)
    band_name = ''
    for jp2_directory in os.listdir(jp2_images_dir):
        resampled_images_specprod_dir = resampled_images_dir + jp2_directory
        os.mkdir(resampled_images_specprod_dir)
        jp2_files_list = []
        for root, dirnames, filenames in os.walk(jp2_images_dir + jp2_directory):
            for filename in filenames:
                jp2_files_list.append(os.path.join(root, filename))
        height_10m, width_10m = tl.get10mFeatures(jp2_files_list)
        for jp2_image in jp2_files_list:
            if '10m' in jp2_image:
                tl.convertJP2toTIF(jp2_image, resampled_images_specprod_dir)
                print 'Copied file: ', jp2_image
                continue
            else:
                for band_name in resizing_band_list:
                    if band_name in jp2_image:
                        break
            dataset = rasterio.open(jp2_image, driver='JP2OpenJPEG')  # Immagine di cui devo fare il resampling
            src_arr = dataset.read(1)  # Array di cui devo fare il resampling
            aff = dataset.transform
            resampled_arr = np.empty((height_10m, width_10m),
                                     dtype=src_arr.dtype)  # Array di destinazione
            x = height_10m / src_arr.shape[1]  # Upsampling
            newaff = Affine(aff.a / x, aff.b, aff.c, aff.d, aff.e / x, aff.f)
            reproject(
                # source parameters
                source=src_arr,
                src_crs=dataset.crs,
                src_transform=dataset.transform,
                # dest parameters
                destination=resampled_arr,
                dst_crs=dataset.crs,
                dst_transform=newaff,
                resampling=Resampling.nearest)
            resampled_file_name = resampled_images_specprod_dir + '/' + 'resampled_image_' \
                                  + str(band_name) + '_10m.tif'
            resampled_image = rasterio.open(resampled_file_name, 'w',
                                            height=resampled_arr.shape[0], width=resampled_arr.shape[1],
                                            count=1, dtype=resampled_arr.dtype, driver='GTiff',
                                            crs=dataset.crs, transform=newaff)
            resampled_image.write(resampled_arr, 1)
            resampled_image.close()
            dataset.close()
            print 'Resampled file: ', resampled_file_name
