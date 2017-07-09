import tweepy
import config
#yo this is secret
consumer_key=config.ConfigVars['cKey']
consumer_secret=config.ConfigVars['cSecret']
access_token=config.ConfigVars['aTok']
access_token_secret=config.ConfigVars['aTokSecret']

def GetTweets(fromU, output):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)
    #WHO AM I
    iamme = api.me()

    test_scnm=output
    print('writing txt file for this user:', fromU)

    #now i wanna see other people. but show me only 5 please
    user1_public_tweets=api.user_timeline(screen_name=fromU,count=config.ConfigVars['TweetCount'])

    with open(output, 'w') as f:
    	for tweet in user1_public_tweets:
    		if 'http' not in tweet.text:
    			f.write(tweet.text)
    			f.write('\n')
