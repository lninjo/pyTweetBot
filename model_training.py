#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# File : pyTweetBot.py
# Description : pyTweetBot main execution file.
# Auteur : Nils Schaetti <n.schaetti@gmail.com>
# Date : 01.05.2017 17:59:05
# Lieu : Nyon, Suisse
#
# This file is part of the pyTweetBot.
# The pyTweetBot is a set of free software:
# you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyTweetBot is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with pyTweetBar.  If not, see <http://www.gnu.org/licenses/>.
#

# Import
import logging
import os
import datetime
from learning.Model import Model
from learning.StatisticalModel import StatisticalModel
from learning.Statistical2GramModel import Statistical2GramModel
from learning.TFIDFModel import TFIDFModel
from learning.TextBlobModel import TextBlobModel
from bs4 import BeautifulSoup
import urllib
import pickle

####################################################
# Functions
####################################################

####################################################
# Main function
####################################################


# Train a classifier on a dataset
def model_training(data_set_file, model_file="", param='dp', model_type='stat'):
    """
    Train a classifier on a dataset.
    :param data_set_file: Path to the dataset file
    :param model_file: Path to model file if needed
    :param param: Model parameter (dp, ...)
    :param model_type: Model's type (stat, tfidf, stat2, textblob)
    """
    # Load model or create
    if os.path.exists(model_file):
        model = Model.load(model_file)
    else:
        if model_type == "stat":
            model = StatisticalModel("tweet_stat_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow(),
                                     smoothing=param, smoothing_param=0.5)
        elif model_type == "tfidf":
            model = TFIDFModel("tweet_tfidf_model", ['tweet', 'skip'], last_update=datetime.datetime.utcnow())
        elif model_type == "stat2":
            model = Statistical2GramModel("tweet_stat2_model", ['tweet', 'skip'],
                                          last_update=datetime.datetime.utcnow(), smoothing=param,
                                          smoothing_param=0.5)
        elif model_type == "NaiveBayes":
            model = TextBlobModel()
        # end if
    # end if

    # Load dataset
    if os.path.exists(data_set_file):
        with open(data_set_file, 'r') as f:
            dataset = pickle.load(f)
            n_samples = len(dataset[0].keys())
        # end with
    else:
        logging.error(u"Cannot find dataset file {}".format(data_set_file))
    # end if

    # Train or test
    count = 0.0
    success = 0.0
    false_positive = 0.0
    false_positive_urls = list()

    try:
        # For each text in the dataset
        for text in dataset:
            # Class
            c = dataset[0][url]

            # Predict
            if ".fr" in url or ".ch" in url:
                prediction, probs = model(text)
            else:
                prediction, probs = model(text)
            # end if

            # Same result
            if probs['tweet'] == probs['skip']:
                prediction = "skip"
            # end if

            # False positive
            if prediction == "tweet" and c == "skip":
                false_positive += 1.0
                false_positive_urls.append(url)
            # end if

            # Compare
            logger.info(u"Predicted {} for observation {}".format(prediction, c))
            if prediction == c:
                success += 1.0
            # end if
            count += 1.0
        # end for
    except (KeyboardInterrupt, SystemExit):
        pass
    # end try

    # Show performance
    logger.info(u"Success rate of {} on dataset, {} false positive".format(success / count * 100.0,
                                                                           false_positive / count * 100.0))

    # Show false positives
    logger.info(u"False positives")
    for url in false_positive_urls:
        print(url)
    # end for

# end if