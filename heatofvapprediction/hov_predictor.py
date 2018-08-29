from subprocess import call
import os
import pickle
import pubchempy as pcp
import httplib
import urllib2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.model_selection import cross_val_score
import statistics
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_predict
from sklearn import metrics

PATH = os.path.dirname(os.path.abspath(__file__))


###INPUT TRAINING DATA 
# def getDataColumns(inputFile, delim="\t", header=True):
#     columns = {}
#     indexToCol = {}
#     for lineNum, line in enumerate(inputFile):
#         if lineNum == 0:
#             headings = line.split(delim)
#             i = 0
#             for heading in headings:
#                 heading = heading.strip()
#                 # See if there actually is a heading
#                 if header:
#                     columns[heading] = []
#                     indexToCol[i] = heading
#                 else:
#                     columns[i] = [heading]
#                     indexToCol[i] = i
#                 i += 1
#         else:
#             cells = line.split(delim)
#             i = 0
#             for cell in cells:
#                 cell = cell.strip()
#                 columns[indexToName[i]] += [cell]
#                 i += 1          
#     return columns, indexToCol

# # Get the data from Heat_of_Vaporization.txt
# datafile = open("Data/Heat_of_Vaporization.txt", "r") 
# cols1, indexToName1 = getColumns(datafile) 
# datafile.close() 

_training_data = 'Data/Heat_of_Vaporization.txt' 

def _parsePadel(compound, _padel_descriptor):
    '''process Padel output'''
    with open(_padel_descriptor, "r") as filebuffer:
        header = filebuffer.readline()
        keys = header.strip().split(',')
        for line in filebuffer:
            ld = []
            linelist = line.strip().split(',')
            for count, var in enumerate(linelist):
                if count != 0:
                    ld.append(var.replace('"', ''))
            compound.setdefault(linelist[0].replace('"', ''), {})
            compound[linelist[0].replace('"', '')]['padelhash'] = ld
    return compound

## GET TRAINING DATA FEATURES
get_sdf = True
predictor_dict = {}
try:
    os.mkdir(PATH+'/temp_training_cpd_sdf/')
except OSError:
    pass
with open(_training_data) as fin:
    header = fin.readline().strip()
    for line in fin:
        line = line.strip()
        larray = line.split('\t')
        # print (line)
        if get_sdf:
            try:
                # pcp.download('SDF', PATH+'/temp_training_cpd_sdf/{}.sdf'.format(larray[1]), larray[1], overwrite=True)
                predictor_dict.setdefault(larray[1], float(larray[2]))
            except (pcp.PubChemHTTPError, httplib.BadStatusLine, urllib2.URLError):
                print line + ' passed'
                pass
median_value_training = statistics.median(predictor_dict.values())



# call(["java", "-jar", "PaDEL-Descriptor.jar", "-threads", "-1",
#         "-dir", PATH+'/temp_training_cpd_sdf/', "-file", 'padel_descriptor_training.out', "-fingerprints",
#         "-retainorder", "-usefilenameasmolname", "-descriptortypes","./descriptors.xml"])
training_compounds = _parsePadel({}, 'temp.out')
# print training_compounds

clf = RandomForestClassifier()
x = []
y = []

for key, value_dict in training_compounds.iteritems():
    try:
      predictor_value = predictor_dict[key]
      x.append(value_dict['padelhash'])
      if predictor_value >= median_value_training:
          y.append(1)
      else:
          y.append(0)
    except:
      pass
clf.fit(x,y)
print (clf.score(x,y))
#1.0

z = []
# for key, value_dict in testing_compounds.iteritems():
#     z.append(value_dict['padelhash'])

# X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

# clf.fit(X_train, y_train)
# mean_accuracy_score = clf.score(X_test, y_test)

# cv = ShuffleSplit(n_splits=10, test_size=0.3, random_state=0)
cv_scores=cross_val_predict(clf, x, y, cv=10)
print (metrics.accuracy_score(y, cv_scores))
print (metrics.average_precision_score(y, cv_scores))
print (cv_scores)

# 0.679487179487 accuracy cv 
# 0.64801061008 precision cv

