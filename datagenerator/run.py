import configparser, pandas, os, msvcrt, csv
from orator import DatabaseManager
from termcolor import colored

os.chdir("C://github_repos/Twitter-Sentiment-Barometer/datagenerator")

class Datagenerator():
    def __init__(self):
        # read config file
        required_fields = {"database": ["host", "database", "user", "password", "idfield", "textfield"]}
        self.config = config = configparser.ConfigParser()
        config.read('../settings.ini')

        for key, values in required_fields.items():
            for value in values:
                if not config.has_option(key, value):
                    raise Exception("Missing '"+str(value)+"' in section '"+str(key)+"' in settings.ini")

    def loadData(self):

        # generate data holding files 
        d = pandas.DataFrame(columns=["id", "Sentiment", "Tweet"])
        if not os.path.exists("../tweets_pos.csv"):
            d.to_csv("../tweets_pos.csv", index=False)
        if not os.path.exists("../tweets_neu.csv"):
            d.to_csv("../tweets_neu.csv", index=False)
        if not os.path.exists("../tweets_neg.csv"):
            d.to_csv("../tweets_neg.csv", index=False)

        pos = pandas.read_csv("../tweets_pos.csv")
        neu = pandas.read_csv("../tweets_neu.csv")
        neg = pandas.read_csv("../tweets_neg.csv")

        tweets_categorized = pos["id"].to_list()+neu["id"].to_list()+neg["id"].to_list()

        tweets = self.getTweets()
        tweets = [{"id": id, "text": text} for id, text in tweets.items() if id not in tweets_categorized and text[0:3] != "RT "]
        tweets_pos = {"id": [], "Sentiment": [], "Tweet": []}
        tweets_neu = {"id": [], "Sentiment": [], "Tweet": []}
        tweets_neg = {"id": [], "Sentiment": [], "Tweet": []}

        i=0
        for tweet in tweets:
            print("###### Tweet No. "+str(i)+"/"+str(len(tweets))+" ######")
            print(tweet["text"])
            print(colored("0, e, s to exit", "white"))
            print(colored("1 for positive", "green"), colored("2 for neutral", "yellow"), colored("3 for negative", "red"))
            key = msvcrt.getch()
            if chr(ord(key)) == "1":
                print("----")
                print(colored("Positiv", 'green'))
                tweets_pos["id"].append(tweet["id"])
                tweets_pos["Sentiment"].append("positiv")
                tweets_pos["Tweet"].append(tweet["text"].replace('\n', ' ').replace('\r', '').replace('"', ""))
            elif chr(ord(key)) == "2":
                print("----")
                print(colored("Neutral", 'yellow'))
                tweets_neu["id"].append(tweet["id"])
                tweets_neu["Sentiment"].append("neutral")
                tweets_neu["Tweet"].append(tweet["text"].replace('\n', ' ').replace('\r', '').replace('"', ""))
            elif chr(ord(key)) == "3":
                print("----")
                print(colored("Negativ", 'red'))
                tweets_neg["id"].append(tweet["id"])
                tweets_neg["Sentiment"].append("negativ")
                tweets_neg["Tweet"].append(tweet["text"].replace('\n', ' ').replace('\r', '').replace('"', ""))
            elif chr(ord(key)) in ["0", "e", "s"]:
                break
            i+=1

            p = pandas.DataFrame.from_dict(tweets_pos)
            p.to_csv("../tweets_pos.csv", mode="a", index=False, header=False, quoting=csv.QUOTE_ALL)
            n = pandas.DataFrame.from_dict(tweets_neu)
            n.to_csv("../tweets_neu.csv", mode="a", index=False, header=False, quoting=csv.QUOTE_ALL)
            n = pandas.DataFrame.from_dict(tweets_neg)
            n.to_csv("../tweets_neg.csv", mode="a", index=False, header=False, quoting=csv.QUOTE_ALL)

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
        tweets = self.db.table(self.config['database']['table']).lists(self.config['database']['textfield'], self.config['database']['idfield'])
        return tweets


generator = Datagenerator()
generator.loadData()