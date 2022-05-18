import numpy as np
import datetime as dt
import re
from wordcloud import WordCloud, STOPWORDS
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk
from get_eps_data import *
from os.path import exists


# Use download if dictionary of words needs updating
nltk.download('vader_lexicon')

def get_sentiment(tickers):
    sentiment = []
    for ticker in tqdm(tickers):
        #Get user input
        query = ticker
        #As long as the query is valid (not empty or equal to '#')...
        if query != '':
            noOfTweet = '100'
            if noOfTweet != '' :
                noOfDays = '2'
                if noOfDays != '':
                        #Creating list to append tweet data
                        tweets_list = []
                        now = dt.date.today()
                        now = now.strftime('%Y-%m-%d')
                        yesterday = dt.date.today() - dt.timedelta(days = int(noOfDays))
                        yesterday = yesterday.strftime('%Y-%m-%d')
                        for i,tweet in enumerate(sntwitter.TwitterSearchScraper(query + ' lang:en since:' +  yesterday + ' until:' + now + ' -filter:links -filter:replies').get_items()):
                            if i > int(noOfTweet):
                                break
                            tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.username])

                        #Creating a dataframe from the tweets list above 
                        df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet Id', 'Text', 'Username'])

                        # print(df)


        # Create a function to clean the tweets
        def cleanTxt(text):
            text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
            text = re.sub('#', '', text) # Removing '#' hash tag
            text = re.sub('RT[\s]+', '', text) # Removing RT
            text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
            return text

        #applying this function to Text column of our dataframe
        df["Text"] = df["Text"].apply(cleanTxt)


        #Sentiment Analysis
        def percentage(part,whole):
            try:
                return 100 * float(part)/float(whole)
            except ZeroDivisionError:
                return 0

        #Assigning Initial Values
        positive = 0
        negative = 0
        neutral = 0
        #Creating empty lists
        tweet_list1 = []
        neutral_list = []
        negative_list = []
        positive_list = []

        #Iterating over the tweets in the dataframe
        for tweet in df['Text']:
            tweet_list1.append(tweet)
            analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
            neg = analyzer['neg']
            neu = analyzer['neu']
            pos = analyzer['pos']
            comp = analyzer['compound']

            if neg > pos:
                negative_list.append(tweet) #appending the tweet that satisfies this condition
                negative += 1 #increasing the count by 1
            elif pos > neg:
                positive_list.append(tweet) #appending the tweet that satisfies this condition
                positive += 1 #increasing the count by 1
            elif pos == neg:
                neutral_list.append(tweet) #appending the tweet that satisfies this condition
                neutral += 1 #increasing the count by 1 

        positive = percentage(positive, len(df)) #percentage is the function defined above
        negative = percentage(negative, len(df))
        neutral = percentage(neutral, len(df))


        #Converting lists to pandas dataframe
        tweet_list1 = pd.DataFrame(tweet_list1)
        neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
        #using len(length) function for counting
        # print("Since " + noOfDays + " days, there have been", len(tweet_list1) ,  "tweets on " + query, end='\n*')
        # print("Positive Sentiment:", '%.2f' % len(positive_list), end='\n*')
        # print("Neutral Sentiment:", '%.2f' % len(neutral_list), end='\n*')
        # print("Negative Sentiment:", '%.2f' % len(negative_list), end='\n*')


        if len(positive_list) == len(negative_list):
            sentiment.append(0)
        else:
            sentiment.append((len(positive_list)-len(negative_list)))

    sentiment_db = pd.DataFrame(columns=tickers)
    a_series = pd.Series(sentiment, index=sentiment_db.columns)
    sentiment_db = sentiment_db.append(a_series, ignore_index=True)
    today = pd.to_datetime('today').normalize()
    sentiment_db.insert(0,'Date', today)

    # If db doesn't exsist, create one. If it does exist, then update
    file_exists = exists('Data/sentiment.xlsx')
    if file_exists:
        df2 = pd.read_excel('Data/sentiment.xlsx')
        result = pd.concat([sentiment_db, df2], ignore_index=True, sort=False)
        result.to_excel('Data/sentiment-update.xlsx', index=False)
        df3 = pd.read_excel('Data/sentiment-update.xlsx')
        df3.to_excel('Data/sentiment.xlsx', index=False)
    else:
        sentiment_db.to_excel('Data/sentiment.xlsx', index=False)


# Get Last Date in DB and Get Today's Date
try:
    df = pd.read_excel('Data/sentiment.xlsx')
    sentiment_db_last_date = df['Date'][0]
except:
    sentiment_db_last_date = 0