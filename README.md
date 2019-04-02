# Stanford University CS 230 Final Project 
Title: Headline Generator

Authors: David Liedtka and Dane Hankamer 

Generates reasonable headlines based on the words in an article using Recurrent Neural Networks (RNNs). Original code forked from https://github.com/udibr/headlines.

Based on Generating News Headlines with Recurrent Neural Networks by Konstantin Lopyrev, available at https://arxiv.org/pdf/1512.01712.pdf.

The dataset we used is available at https://components.one/datasets/#all-the-news. Run generate_pkl.py, which will output data.py.

The notebooks we run are labeled vocabulary-embedding.ipynb, train.ipynb, predict.ipynb, and test.ipynb. Using data.pkl, vocabulary-embedding.ipynb will generate embedding files. Train.ipynb will train for 500 iterations (with each iteration taking approximately 50 minutes on AWS p2.8xlarge instance) and will generate .hdf5 weight files. Predict.ipynb will make predictions on single manually entered inputs, and it also has the framework for generating heat maps. Finally, test.ipynb will output BLEU and Levenshtein scores for a testing set. This testing set will be from the training set if TESTTRAIN is set to True, from the test set if TESTING is set to True, and from the validation set otherwise. You can toggle the input type between first 50 words, first 25 and last 25 words, first 50 words and last 25 words, etc., by changing the value of MODE (explained in the notebook).

We found that running these notebooks is frequently subject to a lost connection, so we recommend converting them to traditional Python scripts and if running on another server, configuring SSH to keep the server alive.

Our final paper and poster are found under the deliverables/ folder.

NOTE:
- All .pkl files (data.pkl, vocabulary-embedding.pkl, vocabulary-embedding-data.pkl), our trained weights file (train.hdf5), and our dataset were too large for a GitHub upload
