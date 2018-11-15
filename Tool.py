import rasterio
from rasterio.warp import reproject
import os
import numpy as np


def convertJP2toTIF(source_file, dest_path):
    jp2_dataset = rasterio.open(source_file, driver='JP2OpenJPEG')
    jp2_arr = jp2_dataset.read()
    dest_file = dest_path + '/' + os.path.basename(source_file)
    dest_file = dest_file[:-3] + 'tif'
    tiff_arr = np.empty((jp2_arr.shape[0], jp2_arr.shape[1]), dtype=jp2_arr.dtype)
    reproject(
        # source parameters
        source=jp2_arr,
        src_crs=jp2_dataset.crs,
        src_transform=jp2_dataset.transform,
        # dest parameters
        destination=tiff_arr,
        dst_crs=jp2_dataset.crs,
        dst_transform=jp2_dataset.transform)
    tiff_image = rasterio.open(dest_file, 'w',
                                    height=jp2_arr.shape[1], width=jp2_arr.shape[2],
                                    count=1, dtype=jp2_arr.dtype, driver='GTiff',
                                    crs=jp2_dataset.crs, transform=jp2_dataset.transform)
    tiff_image.write(jp2_arr)
    tiff_image.close()
    jp2_dataset.close()