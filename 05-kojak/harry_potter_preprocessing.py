# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 11:10:20 2020

@author: Brendan Non-Admin
"""
import os
from book import Book, BookChapter
import unicodedata

datapath = os.path.join('Data', 'Book TXTs')

os.listdir(datapath)

book_filenames = [
    'philosophers_stone.txt',
    'chamber_of_secrets.txt',
    'prisoner_of_azkaban.txt',
    'goblet_of_fire.txt',
    'order_of_the_phoenix.txt',
    'half_blood_prince.txt',
    'deathly_hallows.txt',
]

books = list()
for book_filename in book_filenames:
    book_name_titlecase = (book_filename 
        .replace('.txt', '')
        .replace('_', ' ').title()
    )
    
    filepath = os.path.join(datapath, book_filename)
    
    with open(filepath, 'r') as f:
        book_text = unicodedata.normalize("NFKD", f.read())
    
    unprocessed_book_chapters = list(
        filter(lambda x: len(x) !=0, book_text.split('\n'))
    )
    
    
    book_chapters = list()
    for chapter_number, full_chapter_text in enumerate(unprocessed_book_chapters):
        try:
            chapter = BookChapter(full_chapter_text.strip(), chapter_number + 1)
            book_chapters.append(chapter)
        except Exception as e:
            chapter_excerpt = full_chapter_text[0:min(500, len(full_chapter_text))] + '...'
            print(f"Book: {book_name_titlecase}\n"
                  f"chapter_number: {chapter_number + 1}\n"
                  f"full_chapter_text: {chapter_excerpt}\n\n")
            raise e
    
    book = Book(book_name_titlecase, book_chapters)
    books.append(book)