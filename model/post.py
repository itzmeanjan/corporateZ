#!/usr/bin/python3

from typing import List, Dict
from csv import reader as csvReader
from functools import reduce


class PostOffice(object):
    def __init__(self, officeName: str, pincode: str, officeType: str, deliveryStatus: str, divisionName: str, regionName: str, circleName: str, taluk: str, districtName: str, stateName: str, children: List[PostOffice]):
        self.officeName = officeName
        self.pincode = pincode
        self.officeType = officeType
        self.deliveryStatus = deliveryStatus
        self.divisionName = divisionName
        self.regionName = regionName
        self.circleName = circleName
        self.taluk = taluk
        self.districtName = districtName
        self.stateName = stateName
        self.children = children


class PostOfficeGraph(object):
    def __init__(self, headPOs):
        self.headPostOffices = headPOs

    @staticmethod
    def importFromCSV(targetPath: str) -> PostOfficeGraph:
        def __updateRecordHolderDict__(record: PostOffice, holder: Dict[str, List[PostOffice]]) -> Dict[str, List[PostOffice]]:
            holder.update(
                {record.officeType: [record] + holder.get(record.officeType, [])})
            return holder

        graph = None
        try:
            poList = []
            with open(targetPath, mode='r', encoding='ISO-8859-1') as fd:
                poList = csvReader(fd.readlines()[1:])
            reduce(lambda acc, cur: __updateRecordHolderDict__(
                PostOffice(*cur[:10]), acc), poList, {})
        except Exception:
            graph = None
        finally:
            return graph


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
