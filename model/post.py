#!/usr/bin/python3

from typing import List, Dict
from csv import reader as csvReader
from functools import reduce

'''
    Holds an instance of a certain PostOffice of a certain category

    Possible categories : {'H.O', 'S.O', 'B.O', 'B.O directly a/w Head Office'}

    Now there's a hierarchy that exists among these different kinds
    of PostOffice, which is as follows

    A certain general B.O reports to a certain S.O
    A certain S.O reports to a certain H.O
    A special B.O reports directly to a H.O

    So for a PostOffice of `H.O` type, we store
    references to all `S.O`(s), which are supposed to be
    reporting to `H.O` & all `special B.O`(s), which directly
    reports to this `H.O`, in a Linked List ( in its children property )
'''


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

    '''
        A string representation of a certain PostOffice object
    '''

    def __str__(self):
        super().__str__()
        return '{} -- {} -- {}'.format(self.officeName, self.pincode, self.officeType)


'''
    Following one holds an List of all `H.O`(s)
    present in India

    Well that doesn't really let us find other kind
    of P.O.(s) i.e. S.O, B.O or special B.O ?

    So we keep a reference of all those `S.O`(s)
    which are supposed to be reporting to this `H.O`
    & also all those `special B.O`(s), which directly reports
    to this `H.O`

    And in a PostOffice object for a certain `S.O`,
    we keep reference to all those `B.O`(s),
    which are supposed to be reporting to this `S.O`

    In a PostOffice object of `B.O` type, we don't keep any
    reference to any other object(s), because no other 
    PostOffice is reporting to it

    That's how we have a Graph ( well I'll try optimizing it ) of all PostOffices
'''


class PostOfficeGraph(object):
    def __init__(self, headPOs: List[PostOffice]):
        self.headPostOffices = headPOs

    @staticmethod
    def importFromCSV(targetPath: str) -> PostOfficeGraph:
        '''
            We just update a list of records, which we've
            for a certain `PostOffice category`, with second
            argument passed to this closure

            Returns a Dict[str, List[List[str]]]
        '''
        def __updateRecordHolderDict__(holder: Dict[str, List[List[str]]], record: List[str]) -> Dict[str, List[List[str]]]:
            holder.update(
                {record[2]: [record] + holder.get(record[2], [])})
            return holder

        '''
            Given an instance of PostOffice, holding 
            details about a certain `H.O`,
            we try to find out a PostOffice object
            which is a `S.O` & of given name ( passed as second argument )
        '''
        def __findSO__(currentHO: PostOffice, SOName: str):
            if not SOName:
                return currentHO
            pointer: PostOffice = None
            for i in currentHO.children:
                if i.officeName is SOName:
                    pointer = i
                    break
            return pointer

        '''
            Given the whole PostOfficeGraph, which is still under construction,
            we're asked to find out an instance of PostOffice, which is a `H.O`,
            if & only if `SOName` argument is `None`

            But there may be a situation when we've to find out a `S.O`
            using `SOName` argument, when we'll simply call closure which is written just
            above this one, with requested `SOName` & found `H.O` ( PostOffice object )
        '''
        def __findHO__(graph: PostOfficeGraph, HOName: str, SOName: str = None) -> PostOffice:
            pointer: PostOffice = None
            for i in graph.headPostOffices:
                if i.officeName is HOName:
                    pointer = __findSO__(i, SOName)
                    break
            return pointer

        '''
            We first find out `H.O` for this `S.O`,
            and a newly created instance of PostOffice ( of type `S.O` )
            and append this instance to children list of `H.O`
        '''
        def __linkSOWithHO__(graph: PostOfficeGraph, currentSO: List[str]) -> PostOfficeGraph:
            __findHO__(graph, currentSO[12]).children.append(
                PostOffice(currentSO[:10], []))
            return graph

        '''
            First finding out target `S.O`, then newly created instance of PostOffice ( of type `B.O` )
            is linked up with this `S.O`
        '''
        def __linkBOWithSO__(graph: PostOfficeGraph, currentBO: List[str]) -> PostOfficeGraph:
            __findHO__(graph, currentBO[12], SOName=currentBO[11]).children.append(
                PostOffice(currentBO[:10], None)
            )
            return graph

        '''
            Finds out target `H.O`, where this `special B.O` reports
            & they're linked up
        '''
        def __linkSpecialBOWithHO__(graph: PostOfficeGraph, currentSpecialBO: List[str]) -> PostOfficeGraph:
            __findHO__(graph, currentSpecialBO[12]).children.append(
                PostOffice(currentSpecialBO[:10], None)
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
                           __linkSpecialBOWithHO__(acc, cur),
                           holder['B.O directly a/w Head Office'],
                           reduce(lambda acc, cur:
                                  __linkBOWithSO__(
                                      acc, cur),
                                  holder['B.O'],
                                  reduce(lambda acc, cur:
                                         __linkSOWithHO__(
                                             acc, cur),
                                         holder['S.O'],
                                         PostOfficeGraph([PostOffice(i[:10], [])
                                                          for i in holder['H.O']]))))
        except Exception:
            graph = None
        finally:
            return graph


if __name__ == '__main__':
    print('[!]This module is expected to be used as a backend handler')
    exit(0)
