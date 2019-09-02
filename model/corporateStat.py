#!/usr/bin/python3

from datetime import date
from functools import reduce
from re import compile as regex_compile


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

    @property
    def dateOfRegistration(self):
        return None if self._dateOfRegistration == 'NA' else date(*[int(i) for i in self._dateOfRegistration.split('-')[-1::-1]])


class CompaniesUnderState:
    def __init__(self, state, companies):
        self.state = state
        self.companies = companies

    @staticmethod
    def importFromCSV(state, targetPath):

        def __fixCommaIssueInAddress__(stringToFix):
            # this regex will find out a certain substring ( within a string ), present under double quotation
            # multiple of them can be extracted using re.findall() method
            regex = regex_compile(r'\"([^"]*)\"')
            matches = regex.findall(stringToFix)
            return stringToFix if not matches else reduce(lambda acc, cur: acc.replace(
                cur, cur.replace(',', '').replace('"', '')), matches, stringToFix)

        companiesUnderStateObject = None
        try:
            with open(targetPath, mode='r', encoding='ISO-8859-1') as fd:
                companiesUnderStateObject = CompaniesUnderState(
                    state, (Company(*__fixCommaIssueInAddress__(line).split(',')[:-2]) for line in fd.readlines()[1:]))
        except Exception as e:
            print(e)
            companiesUnderStateObject = None
        finally:
            return companiesUnderStateObject


if __name__ == '__main__':
    print('[!]This module is designed to be used as a backend handler')
    exit(0)
