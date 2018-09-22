from gtfunctions import get_last_downloaded, get_all_tweets, store_tweets

import datetime
import os
ts = datetime.datetime.utcnow().strftime('%Y-%m-%d-%H%M%S')

consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""

users = [
    'FoxNews',
    'foxandfriends',
    'FoxBusiness',
    'ABC',
    'ABCPolitics',
    'AP',
    'AFP',
    'BBCNorthAmerica',
    'CBSNews',
    'CBSPolitics',
    'CBSEveningNews',
    'CNN',
    'HLNTV',
    'MSNBC',
    'NBCNews',
    'NBCPolitics',
    'NRATV',
    'Reuters',
    'DRUDGE_REPORT',
    'rt_com',
    'sputnikint'
]

#users = []


#store_tweets(alltweets, 'tweets_' + ts + '.json')

for user in users:


    if os.path.isdir(user):

        newest_id = get_last_downloaded(user)

    else:
        os.mkdir(user)
        newest_id = 0

    alltweets=get_all_tweets(user, consumer_key, consumer_secret, access_key, access_secret, newest_id)

    print_flag = True
    for i in range(len(alltweets)-1, 0 , -1):
        if int(alltweets[i]._json['id_str']) <= newest_id:
            if print_flag == True:
                print("Removing tweets after ID {}".format(alltweets[i]._json['id_str']))
                print_flag = False

            del alltweets[i]

    store_tweets(alltweets, user + '/' + ts + '.json')
