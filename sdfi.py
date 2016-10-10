#!/usr/bin/python3

import os
import re
import sys
import itertools
import collections
import multiprocessing
import time


CHUNK_SIZE = 2500000  # Process 2,500,000 bytes at a time


def read_file_into_chunks(docs):
    """
    Args:
        docs
    Returns:
        iterator
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
    Flattens a list of lists into a single list of items in linear time
    Args:
        lol: list of lists
    Returns:
        flattened list
    """
    return list(itertools.chain.from_iterable(lol))


def tokenizer(text):
    """
    Tokenize case-insensitive string delimited by any character
    except a-z, A-Z, and 0-9
    Args:
        text: a text str
    Returns:
        list of words
    """
    return re.split('[^a-zA-Z0-9]+', text.strip(), flags=re.IGNORECASE)


def worker(text):
    """
    Args:
        text: a str that is tokenized into a list of words
    Returns:

    """
    # word_list = tokenizer(text)
    # return {word: word_list.count(word) for word in set(word_list)}
    return tokenizer(text)


def consolidator(counts):
    """
    """
    word_list = flatten(counts)
    wl = collections.Counter(word_list)
    return dict(wl.most_common(10))


def scheduler(docs):
    """
    Schedules the
    Args:
        docs: a list of full path text docs
    Returns:
        results: the top 10 words across the list of text docs
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

    docs = [os.path.abspath(doc) for doc in sys.argv[1::]]
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
