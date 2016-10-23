# Beveridge

A collection of tools for scraping AFL statistics and using them to predict the result of AFL matches.

Named after premiership winning coach Luke Beveridge :trophy::red_circle::white_circle::large_blue_circle:.

## Setup
Clone this repository

`git clone https://github.com/bairdj/beveridge.git`

Beveridge includes a Docker image that has everything you need to get started.

Initial build

`docker build -t beveridge .`

Run it

`docker run -it --rm beveridge`

This will put you in a shell in the root directory

## Scrapy

The Scrapy spider scrapes team match statistics from [AFL Tables](http://afltables.com/afl/afl_index.html).
This is a fantastic resource and none of this would be possible without it.

Finals matches are not stored.

The below snippet will get team statistics for all games in the 2015 and 2016 seasons
and store in `stats.csv`.

```bash
cd src/scrapy/afltables/afltables
scrapy crawl -t csv -o stats.csv -a start_season=2015 -a end_season=2016 stats
```

## Machine learning
*This is very experimental and probably not very useful*

### Rationale
The basis of all the machine learning aspects is *relative* team statistics. The scraped data
includes a team's statistics and their opponent's statistics - these scripts then convert these to
relative numbers (i.e. Western Bulldogs had 210 kicks, Sydney had 201 so relative kicks is 1.04).
These relative numbers for all the features (stats) are then used to train the model against a 
win boolean variable.

### Creating model
You first need to train a model to use for your predictions. A logistic regression will be
created, but this currently isn't being used. A random forest classifier will also be created and persisted
to the location you specify.

You will need to pass in the stats CSV that you scraped earlier (or use the sample files). You also need to provide
a filename where the model will be stored.

```
python src/create_model.py stats.csv model
```
### Using the model

This script takes 4 arguments

1. Model file location
2. Stats file (this is used for looking up recent statistics, so should be from the current season ONLY)
3. Home team (see `common.py` for dict with team codes)
4. Away team

You can also optionally pass `--max_round` and `--min_round` options to restrict which
rounds the current statistics will be gathered from. I found a 4-5 week lead in to be most accurate.

```bash
python src/predict.py model stats.csv WB SY

WB: 64.108518%
SY: 71.933388%
```

The returned percentage is the probability of winning. This is usually > 1, so the model is
obviously flawed somewhere.

## Todo/plan
* Tidy up Scrapy to support options etc.
* Persist some default models
* Scripts to automate scraping and fitting models
* Scripts to automate feeding statistics (averages etc.) into models to get predictions