from reader import make_reader

feed_url = "https://webapps.macalester.edu/eventscalendar/events/rss/"

reader = make_reader("db.sqlite")

def add_and_update_feed():
  reader.add_feed(feed_url, exist_ok=True)
  reader.update_feed(feed_url)
  return reader.get_feed(feed_url)

feed = add_and_update_feed()

entries = list(reader.get_entries())

for e in entries:
  print(e.title)