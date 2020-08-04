# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 09:33:06 2020

@author: Brendan Non-Admin
"""

import re

class Book():
    
    def __init__(self, book_name, book_chapters):
        self.book_name = book_name
        self.book_chapters = book_chapters
    
    def __repr__(self):
        return "Book Object --- {}".format(self.book_name)



class BookChapter():
    
    def __init__(self, full_chapter_text, chapter_number):
        args = [full_chapter_text, chapter_number]
        self.chapter_name, self.chapter_text = BookChapter.split_full_chapter_text(*args)
        self.chapter_number = chapter_number
        
    @staticmethod
    def split_full_chapter_text(full_chapter_text, chapter_number):
        """
        The split doesn't work for all books currently
        Need to update
        """
        split = re.split(r'\s{2,}', full_chapter_text, maxsplit=1)
        if len(split) == 1:
            return f"Chapter {chapter_number}", full_chapter_text
        return split
    
    def __repr__(self):
        return "Book Chapter Object --- {}".format(self.chapter_name)