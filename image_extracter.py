# image_extractor.py
from bs4 import BeautifulSoup
import requests
import os
import logging
import configparser

# Initialize logging
logging.basicConfig(filename='pinterest_scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s')

class ImageExtractor:
    def __init__(self, config_file='config.ini'):
        self.config = configparser.ConfigParser()
        self.config.read(config_file)
        self.image_directory = self.config['output']['image_directory']
        os.makedirs(self.image_directory, exist_ok=True)

    def extract_image_urls(self, html_content):
        """Extracts image URLs from the HTML content, filtering for 'https://i.pinimg.com'."""
        if not html_content:
            logging.warning("No HTML content provided for image extraction.")
            return []

        soup = BeautifulSoup(html_content, 'html.parser')
        image_urls = []

        # Pinterest's structure might change, so we need to be adaptable.
        # This selector targets image elements within pin containers.
        img_tags = soup.find_all('img', {'data-test-id': 'pin-closeup-image'})
        if not img_tags:
            logging.warning("Could not find image elements using the primary selector. Trying alternative.")
            img_tags = soup.find_all('img') # Fallback to find all img tags

        for img in img_tags:
            if 'src' in img.attrs:
                url = img['src']
                if url.startswith('http') and "https://i.pinimg.com" in url and not any(exclude in url for exclude in ['analytics', 'pinimg.com/favicons']):
                    image_urls.append(url)

        # Remove duplicates
        unique_image_urls = list(set(image_urls))
        logging.info(f"Found {len(unique_image_urls)} unique image URLs matching the filter.")
        return unique_image_urls

    def download_images(self, image_urls):
        """Downloads images from the given URLs."""
        downloaded_images = []
        for url in image_urls:
            try:
                response = requests.get(url, stream=True, timeout=10)
                response.raise_for_status()  # Raise an exception for bad status codes

                filename = os.path.join(self.image_directory, url.split('/')[-1].split('?')[0])
                with open(filename, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                downloaded_images.append((url, filename))
                logging.info(f"Downloaded image from {url} to {filename}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Error downloading image from {url}: {e}")
            except Exception as e:
                logging.error(f"An unexpected error occurred while downloading image from {url}: {e}")
        return downloaded_images

if __name__ == '__main__':
    extractor = ImageExtractor()
    try:
        with open("pinterest_page.html", "r", encoding="utf-8") as f:
            html_content = f.read()
        urls = extractor.extract_image_urls(html_content)
        if urls:
            extractor.download_images(urls)
    except FileNotFoundError:
        logging.error("pinterest_page.html not found. Run scraper.py first.")
    except Exception as e:
        logging.error(f"An error occurred in image_extractor.py: {e}")
