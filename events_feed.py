from reader import make_reader
from event_entry import EventEntry

feed_url = "https://webapps.macalester.edu/eventscalendar/events/rss/"

reader = make_reader("db.sqlite") # Creating a reader object and initializing a database to store info

def add_feed():
  reader.add_feed(feed_url, exist_ok=True) # Adding Mac RSS feed to feed reader, allowing duplicates and allowing updates
  reader.update_feed(feed_url)
  reader.enable_feed_updates(feed_url)

def get_events():
  event_entries = []
  for entry in reader.get_entries(): 
    event_entries.append(EventEntry(entry)) # Collecting all entries from Mac RSS and transforming them into our EventEntry objects
  return event_entries