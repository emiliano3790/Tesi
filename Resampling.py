import os
import zipfile
import rasterio
import numpy as np
from rasterio.warp import reproject, Resampling
from affine import Affine
from shutil import copyfile

input_zip = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/input_zip/'
jp2_images = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/jp2_images/'
resampled_images = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/resampled_images/'
concatenated_bands = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/concatenated_bands/'
ex_input_10m = '/home/famiglia/Scrivania/T33TTG_20181013T100021_B02_10m.jp2'


extract_band_list = ['B01_60m', 'B02_10m', 'B03_10m', 'B04_10m', 'B05_20m', 'B06_20m', 'B07_20m', 'B08_10m', 'B8A_20m',
                     'B09_60m', 'B11_20m', 'B12_20m']
band_list = ['B01', 'B09', 'B11', 'B8A', 'B05', 'B06', 'B07', 'B12']
resizing_resolution = ['R20m', 'R60m']


def resampling():
    for zip_file in os.listdir(input_zip):
        zip_ref = zipfile.ZipFile(os.path.join(input_zip, zip_file), 'r')
        for zip_item in zip_ref.namelist():
            for index in extract_band_list:
                temp = index + '.jp2'
                if temp in zip_item:
                    # print temp
                    zip_ref.extract(zip_item, jp2_images)
        zip_ref.close()

    jp2_files_list = []
    jp2_files_dir = ''
    imgdata_path = ''
    dir = ''
    for jp2_directory in os.listdir(jp2_images):
        granule_path = jp2_images + jp2_directory + '/GRANULE/'
        for dir in os.listdir(granule_path):
            os.mkdir(resampled_images + dir)
            imgdata_path = granule_path + dir + '/IMG_DATA/'
            for resampling_directory in os.listdir(imgdata_path):
                if resampling_directory in resizing_resolution:
                    jp2_files_dir = imgdata_path + resampling_directory + '/'
                    for root, dirs, files in os.walk(jp2_files_dir):
                        for filename in files:
                            for band_name in band_list:
                                if band_name in filename:
                                    break
                            jp2_file_path = jp2_files_dir + filename
                            dataset_10m = rasterio.open(ex_input_10m)
                            arr_10m = dataset_10m.read()
                            dataset = rasterio.open(jp2_file_path, driver='JP2OpenJPEG')
                            src_arr = dataset.read()  # Array (immagine) di cui devo fare il resampling
                            # print src_arr
                            aff = dataset.transform
                            # print aff
                            resampled_arr = np.empty((arr_10m.shape[1], arr_10m.shape[2]), dtype=src_arr.dtype)  # Array di destinazione
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
                            resampled_file_name = resampled_images + dir + '/' + 'resampled_image_' + str(band_name) +'_10m.tif'
                            print resampled_file_name
                            resampled_image = rasterio.open(resampled_file_name, 'w',
                                                             height=resampled_arr.shape[0], width=resampled_arr.shape[1],
                                                             driver='GTiff', count=1, dtype=resampled_arr.dtype,
                                                             crs=dataset.crs, transform=newaff)
                            resampled_image.write(resampled_arr, 1)
                            resampled_image.close()
                            dataset.close()
        # for images_10m in os.listdir(imgdata_path + 'R10m'):
        #     source = imgdata_path + 'R10m' + '/' + images_10m
        #     destination = resampled_images + dir + '/' + images_10m
        #     new_dest = destination.replace('jp2', 'tif')
        #     dataset_jp2 = rasterio.open(source, driver='JP2OpenJPEG')
        #     arr_jp2 = dataset_jp2.read()
        #     tif_arr = np.empty((arr_jp2.shape[1], arr_jp2.shape[2]), dtype=arr_jp2.dtype)
        #     tif_image = rasterio.open(new_dest, 'w',
        #                                     height=arr_jp2.shape[1], width=arr_jp2.shape[2],
        #                                     driver='GTiff', count=1, dtype=arr_jp2.dtype,
        #                                     crs=dataset.crs, transform=dataset.transform)
        #     tif_image.write(arr_jp2, 1)
        #     tif_image.close()
        #     dataset_jp2.close()
        #     print destination
            # copyfile(source, destination)