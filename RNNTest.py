import csv
import sys
import keras_preprocessing.text
import pandas as pd
import numpy as np

# Read CSV file
kwargs = {'newline': ''}
mode = 'r'
if sys.version_info < (3, 0):
    kwargs.pop('newline', None)
    mode = 'rb'
with open('patentData.csv', mode, encoding="utf8", **kwargs) as fp:
    reader = csv.reader(fp, delimiter=',', quotechar='"')
    next(reader, None)  # skip the headers
    data_read = [row for row in reader]
print(data_read[100][:300])
# Get data - reading the CSV file

tokenizer = keras_preprocessing.text.Tokenizer(num_words=None,
                     filters='#$%&()*+-<=>@[\\]^_`{|}~\t\n',
                     lower = False, split = ' ')

tokenizer.fit_on_texts(data_read)
sequences = tokenizer.texts_to_sequences(data_read)
print(sequences[100][:15])

idx_word = tokenizer.index_word
print(' '.join(idx_word[w] for w in sequences[100][:40]))

features = []
labels = []

training_length = 50
for seq in sequences:
    for i in range(training_length, len(seq)):
        extract = seq[i - training_length:i+1]
        features.append(extract[:-1])
        labels.append(extract[-1])
features = np.array(features)
print(len(features))

num_words = len(idx_word) + 1
label_array = np.zeros((len(features),num_words),dtype = np.int8)
for example_index, word_index in enumerate(labels):
    label_array[example_index,word_index] = 1
print(label_array.shape)