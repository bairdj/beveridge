import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
from sklearn.ensemble import RandomForestClassifier
from beveridge.models import ModelStorage
import pickle

parser = argparse.ArgumentParser(description="Create model from CSV stats data.")
parser.add_argument('file')
parser.add_argument('outfile')
args = parser.parse_args()

#Create DataFrame in Pandas
data = pd.read_csv(args.file)
#Drop team
del data['team']
#Cleanse to numeric data
data = data.apply(lambda x: pd.to_numeric(x, errors='coerce'))
#Delete any completely empty columns
data = data.dropna(axis=1, how='all')
#Delete any rows with empty values
data = data.dropna(axis=0, how='any')
#Set up some columns
data['home'] = data['home'].astype('bool')
data['win'] = data['win'].astype('bool')
#Build relative columns
data['relRebounds'] = data['rebounds'] / data['oppRebounds']
data['relDisposals'] = data['disposals'] / data['oppDisposals']
data['relKicks'] = data['kicks'] / data['oppKicks']
data['relHandballs'] = data['handballs'] / data['oppHandballs']
data['relClearances'] = data['clearances'] / data['oppClearances']
data['relHitouts'] = data['hitouts'] / data['oppHitouts']
data['relMarks'] = data['marks'] / data['oppMarks']
data['relInside50s'] = data['inside50s'] / data['oppInside50s']
data['relTackles'] = data['tackles'] / data['oppTackles']
data['relClangers'] = data['clangers'] / data['oppClangers']
data['relFrees'] = data['frees'] / data['oppFrees']
data['relContested'] = data['contested'] / data['oppContested']
data['relUncontested'] = data['uncontested'] / data['oppUncontested']
data['relContestedMarks'] = data['contestedMarks'] / data['oppContestedMarks']
data['relMarksIn50'] = data['marksIn50'] / data['oppMarksIn50']
data['relOnePercenters'] = data['onePercenters'] / data['oppOnePercenters']
data['relBounces'] = data['bounces'] / data['oppBounces']
#Try building a logistic regression model
print("Building initial logistic regression model.")
model = LogisticRegression()
#Only use the relative columns. I've tested with the absolute values and they are much less useful than relative.
trainColumns = pd.Series(['relRebounds', 'relDisposals', 'relKicks', 'relHandballs', 'relClearances', 'relHitouts', 'relMarks', 'relInside50s', 'relTackles', 'relClangers', 'relFrees', 'relContested', 'relUncontested', 'relContestedMarks', 'relMarksIn50', 'relOnePercenters', 'relBounces', 'home'])
model.fit(data[trainColumns], data['win'])
print("Training data accuracy: {:%}".format(model.score(data[trainColumns], data['win'])))
#Recursive feature selection with cross-validation
print("Running feature selection.")
fs = RFECV(model)
fs.fit(data[trainColumns], data['win'])
print("Accuracy after feature selection: {:%}".format(fs.score(data[trainColumns], data['win'])))
filteredColumns = trainColumns[fs.support_]
#Ignoring filtered columns for the random forest. Seems to produce better results
#Create a random forest model
print("Building random forest")
rf = RandomForestClassifier(n_estimators=100, min_samples_split=0.02, class_weight='balanced')
rf.fit(data[trainColumns], data['win'])
print("Random forest accuracy: {:%}".format(rf.score(data[trainColumns], data['win'])))
#Save random forest model to given filename
with open(args.outfile, 'wb') as file:
    storage = ModelStorage(trainColumns, rf)
    pickle.dump(storage, file)