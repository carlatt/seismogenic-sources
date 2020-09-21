import queue
from _thread import start_new_thread, allocate_lock
import time


import RoadFinder
from Clusterizer import Clusterizer
from FindEmergencySources import *
from tweetMining import tweet_retreiver
from tweetMining import tweetProcessorIF

safeprint = allocate_lock()

# Create a queue object
dataQueue = queue.Queue()

def INGV_coord_producer(queue_tweets=dataQueue):
    '''
    this function is used to follow INGV user and retrieve a location coordinates
    from real time tweets
    @param queue_tweets: data queue where tweets coords are stored
    @return:
    '''
    tweet_retreiver.get_tweets_coords(queue_tweets, tweetProcessorIF.INGVTweetProcessor(),
                                      words_to_track=['STIMA #PROVVISORIA'], user=['121049123'])

def generic_tweet_coord_producer(queue_tweets=dataQueue):
    '''
    this function is used to retrieve coords from tweets posted by any user if they talk
    about a recently happened earthquake
    @param queue_tweets: data queue where tweets coords are stored
    @return:
    '''
    tweet_retreiver.get_tweets_coords(queue_tweets, tweetProcessorIF.genericTweetProcessor(),
                                      words_to_track=['terremoto'])

# Function called by the consumer threads
def consumer(queue_tweets=dataQueue):
    '''
    this function is used to plot useful infos about a recently happened earthquake
    such as place, possible seismogenic sources involved, cities involved and main roads to
    reach the involved area. This is happening only if the queue_tweets is not empty.

    @param queue_tweets: data queue from where tweets coords are loaded
    @return:
    '''
    while True:
        # we check every 2 mins
        time.sleep(120)
        coords = []
        while not queue_tweets.empty():
            try:
                coords.append(queue_tweets.get())
            except queue.Empty:
                pass
        if len(coords) != 0:
            cluster = Clusterizer(coords)
            cluster.calculate_clusters()
            cluster.clusters2hulls()
            gdal_hulls = cluster.export_cluster_hulls_as_GDAL_poly()

            # We find the earthquake affected area
            nSources = 6  # number of possible sources

            SeismSources = SeismogenicSources(gdal_hulls, nSources)
            if len(SeismSources.foundSources) > 0:
                seismogenic_area = SeismSources.foundArea

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

                # we find and then plot the shortest path from capital cities to the emergency area centroid
                for capital in capitals:
                    source = capital.Centroid()
                    destination = emergency_area.Centroid()
                    map.find_route(source.ExportToWkt(), destination.ExportToWkt())
                    map.save_route()
                    # map.plot_route()
                map.plot_routes(EmergSources.totalArea)
            else:
                print('Non ci sono faglie nelle vicinanze')




if __name__ == "__main__":
    '''
    main corpus of the program. The above functions are started in three different thread.
    '''
    tweets = queue.Queue()
    start_new_thread(INGV_coord_producer, (tweets,))
    start_new_thread(generic_tweet_coord_producer, (tweets,))
    consumer(tweets)