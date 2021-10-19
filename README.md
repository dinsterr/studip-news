# studip-news
Fetches the activity stream from the Stud.IP platform deployed at the University of Passau and converts it to an atom feed.\
This way activities in the forum can be monitored outside of the browser (e.g. via a feed reader like newsboat)

## Usage
- For now, this relies on the session hanlding provided by studip-sync and requires a working config for [studip-sync](https://github.com/studip-sync/studip-sync).

- On your personal homepage in Stud.IP, add the "Activity" widget.

- The script automatically extracts the user id from the homepage. If the extraction is not possible you can add your id manually in `config.py`.

The output of the script is the full atom feed, which can be read by a feed reader.\
In [newsboat](https://github.com/newsboat/newsboat) you can add the execution directly as a command to your urls:

`"exec:YOUR_PROJECT_LOCATION/studip-news/studip-news.py"`

Alternatively you can also redirect the output to a file and import it in the reader of your choice.

## Configuration
If you want to filter certain categories from the result you can adapt the `SELECTED_FILTERS` in `config.py`.\
For a selection of possible values, look at the configuration of the Activity widget in Stud.IP.

## Credits
Session handling for Stud.IP is implemented via the great work from [studip-sync](https://github.com/studip-sync/studip-sync)