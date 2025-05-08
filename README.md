# MacEvents Server

This project repository holds a web server written in Python using the Flask microframework.

The purpose of the server is to scrape data on Macalester events from the Macalester-provided RSS feed, format each event in a way where each piece of identifying information is readily available and easily accessible, and serve them up in a simple JSON format to clients through a basic API as provided by the Flask framework. The client in this project is the MacEvents iOS app.

Project Specifications
- Python 3.11

Libraries Needed
- Flask 3.1.0
- Reader 3.17

The process of scraping the event data occurs in the event_feed.py file, where the reader library is used to grab and store the newest available info from the RSS feed in a SQLite database. The events feed is then capable of using those stored events to create EventEntry objects and compiling those entries into a list that is returned. The EventEntry class handles parsing and formatting the data of each event, separating them into clearly-labeled variables that can be accessed by the server. The server, contained in the server.py file, compiles these EventEntry objects into a list of dictionaries to be served up as JSON data.

Before a client can gain access to the events  provided, you must run the server. To run the server, simply run the server.py by typing "python -m server" or "python -m flask --app server.py run" into the terminal