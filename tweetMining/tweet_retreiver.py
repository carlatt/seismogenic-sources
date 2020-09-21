from queue import Empty
import tweepy

class Stream2Queue(tweepy.StreamListener):
    '''
    Stream listener used to store tweet coordinates in a queue
    '''
    def __init__(self, queue, tweet_processor, api=None):
        '''

        @param queue: queue to store coords
        @param tweet_processor: object implementing tweetProcessorIF interface
        @param api: API to use
        '''
        self.api = api or tweepy.API()
        self.tweets = queue
        self.processor = tweet_processor

    def on_status(self, status):
        '''
        called every time a tweet status is caught
        if the processor produces coords, they are stored in the queue
        @param status: tweepy status
        @return:
        '''
        coords = self.processor.gimme_coords(status)
        if coords is not None:
            self.tweets.put(coords)



def keys(name):
    '''
    @param name: API key (string)
    @return: API value (string)
    '''
    keychain = {'TwitKEY': 'nsq5BVLFe5xheMa9NO37poiob',
                'TwitSECRET': 'v2R6uHuzqkk68oM0P0KUAs0XkBezze3uBcujT2Dmlt6GclQJTh',
                'TwitTOKEN': '1270774916388917249-xDVbbwOTJk8kJyjG1SUs3l0NzSRYNg',
                'TwitTOKSEC': '24qRoFKDHiQb8D7tbhMdY56KBm8wYIWpDngBoLW0IgaqV'}
    return keychain[name]

def get_tweets_coords(queue, tweet_processor,  words_to_track=['a'], user=None):
    '''
    function using tweepy to retrieve italian tweets
    @param queue: used to store coords
    @param tweet_processor: object implementing tweetProcessorIF interface
    @param words_to_track: array of strings
    @param user: array of strings
    @return:
    '''
    auth = tweepy.OAuthHandler(keys('TwitKEY'), keys('TwitSECRET'))
    auth.set_access_token(keys('TwitTOKEN'), keys('TwitTOKSEC'))
    api = tweepy.API(auth)

    screen = Stream2Queue(queue, tweet_processor)
    stream = tweepy.streaming.Stream(api.auth, screen)
    stream.filter(track=words_to_track, languages=['it'], follow=user)
