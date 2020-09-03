import _pickle as cPickle
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
import os.path

from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split


class earthquake_detector_SA(object):
    '''
    used to check if a tweet talks about an earthquake happening now or not
    '''
    def __init__(self):
        if os.path.isfile('./data/SVM_state/classifier.pkl') and \
                os.path.isfile('./data/SVM_state/vectorizer.pkl'):
            with open('./data/SVM_state/classifier.pkl', 'rb') as fid:
                self.classifier = cPickle.load(fid)
            with open('./data/SVM_state/vectorizer.pkl', 'rb') as fid:
                self.vectorizer = cPickle.load(fid)
        else:
            self.classifier = svm.SVC(kernel='linear', C=3.3, gamma='auto')
            self.vectorizer = TfidfVectorizer(min_df=5,
                                              max_df=0.8,
                                              sublinear_tf=True,
                                              use_idf=True)

    def train(self, trainData, save_to_file=False):
        '''

        @param trainData: pandas csv with labels 'Content' (tweet), 'Label'
        @return:
        '''
        train_vectors = self.vectorizer.fit_transform(trainData['Content'])
        self.classifier.fit(train_vectors, trainData['Label'])
        if save_to_file:
            with open('../data/SVM_state/classifier.pkl', 'wb') as fid:
                cPickle.dump(self.classifier, fid)
            with open('../data/SVM_state/vectorizer.pkl', 'wb') as fid:
                cPickle.dump(self.vectorizer, fid)
    def predict(self, data):
        '''

        @param data: pandas csv with labels 'Content' (tweet), 'Label'
        @return: array of labels
        '''
        test_vectors = self.vectorizer.transform(data)
        labels = self.classifier.predict(test_vectors)
        return labels
if __name__ == "__main__":
    data = pd.read_csv("../data/earthquake_sentiment_analysis/earthquake_dataset_SA.csv")

    train_data, test_data = train_test_split(data, test_size=0.9)


    detector = earthquake_detector_SA()
    #detector.train(trainData=train_data, save_to_file=True)
    predictions = detector.predict(test_data['Content'])
    report = classification_report(test_data['Label'], predictions, output_dict=True)
    print('positive: ', report['pos'])
    print('negative: ', report['neg'])
    string = 'ha fatto il terremoto'
    df = pd.DataFrame([string], columns=['Content'])
    prediction = detector.predict(df['Content'])
    print()
    print(prediction)
