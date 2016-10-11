#!/usr/bin/python3

import os
import re
import sys
import argparse
import itertools
import collections
import multiprocessing


CHUNK_SIZE = 10000  # Process 10,000 bytes at a time


def read_file_into_chunks(docs):
    """
    Split a text doc into sizable chunks defined by CHUNK_SIZE
    Args:
        docs (list): a list of text docs using full path in str format
    Yields:
        (str): an iterator of a chunk of text
    """
    for doc in docs:
        with open(doc, 'r') as f:
            while True:
                data = f.readlines(CHUNK_SIZE)
                if not data:
                    break
                yield ''.join(data)


def flatten(lol):
    """
    Flattens a list of lists into a single list in linear time
    Args:
        lol (list): list of lists
    Returns:
        (list): a flattened list
    """
    return list(itertools.chain.from_iterable(lol))


def tokenizer(text):
    """
    Tokenize case-insensitive string delimited by any character
    except a-z, A-Z, and 0-9 and removing empty strings.
    Args:
        text (str): a text str
    Returns:
        (list): a list of words
    """
    return re.split('[^a-zA-Z0-9]+', text.strip(), flags=re.IGNORECASE)


def worker(text):
    """
    A worker process that Tokenizes a text blob into words
    Args:
        text (str): Blob of text
    Returns:
         (list): All words found in the text blob
    """
    return tokenizer(text)


def consolidator(words):
    """
    Aggregates and counts the total
    Args:
        words (list): List containing individual words
    Returns:
        (list): Top 10 words and their counts as a tuple in decreasing order
    """
    counted_words = collections.Counter(words)
    return counted_words.most_common(10)


def scheduler(docs):
    """
    Fires up a pool of workers and schedules them to count words from small
    chunks of each doc file.
    Args:
        docs (list): a list of text docs using full path in str format
    Returns:
        (list): Top 10 words and their counts as a tuple in decreasing order
    """
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    counts_list = pool.map(worker, read_file_into_chunks(docs))
    pool.close()
    pool.join()

    return consolidator(flatten(counts_list))


def is_valid_files(docs):
    """
    Determines validity of doc arguments. Checking for file existence and is a
    text file.
    Args:
        docs (list): a list of text docs in str format
    Returns:
        (bool): T if file is valid, F otherwise

    """
    for doc in docs:
        if not os.path.isfile(doc) or os.path.splitext(doc)[1] != '.txt':
            return False
    return True


def main():
    """
    Main starting point for sdfi.
    Parses command line arguments and pretty-prints the top 10 words.
    """
    parser = argparse.ArgumentParser(
            prog='sdfi',
            description='A Simple Distributed File Indexer')
    parser.add_argument("file", nargs='+', help="file to index")
    args = parser.parse_args()

    if not is_valid_files(args.file):
        print("sdfi: File must be in text format and must exist")
        parser.print_help()
        parser.exit()

    docs = [os.path.abspath(doc) for doc in args.file]
    ten_most_common_words_and_counts = scheduler(docs)

    print()
    print("Docs processed:", " ".join(os.path.basename(doc) for doc in docs))
    print()
    print("Word : Count")
    print("------------")
    for word, count in ten_most_common_words_and_counts:
        print("{0} : {1}".format(word, count))


if __name__ == '__main__':
    main()
    sys.exit(0)
