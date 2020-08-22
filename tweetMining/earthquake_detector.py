import _pickle as cPickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import os.path

class earthquake_detector_SVM(object):
    '''
    used to check if a tweet talks about an earthquake happening now or not
    it actually can not be used due to a lack of dataset
    '''
    def __init__(self):
        self.vectorizer = TfidfVectorizer(min_df=5,
                                          max_df=0.8,
                                          sublinear_tf=True,
                                          use_idf=True)
        if os.path.isfile('../data/SVM_state/classifier.pkl') and \
                os.path.isfile('../data/SVM_state/vectorizer.pkl'):
            with open('../data/SVM_state/classifier.pkl', 'rb') as fid:
                self.classifier = cPickle.load(fid)
            with open('../data/SVM_state/vectorizer.pkl', 'rb') as fid:
                self.vectorizer = cPickle.load(fid)
        else:
            self.classifier = svm.SVC(kernel='rbf')
            self.vectorizer = TfidfVectorizer(min_df=5,
                                              max_df=0.8,
                                              sublinear_tf=True,
                                              use_idf=True)

    def train(self, trainData):
        '''

        @param trainData: pandas csv with labels 'Content' (tweet), 'Label'
        @return:
        '''
        train_vectors = self.vectorizer.fit_transform(trainData['Content'])
        self.classifier.fit(train_vectors, trainData['Label'])
        with open('../data/SVM_state/classifier.pkl', 'wb') as fid:
            cPickle.dump(self.classifier, fid)
        with open('../data/SVM_state/vectorizer.pkl', 'wb') as fid:
            cPickle.dump(self.vectorizer, fid)
    def predict(self, data):
        '''

        @param data: pandas csv with labels 'Content' (tweet), 'Label'
        @return: array of labels
        '''
        test_vectors = self.vectorizer.transform(data['Content'])
        labels = self.classifier.predict(test_vectors)
        return labels
if __name__ == "__main__":

    # train Datastareddy/sentiment_analysis/master/data/train.csv")
    # train fake Data
    train_data = pd.read_csv("https://raw.githubusercontent.com/Vasistareddy/sentiment_analysis/master/data/train.csv")
    # test fake Data
    test_data = pd.read_csv("https://raw.githubusercontent.com/Vasistareddy/sentiment_analysis/master/data/test.csv")

    detector = earthquake_detector_SVM()
    detector.train(trainData=train_data)
    print(detector.predict(test_data))
