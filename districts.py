#!/usr/bin/python3

from __future__ import annotations
from typing import List
try:
    from model.companiesUnderState import CountOfCompaniesUnderDistrict, CountOfCompaniesUnderState
    from matplotlib import pyplot as plt
    from matplotlib.ticker import MultipleLocator, PercentFormatter, NullFormatter
except ImportError as e:
    print('[!]Module Unavailable : {}'.format(str(e)))
    exit(1)


def __normalizeValues__(dataSet: List[int]) -> List[float]:
    total = sum(dataSet)
    return [(i/total)*100 for i in dataSet]


def plotDistributionOverDistricts(state: CountOfCompaniesUnderState, title: str, targetPath: str) -> bool:
    try:
        x = __normalizeValues__([i.count for i in state.districts])
        y = [i.name for i in state.districts]
        with plt.style.context('Solarize_Light2'):
            font = {
                'family': 'serif',
                'color': 'darkslategray',
                'weight': 'normal',
                'size': 12
            }
            plt.figure(figsize=(24, 12), dpi=100)
            plt.xlim(0, 100)
            plt.gca().xaxis.set_major_locator(MultipleLocator(10))
            plt.gca().xaxis.set_major_formatter(PercentFormatter())
            plt.gca().xaxis.set_minor_locator(MultipleLocator(1))
            plt.gca().xaxis.set_minor_formatter(NullFormatter())
            plt.barh(y, x, align='center', color='deepskyblue', lw=1.2)
            plt.xlabel('Presence of Companies',
                       labelpad=16, fontdict=font)
            plt.title(title, fontdict=font)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.4, quality=95, dpi=100)
            plt.close()
        return True
    except Exception:
        return False


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
