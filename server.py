# coding:utf8
import time, sys
from datetime import timedelta
from flask import Flask, request, jsonify, render_template, redirect, url_for
from model import *
from spider import citys, getFlight
import traceback
app = Flask(__name__)

app.secret_key = 'flightQuery'


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/list")
def getList():
    params = {}
    try:
        params = request.args
        dCity = params['dCity']
        aCity = params['aCity']
        dCode = citys.get(dCity)
        aCode = citys.get(aCity)
        dayTime = params['dayTime']
        if not dCode or not aCode:
            msg = "城市输入有误"
            flights = []
        else:
            total = Flight.getTotal(dCity, aCity, dayTime)
            if not total:
                try:
                    flights_ = getFlight(dCode, aCode, dayTime)
                    Flight.addMany(flights_)
                except Exception as e:
                    print(e)
            flights = Flight.getList(dCity, aCity, dayTime)
            if not flights:
                msg = "无航班信息"
            else:
                msg = "ok"
    except Exception as e:
        print(e)
        flights = []
        msg = "网络开小差了"
    return render_template("list.html", flights=flights, msg=msg, data=params)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    # # flights = getFlight("SIA", "BJS", "2018-12-14")
    # # Flight.addMany(flights)
    # print(Flight.getList("西安", "北京", "2018-12-14"))


