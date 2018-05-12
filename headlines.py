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

def get_weather(query):
    api_url = "https://www.sojson.com/open/api/weather/json.shtml"
    query = quote(query)
    api_url = api_url + "?city=" + query
    print(api_url)
    r = requests.get(api_url)
    if r.status_code == 200:
        try:
            data = r.json()
        except Exception:
            data = r.text
            return "could not parse json weather info"
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

def get_news(query):
    if query.lower() not in RSS_FEEDS:
         publication = DEFAULTS["publication"] 
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
    app.run(port=5000, debug=True)
    #print(get_wether("成都"))