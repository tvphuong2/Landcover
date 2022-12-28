from osgeo import gdal, osr
import numpy as np

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

path = r'D:/Documents/AI/INT3401 2/BTL/Dataset/LANDSAT8.tif'
dataset = gdal.Open(path, gdal.GA_ReadOnly)
data = dataset.ReadAsArray()

image = np.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount))

for b in range(dataset.RasterCount):
    band = dataset.GetRasterBand(b + 1)
    image[:,:,b] = band.ReadAsArray()

print("Max: ", np.nanmax(data[0]))
print("Min: ", np.nanmin(data[0]))
print("Mean: ", np.nanmean(data[0]))
print("Median: ", np.nanmedian(data[0]))
print("Std: ", np.nanstd(data[0]))

#ndwi = (image[:,:,2] - image[:,:,4] / (image[:,:,2] + image[:,:,4]))
ndvi = (image[:,:,4] - image[:,:,3] / (image[:,:,3] + image[:,:,4]))

array2raster('ndvi.tif',dataset,ndvi)
