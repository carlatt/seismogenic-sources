import tweepy
from pprint import pprint


class Stream2Screen(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or tweepy.API()
        self.n = 0
        self.m = 20

    def on_status(self, status):
        print(status.text)
        if status.coordinates:
            print('coords:', status.coordinates)
        if status.place:
            print('place:', status.place.full_name)
        print()

        self.n += 1
        if self.n < self.m:
            return True
        else:
            print(f'tweets = {self.n}')
            return False


class StopStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or tweepy.API()
        self.n = 0
        self.m = 20

    def on_status(self, status):
        self.n += 1
        if self.n < self.m:
            return True
        else:
            return False


class NewStreamListener(tweepy.StreamListener):
    def __init__(self, api=None):
        self.api = api or tweepy.API()

    def on_status(self, status):
        pass



def keys(name):
    """Return the API key from an API name."""
    keychain = {'TwitKEY': 'nsq5BVLFe5xheMa9NO37poiob',
                'TwitSECRET': 'v2R6uHuzqkk68oM0P0KUAs0XkBezze3uBcujT2Dmlt6GclQJTh',
                'TwitTOKEN': '1270774916388917249-xDVbbwOTJk8kJyjG1SUs3l0NzSRYNg',
                'TwitTOKSEC': '24qRoFKDHiQb8D7tbhMdY56KBm8wYIWpDngBoLW0IgaqV'}
    return keychain[name]



if __name__ == "__main__":
    # Get access to Twitter's API
    auth = tweepy.OAuthHandler(keys('TwitKEY'), keys('TwitSECRET'))
    auth.set_access_token(keys('TwitTOKEN'), keys('TwitTOKSEC'))
    api = tweepy.API(auth)
    # Test it on yourself
    api.me().screen_name


    #user = api.get_user('twitter')
    #pprint(vars(user))

    stream = tweepy.streaming.Stream(api.auth, Stream2Screen())
    stream.filter(track=['of,the,a'], languages=['it'])
