# Inspired by ABingo: www.bingocardcreator.com/abingo

HANDY_Z_SCORE_CHEATSHEET = (
    (1, float('-Inf')),
    (0.10, 1.29),
    (0.05, 1.65),
    (0.025, 1.96),
    (0.01, 2.33),
    (0.001, 3.08))[::-1]

PERCENTAGES = {0.10: '90%', 0.05: '95%', 0.01: '99%', 0.001: '99.9%'}

DESCRIPTION_IN_WORDS = {0.10: 'fairly confident', 0.05: 'confident',
                        0.01: 'very confident', 0.001: 'extremely confident'}


def calculate_variance(n, p):
    """
    Calculate the sample variance for a binominal distribution
    """
    return p * (1 - p) / n


def zscore(alternatives):
    """
    Calculate the z-score
    """
    if len(alternatives) != 2:
        raise ValueError("Cant compute more than two alternatives")

    n0 = alternatives[0].participants
    n1 = alternatives[1].participants

    if n0 == 0 or n1 == 0:
        raise ValueError("No participants for at least one of the experiments")

    hits0 = alternatives[0].hits
    hits1 = alternatives[1].hits

    cr0 = n0 / hits0  # cr: conversion rate
    cr1 = n1 / hits1

    numerator = cr0 - cr1
    variance0 = calculate_variance(n0, cr0)
    variance1 = calculate_variance(n1, cr1)
    return numerator / ((variance0 + variance1) ** 0.5)


def best_p(zscore):
    """
    Find the the p-value using a table
    """
    for p, z in HANDY_Z_SCORE_CHEATSHEET:
        if zscore > z:
            break

    return (p, z)


def test(data):
    pass


def describe(alternatives, p, best, worst):
    index_best = 0
    index_worst = 1

    words = ""

    n0 = alternatives[0].participants
    n1 = alternatives[1].participants

    if n0 < 10 or n1 < 10:
        words += "Take these results with a grain of salt since your " + \
          "samples are so small: "

    words += "The best alternative you have is: %s, which had " % \
      alternatives[best].content
    words += "%d conversions from %d participants " \
      % (alternatives[best].hits, alternatives[best].participants)
    words += "(%f).  The other alternative was %s, " \
      % (alternatives[best].hits / alternatives[best].participants,
         alternatives[worst].content)
    words += "which had %d conversions from %d participants " \
      % (alternatives[worst].hits, alternatives[worst].participants)
    words += "(%f). " % (alternatives[best].hits /
                         alternatives[best].participants)

    if p == 1:
        words += "However, this difference is not statistically significant."
    else:
        words += "This difference is %f likely to be " % p
        words += " statistically significant, which means you can be "
        words += "%s that it is the result of your alternatives actually " \
          % "foo"
        words += " mattering, rather than "
        words += "being due to random chance.  However, this statistical test"
        words += " can't measure how likely the currently "
        words += "observed magnitude of the difference is to be accurate or"
        words + " not.  It only says \"better\", not \"better "
        words += "by so much\"."

    return words
