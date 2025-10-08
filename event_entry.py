from reader import Entry
from datetime import datetime
import re


class EventEntry():
  """A class that formats the data in the reader library's Entry object for clearer use."""

  def __init__(self, entry: Entry):
    self.entry = entry
    self.id = entry.id
    self.title = entry.title.replace(" amp;", "&")
    self.link = entry.link
    self.time = (self.title.strip("Library hours: ")
                 .upper().replace("A", " A")
                 .replace("-", " - ").replace("P", " P")
                 if self.title.lower().startswith("library hours")
                 else None)
    self.start_time, self.end_time = self.time_start_end(self.time)
    self.desc = "Unavailable"
    self.coord = None
    self.parse_summary()

  def parse_summary(self):
    summary = self.entry.summary
    sum_split = summary.split(">")

    desc = ""
    for sub in sum_split:
      if sub.endswith("strong") and sum_split.index(sub) > 0:
        details_split = sub.split("|")
        self.date = details_split[0].strip()
        if len(details_split) > 2:
          self.time = details_split[1].strip().replace("&#8211;", " -")
          self.start_time, self.end_time = self.time_start_end(self.time)
        self.location = details_split[len(details_split) - 1].strip("</strong").strip()
        self.coord = self.get_location_coords(self.location)
        self.location = self.location.replace("&amp;", "&")
      else:
        sub = re.sub(r'/[a-z]+', "", sub)
        sub = re.sub(r'\bp\b(?!\.)', '\n\n', sub)
        sub = re.sub(r'span', "", sub)
        sub = re.sub(r' em ', "", sub)
        sub = re.sub(r'nbsp;', "", sub)
        sub = re.sub(r' b ', "", sub)
        sub = re.sub(r'<[a-z]+', "", sub)
        sub = re.sub(r'>', "", sub)
        sub = re.sub(r'<', "", sub)
        sub = re.sub(r' br ', "", sub)
        sub = re.sub(r'span', "", sub)
        sub = re.sub(r' i ', "", sub)

        sub = re.sub(r'\bli\b', '•', sub)
        sub = re.sub(r'\bul\b', '\n', sub)
        sub = re.sub(r'\b/ul\b', '\n', sub)
        sub = re.sub(r'\b/li\b', '\n', sub)
        sub = re.sub(r'Sponsored by:\s*(.+)', r'\n\n Sponsored by: \1\n\n', sub)

        sub = re.sub(r'\s*href\s*=\s*["\'][^"\']*["\']', '', sub)
        sub = re.sub(r'\n{2,}', '\n\n', sub)
        sub = re.sub(r'[ \t]+', ' ', sub)
        sub = re.sub(r' *\n *', '\n', sub)
        sub = sub.strip()



        desc += sub

    self.desc = desc.strip().replace("amp;", "&")

  """A function that converts a time string to a 24 hour time format.
  Args: time str
  Returns: start time, end time or None, None tuple"""

  def time_start_end(self, time):
    if not time:
        return None, None

    parts = time.split("-")

    if len(parts) != 2:
        return None, None

    start_str = parts[0].strip()
    end_str = parts[1].strip()

    formats = ["%I:%M %p", "%I %p", "%I:%M%p", "%I%p"]

    def format_24_hour(t):
        for fmt in formats:
            try:
                return datetime.strptime(t, fmt).strftime("%H:%M")
            except ValueError:
                continue
        return None

    start_24 = format_24_hour(start_str)
    end_24 = format_24_hour(end_str)

    return start_24, end_24

  location_coords = {
      "Library": [44.93855, -93.16822],
      "Humanities": [44.93712, -93.16928],
      "Old Main": [44.93857, -93.16888],
      "Carnegie Hall": [44.93874, -93.16914],
      "Olin-Rice Science Center": [44.93676, -93.16896],
      "Markim Hall": [44.94033, -93.16777],
      "Kagin Commons": [44.94069, -93.16782],
      ("Ruth Stricker Dayton Campus Center",
       "John B Davis Lecture Hall"): [44.93946, -93.16783],
      ("Music Building Mairs Concert Hall",
       "Janet Wallace Fine Arts Center",
       "Law Warschaw Gallery"): [44.93749, -93.16959],
      "Weyerhaeuser Memorial Chapel": [44.93966, -93.16867],
      ("Leonard Center", "Shaw Field"): [44.93765, -93.16804],
      "Theater and Dance Building": [44.93715, -93.17003],
      ("Weyerhaeuser Hall", "College Admissions Office"): [44.93945, -93.16916],
      "Great Lawn": [44.93725, -93.16855],
      "Macalester Stadium": [44.93523, 93.16734]
  }

  """A function thatatches location str to campus building and returns
  the coordinates of the building, latitude and longitude.
    Args: location str
    Returns: coordinates or None if no match found."""

  def get_location_coords(self, location: str):
    if not location:
      return None
    location = location.lower()
    for key, coord in self.location_coords.items():
      if isinstance(key, tuple):
        if any(name.lower() in location for name in key):
          return coord
      elif isinstance(key, str):
        if key.lower() in location:
          return coord
    return None

  def __str__(self):
    return (f"Title: {self.title}\n\n" +
            f"Summary: {self.desc}\n\n" +
            f"Location: {self.location}\n\n" +
            f"Date: {self.date}\n\n" +
            f"Time: {self.time}\n\n" +
            f"Start Time: {self.start_time}\n\n" +
            f"End Time: {self.end_time}\n\n" +
            f"Link: {self.link}")