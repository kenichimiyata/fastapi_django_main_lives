import scraper
import server_setup
import specification_document

if __name__ == '__main__':
    # Scrape product data
    scraper.daily_scrape()

    # Set up server
    server_setup.setup_server()

    # Create specification document
    specification_document.SpecificationDocument('https://example.com').create_document()