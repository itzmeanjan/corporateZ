#!/usr/bin/python3

from re import compile as reg_compile
from os.path import basename
from functools import reduce
try:
    from model.corporateStat import CompaniesUnderState
    from util import *
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main(targetPath='./data/mca_westbengal_21042018.csv') -> float:
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

    try:
        companiesUnderState = CompaniesUnderState.importFromCSV(
            __extract_state__(basename(targetPath)), targetPath=targetPath)
        return __divide__(
            *__calculateSuccess__([
                plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyStatus(
                    companiesUnderState.companies), './plots/{}_company_status.png'.format(basename(targetPath)[:-4]), 'Status of Companies in West Bengal'),
                plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyClass(
                    companiesUnderState.companies), './plots/{}_company_class.png'.format(basename(targetPath)[:-4]), 'Class of Companies in West Bengal'),
                plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyCategory(
                    companiesUnderState.companies), './plots/{}_company_category.png'.format(basename(targetPath)[:-4]), 'Category of Companies in West Bengal'),
                plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanySubCategory(
                    companiesUnderState.companies), './plots/{}_company_subCategory.png'.format(basename(targetPath)[:-4]), 'SubCategory of Companies in West Bengal'),
                plotCategorizedCompanyDataForACertainState(categorizeAsPerCompanyPrincipalBusinessActivity(
                    companiesUnderState.companies), './plots/{}_company_principalBusinessActivity.png'.format(basename(targetPath)[:-4]), 'Principal Business Activity of Companies in West Bengal')
            ])
        )  # calculating rate of success of these operation(s)
    except Exception:
        return 0.0


if __name__ == '__main__':
    try:
        print('Success: {} %'.format(main()*100))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
