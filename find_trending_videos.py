import requests
from bs4 import BeautifulSoup

# Get HTML response from YouTube trending page
url = "https://www.youtube.com/feed/trending"
response = requests.get(url)
html = response.content

# Parse the HTML response to extract trending video information
soup = BeautifulSoup(html, "html.parser")
videos = soup.findAll("div", {"class": "yt-lockup-content"})

# Extract video information and store in a dictionary
trending_videos = []
for video in videos:
    video_info = {}
    title = video.find("a", {"class": "yt-uix-tile-link"}).text
    video_info["title"] = title
    video_id = video.find("a", {"class": "yt-uix-tile-link"})["href"].split("=")[-1]
    video_info["video_id"] = video_id
    region = video.find("span", {"class": "accessible-description"}).text.strip().split()[-1]
    video_info["region"] = region
    description = video.find("div", {"class": "yt-lockup-description"}).text.strip()
    video_info["description"] = description
    tags = video.find("ul", {"class": "yt-lockup-meta-info"}).findAll("a")
    video_info["tags"] = [tag.text for tag in tags]
    seo = video.find("div", {"class": "yt-lockup-segment"}).text.strip()
    video_info["seo"] = seo
    trending_videos.append(video_info)

# Output the trending video information as a string
trending_videos_string = str(trending_videos)
print("######")
print(trending_videos_string)
