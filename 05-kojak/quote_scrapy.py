import re
import os
import pprint
import csv
import codecs

class QuoteID(object):

    def __init__(self, quote, speaker):
        self.quote = quote
        self.speaker = speaker

characters_file = '/home/bf2398/Metis/projects/05-kojak/.gitignore/files/characters.csv'
book = open("/home/bf2398/Metis/projects/05-kojak/.gitignore/files/book1.txt","r")

characters = []
with open(characters_file) as csvData:
    csvReader = csv.reader(csvData)
    for row in csvReader:
        characters.append(row[0])

page_nums = re.compile('[\d]+\\n')
apostrophes = re.compile(r"\\'")
in_quote = False
quote = ''
non_quote = ''
book_splice = []

for line in book:
    for char in line:
        if char == '"' and not in_quote:
            in_quote = True
            non_quote = page_nums.sub('',non_quote)
            non_quote = non_quote.replace('\n',' ')
            non_quote = apostrophes.sub('',non_quote)
            non_quote = non_quote.replace("\\x0c",'')
            book_splice.append(non_quote)
            non_quote = ''
        elif char == '"' and in_quote:
            in_quote = False
            quote += '"'
            quote = page_nums.sub('',quote)
            quote = quote.replace('\n',' ')
            quote = apostrophes.sub('',quote)
            quote = quote.replace("\\x0c","")
            book_splice.append(quote)
            quote = '"'
        elif in_quote:
            quote += char
        elif not in_quote:
            non_quote += char

book_splice.append('')
for i in range(len(book_splice)-1,-1,-1):
    if len(book_splice[i]) == 0:
        del book_splice[i]

quote_id_list = []
for i, line in enumerate(book_splice):
    if line[0]=='"':
        prev_line = book_splice[i-1]
        if(i!=len(book_splice)-1):
            next_line = book_splice[i+1]
        character = 'Unknown'
        closest_index = -1
        for j in characters:
            if prev_line.find(j)>-1:
                prev_index = len(prev_line)-prev_line.find(j)-len(j)
                if closest_index == -1:
                    closet_index = prev_index
                    character = j
                elif closest_index > prev_index:
                    closest_index = prev_index
                    character = j
            if next_line.find(j)>-1:
                next_index = next_line.find(j)
                if closest_index == -1:
                    closet_index = next_index
                    character = j
                elif closet_index > next_index:
                    closet_index = next_index
                    character = j
        quote_id_list.append(QuoteID(line,character))

print(len(quote_id_list))
for i, q in enumerate(quote_id_list):
    print(q.speaker+':')
    print(q.quote)
