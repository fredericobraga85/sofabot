from sklearn import neighbors

class KNNIndicator:


    def train(self,neighbors, input, output):
        self.clf = neighbors.KNeighborsClassifier(neighbors)
        self.clf.fit(input, output)

    def predict(self , orderState, df, i):
        return self.clf.predict(input)
