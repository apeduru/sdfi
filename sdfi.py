#!/usr/bin/python3

import os
import re
import sys
import argparse
import itertools
import collections
import multiprocessing


CHUNK_SIZE = 2500000  # Process 2,500,000 bytes at a time


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
    except a-z, A-Z, and 0-9
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
        words (list): List of lists containing individual words
    Returns:
        (dict): Top 10 words and their counts in a dict
    """
    word_list = flatten(words)
    wl = collections.Counter(word_list)
    return dict(wl.most_common(10))


def scheduler(docs):
    """
    Fires up a pool of workers and schedules them to count words from small
    chunks of each doc file.
    Args:
        docs (list): a list of text docs using full path in str format
    Returns:
        (dict): the top 10 words across the list of text docs
    """
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    counts = pool.map(worker, read_file_into_chunks(docs))
    pool.close()
    pool.join()

    return consolidator(counts)


def main():
    # TODO: error handling for non-text files

    if len(sys.argv) < 2:
        print("Expected text files")
        sys.exit(1)

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
    ten_most_common_words = scheduler(docs)

    print()
    print("Documents processed:", " ".join(os.path.basename(doc) for doc in docs))
    print()
    print(ten_most_common_words)


if __name__ == '__main__':
    start = time.time()
    main()
    elapsed = time.time() - start
    print("Time: {0} ms".format(elapsed * 1000))
    sys.exit(0)
