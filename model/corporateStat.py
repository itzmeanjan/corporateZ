#!/usr/bin/python3

from datetime import date
from functools import reduce
from re import compile as regex_compile

'''
    This class is expected to hold data for a certain company registered
    under some RoC

    What we mostly do is, we read from CSV data file ( which is actually source dataset ),
    & convert that into python objects, in hope that it'll be easier for us to use that
    formatted, structured & objectified data.
'''


class Company:
    def __init__(self, cin, name, status, companyClass, category, subCategory, dor, state, authorizedCap, paidUpCap, industrialClass, businessActivity, address, roc, email):
        self.corporateIdentificationNumber = cin
        self.name = name
        self.status = status
        self.companyClass = companyClass
        self.category = category
        self.subCategory = subCategory
        self._dateOfRegistration = dor
        self.registeredState = state
        self.authorizedCapital = authorizedCap
        self.paidUpCapital = paidUpCap
        self.industrialClass = industrialClass
        self.principalBusinessActivity = businessActivity
        self.registeredOfficeAddress = address
        self.registrarOfCompanies = roc
        self.email = email

    '''
        this property is expected to convert dateOfRegistration of this company
        from string to an instance of Date class ( which makes manipulation of Date easier)
    '''
    @property
    def dateOfRegistration(self):
        return None if self._dateOfRegistration.lower() == 'na' else date(*[int(i) for i in self._dateOfRegistration.split('-')[-1::-1]])


'''
    Designed to hold a list of all companies present under one certain State of India

    State, about which we're currently talking, can also be looked up from an instance of this class
'''


class CompaniesUnderState:
    def __init__(self, state, companies):
        self.state = state
        self.companies = companies

    '''
        This static method is expected to read from a CSV data file ( holding information about a certain State ),
        and create an instance of this class, holding all data present in CSV file, in objectified form, so manipulating it
        becomes easier
    '''
    @staticmethod
    def importFromCSV(state, targetPath):
        '''
            CSV dataset to be processed is pretty malformed like
            we can't just use `,` ( comma ) as field seperator in CSV.

            Cause there's `,` ( comma ) present in unexpected places, so
            what we're going to do is replace all those unexpected `,` ( commas )
            using '' ( blank string ).

            One good thing that makes our job easier, is that all malformed ( comma added ) substrings 
            are places within double quotations.

            So we're going to use regular expression for extracting all those substrings,
            which are having `,` within it, and replace that using properly formatted substring(s)

            And we finally construct properly formatted string, using `reduce()`.
        '''
        def __fixCommaIssueInAddress__(stringToFix):
            # this regex will find out a certain substring ( within a string ), present under double quotation
            # multiple of them can be extracted using re.findall() method
            return reduce(lambda acc, cur: acc.replace(
                cur, cur.replace(',', '').replace('"', '')), regex_compile(r'\"([^"]*)\"').findall(stringToFix), stringToFix)

        companiesUnderStateObject = None  # this is what's to be returned
        try:
            # reads CSV file content in splitted line form,
            # which is to be processed for creating an instance of Company class
            with open(targetPath, mode='r', encoding='ISO-8859-1') as fd:
                companiesUnderStateObject = CompaniesUnderState(
                    state, [Company(*__fixCommaIssueInAddress__(line).split(',')[:-2]) for line in fd.readlines()[1:]])
        except Exception:
            companiesUnderStateObject = None
        finally:
            return companiesUnderStateObject


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
