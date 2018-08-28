from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Split our data into test data (30%) and training data (70%)
train, test, train_labels, test_labels = train_test_split(features, labels, test_size=0.3, random_state=42)

