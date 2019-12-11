# coding:utf-8
import json, time
from pyutil.resource.dal import get_db_client
import datetime
import requests
import math

db_client = get_db_client()


class Flight(object):

    @classmethod
    def getTotal(cls, dCity, aCity, dtime):
        sql = """
        select count(*) as cnt from tb_flight where departureCity=%s and arrivalCity=%s and dayTime=%s;
        """
        cnt = [i for i in db_client.execute(sql, dCity, aCity, dtime)][0]['cnt']
        return cnt

    @classmethod
    def getList(cls, dCity, aCity, dtime):
        sql = """
        select * from tb_flight where departureCity=%s and arrivalCity=%s and dayTime=%s
        order by lowestPrice;
        """
        ret = [i for i in db_client.execute(sql, dCity, aCity, dtime)]
        for flight in ret:
            try:
                flight['cabins'] = eval(flight['cabins'])
                for i in flight['cabins']:
                    i['rate'] = round(i['rate'] * 10, 2)
                flight['cabins'].sort(key=lambda i: i['price'])
                flight['lowestPrice'] = flight['cabins'][0]['price']
            except:
                flight['cabins'] = []
        return ret

    @classmethod
    def addMany(cls, flights):
        if not flights:
            return
        sql = """
        insert into tb_flight(fightNumber, craftTypeName, airlineName,
                      departureAirport, departureCity, departureTerminal,
                      arrivalAirport, arrivalCity, arrivalTerminal,
                      departureDate, arrivalDate, lowestPrice,
                      cabins, dayTime)
        values {}
        """.format(','.join(flights))
        db_client.execute(sql)


if __name__ == '__main__':
    pass