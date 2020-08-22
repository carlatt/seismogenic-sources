from queue import Empty
import queue
import tweepy


class Stream2Queue(tweepy.StreamListener):
    def __init__(self, queue, api=None):
        self.api = api or tweepy.API()
        self.tweets = queue

    def on_status(self, status):
        self.tweets.put(status)

    def queue_get_all(self):
        items = []
        while True:
            try:
                items.append(self.tweets.get_nowait())
            except Empty as e:
                break
        return items



def keys(name):
    """Return the API key from an API name."""
    ''' must be rearranged'''
    keychain = {'TwitKEY': 'nsq5BVLFe5xheMa9NO37poiob',
                'TwitSECRET': 'v2R6uHuzqkk68oM0P0KUAs0XkBezze3uBcujT2Dmlt6GclQJTh',
                'TwitTOKEN': '1270774916388917249-xDVbbwOTJk8kJyjG1SUs3l0NzSRYNg',
                'TwitTOKSEC': '24qRoFKDHiQb8D7tbhMdY56KBm8wYIWpDngBoLW0IgaqV'}
    return keychain[name]

def get_tweets(queue, words_to_track=['a'], user=None):
    auth = tweepy.OAuthHandler(keys('TwitKEY'), keys('TwitSECRET'))
    auth.set_access_token(keys('TwitTOKEN'), keys('TwitTOKSEC'))
    api = tweepy.API(auth)

    screen = Stream2Queue(queue)
    stream = tweepy.streaming.Stream(api.auth, screen)
    stream.filter(track=words_to_track, languages=['it'], follow=user)

if __name__ == "__main__":
    # Get access to Twitter's API
    auth = tweepy.OAuthHandler(keys('TwitKEY'), keys('TwitSECRET'))
    auth.set_access_token(keys('TwitTOKEN'), keys('TwitTOKSEC'))
    api = tweepy.API(auth)
    # Test it on yourself
    #api.me().screen_name


    #user = api.get_user('twitter')
    #pprint(vars(user))

    queue = queue.Queue()
    screen = Stream2Queue(queue)
    stream = tweepy.streaming.Stream(api.auth, screen)
    # stream.filter(track=['a'], languages=['it'])
    # tweets from ingv
    stream.filter(track=['[STIMA #PROVVISORIA]'], follow=['121049123'])
    print(len(screen.queue_get_all()))
