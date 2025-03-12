from flask import Flask, render_template
import events_feed as feed

app = Flask(__name__)

@app.route("/")
def index():
  events = feed.event_entries
  return render_template('index.html', events=events)

if (__name__ == "__main__"):
  app.run(debug=True)