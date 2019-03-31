"""
Natural language features defind on a single Comment.
"""

import logging

import nltk
from polyglot.detect import Detector
from textblob import TextBlob

from comment import Comment
from feature_extraction.nl_sets import *

logging.basicConfig(filename='./output.log')

def _blob(comment: Comment):
    if comment.blob:
        return comment.blob
    else:
        blob = TextBlob(comment.body)
        comment.blob = blob
        return blob


def comment_languge(comment: Comment):
    d = Detector(comment.body)
    if not d.reliable:
        return 'un'
    else:
        return d.languages[0].code


def word_count(comment: Comment):
    return len(_blob(comment).words)


def percent_first_pronouns(comment: Comment):
    if comment.stats.word_count is None:
        raise Exception("Must calculate word count first.")

    if comment.stats.word_count == 0:
        return None

    prp = [w for w,t in _blob(comment).tags if t == 'PRP']
    prp_count = len([p for p in prp if p in eng_prp_first])
    return prp_count / comment.stats.word_count


def percent_second_pronouns(comment: Comment):
    if comment.stats.word_count is None:
        raise Exception("Must calculate word count first.")

    if comment.stats.word_count == 0:
        return None

    prp = [w for w,t in _blob(comment).tags if t == 'PRP']
    prp_count = len([p for p in prp if p in eng_prp_second])
    return prp_count / comment.stats.word_count


def percent_third_pronouns(comment: Comment):
    if comment.stats.word_count is None:
        raise Exception("Must calculate word count first.")

    if comment.stats.word_count == 0:
        return None

    prp = [w for w,t in _blob(comment).tags if t == 'PRP']
    prp_count = len([p for p in prp if p in eng_prp_third])
    return prp_count / comment.stats.word_count