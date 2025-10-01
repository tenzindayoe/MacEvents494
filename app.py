from flask import Flask, render_template
import events_feed as feed

app = Flask(__name__)

feed.add_feed()

@app.route("/")
def index():
  """An HTML webpage primarily used to test that event attributes are formatted correctly."""
  events = feed.get_events()
  return render_template('index.html', events=events)

@app.route("/events")
def events():
  """The URL path used to retrieve the event data in JSON format."""
  events = feed.get_events()

  event_data = []

  for event in events:
    event_dict = {
      "id" : event.id,
      "title" : event.title,
      "location" : event.location,
      "date" : event.date,
      "time" : event.time,
      "starttime" : event.start_time,
      "endtime" : event.end_time,
      "link" : event.link,
      "coord" : event.coord,
      "description" : event.desc
    }
    event_data.append(event_dict)

  return event_data[::-1] # To have events in (mostly) chronological order

@app.route("/coord")
def coord():
  events = feed.get_events()
  return render_template('coordinates.html', events=events)

@app.route("/times")
def times():
  events = feed.get_events()
  return render_template('startendtimes.html', events=events)

if (__name__ == "__main__"):
  app.run()