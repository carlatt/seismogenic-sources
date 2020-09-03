from tweetMining import earthquake_detector
import pandas as pd
'''
utilities to retreive a location from a tweet
'''
def find_city(city_name):
    with open('data/cities500/cities500.txt', 'r', encoding='utf') as f:
        lines = f.readlines()

        for line in lines:
            city = (line.rstrip()).split('\t')
            if city[2] == city_name:
                found = city
                break

        return {
            'geonameid': found[0],
            'name': found[1],
            'asciiname': found[2],
            'alternatenames': found[3],
            'latitude': found[4],
            'longitude': found[5],
            'feature class': found[6],
            'feature code': found[7],
            'country code': found[8],
            'cc2': found[9],
            'admin1 code': found[10],
            'admin2 code': found[11],
            'admin3 code': found[12],
            'admin4 code': found[13],
            'population': found[14],
            'elevation': found[15],
            'dem': found[16],
            'timezone': found[17],
            'modification date': found[18],
        }


class tweetProcessorIF(object):
    def __init__(self):
        pass
    def gimme_coords(self, tweet):
        raise Exception("NotImplementedException")

class genericTweetProcessor(tweetProcessorIF):
    def __init__(self):
        super().__init__()
        self.SA = earthquake_detector.earthquake_detector_SA()
    def gimme_coords(self, tweet):
        if hasattr(tweet, "retweeted_status"):  # Check if Retweet
            try:
                text = tweet.retweeted_status.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.retweeted_status.text
        else:
            try:
                text = tweet.extended_tweet["full_text"]
            except AttributeError:
                text = tweet.text

        print(text)
        data = pd.read_csv("./data/earthquake_sentiment_analysis/earthquake_dataset_SA.csv")
        #self.SA.train(trainData=data)
        predictions = self.SA.predict([text])
        for pred in predictions:
            print(pred)
            if pred == 'pos':
                if tweet.coordinates is not None:
                    return tweet.coordinates
                elif tweet.place is not None:
                    # we have to take the coords in the bounding_box
                    box = tweet.place.bounding_box.coordinates
                    x = (box[0][1][0]-box[0][0][0])/2
                    y = (box[0][2][1]-box[0][1][1])/2
                    return [x,y]
                    #zone = find_city(tweet.place)
                    #return [float(zone['longitude']), float(zone['latitude'])]


class INGVTweetProcessor(tweetProcessorIF):
    def __init__(self):
        super().__init__()
    def gimme_coords(self, tweet):
        print(tweet.text)
        res = tweet.text.split('prov/zona')
        res = res[1].split()
        place = res[0]
        print(place)
        # then we have to convert place to coords as above
        zone = find_city(place)
        return [float(zone['longitude']), float(zone['latitude'])]

if __name__ == "__main__":
    pass