# Youtube History Organiser and Analyser

A simple program to organise, sort, and analyse your YouTube watch history.

## Features

- Organise your YouTube watch history into a MySQL database.
- Analyse viewing patterns with interactive visualisations:
  - Line graph: category vs. time
  - Bar graph: video consumption by category
  - Animated bar graph: category consumption over time
- Optional: Generate an HTML table of your watch history.

## Prerequisites

- MySQL server installed and set up with user and password ([MySQL Download](https://www.mysql.com)).
- Python installed with pip.
- Jupyter notebook installed (for analysis).

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ayank674/Youtube-history-organiser-and-analyser.git
   ```
   Or download the code from the [repository page](https://github.com/ayank674/Youtube-history-organiser-and-analyser).

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Downloading YouTube History

1. Go to [takeout.google.com](https://takeout.google.com) with your Google account.
2. Deselect all options and select "YouTube and YouTube Music".
3. Click on "Multiple formats" and choose JSON for history.
4. Proceed to create the export and download the file.
5. Unzip the downloaded file to find `watch-history.json`.

## Organising History

1. Run `yt-history-organiser.py`.
2. Enter your MySQL server details when prompted.
3. Choose option 1 to store new history or option 2 to extend previous history.
4. Wait for the script to organise your history into the database.

## Analysing History

1. Open `history_analyser.ipynb` in a Jupyter notebook environment.
2. Run all cells and enter MySQL details when asked.
3. View interactive graphs:
   - Line graph of category vs. time at cell 11.
   - Bar graph of video consumption by category at cell 17.
   - Animated bar graph of category consumption over time at cell 19.

## Optional: Generating HTML Table

You can generate an HTML table of your history using the [Python-html-table-writer](https://github.com/VengeanceOG/Python-html-table-writer) module.

After setting up the database connection, add the following code at the end of `yt-history-organiser.py` or run it separately:

```python
import html_table_writer

cur.execute('select title,channel,category,time,date from video ORDER BY date DESC,time DESC')
if total_rows <= 100:
    history = cur.fetchall()
else:
    history = cur.fetchmany(100)

html_table = html_table_writer.table('history.html', encoding='utf-8', border=2, headers=['Title', 'Channel', 'Category', 'Time', 'Date'])
html_table.write_table(history)

if total_rows > 100:
    while True:
        history = cur.fetchmany(100)
        if history:
            html_table.extend_table(history)
        else:
            break
```

This will create `history.html` with your watch history.

## Examples

<details>
<summary><strong>Selecting JSON format in Google Takeout</strong></summary>
<img src="https://i.postimg.cc/ZKDHPdLj/json.png" width="600"/>
</details>

<details>
<summary><strong>HTML history page</strong></summary>
<img src="https://i.postimg.cc/3JpjGcdr/html-page.png" width="600"/>
</details>

<details>
<summary><strong>Line graph example</strong></summary>
<img src="https://i.ibb.co/xCFBHjq/plot-example.png" width="600"/>
</details>

<details>
<summary><strong>Bar graph example</strong></summary>
<img src="https://i.ibb.co/52cJX1C/bar-plot.png" width="600"/>
</details>

<details>
<summary><strong>Animated bar graph over time</strong></summary>

[Click here to watch the animation](https://github.com/VengeanceOG/Youtube-history-organiser-and-analyser/assets/107803735/eca8731a-edf8-4201-b54e-e30f990f4517)

</details>

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](https://github.com/ayank674/Youtube-history-organiser-and-analyser/blob/main/LICENSE) file for details.
