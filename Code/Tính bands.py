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

#............................................... Từ tháng 9 đến 12
path = r'Tif/raw/LANDSAT9-12.tif'
dataset = gdal.Open(path, gdal.GA_ReadOnly)
print(dataset.GetGeoTransform())
data = dataset.ReadAsArray()
data[np.isnan(data)] = 0
image = np.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount))

for b in range(dataset.RasterCount):
    band = dataset.GetRasterBand(b + 1)
    image[:,:,b] = band.ReadAsArray()

ndvi_9_12 = (image[:,:,4] - image[:,:,3]) / (image[:,:,3] + image[:,:,4])
# ndwi_9_12 = (image[:,:,2] - image[:,:,4]) / (image[:,:,2] + image[:,:,4])

#............................................... từ tháng 5-8
path = r'Tif/raw/LANDSAT5-8.tif'
dataset = gdal.Open(path, gdal.GA_ReadOnly)
print(dataset.GetGeoTransform())
data = dataset.ReadAsArray()
data[np.isnan(data)] = 0
image = np.zeros((dataset.RasterYSize, dataset.RasterXSize, dataset.RasterCount))

for b in range(dataset.RasterCount):
    band = dataset.GetRasterBand(b + 1)
    image[:,:,b] = band.ReadAsArray()

ndvi_5_8 = (image[:,:,4] - image[:,:,3]) / (image[:,:,3] + image[:,:,4])
# ndwi_5_8 = (image[:,:,2] - image[:,:,4]) / (image[:,:,2] + image[:,:,4])


#................................................. tính hiệu các chỉ số
d_ndvi = ndvi_5_8 - ndvi_9_12
# d_ndwi = ndwi_5_8 - ndwi_9_12

#.................................................. xuất dữ liệu
array2raster('Tif/chưa chuyển hóa/d_ndvi.tif',dataset,d_ndvi)
# array2raster('Tif/chưa chuyển hóa/d_ndwi.tif',dataset,d_ndwi)

# 0. ultra_blue (coastal aerosol),
# 1. blue,
# 2. green,
# 3. red,
# 4. nir,
# 5. swir1, (nswir1)
# 6. swir2,
# 7. ndwi,
# 8. ndvi,
# 9. d-ndvi
# 10. vwmi
# 11. bism

