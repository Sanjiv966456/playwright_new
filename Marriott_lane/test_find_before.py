"""
Test: Find 'before and after school care' on flourishelc.com.au
Simple test function to search for the phrase
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse


def test_find_before_and_after_school_care():
    """Test function to find 'before and after school care' phrase"""
    
    base_url = "https://flourishelc.com.au/"
    search_phrase = "before and after school care"
    
    visited = set()
    found_urls = []
    to_visit = [base_url]
    
    print("\n" + "="*70)
    print("SEARCHING FOR: 'before and after school care'")
    print("="*70 + "\n")
    
    while to_visit and len(visited) < 30:
        url = to_visit.pop(0)
        
        if url in visited:
            continue
        
        visited.add(url)
        print(f"[{len(visited):2d}] {url}")
        
        try:
            response = requests.get(url, timeout=8)
            content = response.text.lower()
            
            # Search for phrase
            if search_phrase.lower() in content:
                found_urls.append(url)
                print(f"     ✓ FOUND!")
            
            # Extract links
            soup = BeautifulSoup(response.text, 'html.parser')
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(url, href)
                
                # Only internal links
                if urlparse(full_url).netloc == urlparse(base_url).netloc:
                    clean = full_url.split('#')[0]
                    if clean not in visited and clean not in to_visit:
                        to_visit.append(clean)
        
        except Exception as e:
            print(f"     Error: {str(e)[:40]}")
    
    # Results
    print("\n" + "="*70)
    print(f"RESULTS: Searched {len(visited)} pages")
    print("="*70 + "\n")
    
    if found_urls:
        print(f"✓ FOUND on {len(found_urls)} page(s):\n")
        for url in found_urls:
            print(f"  → {url}\n")
        assert found_urls, "Phrase should be found"
    else:
        print("✗ Phrase not found on any pages\n")
        assert found_urls, f"'{search_phrase}' not found on site"


if __name__ == "__main__":
    test_find_before_and_after_school_care()
