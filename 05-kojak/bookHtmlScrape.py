from bs4 import BeautifulSoup
import pprint
from textblob import TextBlob
import csv

class QuoteID(object):

    def __init__(self, quote, speaker, sentiment, polarity):
        self.quote = quote
        self.speaker = speaker
        self.sentiment = sentiment
        self.polarity = polarity

url = '/media/bf2398/Disk2_Linux_Mint/home/bf2398/book-nlp/data/output/harrypotter/book.id.html'
soup = BeautifulSoup(open(url),"html5lib")

quote_id_list = ["line","character","sentiment","polarity"]
for quote in soup.find_all(class_='bookquote'):
    split = quote.text.split("\'\'")

    # set line and character variables
    # conditional for when there are multiple single quote separators
    if(len(split)>2):
        line = split[0].replace("``","").strip()+' '+split[1].replace("``","").strip()
        character = split[2].replace("(","").replace(")","").strip()
    else:
        line = split[0].replace("``","").strip()
        character = split[1].replace("(","").replace(")","").strip()

    # set sentiment analysis variables
    sent, pol = TextBlob(line).sentiment

    # add QuoteID object to list
    quote_id_list.append([line,character, sent, pol])

"""
#### Finding the unique speakers in a list:
#### Need to update for list instead of Quote_ID class

unique_speakers = set()
totalwords=0
for quote in quote_id_list:
   unique_speakers.add(quote.speaker)
   totalwords+=len(quote.quote)

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(unique_speakers)
print(totalwords)
"""
"""
#### Printout of the sentiment and polarity
#### Need to update for list instead of Quote_ID class

for quote in quote_id_list:
    print("Name: "+ quote.speaker + "\n" +
          "Quote: "+ quote.quote + "\n" +
          "Sentiment and Polarity: " + str(quote.sentiment) + " " + str(quote.polarity)
          )
"""

df = DataFrame(quote_id_list, columns=headers)

