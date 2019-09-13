#!/usr/bin/python3


from typing import Dict
from functools import reduce
from os.path import exists, dirname
from os import mkdir
try:
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def plotAllCompaniesByStateUsingStatus(dataSet: Dict, status: str, targetPath: str) -> bool:
    '''
        calculates total # of companies we're considering
        for a certain state, so that calculation of percentage
        becomes feasible
    '''
    def __calculateTotalNumberOfCompaniesinState__(data: Dict) -> int:
        return sum([data[i] for i in data])

    '''
        calculates percentage of companies in a certain state
        for a specified `status`
    '''
    def __calculatePercentageOfCompaniesOfSimilarStatusInState__(data: Dict) -> float:
        return data.get(status, 0) * 100 / __calculateTotalNumberOfCompaniesinState__(data)

    try:
        if(not exists(dirname(targetPath))):
            mkdir(dirname(targetPath))
        # extracting percentage of companies for a certain type of `status`, present in a State
        extractedData = dict(reduce(lambda acc, cur: [(cur, __calculatePercentageOfCompaniesOfSimilarStatusInState__(dataSet[cur]))
                                                      ] + acc, dataSet, []))
        # checks whether this dataset is having any useful data for all states or not
        # if no, then we'll simply be raising an exception
        # otherwise it'll draw BAR chart
        if(all(map(
                lambda v: False if extractedData[v] > 0 else True, extractedData))):
            raise Exception('Empty Dataset')
        y = sorted(extractedData, key=lambda v: extractedData[v], reverse=True)
        y_pos = range(len(y))
        x = [extractedData[i] for i in y]
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'color': '#264040',
                'weight': 'normal',
                'size': 12
            }
            # creates a figure of size 2400x1200
            plt.figure(figsize=(24, 12), dpi=100)
            plt.xlim((0, 100))
            plt.gca().xaxis.set_major_locator(MultipleLocator(10))
            plt.gca().xaxis.set_major_formatter(PercentFormatter())
            plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
            plt.barh(y_pos, x, align='center', color='cornflowerblue', lw=1.6)
            plt.gca().yaxis.set_ticks(y_pos)
            plt.gca().yaxis.set_ticklabels(y)
            plt.xlabel('`{}` Companies'.format(
                status), fontdict=font, labelpad=12)
            plt.title('`{}` Companies in Different States of India'.format(
                status), fontdict=font, pad=12)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight', pad_inches=.5)
            plt.close()
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
