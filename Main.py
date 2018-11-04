#import sys
#sys.path.append('/home/famiglia/.snap/snap-python')
#import snappy
import os
from snappy import ProductIO
from snappy import GPF
from snappy import jpy
from snappy import HashMap


# input directory with all products
partial_input_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/input_dir/r10m/'
# output folder
output_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/output_dir'

arr_band = ['B2', 'B3', 'B4']
parameters = HashMap()
parameters.put('combine', 'AND')
#parameters.put('combine', 'OR')
parameters.put('resampling', 'Nearest')
parameters.put('crs', 'EPSG:4326')
parameters.put('westBound', '11.35495423')
parameters.put('northBound', '42.44744303')
parameters.put('eastBound', '13.91997284')
parameters.put('southBound', '41.40772619')
parameters.put('pixelSizeX', 0.05)
parameters.put('pixelSizeY', 0.05)
Variable = jpy.get_type('org.esa.snap.core.gpf.common.MosaicOp$Variable')  # Ho richiamato il costruttore Variable
#vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', len(arr_band))
vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', 1)
parameters.put('Region', 'Rectangle(0, 0 , 1000, 1000)')
#Mosaic = GPF.createProduct('Subset', parameters, products)

for band in arr_band:
    # creating file with input images
    products = []
    input_dir = partial_input_dir + band
    print input_dir
    for product in os.listdir(input_dir):  # os.listdir restituisce una lista con tutti gli elementi contenuti nella cartella specificata
        products.append(ProductIO.readProduct(os.path.join(input_dir, product)))
        vars[0] = Variable(band, 'band_1')
        parameters.put('variables', vars)
        # creating mosaic
        Mosaic = GPF.createProduct('Mosaic', parameters, products)
        # Writing output
        out_file_name = 'out_file' + band
        ProductIO.writeProduct(Mosaic, os.path.join(output_dir, out_file_name), 'BEAM-DIMAP')