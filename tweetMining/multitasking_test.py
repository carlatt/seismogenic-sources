# Specify the number of consumer and producer threads
numconsumers = 1
numproducers = 1
nummessages = 4

import queue
from _thread import allocate_lock, start_new_thread
from tweetMining import tweet_retreiver

# Create a lock so that only one thread writes to the console at a time
safeprint = allocate_lock()

# Create a queue object
dataQueue = queue.Queue()


# Function called by the producer thread
def producer(queue_tweets=dataQueue, words_to_track=['a'], user=None):
    tweet_retreiver.get_tweets(queue_tweets, words_to_track=words_to_track, user=user)

# Function called by the consumer threads
def consumer(queue_tweets=dataQueue):
    while True:
        try:
            data = queue_tweets.get()
        except queue.Empty:
            pass
        else:
            with safeprint:
                # TODO: replace print with data processing
                print('consumer got => ', data.text)


if __name__ == '__main__':
    # Create consumers
    tweets = queue.Queue()
    for i in range(numconsumers):
        start_new_thread(consumer, (tweets,))

    # Create producers
    for i in range(numproducers):
        start_new_thread(producer, (tweets,))

    # una zozzeria
    while True:
        pass
    # Exit the program
    print('Main thread exit')