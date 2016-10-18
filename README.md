# Beveridge

A collection of tools for scraping AFL statistics and using them to predict the result of AFL matches.

Named after premiership winning coach Luke Beveridge.

## Setup
Clone this repository

`git clone https://github.com/bairdj/beveridge.git`

Beveridge includes a Docker image that has everything you need to get started.

Initial build

`docker build -t beveridge .`

Run it

`docker run -it --rm beveridge`

This will put you in a shell in the src directory

## Scrapy
WIP

## Todo/plan
* Tidy up Scrapy to support options etc.
* Persist some default models
* Scripts to automate scraping and fitting models
* Scripts to automate feeding statistics (averages etc.) into models to get predictions