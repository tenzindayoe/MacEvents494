from flask import Flask, render_template
import events_feed as feed

app = Flask(__name__)

feed.add_feed()

@app.route("/")
def index():
  events = feed.get_events()
  return render_template('index.html', events=events)

@app.route("/events")
def events():
  events = feed.get_events()

  event_data = []

  for event in events:
    event_dict = {
      "id" : event.id,
      "title" : event.title,
      "location" : event.location,
      "date" : event.date,
      "time" : event.time,
      "start time" : event.start_time,
      "end time" : event.end_time,
      "link" : event.link,
      "coord" : event.coord
    }
    event_data.append(event_dict)

  return event_data[::-1]

@app.route("/coord")
def coord():
  events = feed.get_events()
  return render_template('coordinates.html', events=events)

@app.route("/times")
def times():
  events = feed.get_events()
  return render_template('startendtimes.html', events=events)

if (__name__ == "__main__"):
  app.run(debug=True)