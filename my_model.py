import time
from collections import deque
import numpy as np


class NGramModel:
    def __init__(self, N):
        self.N = N
        self.model = dict()

    # TODO: first delete all non-alphabet symbols, then split them
    # TODO: make static?
    # separate different parts somehow to keep the songs from mixing
    def prepare(self, text):
        # preparation
        # make lowercase, delete all non-alphabet symbols
        alphabet = 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'
        text = text.lower()
        out = []
        for word in text.split():
            to_write = ''
            for e in word:
                if e in alphabet:
                    to_write += e
            if to_write not in ['', '-']:  # need it because accept words like что-то
                out.append(to_write)

        return out

    # TODO: make faster by replacing slices with queue
    # TODO: idea: split by '.' and make n-grams inside sentences - more sense
    def fit(self, text):
        sequence = self.prepare(text)
        for i in range(self.N, len(sequence)):
            key = tuple(sequence[i - self.N: i])
            word = sequence[i]
            if key not in self.model:
                self.model[key] = []
            self.model[key].append(word)

    def random_ngram(self):
        keys = tuple(self.model.keys())
        resp = keys[np.random.randint(0, len(self.model))]
        return resp

    # TODO: add seed to random
    def generate(self, length, prefix='', seed=int(time.time() * 1000) % (2 ** 32)):
        np.random.seed(seed)
        sequence = deque()
        response = ''

        # begging of the text and the first n-gram
        prefix = self.prepare(prefix)

        if len(prefix) < self.N:
            # if we can't use prefix as the first n-gram,
            # fill it up with random values
            # TODO: try to fill with existing n-gram,
            #  that starts with prefix
            i = len(prefix)
            to_use = self.random_ngram()
            prefix = list(prefix)  # make mutable
            while i < self.N:
                prefix.append(to_use[i])
                i += 1
            prefix = tuple(prefix)  # make immutable again

        for word in self.random_ngram():
            sequence.append(word)
            if len(sequence) > self.N:
                sequence.popleft()
            response += word + ' '

        # generating text
        for i in range(length - self.N):
            key = tuple(sequence)
            if key not in self.model:
                # get random ngram.
                # TODO: get random among the nearest
                #  (max number of respectively equal numbers)
                key = self.random_ngram()
            to_choose = self.model[key]
            word = np.random.choice(to_choose)
            sequence.popleft()
            sequence.append(word)
            response += word + ' '
        return response


def main():
    file_name = 'texts/pyrokinesis.txt'
    file = open(file_name, encoding='utf-8')
    text = file.read()
    file.close()

    model = NGramModel(2)
    model.fit(text)
    result = model.generate(50)

    file = open('texts/pyrokinesis_result.txt', 'w')
    file.write(result)
    file.close()


if __name__ == '__main__':
    main()
