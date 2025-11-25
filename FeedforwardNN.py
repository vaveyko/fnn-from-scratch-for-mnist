import numpy as np
from typing import List

def sigmoid(x: np.ndarray[int]) -> np.ndarray:
    return 1/(1 + np.exp(-x))

class FeedforwardNN:
    def __init__(self, layers_size: List[int,]):
        self.weights: List[np.ndarray, ] = []
        self._init_weights(layers_size)

    def fit(self):
        pass

    def predict(self):
        pass

    def _init_weights(self, layers_size: List[int,], is_norm_dist: bool = True) -> None:
        for i in range(1, len(layers_size)):
            self.weights.append(np.ndarray(shape=(layers_size[i], layers_size[i-1])))
            size = (layers_size[i], layers_size[i-1])
            matrix = np.random.normal(0, 1, size) if is_norm_dist else np.random.uniform(-1, 1, size)
            self.weights.append(matrix)

