#!/usr/bin/python3

try:
    from model.corporateStat import CompaniesUnderState
except ImportError as e:
    print('[!]Module Unavailable: {}'.format(str(e)))
    exit(1)


def main(targetPath='./data/mca_westbengal_21042018.csv'):
    try:
        companiesUnderStateObject = CompaniesUnderState.importFromCSV(
            'West Bengal', targetPath=targetPath)
        for index, company in enumerate(companiesUnderStateObject.companies):
            print('{} -- {} -- {}'.format(index,
                                          company.name, company.dateOfRegistration))
        else:
            return True
    except Exception:
        return False


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\n[!]Terminated')
    finally:
        exit(0)
