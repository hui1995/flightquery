# coding:utf8
import requests


def getFlight(dcity, acity, dayTime):
    url = "http://flights.ctrip.com/itinerary/api/12808/products"
    res_flights = []
    headers = {
        "Content-Type": "application/json",
        "Host": "flights.ctrip.com",
        "Referer": "http://flights.ctrip.com/itinerary/oneway/sha-bjs?allianceid=4897&date=2018-12-09&sid=155952",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36"
    }
    data = """{
        "flightWay": "Oneway",
        "classType": "ALL",
        "hasChild": false,
        "hasBaby": false,
        "searchIndex": 1,
        "allianceid": "4897",
        "sid": "155952",
        "airportParams": [{
            "dcity": "%s",
            "acity": "%s",
            "date": "%s",
            "dcityid": 2,
            "acityid": 1
        }]
    }""" % (dcity, acity, dayTime)

    resp = requests.post(url, data.encode().decode('latin-1'), headers=headers)

    info = resp.json()
    flightList = info['data']['routeList']

    carbin_map = {
        "Y": "经济舱",
        "F": "头等舱",
        "C": "公务舱"
    }

    for flight in flightList:
        if flight['routeType'] == "Flight":
            flightInfo = flight['legs'][0]["flight"]
            lowestPrice = flight['legs'][0]["characteristic"]['lowestPrice']  # 最低价格
            cabins = []
            cabins_ = flight['legs'][0]['cabins']
            for cabin_ in cabins_:
                try:
                    cabin = {
                        "cabinClass": carbin_map.get(cabin_["cabinClass"], "经济舱"),
                        "price": cabin_['price']['price'],
                        "rate": cabin_['price']['rate']
                    }
                except Exception as e:
                    print(e)
                    continue
                cabins.append(cabin)
            id = flightInfo['id']
            fightNumber = flightInfo['flightNumber']  # 航班号
            craftTypeName = flightInfo['craftTypeName']  # 飞机型号
            airlineName = flightInfo['airlineName']  # 航空公司
            departureAirportInfo = flightInfo['departureAirportInfo']
            departureAirport = departureAirportInfo['airportName']  # 起飞机场
            departureCity = departureAirportInfo['cityName']
            departureTerminal = departureAirportInfo['terminal']['name']
            arrivalAirportInfo = flightInfo['arrivalAirportInfo']
            arrivalAirport = arrivalAirportInfo['airportName']  # 降落机场
            arrivalCity = arrivalAirportInfo['cityName']
            arrivalTerminal = arrivalAirportInfo['terminal']['name']
            departureDate = flightInfo['departureDate']  # 起飞时间
            arrivalDate = flightInfo['arrivalDate']  # 降落时间
            punctualityRate = flightInfo['punctualityRate']  # 准点率

            flight = (fightNumber, craftTypeName, airlineName,
                      departureAirport, departureCity, departureTerminal,
                      arrivalAirport, arrivalCity, arrivalTerminal,
                      departureDate, arrivalDate, lowestPrice,
                      str(cabins), dayTime)
            res_flights.append(str(flight))
    return res_flights


if __name__ == '__main__':
    print(getFlight("SHA", "BJS", "2018-12-14"))
