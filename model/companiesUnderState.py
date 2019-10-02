#!/usr/bin/python3

from __future__ import annotations
from typing import List
from functools import reduce

'''
    Holds count of companies present in a certain district of India,
    which is to be used for plotting distribution of companies across Indian States,
    in district level
'''


class CountOfCompaniesUnderDistrict(object):
    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count

    '''
        Utility method for incrementing count of companies in this district
    '''

    def incrementCount(self, by: int):
        self.count += by

    def __str__(self):
        super().__str__()
        return 'District : {} - {}'.format(self.name, self.count)


'''
    Holds all districts present under an Indian State,
    along with their corresponding `# of companies present`
'''


class CountOfCompaniesUnderState(object):
    def __init__(self, name: str, districts: List[CountOfCompaniesUnderDistrict]):
        self.name = name
        self.districts = districts

    '''
        Appends new district record for a certain state
        ( when that district isn't yet present ) or
        increments count of companies for a certain district 
        ( otherwise found districts company count is incremented )
    '''

    def updateCountForDistrict(self, districtName: str, by: int):
        found: CountOfCompaniesUnderDistrict = reduce(lambda acc, cur: cur if cur.name ==
                                                      districtName else acc, self.districts, None)
        if found:
            found.incrementCount(by)
        else:
            self.districts.append(
                CountOfCompaniesUnderDistrict(districtName, by))

    def __str__(self):
        super().__str__()
        return 'State : {} - {}'.format(self.name, len(self.districts))


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(1)
