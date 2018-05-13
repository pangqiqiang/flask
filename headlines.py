import feedparser
import json, requests
from urllib.request import urlopen, quote
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            '36kr': 'http://36kr.com/feed',
            'chong4': 'http://www.chong4.com.cn/feed.php',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}
ALL_CURRENCIES = ['USD', 'HKD', 'AUD', 'JPY', 'EUR', 'GBP', 'KRW', 'CNY']
DEFAULTS = {"publication": "bbc", "city": "北京", 
            "currency_from": "USD", "currency_to": "CNY"}
WEATHER_URL = "https://www.sojson.com/open/api/weather/json.shtml"
CURRENCY_URL = "http://api.k780.com/"


def get_weather(city):
    api_url = WEATHER_URL + "?city=" + city
    r = requests.get(api_url)
    if r.status_code == 200:
        data = r.json()
        #parse = json.loads(data)
        raw_weather = data.get("data")
        weather = None
        if raw_weather and data.get("city"):
            weather = {"city": data.get("city"),
                        "wendu": raw_weather.get("wendu"),
                        "shidu": raw_weather.get("shidu"),
                        "pm25": raw_weather.get("pm25"),
                        "quality": raw_weather.get("quality")
                         }
        return weather

def get_rate(frm, to):
    APPKEY="10003"
    SIGN="b59bc3ef6191eb9f747dd4e83c99f2a4"
    queries = "?app={app}&scur={frm}&tcur={to}&appkey={appkey}&sign={sign}".format(
        app="finance.rate", frm=frm.upper(), to=to.upper(), appkey=APPKEY, sign=SIGN)
    api_url = CURRENCY_URL + queries
    r = requests.get(api_url)
    if r.status_code == 200:
        data = r.json()
        rate = data.get("result").get("rate")
    return rate


def get_news(publication):
    if publication.lower() not in RSS_FEEDS:
         publication = DEFAULTS["publication"] 
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed.get("entries")   

@app.route("/")
def home():
    publication = request.args.get("publication")
    city = request.args.get("city")
    currency_from = request.args.get("currency_from")
    currency_to = request.args.get("currency_to")
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)
    if not currency_from or not currency_to:
        currency_from, currency_to = DEFAULTS["currency_from"], DEFAULTS["currency_to"]
    rate = get_rate(currency_from, currency_to)

    return render_template("home.html",articles=articles, weather=weather, 
    currency_from=currency_from, currency_to=currency_to, rate=rate, all_currencies=sorted(ALL_CURRENCIES))

if __name__ == "__main__":
    app.run(port=5000, debug=True)