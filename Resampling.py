import os
import zipfile
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
from affine import Affine

output_zip = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/output_zip/' # directory dove salvo le immagini di cui fare il resampling
input_zip = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/input_zip/'
# resampled_image_path = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio//output_zip/S2A_MSIL2A_20181013T100021_N0209_R122_T33TTG_20181013T114121.SAFE/GRANULE/L2A_T33TTG_A017279_20181013T100023/IMG_DATA/resampled_images/'
extract_band_list = ['B01_60m', 'B02_10m', 'B03_10m', 'B04_10m', 'B05_20m', 'B06_20m', 'B07_20m', 'B08_10m', 'B8A_20m',
                     'B09_60m', 'B11_20m', 'B12_20m']


resampled_image_path = '/home/famiglia/Scrivania/'
def resampling():
    # for zip_file in os.listdir(input_zip):
    #     zip_ref = zipfile.ZipFile(os.path.join(input_zip, zip_file), 'r')
    #     for zip_item in zip_ref.namelist():
    #         for index in extract_band_list:
    #             temp = index + '.jp2'
    #             # print zip_item
    #             if temp in zip_item:
    #                 print temp
    #                 zip_ref.extract(zip_item, output_zip)
    #     zip_ref.close()


    # ex_input_20m = '/home/famiglia/Scrivania/T33TTG_20181013T100021_B05_20m.jp2'
    ex_input_10m = '/home/famiglia/Scrivania/T33TTG_20181013T100021_B02_10m.jp2'
    dataset_10m = rasterio.open(ex_input_10m)
    arr_10m = dataset_10m.read()
    path = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/output_zip/S2A_MSIL2A_20181013T100021_N0209_R122_T33TTG_20181013T114121.SAFE/GRANULE/'
    temp = os.listdir(path)
    path = path + temp[0] + '/IMG_DATA/'
    i = 0
    for resize_dirs in os.listdir(path):
        if 'R10m' not in resize_dirs:
            # print path
            temp_path = path + resize_dirs
            for resize_jp2 in os.listdir(temp_path):
                resize_file_path = temp_path + '/' + resize_jp2
                dataset = rasterio.open(resize_file_path, driver='JP2OpenJPEG')
                src_arr = dataset.read()  # Array (immagine) di cui devo fare il resampling
                # print src_arr
                aff = dataset.transform
                # print aff
                resampled_arr = np.zeros((arr_10m.shape[1], arr_10m.shape[2]), dtype=src_arr.dtype)  # Array di destinazione
                x = 10980/src_arr.shape[1]
                # print src_arr.shape
                # print x
                # srcaff = Affine(1.0, 0.0, 0.0, 0.0, 1.0, 0.0)
                newaff = Affine(aff.a / x, aff.b, aff.c, aff.d, aff.e / x, aff.f)
                # print aff.g
                # print newaff
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
                print resampled_arr.shape[0], resampled_arr.shape[1]
                resampled_file_name = resampled_image_path + 'resampled_image_' + 'B' + str(i) +'_R10m.jp2'
                print resampled_file_name
                # print resampled_arr
                resampled_image = rasterio.open(resampled_file_name, 'w',
                                                height=resampled_arr.shape[0], width=resampled_arr.shape[1],
                                                driver='JP2OpenJPEG', count=1, dtype=resampled_arr.dtype,
                                                crs=dataset.crs, transform=newaff)
                print resampled_image.block_shapes
                print 'Sto per scrivere'
                resampled_image.write(resampled_arr, 1)
                # resampled_image.close()
                print 'Ho scritto'
                i += 1
                dataset.close()

