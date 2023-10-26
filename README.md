# Notion Library

Allows you to export data from livelib site to you Notion database


### Installation

Copy config example and fill settings for your Notion access

```bash
cp config/config.ini.example config/config.ini
```

### Notion Book base properties

```ini
Name : title
cover : url
```

### Notion Book additional properties

```ini
Publish year : number
Publishing House : select
ISBN : rich_text
Link : url
```

### Usage

Just set book_id in the main.py script and run it

```regexp
https://www.livelib.ru/book/1003006746-sovershennyj-kod-masterklass-stiv-makkonnell
                            |-- id --|
```