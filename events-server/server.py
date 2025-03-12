from flask import Flask, render_template, url_for
import events_feed as feed

app = Flask(__name__)

@app.route("/")
def index():
  feed.add_feed()
  feed.update_feed()
  events = feed.event_entries
  return render_template('index.html', events=events)

if (__name__ == "__main__"):
  app.run(debug=True)