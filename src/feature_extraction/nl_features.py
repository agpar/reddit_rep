"""
Natural language features defind on a single Comment.
"""

import logging

import nltk
from polyglot.detect import Detector
from textblob import TextBlob
from profanity_check import predict_prob as profanity

from comment import Comment, CommentFeatures
from feature_extraction.nl_sets import *

logging.basicConfig(filename='./output.log')

def compute_nl_features(c: Comment):
    c.stats = CommentFeatures()
    stats = c.stats

    stats['lang'] = comment_languge(c)
    stats['word_count'] = word_count(c)
    stats['prp_first'] = percent_first_pronouns(c)
    stats['prp_second'] = percent_second_pronouns(c)
    stats['prp_third'] = percent_third_pronouns(c)
    stats['sent'] = sentiment(c)
    stats['punc_ques'] = percent_punc_question(c)
    stats['punc_excl'] = percent_punc_exclamation(c)
    stats['punc_per'] = percent_punc_period(c)
    stats['punc'] = percent_punc(c)
    stats['profanity'] = profanity_prob(c)


def _blob(comment: Comment):
    if comment.blob:
        return comment.blob
    else:
        blob = TextBlob(comment.body)
        comment.blob = blob
        return blob


def comment_languge(comment: Comment):
    if comment.body == '[deleted]':
        return 'en'

    d = Detector(comment.body, quiet=True)
    if not d.reliable:
        return 'un'
    else:
        return d.languages[0].code


def word_count(comment: Comment):
    return len(_blob(comment).words)


def should_nl_bail(comment: Comment):
    if comment.stats.get('word_count') is None:
        raise Exception("Must calculate word count first.")

    if comment.stats['word_count'] == 0:
        return True

    if comment.stats['lang'] != 'en':
        return True

    return False


def percent_first_pronouns(comment: Comment):
    if should_nl_bail(comment):
        return None

    prp = [w.lower() for w,t in _blob(comment).tags if t == 'PRP']
    if len(prp) == 0:
        return 0
    prp_count = len([p for p in prp if p in eng_prp_first])
    return prp_count / len(prp)


def percent_second_pronouns(comment: Comment):
    if should_nl_bail(comment):
        return None

    prp = [w.lower() for w,t in _blob(comment).tags if t == 'PRP']
    if len(prp) == 0:
        return 0
    prp_count = len([p for p in prp if p in eng_prp_second])
    return prp_count / len(prp)


def percent_third_pronouns(comment: Comment):
    if should_nl_bail(comment):
        return None

    prp = [w.lower() for w,t in _blob(comment).tags if t == 'PRP']
    if len(prp) == 0:
        return 0
    prp_count = len([p for p in prp if p in eng_prp_third])
    return prp_count / len(prp)

def sentiment(comment: Comment):
    if should_nl_bail(comment):
        return None

    return _blob(comment).polarity


def percent_punc_question(comment: Comment):
    if should_nl_bail(comment):
        return None

    punc = [p for p in _blob(comment).tokens if p in eng_punc]
    if len(punc) == 0:
        return 0
    ques = [p for p in punc if p == '?']
    return len(ques) / len(punc)


def percent_punc_exclamation(comment: Comment):
    if should_nl_bail(comment):
        return None

    punc = [p for p in _blob(comment).tokens if p in eng_punc]
    if len(punc) == 0:
        return 0
    excl = [p for p in punc if p == '!']
    return len(excl) / len(punc)


def percent_punc_period(comment: Comment):
    if should_nl_bail(comment):
        return None

    punc = [p for p in _blob(comment).tokens if p in eng_punc]
    if len(punc) == 0:
        return 0
    per = [p for p in punc if p == '.']
    return len(per) / len(punc)


def percent_punc(comment: Comment):
    if should_nl_bail(comment):
        return None
    punc = [p for p in _blob(comment).tokens if p in eng_punc]
    if len(punc) == 0:
        return 0
    return len(punc)/len(_blob(comment).tokens)


def profanity_prob(comment: Comment):
    if should_nl_bail(comment):
        return None
    return float(profanity([comment.body])[0])