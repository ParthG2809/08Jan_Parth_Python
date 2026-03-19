import requests
from bs4 import BeautifulSoup

url = "https://jellywp.com/wp/wesper8/"

page = requests.get(url)

soup = BeautifulSoup(page.content, "html.parser")

page_title = soup.title.text.strip()

print(f"The title of the page is: {page_title}")
