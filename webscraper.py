
# ------------------------------------------------------------------------------
# ABSTRACTIVE SUMMARIZATION
# ------------------------------------------------------------------------------

# Packages
from selenium import webdriver
import nltk

# Functions

# Open chrome
driver = webdriver.Chrome('/Users/samu_hugo/Downloads/chromedriver')

# Select website
driver.get('https://www.hltv.org/')

# Find elements
articles = driver.find_elements_by_class_name('article')

# Store all article links in an array
article_ids = []
for a in articles:
    article_ids.append(a.get_property('href'))

# Redirect to first article link
driver.get(article_ids[0])

# Find elements
paragraphs = driver.find_elements_by_class_name('news-block')

# Concatenate paragraphs
article_text = ""
for p in paragraphs:
    article_text += p.text + " "

article_text = ""


def read_article(article_text):
    article = article_text.split(". ")
    sentences = []
    for sentence in article:
        print(sentence)
        sentences.append(sentence.replace("[^a-zA-Z]", " ").split(" "))
        sentences.pop()
    return sentences
