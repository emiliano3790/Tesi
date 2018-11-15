import rasterio
from rasterio.mask import mask
import os
import json
import fiona


masked_image_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/5_masked_image/'
mosaiced_image_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/4_mosaiced_image/'
geojson_path = '/home/famiglia/Scrivania/GeoJSON_ex.json'
resampled_images_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_Rasterio/3_resampled_images/S2A_MSIL2A_20181013T100021_N0209_R122_T33TTG_20181013T114121.SAFE/'


def maskImage():
    geojson = open(geojson_path, 'r').read()
    readable_json = json.loads(geojson)
    print type(readable_json)
    print readable_json

    # polygon = []
    # for key, value in dict.items(readable_json):
    #     print key, value
    #     if key == 'geometry':
    #         # print value
    #         polygon.append(value)
    # # print polygon
    # print type(polygon)
    # points = [(309910.6, 4678129.3),
    #           (351822.5, 4668851.3),
    #           (349591.4, 4650291.6),
    #           (313428.7, 4654113.9),
    #           (309910.6, 4678129.3)]
    # geoms = [{'type': 'Polygon',
    #           'coordinates': [points]}]
    # print geoms
    # print type(geoms)
    with fiona.open(geojson_path, "r") as shapefile:
        for feature in shapefile:
            print feature
        features = [feature["geometry"] for feature in shapefile]
    print features
    for mosaiced_image in os.listdir(mosaiced_image_dir):
        print mosaiced_image
        with rasterio.open(mosaiced_image_dir + mosaiced_image, 'r') as src:
            out_image, out_transform = mask(src, readable_json, crop=True)
        out_meta = src.meta.copy()
        out_meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
        with rasterio.open(masked_image_dir + 'masked_' + mosaiced_image[-8:-4] + '.tif', "w", **out_meta) \
                as dest:
            dest.write(out_image)