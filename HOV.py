from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Disclaimer: The function below is taken from the website
# http://code.activestate.com/recipes/577444-get-columns-of-data-from-text-files/
def getColumns(inFile, delim="\t", header=True):
    """
    Get columns of data from inFile. The order of the rows is respected
    
    :param inFile: column file separated by delim
    :param header: if True the first line will be considered a header line
    :returns: a tuple of 2 dicts (cols, indexToName). cols dict has keys that 
    are headings in the inFile, and values are a list of all the entries in that
    column. indexToName dict maps column index to names that are used as keys in 
    the cols dict. The names are the same as the headings used in inFile. If
    header is False, then column indices (starting from 0) are used for the 
    heading names (i.e. the keys in the cols dict)
    """
    cols = {}
    indexToName = {}
    for lineNum, line in enumerate(inFile):
        if lineNum == 0:
            headings = line.split(delim)
            i = 0
            for heading in headings:
                heading = heading.strip()
                if header:
                    cols[heading] = []
                    indexToName[i] = heading
                else:
                    # in this case the heading is actually just a cell
                    cols[i] = [heading]
                    indexToName[i] = i
                i += 1
        else:
            cells = line.split(delim)
            i = 0
            for cell in cells:
                cell = cell.strip()
                cols[indexToName[i]] += [cell]
                i += 1
                
    return cols, indexToName


"Get data from files and make dictionaries/list"

# Get the data from Heat_of_Vaporization.txt
datafile = open("Data/Heat_of_Vaporization.txt", "r") 
cols1, indexToName1 = getColumns(datafile) 
datafile.close() 

# Get features from Features.txt (chemoinformatics)
featfile = open("Data/Features.txt", "r")
flist = [] 
for line in featfile:
    newline = line.strip() 
    flist.append(newline) 
featfile.close()


"Assign the data"

label_names = ['#Name', 'PubChem', 'Heat_of_Vaporization'] 
labels = cols1['#Name'], cols1['PubChem'], cols1['Heat_of_Vaporization'] 
feature_names = flist
# We need to pull in the feature values of the compounds using their PubChem IDs



"Organize data into training and test sets"

# Set random seed 
np.random.seed(0) 

# Split our data into test data (30%) and training data (70%)
train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.3, random_state=42)

clf = RandomForestClassifier(max_depth=2, random_state=0) 

# Train the classifier
model = clf.fit(train, train_labels)

# Make predictions
