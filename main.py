from collections import deque
import numpy as np


class NGramModel:
    def __init__(self, N):
        self.N = N
        self.model = dict()

    # TODO: first delete all non-alphabet symbols, then split them
    # TODO: make static?
    def prepare(self, text):
        # preparation
        # make lowercase, delete all non-alphabet symbols
        alphabet = 'abcdefghijklmnopqrstuvwxyz'
        text = text.lowercase()
        out = []
        for word in text.split():
            is_word = True
            for e in word:
                if e not in alphabet:
                    is_word = False
                    break
            if is_word:
                out.append(word)

        return out

    # TODO: make faster by replacing slices with queue
    def fit(self, text):
        sequence = self.prepare(text)
        for i in range(self.N, len(sequence)):
            key = sequence[i - self.N: i]
            word = sequence[i]
            self.model[key] = word

    # TODO: add seed to random
    def generate(self, length, seed=1337):
        sequence = deque()
        response = ""

        # first n-gram
        for word in np.random.choice(self.model.keys()):
            sequence.append(word)
            response += word + " "

        # generating text
        for i in range(length - self.N):
            key = list(sequence)
            if key not in self.model:
                # get random word. actually, it's better to get random among the nearest
                key = np.random.choice(self.model.keys())
            word = np.random.choice(self.model[key])
            sequence.popleft()
            sequence.append(word)
            response += word + " "
        return response


def main():
    file = ""


if __name__ == '__main__':
    main()
