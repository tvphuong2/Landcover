import numpy as np
import csv
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV 
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
import seaborn as sn
import pandas as pd
import matplotlib.cm as cm

def csv2array(path):
    res = []
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader,None)
        for row in reader:
            r = np.array(row[2:10], dtype=float)

            # r = np.append(r, (r[4] - r[3]) / (r[4] + r[3]))
            # r = np.append(r, (r[2] - r[4]) / (r[2] + r[4]))
            res.append(r)
    res = np.array(res)
    return res

def showMatrix(matrix):
    df_cm = pd.DataFrame(matrix, index=["grassland","cropland","aquaculture","rice_paddies","forest","scrub","open_water","wetland","barrenland","residential"], 
                                columns=["grassland","cropland","aquaculture","rice_paddies","forest","scrub","open_water","wetland","barrenland","residential"])
    sn.set(font_scale=2) # for label size
    sn.heatmap(df_cm, annot=True, annot_kws={"size": 16}, cmap= cm.binary) # font size
    plt.show()

def train(arrays):
    train = np.concatenate(arrays, axis=0)
    lable  = []
    for i in range(len(arrays)):
      for j in arrays[i]:
        lable.append(i)
    lable = np.array(lable)
    print(lable.shape, train.shape)

    # clf = SVC(kernel='poly', gamma=4, coef0 = 0)
    # clf.fit(train_, train_lb)

    # print(clf.score(test_, test_lb))
    # tg = np.split(test_,len(test_)/SIZE)
    # tg_lable = np.split(test_lb,len(test_)/SIZE)
    # for i in range(len(tg)):
    #   print(i, clf.score(tg[i], tg_lable[i]))

    param_grid = {'C': [100],  
              'gamma': [10], 
              'kernel': ['poly']}  
  
    grid = GridSearchCV(SVC(), param_grid, refit = True, verbose = 3) 
    grid.fit(train, lable)

    print(classification_report(lable,grid.best_estimator_.predict(train)))
    print(grid.best_params_)
    print(grid.best_estimator_) 
    print (confusion_matrix(lable,grid.best_estimator_.predict(train)))
    showMatrix(confusion_matrix(lable,grid.best_estimator_.predict(train)))

grassland = csv2array('grassland.csv')
cropland = csv2array('croplands2.csv')
aquaculture = csv2array('aquaculture.csv')
rice_paddies = csv2array('rice_paddies.csv')
forest = csv2array('forest_points.csv')
scrub = csv2array('scrub_shrub.csv')
open_water = csv2array('water2.csv')
wetland = csv2array('wetlands.csv')
barrenland = csv2array('barren_land.csv')
residential = csv2array('residential.csv')
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
