# Youtube History Organiser and Analyser

## This is a simple program to organise, sort and analyse your youtube history.

### Guidelines to use:
1. Download, install and setup mysql server.

2. Install all the dependencies from requirements.txt

3. Download your history from [google takeout](takeout.google.com) in **json format**.

4. Use yt_history_organiser program to sort and store your history in mysql database.

5. Use history analyser program to create interactive graphs of your history consumption.

## Detailed explanation to use:

### Setup mysql server.

Download and install mysql from [here](www.mysql.com) and setup server with proper user and password.

### Installing dependencies.

use the following command in terminal:

    pip install -r requirements.txt

### downloading history from takeout.google.com

- Open [google takeout](takeout.google.com) with your preferred google account on a browser.

- Press on deselect all option in 'create a new takeout' menu.

- Navigate down to youtube and Youtube Music section and select it.

- Click on multiple formats button and select json in history.
![json.png](https://i.postimg.cc/ZKDHPdLj/json.png)

- Click on next step and then press create export button.

- Wait till your history is being exported and then reload the page.

- Go to manage exports and then download your exported history from it.

- unzip the exported history and you'll find watch-history.json in it.

## Using yt-history-organiser.py

- Run the program on your device and enter the mysql details.

- If you want to store a new history, enter 1.

- If you want to extend a previous history, enter 2.

- Wait till your history is being organised.

### Tip: You can display your history on a html page by using my [Python-html-table-writer](https://github.com/VengeanceOG/Python-html-table-writer). Just add this code at the end of program:

    import html_table_writer

    cur.execute('select title,channel,category,time,date from video ORDER BY date DESC,time DESC')
    if total_rows<=100:
        history = cur.fetchall()
    else:
        history = cur.fetchmany(100)

    html_table = html_table_writer.table('history.html',encoding= 'utf-8',border=2,headers=['Title','Channel','Category','Time','Date'])
    html_table.write_table(history)

    if total_rows>100: #create html table of all the history by looping every 100 videos in database.
        while True:
            history = cur.fetchmany(100)
            if history:
                html_table.extend_table(history)
            else:
                break

It would produce a html page of your history like the following:

![html page image](https://i.postimg.cc/3JpjGcdr/html-page.png)

## Using Data analyser program:

- Run history_analyser.ipynb as a jupyter notebook.

- Run all the cells and enter mysql details where asked.

- You'll find an interactive line graph of category vs. time on 11th cell. (Here category is type of video watched like entertainment, comedy, etc.) Here's an example:
![line graph image](https://i.ibb.co/xCFBHjq/plot-example.png)

- You'll also find an interactive bar graph of video consumption by category at 17th cell. Here's an example:
![bar graph image](https://i.ibb.co/52cJX1C/bar-plot.png)

- At last, you'll find an animated bar graph at 19th cell that shows category consumption over time. Here's an example:


https://github.com/VengeanceOG/Youtube-history-organiser-and-analyser/assets/107803735/eca8731a-edf8-4201-b54e-e30f990f4517

