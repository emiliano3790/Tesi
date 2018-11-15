import Resampling as rs
import MosaicImage as mi
import MaskImage as mki
import StackBands as ms
import os
import Tkinter, tkFileDialog
import shutil


jp2_images_dir = '/1_jp2_images/'
resampled_images_dir = '/2_resampled_images/'
mosaiced_image_dir = '/3_mosaiced_image/'
masked_image_dir = '/4_masked_image/'
stacked_bands_dir = '/5_stacked_bands/'

work_dir = raw_input("Choose name for working directory: ")
root = Tkinter.Tk()
filez = tkFileDialog.askopenfilenames(parent=root, title='Choose a file')
zip_path_list = list(filez)
cwd = os.getcwd() + '/' + work_dir
os.mkdir(cwd)
os.mkdir(cwd + jp2_images_dir)
os.mkdir(cwd + resampled_images_dir)
os.mkdir(cwd + mosaiced_image_dir)
os.mkdir(cwd + masked_image_dir)
os.mkdir(cwd + stacked_bands_dir)

rs.resampling(cwd + jp2_images_dir, cwd + resampled_images_dir, zip_path_list)
mi.mosaic_images(cwd + resampled_images_dir, cwd + mosaiced_image_dir)
# work_dir = raw_input("Choose name for working directory: ")
# root = Tkinter.Tk()
# cwd = os.getcwd() + '/' + work_dir
geojson_path = tkFileDialog.askopenfilenames(parent=root, title='Choose a valid geoJSON file')
mki.mask_image(cwd + mosaiced_image_dir, cwd + masked_image_dir, geojson_path[0])
ms.stack_bands(cwd + masked_image_dir, cwd + stacked_bands_dir)

shutil.rmtree(cwd + jp2_images_dir)
shutil.rmtree(cwd + resampled_images_dir)