import os
import json
from core.proxy_manager import IPRotator
from core.captcha_solver import AntiBotBypass
from core.request_handler import ConnectionEngine
from core.parser import ContentExtractor

def run_pipeline():
    # Empty list for local direct fallback operation
    assigned_proxies = []
    
    # Configuration parameter strings
    CAPTCHA_CREDENTIAL_TOKEN = "YOUR_2CAPTCHA_API_KEY_HERE" 
    target_web_address = "http://books.toscrape.com/index.html"

    # Instantiate the structural engine modules
    ip_pool_manager = IPRotator(incoming_ips=assigned_proxies)
    security_override = AntiBotBypass(validation_token=CAPTCHA_CREDENTIAL_TOKEN)
    http_client = ConnectionEngine(routing_hub=ip_pool_manager, security_bypass=security_override)

    print("🚀 Initializing Scraping Operations Blueprint...")
    page_markup_string = http_client.acquire_source(target_web_address)

    if page_markup_string:
        # Pass document string to updated parsing layout
        final_dataset = ContentExtractor.process_book_elements(page_markup_string)
        print(f"✨ Successfully collected {len(final_dataset)} entries.")

        # Save structured results to file system
        os.makedirs("data", exist_ok=True)
        with open("data/output.json", "w", encoding="utf-8") as target_file:
            json.dump(final_dataset, target_file, indent=4, ensure_ascii=False)
        print("📂 Complete structured payload committed safely to 'data/output.json'.")
    else:
        print("❌ Scraper operation ended prematurely due to connectivity constraints.")

if __name__ == "__main__":
    run_pipeline()