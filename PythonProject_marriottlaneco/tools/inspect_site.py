import re, urllib.request, sys

def inspect(url='https://marriottlaneco.wpenginepowered.com/'):
    try:
        html = urllib.request.urlopen(url, timeout=30).read().decode('utf-8', errors='ignore')
    except Exception as e:
        print('ERROR fetching URL:', e)
        return
    title = re.search(r'<title.*?>(.*?)</title>', html, re.I|re.S)
    h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', html, re.I|re.S)
    meta = re.search(r"<meta[^>]*name=[\'\"]description[\'\"][^>]*content=[\'\"](.*?)[\'\"]", html, re.I|re.S)
    links = re.findall(r'href=[\'\"]([^\'\"]*(?:contact|property|properties)[^\'\"]*)[\'\"]', html, re.I)
    print('TITLE:', title.group(1).strip() if title else '<NONE>')
    print('H1s:', [re.sub(r'<.*?>','',h).strip() for h in h1s][:10])
    print('META:', meta.group(1).strip() if meta else '<NONE>')
    print('LINKS SAMPLE:', links[:20])

if __name__ == '__main__':
    url = sys.argv[1] if len(sys.argv) > 1 else 'https://marriottlaneco.wpenginepowered.com/'
    inspect(url)

