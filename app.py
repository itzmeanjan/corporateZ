#!/usr/bin/python3

from re import compile as reg_compile
from os.path import basename, join
from os import listdir
from functools import reduce
from itertools import chain
try:
    from model.corporateStat import CompaniesUnderState
    from util import *
    from utilMultiState import plotAllCompaniesByStateUsingStatus, extractAllCompanyEmailProvider
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)

'''
    Reads from each CSV datafiles present in `./data/`,
    holding Ministry of Corporate Affair's ( M.C.A. ) Company Data
    for a certain state & generates 6 plots for each of them.

    5 of them will be PIE charts & 1 will be simple plotting
    of registration year vs. #-of companies registered in that year.
'''


def main(targetPath='./data/') -> float:
    '''
        Given a CSV data file name, it'll simply extract
        State name using Regular Expression(s)

        In case of error, returns None
    '''
    def __extract_state__(fromIt: str) -> str:
        match_obj = reg_compile(r'^mca_(\w+)_[0-9]{8,}\.csv$').match(fromIt)
        return match_obj.group(1).capitalize() if match_obj else None

    '''
        A utility function to calculate division of 2-element tuple
    '''
    def __divide__(a: int, b: int) -> float:
        return 0 if not b else a/b

    '''
        Given a iterable of boolean values, it'll return a 2-element tuple,
        where first one will hold number of Truth values & last one will keep
        total # of values we're considering
    '''
    def __calculateSuccess__(result):
        return reduce(lambda acc, cur: (acc[0] + 1, acc[1]+1) if cur else (acc[0], acc[1]+1), result, (0, 0))

    def __getAllPossibleCompanyStatus__(companyDataSet):
        return reduce(lambda acc, cur: acc.union(set(
            companyDataSet[cur].keys())), companyDataSet, set())

    try:
        '''
        return __divide__(
            *__calculateSuccess__(
                reduce(lambda acc, cur: [
                    plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyStatus(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_status.png'.format(basename(cur)[:-4]), 'Status of Companies in {}'.format(__extract_state__(basename(cur)))),
                    plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyClass(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_class.png'.format(basename(cur)[:-4]), 'Class of Companies in {}'.format(__extract_state__(basename(cur)))),
                    plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyCategory(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_category.png'.format(basename(cur)[:-4]), 'Category of Companies in {}'.format(__extract_state__(basename(cur)))),
                    plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanySubCategory(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_subCategory.png'.format(basename(cur)[:-4]), 'SubCategory of Companies in {}'.format(__extract_state__(basename(cur)))),
                    plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyPrincipalBusinessActivity(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_principalBusinessActivity.png'.format(basename(cur)[:-4]), 'Principal Business Activity of Companies in {}'.format(__extract_state__(basename(cur)))),
                    plotCompanyRegistrationDateWiseCategorizedData(categorizeAsPerCompanyDateOfRegistration(
                        CompaniesUnderState.importFromCSV(
                            __extract_state__(basename(cur)), targetPath=cur).companies), './plots/{}_company_dateOfRegistration.png'.format(basename(cur)[:-4]), 'Registration of Companies in {}'.format(__extract_state__(basename(cur))))
                ] + acc,
                    map(lambda v: join(targetPath, v),
                        filter(lambda v: v.endswith('csv'), listdir(targetPath))), [])
            )
        )  # calculating rate of success of these operation(s)
        allCompanyStatus = dict(map(lambda v:
                                    (__extract_state__(basename(v)), categorizeAsPerCompanyStatus(CompaniesUnderState.importFromCSV(
                                        __extract_state__(basename(v)), targetPath=v).companies)),
                                    map(lambda v: join(targetPath, v),
                                        filter(lambda v: v.endswith('csv'), listdir(targetPath)))))
        return __divide__(
            *__calculateSuccess__(
                map(lambda v: plotAllCompaniesByStateUsingStatus(
                    allCompanyStatus, v,
                    './allCompanyStatusPlots/mca_all_{}_companies.png'.format(v.replace(' ', '_').lower())),
                    __getAllPossibleCompanyStatus__(allCompanyStatus))
            ))
        '''
        allCompanies = map(
            lambda v: CompaniesUnderState.importFromCSV(
                __extract_state__(v), targetPath=join(targetPath, v)).companies,
            filter(
                lambda v: v.endswith('csv'), listdir(targetPath)))
        print(extractAllCompanyEmailProvider(allCompanies))
        return 1.0
    except Exception:
        return 0.0


if __name__ == '__main__':
    try:
        print('Success: {} %'.format(main()*100))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
