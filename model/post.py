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

    def __str__(self):
        super().__str__()
        return '{} -- {} -- {}'.format(self.officeName, self.pincode, self.officeType)


class PostOfficeGraph(object):
    def __init__(self, headPOs: List[PostOffice]):
        self.headPostOffices = headPOs

    @staticmethod
    def importFromCSV(targetPath: str) -> PostOfficeGraph:
        def __updateRecordHolderDict__(holder: Dict[str, List[List[str]]], record: List[str]) -> Dict[str, List[List[str]]]:
            holder.update(
                {record[2]: [record] + holder.get(record[2], [])})
            return holder

        def __findSO__(currentHO: PostOffice, SOName: str):
            if not SOName:
                return currentHO
            pointer: PostOffice = None
            for i in currentHO.children:
                if i.officeName is SOName:
                    pointer = i
                    break
            return pointer

        def __findHO__(graph: PostOfficeGraph, HOName: str, SOName: str = None) -> PostOffice:
            pointer: PostOffice = None
            for i in graph.headPostOffices:
                if i.officeName is HOName:
                    pointer = __findSO__(i, SOName)
                    break
            return pointer

        def __linkSOWithHO__(graph: PostOfficeGraph, currentSO: List[str]) -> PostOfficeGraph:
            __findHO__(graph, currentSO[12]).children.append(
                PostOffice(currentSO[:10], []))
            return graph

        def __linkBOWithSO__(graph: PostOfficeGraph, currentBO: List[str]) -> PostOfficeGraph:
            __findHO__(graph, currentBO[12], SOName=currentBO[11]).children.append(
                PostOffice(currentBO[:10], [])
            )
            return graph

        graph = None
        try:
            poList = []
            with open(targetPath, mode='r', encoding='ISO-8859-1') as fd:
                poList = csvReader(fd.readlines()[1:])
            holder = reduce(lambda acc, cur: __updateRecordHolderDict__(
                acc, cur), poList, {})
            graph = reduce(lambda acc, cur:
                           __linkBOWithSO__(
                               acc, cur),
                           holder['B.O'],
                           reduce(lambda acc, cur:
                                  __linkSOWithHO__(
                                      acc, cur),
                                  holder['S.O'],
                                  PostOfficeGraph([PostOffice(i[:10], [])
                                                   for i in holder['H.O']])))
            # ['B.O directly a/w Head Office']
        except Exception:
            graph = None
        finally:
            return graph


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
