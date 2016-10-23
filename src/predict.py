import argparse
import pickle
import pandas as pd

teamColumns = ['rebounds', 'disposals', 'kicks', 'handballs', 'clearances', 'hitouts', 'marks', 'inside50s', 'tackles', 'clangers', 'frees', 'contested', 'uncontested', 'contestedMarks', 'marksIn50', 'onePercenters', 'bounces']

def get_team_probability(modelStorage, data_frame, home_team, away_team):
    home = data_frame[data_frame['team'] == home_team][teamColumns].mean()
    away = data_frame[data_frame['team'] == away_team][teamColumns].mean()
    home['relRebounds'] = home['rebounds'] / away['rebounds']
    home['relDisposals'] = home['disposals'] / away['disposals']
    home['relKicks'] = home['kicks'] / away['kicks']
    home['relHandballs'] = home['handballs'] / away['handballs']
    home['relClearances'] = home['clearances'] / away['clearances']
    home['relHitouts'] = home['hitouts'] / away['hitouts']
    home['relMarks'] = home['marks'] / away['marks']
    home['relInside50s'] = home['inside50s'] / away['inside50s']
    home['relTackles'] = home['tackles'] / away['tackles']
    home['relClangers'] = home['clangers'] / away['clangers']
    home['relFrees'] = home['frees'] / away['frees']
    home['relContested'] = home['contested'] / away['contested']
    home['relUncontested'] = home['uncontested'] / away['uncontested']
    home['relContestedMarks'] = home['contestedMarks'] / away['contestedMarks']
    home['relMarksIn50'] = home['marksIn50'] / away['marksIn50']
    home['relOnePercenters'] = home['onePercenters'] / away['onePercenters']
    home['relBounces'] = home['bounces'] / away['bounces']
    home['home'] = 1
    return modelStorage.randomForest.predict_proba([home[modelStorage.columns]])[0][1]


parser = argparse.ArgumentParser(description="Predict match result given a model and historical data for teams")
parser.add_argument("model")
parser.add_argument("stats")
parser.add_argument("home")
parser.add_argument("away")
parser.add_argument('--min_round', type=int)
parser.add_argument('--max_round', type=int)
args = parser.parse_args()

with open(args.model, 'rb') as file:
    modelStorage = pickle.load(file)
    randomForest = modelStorage.randomForest
    #Load stats
    data = pd.read_csv(args.stats)
    data[teamColumns] = data[teamColumns].apply(lambda x: pd.to_numeric(x, errors='coerce'))
    if args.max_round is not None:
        print(data['round'])
        data = data[data['round'] <= args.max_round]
    if args.min_round is not None:
        data = data[data['round'] >= args.min_round]

    homeProbability = get_team_probability(modelStorage, data, args.home, args.away)
    awayProbability = get_team_probability(modelStorage, data, args.away, args.home)
    print("{}: {:%}".format(args.home, homeProbability))
    print("{}: {:%}".format(args.away, awayProbability))
    #TODO add options to filter by round/date
    #Clean up data