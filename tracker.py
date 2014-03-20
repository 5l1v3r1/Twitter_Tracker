#!/usr/bin/env python

import pygmaps
import tweepy
import json
import argparse

consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

gmap = pygmaps.maps('35.6500', '-97.4667', 5)

coords = []

class Listener(tweepy.StreamListener):
    def on_data(self, data):
        decoded = json.loads(data)

        try:
            gmap.addpoint(str(decoded['coordinates']['coordinates'][1]), str(decoded['coordinates']['coordinates'][0]), '#FF0000')
        except:
            print "Lat: " + str(decoded['coordinates']['coordinates'][1])
            print "Lon: " + str(decoded['coordinates']['coordinates'][0])

        with open('tweets.txt', 'a+') as f:
            json.dump(decoded['text'].encode('ascii', 'ignore'), f)
        """
        print '@%s: %s' % (decoded['user']['screen_name'], decoded['text'].encode('ascii', 'ignore'))
        print ''
        """
        gmap.draw('test.html')
        return True

    def on_error(self, status):
        print status


if __name__ == "__main__":
    try:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        parser = argparse.ArgumentParser(description="Track a User or Topic with GPS")
        parser.add_argument('-u', '--user', nargs='+', type=str, help="Twitter username")
        parser.add_argument('-t', '--topic', nargs='+', type=str, help="Hashtags to follow")
        args = vars(parser.parse_args())

        if args['user']:
            users = [str(tweepy.API(auth).get_user(x).id) for x in args['user']]
        else:
            users = []
        if args['topic']:
            topics = [x for x in args['topic']]
        else:
            topics = []

        l = Listener()
        stream = tweepy.Stream(auth, l)
        stream.filter(follow=users, track=topics)
    except KeyboardInterrupt:
        print '\nGoodbye!'


