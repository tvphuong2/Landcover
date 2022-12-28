import numpy as np
from numpy import exp
import csv
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import GridSearchCV 

BANDS = 13

def csv2array(path):
  res = []
  for i in range(BANDS):
    res.append([])
  with open(path) as csvfile:
    reader = csv.reader(csvfile)
    next(reader,None)
    for row in reader:
      for i in range(12):
        res[i].append(float(row[i]))
      
      vwmi = float(row[10])*2.5 - 9*float(row[7]) + 2
      res[12].append(vwmi)

    #   bism = float(row[2])*6 - 5*float(row[4]) + 0.12
    #   res[13].append(bism)
  res = np.array(res)
  # res[7] = (res[7] - 0.016)/(0.38 - 0.016)
  # print(np.min(res[7]), np.max(res[7]) , res[7].shape)
  return res

def train(arrays):
    for i in range(len(arrays)):
        for j in range(len(arrays[i])):
            for k in range(len(arrays[i][j])):
                if np.isnan(arrays[i][j][k]):
                    arrays[i][j][k] = 0


    SIZE = 15
    train_ = arrays[0][:-SIZE]
    test_ = arrays[0][-SIZE:]
    train_lb = [0] * len(arrays[0][:-SIZE])
    test_lb = [0] * len(arrays[0][-SIZE:])
    for a in range(1,len(arrays)):
        train_ = np.append(train_, arrays[a][:-SIZE], axis= 0)
        test_ = np.append(test_, arrays[a][-SIZE:], axis = 0)
        for i in range(len(arrays[a][:-SIZE])):
            train_lb.append(a)
        for i in range(len(arrays[a][-SIZE:])):
            test_lb.append(a)

    train_lb = np.array(train_lb)
    test_lb = np.array(test_lb)
    print(train_.shape, train_lb.shape)
    print(test_.shape, test_lb.shape)

    # clf = SVC(kernel='poly', gamma=4, coef0 = 0)
    # clf.fit(train_, train_lb)

    # print(clf.score(test_, test_lb))
    # tg = np.split(test_,len(test_)/SIZE)
    # tg_lable = np.split(test_lb,len(test_)/SIZE)
    # for i in range(len(tg)):
    #   print(i, clf.score(tg[i], tg_lable[i]))

    param_grid = {'C': [0.1, 1, 10, 100, 1000],  
              'gamma': [1, 0.1, 0.01, 0.001, 0.0001], 
              'kernel': ['rbf']}  
  
    grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 
    grid.fit(train_, train_lb)
    print(grid.best_params_)
    print(grid.best_estimator_) 

grassland = csv2array('Grassland.csv')[2:].T
cropland = csv2array('Croplands.csv')[2:].T
aquaculture = csv2array('Aquaculture.csv')[2:].T
rice_paddies = csv2array('Rice_paddies.csv')[2:].T
forest = csv2array('Forest.csv')[2:].T
scrub = csv2array('Scrub_shrub.csv')[2:].T
open_water = csv2array('Open_water.csv')[2:].T
wetland = csv2array('wetlands.csv')[2:].T
barrenland = csv2array('BarrenLand.csv')[2:].T
residential = csv2array('Residential-land.csv')[2:].T
#(len,12)
#         1          2           3           4             5     6       7          8          9          10
train([grassland, cropland, aquaculture, rice_paddies, forest, scrub, open_water, wetland, barrenland,residential])

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
