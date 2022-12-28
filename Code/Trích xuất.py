from osgeo import gdal, osr
import numpy as np
from numpy import exp
import math
import csv
import matplotlib.pyplot as plt
import matplotlib

raw_x = []
raw_y = []

def printMaxMin(data):
  print("Max: ", np.nanmax(data))
  print("Min: ", np.nanmin(data))
  print("Mean: ", np.nanmean(data))
  print("Median: ", np.nanmedian(data))
  print("Std: ", np.nanstd(data))

def csv2array(path, x_root, y_root, height, width):
  x = []
  y = []
  with open(path) as csvfile:
    #reader = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC) # change contents to floats
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
        x.append(int((float(row[0]) - x_root) / width))
        y.append(int((float(row[1]) - y_root) / height))
        raw_x.append(row[0])
        raw_y.append(row[1])
  return x,y

def array2raster(newRasterfn,raster,array):
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]
    cols = array.shape[1]
    rows = array.shape[0]

    driver = gdal.GetDriverByName('GTiff')
    outRaster = driver.Create(newRasterfn, cols, rows, 1, gdal.GDT_Float32)
    outRaster.SetGeoTransform((originX, pixelWidth, 0, originY, 0, pixelHeight))

    outband = outRaster.GetRasterBand(1)
    outband.WriteArray(array)
    outRasterSRS = osr.SpatialReference()
    outRasterSRS.ImportFromWkt(raster.GetProjectionRef())
    outRaster.SetProjection(outRasterSRS.ExportToWkt())
    outband.FlushCache()

def raster2array(dataset):
  image = np.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount))
  for b in range(dataset.RasterCount):
      band = dataset.GetRasterBand(b + 1)
      barray = band.ReadAsArray()
      nan = barray[0][0]
      barray[barray == nan] = np.nan
      image[:,:,b] = barray
  return image


project_raster_path = r'Mẫu v2/LANDSAT8_ProjectRaster11.tif'    # 7 bands dữ liệu
d_ndvi_path = r'Tif/UTM/d_ndvi_ProjectRaster21.tif'          # 1 bands d-ndvi
# d_ndwi_path = r'Tif/UTM/d_ndwi_ProjectRaster1.tif' 

filein = 'Mẫu v6/wetland_points_v5.csv'                                  # csv đầu vào
fileout = 'Mẫu v3/Trích xuất v6/Wetlands_v5.csv'                    # csv sau khi trích xuất

dataset = gdal.Open(project_raster_path, gdal.GA_ReadOnly)      # mở raster
d_ndvi_dataset = gdal.Open(d_ndvi_path, gdal.GA_ReadOnly)      
# d_ndwi_dataset = gdal.Open(d_ndwi_path, gdal.GA_ReadOnly)      

geo_trans = dataset.GetGeoTransform()
x_root = geo_trans[0]
y_root = geo_trans[3]
width = geo_trans[1]
height = geo_trans[5]
x,y = np.array(csv2array(filein, x_root, y_root, height, width))


# chuyển dataset sang dạng mảng
image = raster2array(dataset)
image2 = raster2array(d_ndvi_dataset)
# image3 = raster2array(d_ndwi_dataset)

# xuất ra các mẫu đã trích xuất
with open(fileout, 'w') as output:
  output.write('x,y,ultra_blue,blue,green,red,nir,swir1,swir2,d-ndvi\n')
  for i in range(len(x)):
    if (str(image[y[i]][x[i]][0]) != "nan"):
        output.write(raw_x[i] + ',')
        output.write(raw_y[i] + ',')
        for j in range(7):
            output.write(str(image[y[i]][x[i]][j]) + ',')

        output.write(str(image2[y[i]][x[i]][0]) + ',')
        # output.write(str(image3[y[i]][x[i]][0]))
        output.write('\n')

# Hiển thị các mẫu vừa trích xuất lên bản đồ để biết sự phân bố của các mẫu vừa trích xuất
plt.plot(x, y,'b.')
plt.imshow(image2[:,:,0], cmap='Greens')
plt.colorbar()
plt.show()