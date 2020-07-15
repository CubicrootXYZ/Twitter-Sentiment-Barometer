# Twitter-Sentiment-Barometer
Recognizing the mood of a tweet by machine learning approaches

Sadly, I am not allowed to share any tweet collections due to the regularizations made by Twitter. The Datagenerator might help you with generating some training data. The classifier requires a `tweets_pos.csv` and a `tweets_neg.csv` with the columns `id` and `Tweet`.

# Modules

## Datagenerator

A tool to collect tweets from a database and then sort them into positiv, neutral, negative and saving them to CSV files. 

! The command line input via `msvcrt.getch` might only work on Windows machines. !

## Calssifier

A Naive Bayes Text Classifier. 
