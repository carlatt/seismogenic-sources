import queue
from _thread import start_new_thread, allocate_lock

import FindEmergencySources
import RoadFinder
from Clusterizer import Clusterizer
from FindEmergencySources import *
from tweetMining import tweet_retreiver
from tweetMining import tweetProcessorIF

safeprint = allocate_lock()

# Create a queue object
dataQueue = queue.Queue()


# Function called by the producer thread
def generic_producer(tweet_processor, queue_tweets=dataQueue, words_to_track=['a'], user=None):
    tweet_retreiver.get_tweets_coords(queue_tweets, tweet_processor, words_to_track=words_to_track, user=user)

def INGV_coord_producer(queue_tweets=dataQueue):
    tweet_retreiver.get_tweets_coords(queue_tweets, tweetProcessorIF.INGVTweetProcessor(),
                                      words_to_track=['STIMA #PROVVISORIA'], user=['121049123'])
    #tweet_retreiver.get_tweets_coords(queue_tweets, tweetProcessorIF.INGVTweetProcessor(),
    #                                  words_to_track=['STIMA #PROVVISORIA'], user=['175041414'])
def generic_tweet_coord_producer(queue_tweets=dataQueue):
    tweet_retreiver.get_tweets_coords(queue_tweets, tweetProcessorIF.genericTweetProcessor(),
                                      words_to_track=['terremoto'])

# Function called by the consumer threads
def consumer(queue_tweets=dataQueue):
    while True:
        coords = []
        if queue_tweets.full():
            while not queue_tweets.empty():
                try:
                    coords.append(queue_tweets.get())
                except queue.Empty:
                    pass
            cluster = Clusterizer(coords)
            cluster.calculate_clusters()
            cluster.clusters2hulls()
            gdal_hulls = cluster.export_cluster_hulls_as_GDAL_poly()

            # We find the earthquake affected area
            nSources = 6  # number of possible sources

            SeismSources = SeismogenicSources(gdal_hulls, nSources)
            seismogenic_area = SeismSources.findedArea

            SeismSources.plot_seismogenic_data(plotItaly=True)
            plt.savefig('seismogenicSources')
            plt.show()

            EmergSources = EmergencySources(seismogenic_area)
            emergency_area = EmergSources.emergencyArea

            EmergSources.plot_emergency_data(plotItaly=True)
            plt.savefig('emergencySources')
            plt.show()

            # We find province capitals near earthquake affected (emergency) area from where
            # rescues come from
            capitals = EmergSources.emergencySources


            # We load a map of Italy containing highways and primary roads
            map = RoadFinder.Italy_Road_Finder()

            #we find and then plot the shortest path from capital cities to the emergency area centroid
            for capital in capitals:
                source = capital.Centroid()
                destination = emergency_area.Centroid()
                map.find_route(source.ExportToWkt(), destination.ExportToWkt())
                map.save_route()
                # map.plot_route()
            map.plot_routes()


if __name__ == "__main__":
    # queue length tell us how much tweet we want to consider before calculating seismogenic sources
    tweets = queue.Queue(1)
    start_new_thread(INGV_coord_producer, (tweets,))
    start_new_thread(generic_tweet_coord_producer, (tweets,))
    #start_new_thread(consumer, (tweets,))
    consumer(tweets)