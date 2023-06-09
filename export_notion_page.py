import os
import urllib3
from notion.client import NotionClient
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

# Set the required version of urllib3
# urllib3.disable_warnings()
# urllib3.__version__ = "1.26.6"

# Create a custom Retry object with the correct attribute
# retry = Retry(
#     total=5,
#     backoff_factor=0.3,
#     status_forcelist=[500, 502, 503, 504],
#     method_whitelist=False
# )

# Create a custom HTTPAdapter with the custom Retry object
# adapter = HTTPAdapter(max_retries=retry)

# Create a new session and mount the custom adapter
# session = urllib3.PoolManager()
# session.mount("http://", adapter)
# session.mount("https://", adapter)

# Downgrade urllib3 to a compatible version
urllib3_version = "1.25.11"
urllib3.__version__ = urllib3_version
urllib3.disable_warnings()

# Disable warnings from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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
