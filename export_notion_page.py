import os
import urllib3
from notion.client import NotionClient

# Set the required version of urllib3
urllib3.disable_warnings()
urllib3.__version__ = "1.26.6"

# Get Notion token and page URL from environment variables
token = os.environ.get("NOTION_TOKEN")
page_url = os.environ.get("NOTION_PAGE_URL")

# Authenticate with Notion using token
client = NotionClient(token_v2=token)

# Get the Notion page
page = client.get_collection_view(page_url)

# Function to recursively retrieve all subpages
def retrieve_subpages(page, result):
    if hasattr(page, "rows"):
        for row in page.rows:
            result.append(row)
            retrieve_subpages(row, result)

# Retrieve all subpages recursively
subpages = []
retrieve_subpages(page, subpages)

# Export each subpage as HTML
for subpage in subpages:
    # Create a subdirectory for each subpage
    subdirectory = subpage.id.replace("-", "_")
    os.makedirs(subdirectory, exist_ok=True)

    # Export the subpage as HTML
    html_content = subpage.export("html")

    # Save the exported HTML file
    with open(os.path.join(subdirectory, "index.html"), "w", encoding="utf-8") as file:
        file.write(html_content)
