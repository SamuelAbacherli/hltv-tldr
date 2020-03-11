
# ------------------------------------------------------------------------------
# ABSTRACTIVE SUMMARIZATION - USING GloVe
# ------------------------------------------------------------------------------

# Packages
from selenium import webdriver
import os.path
from keras.layers import Embedding
from numpy import array
from numpy import asarray
from numpy import zeros
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers import Embedding

# Functions

# Open chrome
driver = webdriver.Chrome('/Users/samu_hugo/Downloads/chromedriver')

# Select website
driver.get('https://www.hltv.org/')

# Find elements
articles = driver.find_elements_by_class_name('article')

# Redirect to first article link
driver.get(articles[0].get_property('href'))

# Find elements
paragraphs = driver.find_elements_by_class_name('news-block')

# Concatenate paragraphs
article_text = ""
for p in paragraphs:
    article_text += p.text + " "


def read_article(article_text):
    article = article_text.split(". ")
    sentences = []
    for sentence in article:
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
    return sentences

sentences = read_article(article_text)

# Perparing GloVe
embeddings_index = {}
EMBEDDING_DIM = 100
f = open(os.path.join('/Users/samu_hugo/Desktop/dev/hltv-tldr/glove.6B/',
                      'glove.6B.{}d.txt'.format(EMBEDDING_DIM)))
for line in f:
    values = line.split()
    word = values[0]
    coefs = asarray(values[1:], dtype='float32')
    embeddings_index[word] = coefs
f.close()

t = Tokenizer()
embedding_matrix = zeros((len(t.word_index) + 1, EMBEDDING_DIM), dtype = 'float32')
for word, i in t.word_index.items():
    embedding_vector = embeddings_index.get(word)
    if embedding_vector is not None:
    # Words not found in glove will be zeros
        embedding_matrix[i] = embedding_vector

# Embedding weight matrix
MAX_INPUT_LENGTH = 100
embedding_layer = Embedding(len(t.word_index) + 1,
                            EMBEDDING_DIM,
                            weights = [embedding_matrix],
                            input_length = MAX_INPUT_LENGTH,
                            trainable = False,
                            name = 'embedding_layer')

# Define model
t.fit_on_texts(sentences)
