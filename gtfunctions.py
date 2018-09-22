import tweepy
import json
import sys
import copy
import glob
import os


#Twitter API credentials




def get_last_downloaded(screen_name):
    newest = 0
    files = glob.glob(screen_name + '/*.json')
    #print(screen_name, files)
    if len(files) > 0:
        newest = max(files, key=os.path.getctime)
        with open(newest, 'r') as f:
            olddata = json.load(f)
            newest = int(olddata[0]['id_str'])
    return newest

def get_all_tweets(screen_name,  consumer_key, consumer_secret, access_key, access_secret, newest=0):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    print('User: {}, \tlast tweet ID: {}'.format(screen_name, newest))

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(
                                   screen_name = screen_name,
                                   count=199,
                                   tweet_mode='extended'
                                  )





    # save most recent tweets
    alltweets.extend(new_tweets)

    '''
    overlap_abort = False
    print_flag = True
    for i in range(len(alltweets), 0, -1):
        print(type(alltweets), len(alltweets), i)

        if int(alltweets[i]._json['id_str']) <= newest:
            if print_flag == True:
                print('Previous old tweet {} ID threshold surpassed.'.format(alltweets[i]._json['id_str']))
                print_flag = False

            del alltweets[i]
            overlap_abort = True
    '''


    # save the id of the oldest tweet less one
    batch_oldest = alltweets[-1].id - 1
    overlap_abort = False
    if int(batch_oldest) <= newest:
        overlap_abort = True

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0 and overlap_abort == False:

        #all subsiquent requests use the max_id param to prevent duplicates
        new_tweets = api.user_timeline(screen_name = screen_name,
                                       count=199,
                                       max_id=batch_oldest,
                                       tweet_mode='extended')

        #save most recent tweets
        alltweets.extend(new_tweets)


        '''
        print_flag = True
        for i in range(len(new_tweets), 0, -1):
            if int(alltweets[i]._json['id_str']) <= newest:
                if print_flag == True:
                    print('Previous old tweet {} ID threshold surpassed.'.format(alltweets[i]._json['id_str']))
                    print_flag = False

                del alltweets[i]
                overlap_abort = True
        '''


        #update the id of the oldest tweet less one
        batch_oldest = alltweets[-1].id - 1

        if int(batch_oldest) <= newest:
            overlap_abort = True

    # print total tweets fetched from given screen name
    print("Total tweets downloaded from %s are %s" % (screen_name,len(alltweets)))

    return alltweets

def fetch_tweets(screen_names):

    # initialize the list to hold all tweets from all users
    alltweets=[]

    # get all tweets for each screen name
    for  screen_name in screen_names:
        alltweets.extend(get_all_tweets(screen_name, consumer_key, consumer_secret, access_key, access_secret))

    return alltweets

def store_tweets(alltweets,file='tweets.json'):

    # a list of all formatted tweets
    tweet_list=[]

    for tweet in alltweets:

        # a dict to contain information about single tweet
        tweet_information=dict()

        # text of tweet
        tweet_information['full_text']= tweet._json['full_text'] #tweet.full_text.encode("utf-8") #tweet.text.encode('utf-8')

        # date and time at which tweet was created
        #str(alltweets[0].created_at.strftime("%Y-%m-%d %H:%M:%S"))
        tweet_information['created_at']=str(tweet.created_at.strftime("%Y-%m-%d %H:%M:%S"))

        try:
            tweet_information['in_reply_to_id'] = tweet._json['in_reply_to_status_id']
        except:
            pass

        # included entities
        entities_dict = tweet._json['entities']
        tweet_information['entities'] = copy.deepcopy(entities_dict)

        # id of this tweet
        tweet_information['id_str']=tweet._json['id_str']

        # retweet count
        tweet_information['retweet_count']=tweet._json['retweet_count']

        # favourites count
        tweet_information['favorite_count']=tweet._json['favorite_count']

        # screename of the user to which it was replied (is Nullable)
        tweet_information['in_reply_to_screen_name']=tweet._json['in_reply_to_screen_name']

        # user information in user dictionery
        user_dictionery=tweet._json['user']

        # no of followers of the user
        tweet_information['followers_count']=user_dictionery['followers_count']

        # screename of the person who tweeted this
        tweet_information['screen_name']=user_dictionery['screen_name']



        # add this tweet to the tweet_list
        tweet_list.append(tweet_information)


    # open file desc to output file with write permissions
    file_des=open(file,'w')

    # dump tweets to the file
    json.dump(tweet_list,file_des,indent=4,sort_keys=True)

    # close the file_des
    file_des.close()
