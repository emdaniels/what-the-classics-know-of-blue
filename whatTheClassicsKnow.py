#! /usr/bin/env python2

"""
Filename: whatTheClassicsKnow.py
Author: Emily Daniels
Date: January 2016
Purpose: Creates a text of sentences that contain the word 'blue'.
"""

import re
import os


def read_text(filename):
    """
    Reads the text from a text file.
    """
    with open(filename, "rb") as f:
        text = f.read()
    return text


def split_into_sentences(text):
    """
    Split sentences on .?! "" and not on abbreviations of titles.
    """
    sentence_enders = re.compile(r"""
        # Split sentences on whitespace between them.
        (?:               # Group for two positive lookbehinds.
        (?<=[.!?])      # Either an end of sentence punct,
        | (?<=[.!?]['"])  # or end of sentence punct and quote.
        )                 # End group of two positive lookbehinds.
        (?<!  Mr\.   )    # Don't end sentence on "Mr."
        (?<!  Mrs\.  )    # Don't end sentence on "Mrs."
        (?<!  Ms\.   )    # Don't end sentence on "Ms."
        (?<!  Jr\.   )    # Don't end sentence on "Jr."
        (?<!  Dr\.   )    # Don't end sentence on "Dr."
        (?<!  Prof\. )    # Don't end sentence on "Prof."
        (?<!  Sr\.   )    # Don't end sentence on "Sr."
        (?<!  St\.   )    # Don't end sentence on "St."
        (?<!  M\.   )    # Don't end sentence on "M."
        \s+               # Split on whitespace between sentences.
        """, re.IGNORECASE | re.VERBOSE)
    return sentence_enders.split(text)


def extract_sentences(modifier, split_text):
    """
    Extracts the sentences that contain the modifier references.
    """
    extracted_text = []
    for sentence in split_text:
        if re.search(r"\b(?=\w)%s\b(?!\w)" % re.escape(modifier), sentence,
                     re.IGNORECASE):
            extracted_text.append(sentence)
    return extracted_text


def write_text(modifier, extracted_text):
    """
    Writes the extracted sentences to a text file.
    """
    with open("what_the_classics_know_of_" + modifier + ".txt", "wb") as f:
        for list in extracted_text:
            for line in list:
                f.write("%s\n\n" % str(line))

if __name__ == "__main__":
    modifier = 'blue'
    all_extracted_text = []
    book_dir = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                            "classics"))
    for filename in os.listdir(book_dir):
        text = read_text(os.path.join(book_dir, filename))
        split_text = split_into_sentences(text)
        extracted_text = extract_sentences(modifier, split_text)
        all_extracted_text.append(extracted_text)
    write_text(modifier, all_extracted_text)
