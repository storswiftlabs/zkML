# -*- coding:utf-8 -*-
import numpy as np
from matplotlib import pyplot


class K_Means(object):
    # k is class number; tolerance is center point tolerance; max_iter is iteration number 
    def __init__(self, k=2, tolerance=0.0001, max_iter=300):
        self.k_ = k
        self.tolerance_ = tolerance
        self.max_iter_ = max_iter

    def fit(self, data):
        self.centers_ = {}
        for i in range(self.k_):
            self.centers_[i] = data[i]

        for i in range(self.max_iter_):
            self.clf_ = {}
            for i in range(self.k_):
                self.clf_[i] = []
            for feature in data:
                # distances = [np.linalg.norm(feature-self.centers[center]) for center in self.centers]
                distances = []
                for center in self.centers_:
                    # Euler distance
                    # np.sqrt(np.sum((features-self.centers_[center])**2))
                    distances.append(np.linalg.norm(feature - self.centers_[center]))
                classification = distances.index(min(distances))
                self.clf_[classification].append(feature)

            prev_centers = dict(self.centers_)
            for c in self.clf_:
                self.centers_[c] = np.average(self.clf_[c], axis=0)

            # 'center point'Is it within tolerance
            optimized = True
            for center in self.centers_:
                org_centers = prev_centers[center]
                cur_centers = self.centers_[center]
                if np.sum((cur_centers - org_centers) / org_centers * 100.0) > self.tolerance_:
                    optimized = False
            if optimized:
                break

    def predict(self, p_data):
        # np.sqrt((p_data[0]-self.centers_[center][0])**2+(p_data[1]-self.centers_[center][1])**2)
        distances = [np.linalg.norm(p_data - self.centers_[center]) for center in self.centers_.keys()]
        index = distances.index(min(distances))
        return index


if __name__ == '__main__':
    x = np.array([[1, 2], [1.5, 1.8], [5, 8], [8, 8], [1, 0.6], [9, 11]])
    k_means = K_Means(k=2)
    k_means.fit(x)
    print(k_means.centers_)
    for index, center in enumerate(k_means.centers_):
        pyplot.scatter(k_means.centers_[center][0], k_means.centers_[center][1], marker='*', s=150, c=('r' if index == 0 else 'b'))

    for cat in k_means.clf_:
        for point in k_means.clf_[cat]:
            pyplot.scatter(point[0], point[1], c=('r' if cat == 0 else 'b'))

    predict_data = [[2, 6 ]]
    for feature in predict_data:
        cat = k_means.predict(feature)
        pyplot.scatter(feature[0], feature[1], c=('r' if cat == 0 else 'b'), marker='x')
    pyplot.show()