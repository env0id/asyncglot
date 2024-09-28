import aiohttp
from bs4 import BeautifulSoup
import asyncio

class GoogleTranslator:
  BASE_URL = "https://translate.google.com/m"
  HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"
  }

  def __init__(self, source='auto', target='en'):
    self.source = source
    self.target = target

  async def translate(self, text):
    if not text or self.source == self.target:
      return text
    
    params = {
      'sl': self.source,
      'tl': self.target,
      'q': text
    }

    async with aiohttp.ClientSession() as session:
      async with session.get(self.BASE_URL, headers=self.HEADERS, params=params) as response:
        if response.status == 429:
          raise Exception("Too many requests")
        
        if response.status != 200:
          raise Exception(f"Request failed with status code {response.status}")

        html = await response.text()
        soup = BeautifulSoup(html, "html.parser")

        translation_element = soup.find('div', class_='result-container')
        
        if not translation_element:
          raise Exception("Translation not found")
        
        return translation_element.get_text(strip=True)

  async def translate_batch(self, texts):
    tasks = [self.translate(text) for text in texts]
    return await asyncio.gather(*tasks)
   