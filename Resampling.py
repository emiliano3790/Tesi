import os
import zipfile
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
from affine import Affine
from shutil import copy


input_zip = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/1_input_zip/'
jp2_images = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/2_jp2_images/'
resampled_images = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/3_resampled_images/'
concatenated_bands = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/4_concatenated_bands/'
ex_input_10m = '/home/famiglia/Scrivania/T33TTG_20181013T100021_B02_10m.jp2'


extract_band_list = ['B01_60m', 'B02_10m', 'B03_10m', 'B04_10m', 'B05_20m', 'B06_20m', 'B07_20m', 'B08_10m', 'B8A_20m',
                     'B09_60m', 'B11_20m', 'B12_20m']
resizing_band_list = ['B01', 'B09', 'B11', 'B8A', 'B05', 'B06', 'B07', 'B12']


def resampling():
    # con questo primo for estraggo le immagini jp2 di cui devo fare il resampling
    for zip_file in os.listdir(input_zip):
        zip_ref = zipfile.ZipFile(os.path.join(input_zip, zip_file), 'r')
        for zip_item in zip_ref.namelist():
            for index in extract_band_list:
                temp = index + '.jp2'
                if temp in zip_item:
                    zip_ref.extract(zip_item, jp2_images)
        zip_ref.close()

    dataset_10m = rasterio.open(ex_input_10m)
    arr_10m = dataset_10m.read()
    band_name = ''
    for jp2_directory in os.listdir(jp2_images):
        resampled_images_dir = resampled_images + jp2_directory
        print resampled_images_dir
        os.mkdir(resampled_images_dir)
        jp2_files_list = []
        for root, dirnames, filenames in os.walk(jp2_images + jp2_directory):
            for filename in filenames:
                # print os.path.join(root, filename)
                jp2_files_list.append(os.path.join(root, filename))
        for jp2_image in jp2_files_list:
            if '10m' in jp2_image:
                copy(jp2_image, resampled_images_dir)
                continue
            else:
                for band_name in resizing_band_list:
                    if band_name in jp2_image:
                        break
            dataset = rasterio.open(jp2_image, driver='JP2OpenJPEG')  # Immagine di cui devo fare il resampling
            src_arr = dataset.read()  # Array di cui devo fare il resampling
            aff = dataset.transform
            resampled_arr = np.empty((arr_10m.shape[1], arr_10m.shape[2]),
                                     dtype=src_arr.dtype)  # Array di destinazione
            x = arr_10m.shape[1] / src_arr.shape[1]  # Upsampling
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
            resampled_file_name = resampled_images_dir + '/' + 'resampled_image_' \
                                  + str(band_name) + '_10m.tif'
            print resampled_file_name
            resampled_image = rasterio.open(resampled_file_name, 'w',
                                            height=resampled_arr.shape[0], width=resampled_arr.shape[1],
                                            count=1, dtype=resampled_arr.dtype, driver='GTiff',
                                            crs=dataset.crs, transform=newaff)
            resampled_image.write(resampled_arr, 1)
            resampled_image.close()
            dataset.close()
    dataset_10m.close()