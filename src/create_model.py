import argparse
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import RFECV
import pickle

parser = argparse.ArgumentParser(description="Create model from CSV stats data.")
parser.add_argument('file')
args = parser.parse_args()

#Create DataFrame in Pandas
data = pd.read_csv(args.file)
#Delete any completely empty columns
data = data.dropna(axis=1, how='all')
#Delete any rows with empty values
data = data.dropna(axis=0, how='any')
#Set up some columns
data['home'] = data['home'].astype('bool')
data['team'] = data['team'].astype('category')
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
#Try building a logistic regression model
print("Building initial logistic regression model.")
model = LogisticRegression()
#Only use the relative columns. I've tested with the absolute values and they are much less useful than relative.
trainColumns = ['relRebounds', 'relDisposals', 'relKicks', 'relHandballs', 'relClearances', 'relHitouts', 'relMarks', 'relInside50s', 'relTackles', 'relClangers', 'home']
model.fit(data[trainColumns], data['win'])
print("Training data accuracy: {:%}".format(model.score(data[trainColumns], data['win'])))
#Recursive feature selection with cross-validation
print("Running feature selection.")
fs = RFECV(model)
fs.fit(data[trainColumns], data['win'])
print("Accuracy after feature selection: {:%}".format(fs.score(data[trainColumns], data['win'])))
#TODO Save the model