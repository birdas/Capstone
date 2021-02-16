import requests
from bs4 import BeautifulSoup

response = requests.get(
	url="https://en.wikipedia.org/wiki/Web_scraping",
    #url='https://en.wikipedia.org/wiki/Backpropagation',
)
soup = BeautifulSoup(response.content, 'html.parser')

blacklist = [
  'style',
  'script',
  # other elements,
]
text_elements = [t for t in soup.find_all(text=True) if t.parent.name not in blacklist]
text = "".join(text_elements).split('\n')
print(response.status_code)
print(text)