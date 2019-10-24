#!/usr/bin/python3

from __future__ import annotations
from re import compile as reg_compile
from os.path import basename, join
from os import listdir
from functools import reduce
from itertools import chain
try:
    from model.corporateStat import CompaniesUnderState
    from model.post import PostOfficeGraph
    from util import *
    from utilMultiState import *
    from districts import plotDistributionOverDistricts
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
        Given a iterable of boolean values, it'll return a 2-element tuple,
        where first one will hold number of Truth values & last one will keep
        total # of values we're considering
    '''
    def __calculateSuccess__(result: List[bool]) -> float:
        '''
            A utility function to calculate division of 2-element tuple
        '''
        def __divide__(a: int, b: int) -> float:
            return 0 if not b else a/b

        return __divide__(
            *reduce(
                lambda acc, cur: (acc[0] + 1, acc[1] +
                                  1) if cur else (acc[0], acc[1]+1),
                result, (0, 0)))

    def __getAllPossibleCompanyStatus__(companyDataSet):
        return reduce(lambda acc, cur: acc.union(set(
            companyDataSet[cur].keys())), companyDataSet, set())

    try:
        allCompanyStatus = dict(map(lambda v:
                                    (__extract_state__(basename(v)), categorizeAsPerCompanyStatus(CompaniesUnderState.importFromCSV(
                                        __extract_state__(basename(v)), targetPath=v).companies)),
                                    map(lambda v: join(targetPath, v),
                                        filter(lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath)))))
        return __calculateSuccess__(
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
                    filter(lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath))), [])
            +
            list(map(lambda v: plotAllCompaniesByStateUsingStatus(
                allCompanyStatus, v,
                './allCompanyStatusPlots/mca_all_{}_companies.png'.format(v.replace(' ', '_').lower())),
                __getAllPossibleCompanyStatus__(allCompanyStatus)))
            +
            [plotTopEmailProvidersShare(
                *extractAllCompanyEmailProvider(
                    map(
                        lambda v: CompaniesUnderState.importFromCSV(
                            __extract_state__(v),
                            targetPath=join(targetPath, v)).companies,
                        filter(
                            lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath)))),
                'Email Service used by Companies in India',
                './plots/mca_email_service_used_by_companies.png')]
            +
            [
                plotAllRoCStatistics(
                    extractRoCStatForAllCompanies(
                        map(
                            lambda v: CompaniesUnderState.importFromCSV(
                                __extract_state__(v),
                                targetPath=join(targetPath, v)).companies,
                            filter(
                                lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath)))),
                    './plots/mca_company_registration_under_roc.png'
                )
            ]
            +
            [
                plotCompanyRegistrationDateWiseCategorizedData(
                    categorizeAsPerCompanyDateOfRegistration(
                        chain(
                            *[CompaniesUnderState.importFromCSV(
                                __extract_state__(i),
                                targetPath=join(targetPath, i)).companies for i in filter(
                                lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath))]
                        )),
                    './plots/registration_of_companies_around_years_all_india.png',
                    'Rate of Registration of Companies around the Years'
                )
            ]
            +
            [plotDistributionOverDistricts(i,
                                           'Distribution of Companies over Districts in {}, India'.format(
                                               i.name),
                                           'plots/distributionOfCompaniesOverDistrictsIn{}.jpg'.format(
                                               '_'.join(i.name.lower().split())))
             for i in pincodeToDistrictNameMapper(
                classifyCompaniesUsingPinCodeOfRegisteredAddress(
                    chain(
                        *[CompaniesUnderState.importFromCSV(
                            __extract_state__(i),
                            targetPath=join(targetPath, i)).companies for i in filter(
                            lambda v: v.startswith('mca') and v.endswith('csv'), listdir(targetPath))]
                    )
                ),
                PostOfficeGraph.importFromCSV(
                    './data/all_india_PO_list_without_APS_offices_ver2_lat_long.csv')
            )]
        )
    except Exception as e:
        print('[!]Error : {}'.format(e))
        return 0.0


if __name__ == '__main__':
    try:
        print('Success: {} %'.format(main()*100))
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
