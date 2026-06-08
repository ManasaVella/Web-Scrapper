from bs4 import BeautifulSoup

class ContentExtractor:
    @staticmethod
    def process_book_elements(html_document):
        """Traverses down DOM markup arrays to capture specific text fields safely."""
        if not html_document:
            return []

        dom_parser = BeautifulSoup(html_document, "html.parser")
        scraped_records = []
        
        # Primary container mapping targeting specific layout elements
        item_nodes = dom_parser.select("article.product_pod")
        
        if not item_nodes:
            item_nodes = dom_parser.select(".product_pod")
            
        for current_node in item_nodes:
            try:
                anchor_tag = current_node.select_one("h3 a")
                cost_tag = current_node.select_one(".price_color")
                inventory_tag = current_node.select_one(".instock.availability")

                if anchor_tag and cost_tag:
                    # Changes output object labels entirely ("name" instead of "title", etc.)
                    scraped_records.append({
                        "book_name": anchor_tag.get("title", anchor_tag.text).strip(),
                        "item_cost": cost_tag.text.strip(),
                        "stock_status": inventory_tag.text.strip() if inventory_tag else "Unavailable"
                    })
            except Exception as extraction_fault:
                print(f"⚠️ Omitting corrupted element node from output construction: {extraction_fault}")
                continue

        return scraped_records