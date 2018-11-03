import tweepy
from textblob import TextBlob

def primary(input_hashtag,no_of_tweets):
    Consumer_Key = 'hqzcXRnqj5AoYr4MvTF9dbeYU' 
    Consumer_Secret = 'jlTXxVjt3Nc0tA9fDtkwpIwoFXjXzeF4AQtGEDgni8nCy2mNES' 
    Access_Token = '973076672231587840-Dh6SZrWFo0HcSAC82nNdXieL8ZKwF3R'
    Access_Token_Secret = 'pVaaWWUYZPrmOatlgAmnQTb26o1WXaQKHBJsOTZzZ94ax'

    auth = tweepy.OAuthHandler (Consumer_Key,Consumer_Secret)
    auth.set_access_token (Access_Token,Access_Token_Secret)
    connect = tweepy.API(auth)

    N = no_of_tweets                       #Number of Tweets
    Tweets = tweepy.Cursor(connect.search, q=input_hashtag).items(N)
    neg = 0.0
    pos = 0.0
    neg_count = 0
    neutral_count = 0
    pos_count = 0
    tweets_list = []
    for tweet in Tweets:
        blob = TextBlob(tweet.text)
        tweets_list.append(blob)

        if blob.sentiment.polarity < 0:         #Negative
            neg += blob.sentiment.polarity
            neg_count += 1
        elif blob.sentiment.polarity == 0:      #Neutral
            neutral_count += 1
        else:                                   #Positive
            pos += blob.sentiment.polarity
            pos_count += 1
    print (tweets_list)
    return [['Sentiment', 'no. of tweets'],['Positive',pos_count]
            ,['Neutral',neutral_count],['Negative',neg_count]]
