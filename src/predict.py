import argparse
import pickle
import pandas as pd

parser = argparse.ArgumentParser(description="Predict match result given a model and historical data for teams")
parser.add_argument("model")
parser.add_argument("stats")
parser.add_argument("home")
parser.add_argument("away")
parser.add_argument('--min_round', type=int)
parser.add_argument('--max_round', type=int)
args = parser.parse_args()

teamColumns = ['rebounds', 'disposals', 'kicks', 'handballs', 'clearances', 'hitouts', 'marks', 'inside50s', 'tackles', 'clangers', 'frees', 'contested', 'uncontested', 'contestedMarks', 'marksIn50', 'onePercenters', 'bounces']

with open(args.model, 'rb') as file:
    modelStorage = pickle.load(file)
    randomForest = modelStorage.randomForest
    #logRegression = modelStorage.logRegression
    #Load stats
    data = pd.read_csv(args.stats)
    data[teamColumns] = data[teamColumns].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    if args.max_round is not None:
        print(data['round'])
        data = data[data['round'] <= args.max_round]
    if args.min_round is not None:
        data = data[data['round'] >= args.min_round]
    homeStats = data[data['team'] == args.home][teamColumns].mean()
    awayStats = data[data['team'] == args.away][teamColumns].mean()
    #TODO add options to filter by round/date
    #Clean up data

    homeStats['relRebounds'] = homeStats['rebounds'] / awayStats['rebounds']
    homeStats['relDisposals'] = homeStats['disposals'] / awayStats['disposals']
    homeStats['relKicks'] = homeStats['kicks'] / awayStats['kicks']
    homeStats['relHandballs'] = homeStats['handballs'] / awayStats['handballs']
    homeStats['relClearances'] = homeStats['clearances'] / awayStats['clearances']
    homeStats['relHitouts'] = homeStats['hitouts'] / awayStats['hitouts']
    homeStats['relMarks'] = homeStats['marks'] / awayStats['marks']
    homeStats['relInside50s'] = homeStats['inside50s'] / awayStats['inside50s']
    homeStats['relTackles'] = homeStats['tackles'] / awayStats['tackles']
    homeStats['relClangers'] = homeStats['clangers'] / awayStats['clangers']
    homeStats['relFrees'] = homeStats['frees'] / awayStats['frees']
    homeStats['relContested'] = homeStats['contested'] / awayStats['contested']
    homeStats['relUncontested'] = homeStats['uncontested'] / awayStats['uncontested']
    homeStats['relContestedMarks'] = homeStats['contestedMarks'] / awayStats['contestedMarks']
    homeStats['relMarksIn50'] = homeStats['marksIn50'] / awayStats['marksIn50']
    homeStats['relOnePercenters'] = homeStats['onePercenters'] / awayStats['onePercenters']
    homeStats['relBounces'] = homeStats['bounces'] / awayStats['bounces']
    homeStats['home'] = 1
    print(homeStats[modelStorage.columns])
    print(randomForest.predict_proba([homeStats[modelStorage.columns]]))
    #print(logRegression.predict_proba([homeStats[modelStorage.columns]]))
    print(randomForest.predict([homeStats[modelStorage.columns]]))