import numpy as np
from typing import List, Callable

def sigmoid(x: np.ndarray[int,]) -> np.ndarray:
    return 1/(1 + np.exp(-x))

class FeedforwardNN:
    def __init__(self, layers_size: List[int,], f_activation: Callable[[np.ndarray[int]], np.ndarray] = sigmoid):
        self.activation = f_activation
        self.weights: List[np.ndarray, ] = []
        self._init_weights(layers_size)

    def fit(self):
        pass

    def predict(self, X: List[List[int,]]) -> list[int]:
        result = []
        for sample in X:
            result.append(self._predict_one(sample))
        return result

    def _predict_one(self, X: List[int,]) -> int:
        input_layer = np.array(X)
        h_layer = input_layer
        for matrix in self.weights:
            h_layer = h_layer.dot(matrix)
            h_layer = self.activation(h_layer)
        return int(h_layer.argmax())


    def _init_weights(self, layers_size: List[int,], is_norm_dist: bool = True) -> None:
        for i in range(1, len(layers_size)):
            size = (layers_size[i-1], layers_size[i])
            np.random.seed(42)
            matrix = np.random.normal(0, 1, size) if is_norm_dist else np.random.uniform(-1, 1, size)
            self.weights.append(matrix)

