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
PATH = os.path.dirname(os.path.abspath(__file__))


###INPUT TRAINING DATA 
_training_data = ''

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

### GET TRAINING DATA FEATURES
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
        if get_sdf:
            try:
                pcp.download('SDF', PATH+'/temp_training_cpd_sdf/{}.sdf'.format(larray[1]), larray[1], overwrite=True)
                predictor_dict.setdefault(larray[1], larray[2])
            except (pcp.PubChemHTTPError, httplib.BadStatusLine, urllib2.URLError):
                print line + ' passed'
                pass
median_value_training = statistics.median(predictor_dict.values())



call(["java", "-jar", "./Chemoinformatics/PaDEL-Descriptor.jar", "-threads", "-1",
        "-dir",PATH+'/temp_training_cpd_sdf/', "-file", './padel_descriptor_training.out', "-chemoinformatics",
        "-retainorder", "-usefilenameasmolname", "-descriptortypes","./descriptors.xml"])
training_compounds = _parsePadel({}, './padel_descriptor_training.out')


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
z = []
for key, value_dict in testing_compounds.iteritems():
    z.append(value_dict['padelhash'])

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.4, random_state=0)

# clf.fit(X_train, y_train)
# mean_accuracy_score = clf.score(X_test, y_test)
v  = clf.predict(z)
prob = clf.predict_proba(z)
