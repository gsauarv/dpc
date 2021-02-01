from os import fdopen
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
f = open('./logFiles/access.log')
lines = f.readlines()


def index(request):
    country = getCountry()
    dateTime = getDate()
    os = getOs()
    browsers = getBrowser()
    Countrycount = {}
    osCount = {}
    browserCount = {}
    for cou in country:
        if cou in Countrycount:
            Countrycount[cou] = Countrycount[cou]+1
        else:
            Countrycount[cou] = 1

    for oses in os:
        if oses in osCount:
            osCount[oses] = osCount[oses]+1
        else:
            osCount[oses] = 1

    for browser in browsers:
        if browser in browserCount:
            browserCount[browser] = browserCount[browser]+1
        else:
            browserCount[browser] = 1

    
    return render(request, 'index.html', {'c': Countrycount, 'dateTime': dateTime, 'os': osCount, 'browser': browserCount})


def getIP():

    listIP = []
    for line in lines:
        ip = line.split()[0]
        listIP.append(ip)
    return listIP


def getCountry():
    import requests
    import json
    ips = getIP()
    countries = []
    apiKey = 'b67567fd8a344bd88f011e4d1b865c5d'
    for ip in ips:
        url = 'https://api.ipgeolocation.io/ipgeo?apiKey=' + \
            apiKey+'&ip='+ip + '&fields=country_name'
        response = requests.get(url)
        a = response.text
        data = json.loads(a)
        countries.append(data['country_name'])
        print(response)
    return countries


def getDate():
    listDate = []
    dates = []
    time = []
    for line in lines:
        ip = line.split()[3]
        listDate.append(ip)

    for dateTime in listDate:
        import re
        line = re.sub('[[]', '', dateTime)
        dates.append(line)

    for date in dates:
        temp = (date.split(':')[-3:-1])
        temp = "/".join(temp)
        time.append(temp)

    return time


def getOs():
    listOs = []
    for line in lines:
        os = line.split()[12]
        listOs.append(os)

    return listOs


def getBrowser():
    listBrowser = []
    for line in lines:
        browser = line.split()[11]
        listBrowser.append(browser)

    return listBrowser
