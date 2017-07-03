from sklearn import neighbors

class KNNIndicator:


    def train(self,neighbors, input, output):
        self.clf = neighbors.KNeighborsClassifier(neighbors)
        self.clf.fit(input, output)

    def predict(self, input):
        return self.clf.predict(input)
