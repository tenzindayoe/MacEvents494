import lxml.html
from reader import Entry
import lxml

class EventEntry():
  def __init__(self, entry: Entry):
    self.entry = entry
    self.title = entry.title
    self.link = entry.link
    self.time = self.title.strip("Library hours: ").upper().replace("A", " A").replace("-", " - ").replace("P", " P") if self.title.lower().startswith("library hours") else None
    self.desc = None
    self.parse_summary()

  def parse_summary(self):
    summary = self.entry.summary
    sum_split = summary.split(">")

    for sub in sum_split:
      if sub.endswith("strong") and sum_split.index(sub) > 0:
        details_split = sub.split("|")
        self.date = details_split[0].strip()
        if len(details_split) > 2:
          self.time = details_split[1].strip().replace("&#8211;", " -")
        self.location = details_split[len(details_split) - 1].strip("</strong").strip()

  def __str__(self):
    return f"Title: {self.title}\n\nSummary: {self.desc}\n\nLocation: {self.location}\n\nDate: {self.date}\n\nTime: {self.time}\n\nLink: {self.link}"