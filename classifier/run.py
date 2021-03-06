import nltk.classify.util, pandas, os, configparser, collections, re
from nltk.classify import NaiveBayesClassifier
from orator import DatabaseManager

os.chdir("C://github_repos/Twitter-Sentiment-Barometer/classifier")

class Classifier:
    def __init__(self, train_test_split):
        self.split = train_test_split
        # read config file
        required_fields = {"database": ["host", "database", "user", "password", "idfield", "textfield"]}
        self.config = config = configparser.ConfigParser()
        config.read('../settings_private.ini')

        for key, values in required_fields.items():
            for value in values:
                if not config.has_option(key, value):
                    raise Exception("Missing '"+str(value)+"' in section '"+str(key)+"' in settings.ini")

    def train(self):
        self.pos = pandas.read_csv("../tweets_pos.csv")
        self.pos = self.pos["Tweet"].to_list()
        self.pos = list(set(self.pos))
        self.neg = pandas.read_csv("../tweets_neg.csv")
        self.neg = self.neg["Tweet"].to_list()
        self.neg = list(set(self.neg))


        X_train, X_test = self.buildFeatures()

        self.classifier = NaiveBayesClassifier.train(X_train)
        print("Accuracy of the classifier: ", nltk.classify.util.accuracy(self.classifier, X_test))

    def extract_features(self, word_list):
        return dict([(word, True) for word in word_list])

    def buildFeatures(self):
        pos_th = int(self.split*len(self.pos))
        neg_th = int(self.split*len(self.pos))

        feat_pos = [(self.extract_features(t.split()), 'Positive') for t in self.pos]
        feat_neg = [(self.extract_features(t.split()), 'Negative') for t in self.neg]

        return feat_pos[0:pos_th]+feat_neg[0:neg_th], feat_pos[pos_th:]+feat_neg[neg_th:]

    def predict(self, text):
        print("PREDICT: ", text)
        probdist = self.classifier.prob_classify(self.extract_features(str(text).split()))
        pred_sentiment = probdist.max()
        print("Predicted sentiment: ", pred_sentiment)
        print("Probability: ", round(probdist.prob(pred_sentiment), 2))
        return pred_sentiment, round(probdist.prob(pred_sentiment), 2)

    def mostImportant(self):
        print("Top ten most informative words: ")

        for item in self.classifier.most_informative_features()[:10]:
            print(item[0])

    def save(self, filename):
        import pickle
        f = open(filename, 'wb')
        pickle.dump(self.classifier, f)
        f.close()

    def load(self, filename):
        import pickle
        f = open(filename, 'rb')
        self.classifier = pickle.load(f)
        f.close()

    # read tweets from a database
    def getTweets(self):
        config = {
            'mysql': {
                'driver': 'mysql',
                'host': self.config['database']['host'],
                'database': self.config['database']['database'],
                'user': self.config['database']['user'],
                'password': self.config['database']['password'],
                'prefix': ''
            }
        }

        self.db = DatabaseManager(config)
        tweets = self.db.table(self.config['database']['table']).where(self.config['database']['retweetfield'], '=', '0').lists(self.config['database']['textfield'])
        return tweets

    def predictFromDb(self):
        tweets = self.getTweets()
        tweets = [re.sub('<[^<]+?>', '', text) for text in tweets if text[0:3] != "RT "]
        preds = []

        for tweet in tweets:
            pred, acc = self.predict(tweet.replace('\n', ' ').replace('\r', '').replace('"', ""))
            if float(acc) < 0.65:
                preds.append("Unsure")
                print("Unsure: ", acc)
            else:
                preds.append(pred)

        return preds


cl = Classifier(0.8)
#cl.mostImportant()
cl.load("test.pickle")
#cl.predict("")
#cl.save("test.pickle")
preds = cl.predictFromDb()

cnt = collections.Counter(preds)

for item, count in cnt.items():
    print(item)
    print(count)
