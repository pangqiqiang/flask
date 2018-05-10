import feedparser
from flask import Flask
from flask import render_template

app = Flask(__name__)
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
            '36kr': 'http://36kr.com/feed',
            'chong4': 'http://www.chong4.com.cn/feed.php',
            'iol': 'http://www.iol.co.za/cmlink/1.640'}
@app.route("/")
@app.route("/<publication>")
def get_news(publication="36kr"):
    feed = feedparser.parse(RSS_FEEDS.get(publication))
    first_article = feed["entries"][0]
    return render_template("home.html",
    title=first_article.get("title"),
    published=first_article.get("published"),
    summary=first_article.get("summary"))

if __name__ == "__main__":
    app.run(port=5000, debug=True)