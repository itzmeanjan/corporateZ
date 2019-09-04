#!/usr/bin/python3

from functools import reduce

'''
    Takes a generator ( generating model.corporateStat.Company as stream ) as argument
    & returns a Dict[str, model.corporateStat.Company] holding all companies of a 
    certain state, categorzied as per their status, which is to be used for plotting.
'''


def categorizeAsPerCompanyStatus(dataSet):
    return reduce(lambda acc, cur: dict([(cur.status, [cur])] if not acc else ((k, [cur] + v) if k == cur.status else (k, v) for k, v in acc.items())), dataSet, {})


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
