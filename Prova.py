import os
from snappy import ProductIO
from snappy import GPF
from snappy import jpy
from snappy import HashMap

# input directory with all products
partial_input_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/S2A_MSIL2A_20181013T100021_N0209_R122_T33TUG_20181013T114121.zip'
# output folder
output_dir = '/home/famiglia/Scrivania/Tesi_Magistrale/Prova_Tesi/output_dir'

# arr_band = ['B2', 'B3', 'B4']
# parameters = HashMap()
# parameters.put('combine', 'AND')
# parameters.put('combine', 'OR')
# parameters.put('resampling', 'Nearest')
# parameters.put('crs', 'EPSG:4326')
# parameters.put('westBound', '11.35495423')
# parameters.put('northBound', '42.44744303')
# parameters.put('eastBound', '13.91997284')
# parameters.put('southBound', '41.40772619')
# parameters.put('pixelSizeX', 0.05)
# parameters.put('pixelSizeY', 0.05)
# Variable = jpy.get_type('org.esa.snap.core.gpf.common.MosaicOp$Variable')  # Ho richiamato il costruttore Variable
# vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', len(arr_band))
# vars = jpy.array('org.esa.snap.core.gpf.common.MosaicOp$Variable', 1)
# parameters.put('Region', 'Rectangle(0, 0 , 1000, 1000)')
# Mosaic = GPF.createProduct('Subset', parameters, products)

image = ProductIO.readProduct(partial_input_dir)
B = image.getBand('B2')
G = image.getBand('B3')
R = image.getBand('B4')
print B, G, R