import time
import random
import requests
from bs4 import BeautifulSoup

class ConnectionEngine:
    def __init__(self, routing_hub, security_bypass=None):
        self.router = routing_hub
        self.bypass_tool = security_bypass
        self.web_session = requests.Session()
        
        self.browser_signatures = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]

    def _compile_random_headers(self):
        """Assembles randomized client application profiles to evade fingerprint analysis."""
        return {
            "User-Agent": random.choice(self.browser_signatures),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        }

    def acquire_source(self, destination_url, limit_retries=4):
        """Downloads document source files safely utilizing rotating endpoints and variable delay blocks."""
        initial_delay = 1.5

        for current_run in range(limit_retries):
            selected_proxy = self.router.fetch_next_node()
            proxy_mapping = {"http": selected_proxy, "https": selected_proxy} if selected_proxy else None
            
            # Human-like delay offset with unique microsecond variations
            time.sleep(random.uniform(1.2, 3.1))
            
            try:
                print(f"🚀 Connecting to host: {destination_url} | Node: {selected_proxy if selected_proxy else 'Local Connection'}")
                client_headers = self._compile_random_headers()
                
                web_payload = self.web_session.get(destination_url, headers=client_headers, proxies=proxy_mapping, timeout=10)
                
                if web_payload.status_code in [403, 429, 503]:
                    print(f"⚠️ Access restriction thrown by host system (Error Code: {web_payload.status_code}).")
                    self.router.register_fault(selected_proxy)
                    raise requests.exceptions.RequestException()

                # Content Validation Assertion Rule
                if web_payload.status_code == 200 and "Books to Scrape" not in web_payload.text:
                    print("⚠️ Content Integrity Compromised: Target text elements missing from incoming stream.")
                    self.router.register_fault(selected_proxy)
                    raise requests.exceptions.RequestException("Altered payload received")

                dom_tree = BeautifulSoup(web_payload.text, "html.parser")
                anti_bot_flag = dom_tree.find(class_="g-recaptcha")
                if anti_bot_flag and self.bypass_tool:
                    print("🧩 Active verification wall discovered! Routing to credential array...")
                    extracted_key = anti_bot_flag.get("data-sitekey")
                    resolved_hash = self.bypass_tool.execute_bypass(extracted_key, destination_url)
                    if not resolved_hash:
                        self.router.register_fault(selected_proxy)
                        raise requests.exceptions.RequestException("Bypass routine failure.")

                self.router.register_success(selected_proxy)
                return web_payload.text

            except requests.exceptions.RequestException:
                # Math formula modification: Adding random fractional offset values to break structural detection
                wait_time = (initial_delay * (2 ** current_run)) + random.uniform(0.1, 0.9)
                print(f"⏳ Connection dropped. Entering retry fallback sequence in {round(wait_time, 2)}s...")
                time.sleep(wait_time)

        print(f"❌ Request routine terminated. Unable to retrieve content across available options.")
        return None