# import sys
# sys.path.append('/home/famiglia/.snap/snap-python')
# import snappy
import os
from snappy import ProductIO
from snappy import GPF
from snappy import jpy
from snappy import HashMap


# input directory
partial_input_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_1/input_dir/r10m/'
# input_dir = '/home/famiglia/Scrivania/Prova_Germania/input'
# output folder
output_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/Prova_1/output_dir/'
# output_dir = '/home/famiglia/Scrivania/Prova_Germania/output'

band_list = ['B2', 'B3', 'B4']
parameters = HashMap()
subset_parameters = HashMap()
# parameters.put('combine', 'OR')
parameters.put('resampling', 'Nearest')
parameters.put('crs', 'EPSG:4326')
parameters.put('westBound', '11.35495423')
parameters.put('northBound', '42.44744303')
parameters.put('eastBound', '13.91997284')
parameters.put('southBound', '41.40772619')
# parameters.put('westBound', '7.58808614')
# parameters.put('northBound', '50.55229211')
# parameters.put('eastBound', '10.54932815')
# parameters.put('southBound', '47.75740353')
parameters.put('pixelSizeX', 0.01)
parameters.put('pixelSizeY', 0.01)
Variable = jpy.get_type('org.esa.snap.core.gpf.common.MosaicOp$Variable')  # Ho richiamato il costruttore Variable
# vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', len(arr_band))
vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', 1)

for band in band_list:
    # creating file with input images
    products = []
    input_dir = partial_input_dir + band
    print input_dir
    for product in os.listdir(input_dir):  # os.listdir restituisce una lista con tutti gli elementi contenuti nella cartella specificata
            temp = ProductIO.readProduct(os.path.join(input_dir, product))
            # temp_arr = temp.getBandNames()
            print temp
            products.append(temp)
    vars[0] = Variable(band, 'band_1')
    parameters.put('variables', vars)
    # creating mosaic
    Mosaic = GPF.createProduct('Mosaic', parameters, products)
    # Writing output
    out_file_name = 'out_file_mosaic_' + band
    ProductIO.writeProduct(Mosaic, os.path.join(output_dir, out_file_name), 'BEAM-DIMAP')
    # parameters.clear()
    # subset_parameters.put('Region', 'Rectangle(103, 37, 20, 70)')
    subset_parameters.put('geoRegion', 'POLYGON((11.8050 42.3575, '
                                       '13.4450 42.3475, 13.6150 41.8875,12.3850 42.0775, 11.8050 42.3575))')
    Subset = GPF.createProduct('Subset', subset_parameters, Mosaic)
    out_file_name += 'out_file_subset_' + band
    ProductIO.writeProduct(Subset, os.path.join(output_dir, out_file_name), 'BEAM-DIMAP')