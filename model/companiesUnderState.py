#!/usr/bin/python3

from __future__ import annotations
from typing import List, Tuple
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

    '''
        Returns requested # of top districts
        ( in terms of registered company count )
        from this State
    '''

    def getTopXDistricts(self, x: int) -> List[CountOfCompaniesUnderDistrict]:
        return sorted(self.districts, key=lambda e: e.count, reverse=True)[:x]

    def __str__(self):
        super().__str__()
        return 'State : {} - {}'.format(self.name, len(self.districts))


'''
    This function takes a collection of CountOfCompaniesUnderState objects,
    each of them holding distribution of companies over Districts
    under current State.

    Now we'll iterate over each districts & pull out their name &
    count of registered companies, which is to be eventually sorted
    descendingly, so that we can pick up first X elements,
    which will be returned
'''


def getTopXDistricts(states: List[CountOfCompaniesUnderState], x: int) -> List[Tuple[str, int]]:
    return sorted(reduce(lambda acc, cur:
                         acc + reduce(lambda accInner, curInner:
                                      accInner +
                                      [('{}, {}'.format(
                                          curInner.name, cur.name), curInner.count)],
                                      cur.districts, []),
                         states, []), key=lambda e: e[1], reverse=True)[:x]


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(1)
