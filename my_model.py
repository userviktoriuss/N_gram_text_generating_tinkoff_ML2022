import time
from collections import deque
import numpy as np
import re


# DISCLAIMER
# You asked to create only 3 files, but I think
# that it's better to put my class in a separate file
# So, here it is

class NGramModel:
    def __init__(self, N):
        self.N = N
        self.model = dict()

    # preparation
    # separate different parts to keep the
    # sentences from mixing (e.g. split by '.').
    # make lowercase, delete all non-alphabet symbols
    # returns array of arrays of strings
    def prepare(self, text):
        alphabet = "abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя-'"
        text = text.lower()
        out = []  # resulting array of arrays of words
        for line in re.split(';|\.|!|\?|:|\*|\n|\(|\)|\[|\]', text):
            out.append([])
            for word in line.split():
                to_write = ''
                for e in word:
                    if e in alphabet:
                        to_write += e

                # need it because accept words like "что-то" and "I'm"
                if to_write not in ['', '-', "'"]:
                    out[-1].append(to_write)

        return out

    def fit(self, text):
        sequence = self.prepare(text)
        for line in sequence:
            for i in range(self.N, len(line)):
                key = tuple(line[i - self.N: i])
                word = line[i]
                if key not in self.model:
                    self.model[key] = []
                self.model[key].append(word)

    def random_ngram(self):
        keys = tuple(self.model.keys())
        resp = keys[np.random.randint(0, len(self.model))]
        return resp

    def generate(self, length, prefix='', seed=int(time.time() * 1000) % (2 ** 32)):
        np.random.seed(seed)
        sequence = deque()
        response = ''

        # begging of the text and the first n-gram
        tmp = []
        # prepare prefix assuming that it's ONE simple sentence
        for line in self.prepare(prefix):
            for word in line:
                tmp.append(word)
        prefix = tmp

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

        for word in prefix:
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
                #  (max number of respectively equal numbers, for example)
                key = self.random_ngram()
            to_choose = self.model[key]
            word = np.random.choice(to_choose)
            sequence.popleft()
            sequence.append(word)
            response += word + ' '
        return response
