import urllib.request

req = urllib.request.Request(
    'https://api.pissmissle.fun/claim?token=r8uvrh8k59148cs34wcnqp',
    headers={'User-Agent': 'Mozilla/5.0'}
)
try:
    with urllib.request.urlopen(req) as response:
        content = response.read().decode()
        # Find the form or instructions
        import re
        body = re.search(r'<body.*?>(.*?)</body>', content, re.DOTALL)
        if body:
            print("BODY CONTENT:")
            # Simple html to text
            text = re.sub(r'<[^>]+>', ' ', body.group(1))
            text = re.sub(r'\s+', ' ', text)
            print(text[:1000])
except Exception as e:
    print(e)
