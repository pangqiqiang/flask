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
DEFAULTS = {"publication": "bcc", "city": "北京", 
            "currency_from": "USD", "currency_to": "CNY"}
WEATHER_URL = "https://www.sojson.com/open/api/weather/json.shtml/"
CURRENCY_URL = "http://api.k780.com/"
APPKEY="10003"
SIGN="b59bc3ef6191eb9f747dd4e83c99f2a4"

def get_weather(query):
    query = quote(query)
    api_url = WEATHER_URL + "?city=" + query
    r = requests.get(api_url)
    if r.status_code == 200:
        data = r.json()
        #parse = json.loads(data)
        raw_weather = data.get("data")
        weather = None
        if raw_weather and data.get("city"):
            raw_weather = raw_weather
            weather = {"city": data.get("city"),
                        "wendu": raw_weather.get("wendu"),
                        "shidu": raw_weather.get("shidu"),
                        "pm25": raw_weather.get("pm25"),
                        "quality": raw_weather.get("quality")
                         }
        return weather

def get_rate(frm=None, to=None):
    if not frm or not to:
        frm, to = DEFAULTS["currency_from"], DEFAULTS["currency_to"]
    queries = "?app={app}&scur={frm}&tcur={to}&appkey={appkey}&sign={sign}".format(
        app="finance.rate", frm=frm.upper(), to=to.upper(), appkey=APPKEY, sign=SIGN)
    api_url = CURRENCY_URL + queries
    r = requests.get(api_url)
    if r.status_code == 200:
        data = r.json()
        rate = data.get("result").get("rate")
    return rate


def get_news(query):
    if query.lower() not in RSS_FEEDS:
         query = DEFAULTS["publication"] 
    feed = feedparser.parse(RSS_FEEDS[query])
    return feed.get("entries")   

@app.route("/")
def home():
    publication = request.args.get("publication")
    city = request.args.get("city")
    DEFAULTS={"publication": "bbc", "city": "成都"}
    if not publication:
        publication = DEFAULTS["publication"]
    articles = get_news(publication)
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)
    return render_template("home.html",articles=articles, weather=weather)

if __name__ == "__main__":
    #app.run(port=5000, debug=True)
    print(get_rate())