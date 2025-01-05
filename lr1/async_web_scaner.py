import asyncio
import aiohttp
import json

class AsyncWebScraper:
    def __init__(self, urls):
        self.urls = urls

    async def fetch(self, session, url):
        try:
            async with session.get(url) as response:
                return await response.text()
        except Exception as e:
            print(f"Failed to fetch {url}: {e}")
            return None

    async def scrape_all(self):
        async with aiohttp.ClientSession() as session:
            tasks = [self.fetch(session, url) for url in self.urls]
            return await asyncio.gather(*tasks)

class AsyncScraperManager:
    def __init__(self, urls_file):
        self.urls_file = urls_file

    async def __aenter__(self):
        with open(self.urls_file, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
        self.scraper = AsyncWebScraper(urls)
        return self.scraper

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass

async def main():
    urls_file = 'urls.txt'
    async with AsyncScraperManager(urls_file) as scraper:
        results = await scraper.scrape_all()
        for i, result in enumerate(results):
            if result:
                print(f"Result {i+1}:\n{result[:200]}...\n")

if __name__ == "__main__":
    asyncio.run(main())