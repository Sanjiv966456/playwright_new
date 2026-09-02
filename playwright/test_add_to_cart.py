"""
Pytest script to find "Add to cart" text on pavershop.com.au and navigate all pages
"""
import pytest
from playwright.sync_api import Page, sync_playwright


def find_add_to_cart_buttons(page):
    """Find all 'Add to cart' elements on current page"""
    cart_buttons = []
    
    buttons = page.query_selector_all('button, a, input[type="button"], input[type="submit"]')
    
    for button in buttons:
        text = button.text_content() or ""
        if "add to cart" in text.lower():
            cart_buttons.append({
                'text': text.strip(),
                'tag': button.tag_name,
                'url': page.url
            })
    
    return cart_buttons


def test_find_add_to_cart_on_pavershop():
    """Test to find 'Add to cart' buttons across pavershop.com.au"""
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        
        try:
            page = browser.new_page()
            
            start_url = "https://pavershop.com.au/"
            visited_pages = set()
            pages_to_visit = [start_url]
            all_findings = []
            page_count = 0
            max_pages = 15
            
            print("[*] Starting scan of {}...\n".format(start_url))
            
            while pages_to_visit and page_count < max_pages:
                url = pages_to_visit.pop(0)
                
                if url in visited_pages:
                    continue
                
                visited_pages.add(url)
                page_count += 1
                
                print("[PAGE {}] {}".format(page_count, url))
                
                try:
                    page.goto(url, wait_until='load', timeout=15000)
                    page.wait_for_timeout(2000)
                    
                    findings = find_add_to_cart_buttons(page)
                    
                    if findings:
                        print("   [FOUND] {} 'Add to cart' button(s)".format(len(findings)))
                        for finding in findings:
                            print("      - {} ({})".format(finding['text'][:50], finding['tag']))
                            all_findings.append(finding)
                    else:
                        print("   [NOT FOUND] No 'Add to cart' found")
                    
                    links = page.query_selector_all('a[href]')
                    for link in links:
                        href = link.get_attribute('href') or ""
                        
                        if href.startswith('/') or start_url.split('/')[2] in href:
                            full_url = href if href.startswith('http') else start_url.rstrip('/') + href
                            
                            if full_url not in visited_pages and len(pages_to_visit) < 20:
                                pages_to_visit.append(full_url)
                    
                except Exception as e:
                    print("   [ERROR] {}".format(str(e)[:80]))
                
                print()
            
            print("="*60)
            print("[SUMMARY]")
            print("   Pages scanned: {}".format(page_count))
            print("   'Add to cart' found: {} total".format(len(all_findings)))
            print("   Pages with cart buttons: {}".format(len(set(f['url'] for f in all_findings))))
            print("="*60)
            
            if all_findings:
                print("\n[DETAILED FINDINGS]:")
                for idx, finding in enumerate(all_findings, 1):
                    print("{}. {} (on {})".format(idx, finding['text'][:60], finding['url']))
            
            assert len(all_findings) > 0, "No 'Add to cart' buttons found"
            assert page_count > 0, "No pages were scanned"
            
            print("\n[PASS] Test completed - Found {} buttons across {} pages".format(len(all_findings), page_count))
        
        finally:
            browser.close()

