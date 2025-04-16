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
      "favorited" : event.favorited,
      "title" : event.title,
      "location" : event.location,
      "description" : event.desc,
      "date" : event.date,
      "time" : event.time,
      "link" : event.link,
      "coord" : event.coord
    }
    event_data.append(event_dict)

  return event_data[::-1]

if (__name__ == "__main__"):
  app.run(debug=True)