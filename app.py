#!/usr/bin/python3

from re import compile as reg_compile
from os.path import basename
try:
    from model.corporateStat import CompaniesUnderState
    from util import categorizeAsPerCompanyStatus, plotCompanyStatusDataForAState
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main(targetPath='./data/mca_westbengal_21042018.csv'):
    def __extract_state__(fromIt: str):
        match_obj = reg_compile(r'^mca_(\w+)_[0-9]{8,}\.csv$').match(fromIt)
        return match_obj.group(1).capitalize() if match_obj else None

    try:
        companiesUnderStateObject = CompaniesUnderState.importFromCSV(
            __extract_state__(basename(targetPath)), targetPath=targetPath)
        return plotCompanyStatusDataForAState(categorizeAsPerCompanyStatus(
            companiesUnderStateObject.companies), './plots/{}_company_status.png'.format(basename(targetPath)[:-4]))
    except Exception:
        return False


if __name__ == '__main__':
    try:
        print('Success' if main() else 'Failure')
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
