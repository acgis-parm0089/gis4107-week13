url = "http://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/4.5_day.atom"
d = feedparser.parse(url)
print(f'{d.feed.title}' + '\n')
print(f'{"Title":51}{"Longitude":^12}{"Latitude":^12}')
for entry in d.entries:
    latitude,longitude = entry['where']['coordinates']
    print(f'{entry["title"]:50}{longitude:11}{latitude:12}')
print()
print(f'There were {len(d.entries)} x 4.5+ magnitude Earthquakes this past day')
