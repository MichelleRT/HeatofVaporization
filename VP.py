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

# Get the data from text files
datafile = open("Data/vapor_pressure.txt", "r") 
# Make a dictionary for the column names and data
cols, indexToName = getColumns(datafile) 
datafile.close() 

# print(cols['Vapor_Pressure'])  

label_names = ['#Name', 'PubChem', 'Vapor_Pressure'] 
labels = cols['#Name'], cols['PubChem'], cols['Vapor_Pressure'] 
# This is where the chemoinformatics comes in for features!!
# Chemoinformatics from the pubchem number is how we identify/describe the compound


# # Set random seed 
# np.random.seed(0) 

# # Split our data into test data (30%) and training data (70%)
# train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.3, random_state=42)

# clf = RandomForestClassifier(max_depth=2, random_state=0) 

# # Train the classifier
# model = clf.fit(train, train_labels)

# # Make predictions
