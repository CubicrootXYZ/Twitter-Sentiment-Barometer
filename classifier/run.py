import nltk.classify.util, pandas, os
from nltk.classify import NaiveBayesClassifier

os.chdir("C://github_repos/Twitter-Sentiment-Barometer/classifier")

class Classifier:
    def __init__(self, train_test_split):
        self.split = train_test_split
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
        probdist = self.classifier.prob_classify(self.extract_features(text.split()))
        pred_sentiment = probdist.max()
        print("Predicted sentiment: ", pred_sentiment)
        print("Probability: ", round(probdist.prob(pred_sentiment), 2))

    def mostImportant(self):
        print("Top ten most informative words: ")

        for item in self.classifier.most_informative_features()[:10]:
            print(item[0])


cl = Classifier(0.8)
cl.mostImportant()
cl.predict("Ihr seid scheiße, niemals wähle ich euch")