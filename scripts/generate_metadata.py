import aiohttp
import asyncio
from bs4 import BeautifulSoup
import re
import json
import logging
import aiofiles
from transformers import pipeline
from aiohttp import ClientTimeout

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configure NLP summarization
summarizer = pipeline("summarization")

async def safe_fetch(session, url, retries=3, timeout=10):
    try:
        timeout = ClientTimeout(total=timeout)
        async with session.get(url, timeout=timeout) as response:
            response.raise_for_status()
            return await response.text()
    except (aiohttp.ClientError, asyncio.TimeoutError) as e:
        if retries > 0:
            logging.warning(f"Retrying {url}, {retries} retries left due to {e}")
            return await safe_fetch(session, url, retries - 1, timeout)
        else:
            logging.error(f"Failed to fetch {url} after several retries.")
            raise

async def get_article_links(session, url):
    html = await safe_fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    pattern = re.compile(r'/1999-4915/\d+/\d+/\d+$')
    
    article_links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if pattern.search(href):
            article_links.append(f"https://www.mdpi.com{href}")
    
    return list(set(article_links))

async def fetch_article_content(session, url):
    html = await safe_fetch(session, url)
    soup = BeautifulSoup(html, 'html.parser')
    
    title = soup.find('meta', property='og:title')['content']
    abstract = soup.find('meta', property='og:description')['content']
    keywords = [meta['content'] for meta in soup.find_all('meta', attrs={'name': 'keywords'})]
    content = soup.get_text(strip=True)
    
    start_phrases = ["1. Introduction", "1. Emergence"]
    for phrase in start_phrases:
        start_index = content.find(phrase)
        if start_index != -1:
            break
    
    if start_index != -1:
        end_index = content.find("References", start_index)
        if end_index != -1:
            content = content[start_index:end_index]
    
    summary = extract_summarized_content(content)
    
    article_data = {
        'url': url,
        'title': title,
        'abstract': abstract,
        'keywords': keywords,
        'summary': summary,
        'content': content
    }
    
    return article_data
def split_and_summarize(content):
    # Define the size of each part based on the model's limitations
    part_size = 1024
    parts = [content[i:i + part_size] for i in range(0, len(content), part_size)]
    summarized_parts = []
    
    for part in parts:
        max_length = min(1024, int(len(part.split()) * 0.8))  # Adjust max_length dynamically
        min_length = max(100, int(max_length * 0.3))
        try:
            summary = summarizer(part, max_length, min_length)
            summarized_parts.append(summary[0]['summary_text'])
        except Exception as e:
            logging.error(f"Error summarizing part: {e}")
            summarized_parts.append("None") 

def extract_summarized_content(content):
    return split_and_summarize(content)

async def fetch_all_articles_content(article_links):
    articles_data = []
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_article_content(session, url) for url in article_links]
        articles_data = await asyncio.gather(*tasks, return_exceptions=True)
    
    valid_articles_data = []
    for data in articles_data:
        if isinstance(data, Exception):
            logging.error(f"Error fetching article: {data}")
        else:
            valid_articles_data.append(data)
    
    return valid_articles_data

async def async_save_json(data, filename):
    async with aiofiles.open(filename, mode='w') as f:
        await f.write(json.dumps(data, indent=4))

async def main():
    url = "https://www.mdpi.com/journal/viruses/most_cited"
    async with aiohttp.ClientSession() as session:
        article_links = await get_article_links(session, url)
    article_links = ["https://www.mdpi.com/1999-4915/14/6/1334"]
    articles_data = await fetch_all_articles_content(article_links)

    for article in articles_data:
        print(f"Content:\n\n\n{article['content']}")
        print("=" * 50)  # Separate articles for readability
        print("\n\n")

    await async_save_json(articles_data, 'articles_data.json')

if __name__ == "__main__":
    asyncio.run(main())
