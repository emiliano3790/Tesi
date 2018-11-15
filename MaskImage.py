import rasterio
from rasterio.mask import mask
import os
import json


def mask_image(mosaiced_image_dir, masked_image_dir, geojson_path):
    geojson = open(geojson_path, 'r').read()
    readable_json = json.loads(geojson)
    polygon = []
    polygon.append(readable_json.get('geometry'))
    for mosaiced_image in os.listdir(mosaiced_image_dir):
        with rasterio.open(mosaiced_image_dir + mosaiced_image, 'r') as src:
            out_image, out_transform = mask(src, polygon, crop=True)
        print 'Masked ok for file: ', mosaiced_image
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
        with rasterio.open(masked_image_dir + 'masked_' + mosaiced_image[-8:-4] + '.tif', "w", **out_meta) \
                as dest:
            dest.write(out_image)