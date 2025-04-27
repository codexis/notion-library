# Notion Library

A desktop application that allows you to export book data from livelib.ru to your Notion database and Obsidian vault. The app extracts book metadata including title, authors, publisher, year, pages, ISBN, and cover image, making it easy to build and maintain your digital book collection.

## Features

- Extract book metadata from livelib.ru URLs
- Preview book information before saving
- Export to Notion database with customizable properties
- Save as Markdown files in Obsidian with proper formatting
- Cache book covers locally for faster access

## Requirements

- Python 3.8+
- Required packages: requests, beautifulsoup4, customtkinter, notionhq_client, python-dotenv

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up configuration:

### Notion Configuration

Create a `.env` file in the project root with your Notion API credentials:

```bash
# Notion settings
NOTION_API_KEY="your_notion_api_key"
NOTION_DATABASE_ID="your_notion_database_id"

# Obsidian paths (optional)
BOOKS_DIR="PATH_TO_YOUR_LIBRARY\\@Books"
COVERS_DIR="PATH_TO_YOUR_LIBRARY\\_covers"
```

Alternatively, you can create a `config/config.ini` file based on the example:

```ini
[NOTION]
api_token = YOUR_NOTION_TOKEN
database_id = YOUR_DATABASE_ID
```

### Notion Database Setup

Your Notion database should have these properties:

#### Base properties (required)
```ini
Name : title       # Book title
cover : url        # URL to book cover image
```

#### Additional properties (recommended)
```ini
Publish year : number      # Year of publication
Publishing House : select  # Publisher name as a select option
ISBN : rich_text           # Book ISBN number
Link : url                 # URL to the book page
```

## Usage

1. Run the application:
```bash
python src/application/main_window.py
```

2. Enter a livelib.ru book URL in the input field
3. Click "Preview" to see the extracted book information
4. Review the data and book cover
5. Click "Save to Notes" to export the book to Notion and/or Obsidian
