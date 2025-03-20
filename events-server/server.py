from flask import Flask, render_template
import events_feed as feed

app = Flask(__name__)

feed.add_feed()

@app.route("/")
def index():
  feed.update_feed()
  events = feed.event_entries
  return render_template('index.html', events=events)

@app.route("/events")
def events():
  feed.update_feed()
  events = feed.event_entries

  event_data = {}
  i = 0

  for event in events:
    i += 1
    event_dict = {
      "title" : event.title,
      "location" : event.location,
      "description" : event.desc,
      "date" : event.date,
      "time" : event.time,
      "link" : event.link
    }
    event_data[i] = event_dict

  return event_data

if (__name__ == "__main__"):
  app.run(debug=True)