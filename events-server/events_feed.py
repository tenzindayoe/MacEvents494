from reader import make_reader
from event_entry import EventEntry

feed_url = "https://webapps.macalester.edu/eventscalendar/events/rss/"

reader = make_reader("db.sqlite")

def add_feed():
  reader.add_feed(feed_url, exist_ok=True)
  # reader.update_feed(feed_url)
  # reader.enable_feed_updates(feed_url)
  #return reader.get_feed(feed_url)

# feed = add_feed()

def update_feed():
  reader.update_feeds()

def get_events():
  event_entries = []
  for entry in reader.get_entries():
    event_entries.append(EventEntry(entry))
  return event_entries