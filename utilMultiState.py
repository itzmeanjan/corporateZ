#!/usr/bin/python3


from typing import Dict
from functools import reduce
from os.path import exists, dirname, basename
from os import mkdir
from re import compile as reg_compile
from itertools import chain
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


'''
    Plots a PIE chart, showing usage percentage for Top 10 email
    service providers in India ( only company data I collected
    from data.gov.in was used )

    So this shows popularity of various email service providers
    among Indian Companies
'''


def plotTopEmailProvidersShare(dataSet: Dict[str, int], total: int, title: str, targetPath: str) -> bool:
    try:
        wedgeSizes = [dataSet[i] for i in dataSet]
        labels = ['{} ( {:.2f} % )'.format(i.capitalize(), dataSet[i]*100 / total)
                  for i in dataSet]
        font = {
            'family': 'serif',
            'color': '#264040',
            'weight': 'normal',
            'size': 12
        }
        plt.figure(figsize=(24, 12), dpi=100)
        patches, _ = plt.pie(wedgeSizes)
        plt.legend(patches, labels, loc='best', fontsize='medium')
        plt.title(title, fontdict=font)
        plt.axis('equal')
        plt.tight_layout()
        plt.savefig(targetPath, bbox_inches='tight',
                    pad_inches=.5)
        plt.close()
        return True
    except Exception:
        return False


'''
    Merges two count holder dictionaries (one holding everything calculated upto this point )
    and another one holding record for a certain state ( which we just processed )
    will return merged one, which is to be used as next accumulated dictionary,
    holding everything upto this point

    Can be used for simply merging two Dict[str, int]
'''


def __mergeTwoDicts__(first: Dict[str, int], second: Dict[str, int]) -> Dict[str, int]:
    return reduce(lambda acc, cur: dict(
        [(cur, second[cur])] + [(k, v) for k, v in acc.items()]) if cur not in acc else dict([(k, v + second[cur]) if k == cur else (k, v) for k, v in acc.items()]),
        second, first)


'''
    expected to take a chain of generator(s),
    each of them generating a stream of model.corporateStat.Company object(s),
    located in a certain State of India.

    So this chain will finally generate a list of all companies
    registered in India ( as of 21/04/2018 ), when iterated over

    And finally giving us a Dict[str, int], holding a distribution
    of email provider(s) & their corresponding count
'''


def extractAllCompanyEmailProvider(dataStream: map) -> (Dict[str, int], int):
    # Extracts email service provider's name using regular expression

    def __getEmailProvider__(email: str) -> str:
        matchObj = reg.search(email)
        return matchObj.group().lower() if(matchObj) else None

    # Increments usage count email service provider & returns updated Dictionary
    def __updateCounter__(holder: Dict[str, int], email: str) -> Dict[str, int]:
        if(email):
            holder.update({email: holder.get(email, 0) + 1})
        return holder
        '''
        return holder if not email else dict([(email, 1)] + [(k, v) for k, v in holder.items()]) if email not in holder else dict(
            [(k, v + 1) if k == email else (k, v) for k, v in holder.items()])
        '''

    # Keeps only top 5 elements ( having highest usage count ) in dictionary
    def __cleanupCounter__(holder: Dict[str, int], count: int, findTotal: bool = True) -> Dict[str, int]:
        nonlocal total
        total += sum(holder.values()) if findTotal else 0
        return dict(map(lambda v: (v, holder[v]), sorted(
            holder, key=lambda v: holder[v], reverse=True)[:count]))

    try:
        total = 0
        reg = reg_compile(r'(?<=@)[^.]+(?=\.)')
        # processes each state of India at a time & extracts top 5
        # email service providers, finally we calculate top 5
        # email service providers used by companies spread across different states of India
        return __cleanupCounter__(reduce(lambda acc, cur:
                                         __mergeTwoDicts__(acc, __cleanupCounter__(
                                             reduce(lambda acc, cur: __updateCounter__(
                                                 acc, __getEmailProvider__(cur.email)), cur, {}), 10)), dataStream, {}), 10, findTotal=False), total
    except Exception:
        return None


'''
    Plots `How many companies are registered under which RoC` data,
    in a PIE chart, which is exported into a target file
'''


def plotAllRoCStatistics(data: Dict[str, int], targetPath: str) -> bool:
    try:
        # removing those records which didn't have any useful information regarding their RoC
        data.pop('NA', None)
        y = sorted(data, key=lambda e: data[e], reverse=True)
        y_pos = range(len(y))
        x = [data[i] for i in y]
        with plt.style.context('ggplot'):
            font = {
                'family': 'serif',
                'style': 'normal',
                'color': '#264040',
                'weight': 'regular',
                'size': 16
            }
            plt.figure(figsize=(24, 12), dpi=100)
            plt.barh(y_pos, x, align='center', color='cornflowerblue',
                     lw=1.6, joinstyle='miter')
            plt.gca().yaxis.set_ticks(y_pos)
            plt.gca().yaxis.set_ticklabels(y)
            plt.xlabel('# of Companies Registered', fontdict=font, labelpad=16)
            plt.title('Company Registration under RoC(s)',
                      fontdict=font, pad=12)
            plt.tight_layout()
            plt.savefig(targetPath, bbox_inches='tight',
                        pad_inches=.5, dpi=100, format=basename(targetPath).split('.')[-1])
            plt.close()
        return True
    except Exception:
        return False


'''
    Extracts how many companies are registered under which RoC ( Registrar of Companies ),
    all over India
'''


def extractRoCStatForAllCompanies(dataStream: map) -> Dict[str, int]:
    try:
        return reduce(lambda acc, cur:
                      __mergeTwoDicts__(acc, reduce(
                          lambda accInner, curInner:
                          dict([(curInner.registrarOfCompanies, 1)] + [(k, v) for k, v in accInner.items()]) if curInner.registrarOfCompanies not in accInner else dict([(k, v+1) if k == curInner.registrarOfCompanies else (k, v) for k, v in accInner.items()]), cur, {})),
                      dataStream, {})
    except Exception:
        return None


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
