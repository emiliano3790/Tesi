#import sys
#sys.path.append('/home/famiglia/.snap/snap-python')
#import snappy
import os
from snappy import ProductIO
from snappy import GPF
from snappy import jpy
from snappy import HashMap


# input directory with all products
input_dir = '/home/famiglia/Scrivania/Prova_Tesi/input_dir'
# output folder
output_dir = '/home/famiglia/Scrivania/Prova_Tesi/output_dir'

parameters = HashMap()
parameters.put('combine', 'OR')
parameters.put('combine', 'OR')
parameters.put('resampling', 'Nearest')
parameters.put('crs', 'EPSG:4326')
parameters.put('westBound', '11.35495423')
parameters.put('northBound', '42.44744303')
parameters.put('eastBound', '13.91997284')
parameters.put('southBound', '41.40772619')
parameters.put('pixelSizeX', 0.001)
parameters.put('pixelSizeY', 0.001)
Variable = jpy.get_type('org.esa.snap.core.gpf.common.MosaicOp$Variable')  # Ho richiamato il costruttore Variable
vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', 1)
vars[0] = Variable('band_1', 'band_1')
parameters.put('variables', vars)


# creating file with input images
products = []
for product in os.listdir(input_dir):  # os.listdir restituisce una lista con tutti gli elementi contenuti nella cartella specificata
    products.append(ProductIO.readProduct(os.path.join(input_dir, product)))
# bnames = products[0].getBandNames()
# print type(bnames)
# print str(bnames[0])
# band_1 = str(bnames[0])
# parameters.put('variables.variable.name', band_1)

# creating mosaic
Mosaic = GPF.createProduct('Mosaic', parameters, products)
# Writing output
ProductIO.writeProduct(Mosaic, os.path.join(output_dir, 'out_file'), 'BEAM-DIMAP')
