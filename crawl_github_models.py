import urllib.request
import urllib.parse
import json
import os
import time

def search_github_glb(query, max_results=5):
    url = f"https://api.github.com/search/code?q={urllib.parse.quote(query)}"
    req = urllib.request.Request(url, headers={'Accept': 'application/vnd.github.v3+json'})
    print(f"Searching GitHub: {url}")
    
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Error: {e.code}")
        print(e.read().decode())
        return []

    items = data.get('items', [])
    downloaded = []
    
    os.makedirs('models/downloaded', exist_ok=True)
    
    count = 0
    for item in items:
        if count >= max_results:
            break
        name = item['name']
        repo = item['repository']['full_name']
        path = item['path']
        
        if not name.endswith('.glb'):
            continue
            
        raw_url = f"https://raw.githubusercontent.com/{repo}/master/{urllib.parse.quote(path)}"
        
        print(f"Downloading {name} from {repo}...")
        try:
            r = urllib.request.urlopen(raw_url)
            content = r.read()
            if len(content) > 1024:
                file_path = f"models/downloaded/{repo.replace('/','_')}_{name}"
                with open(file_path, 'wb') as f:
                    f.write(content)
                downloaded.append(file_path)
                print(f"Saved to {file_path}")
                count += 1
            else:
                raise ValueError("File too small")
        except Exception as e:
            try:
                # Try 'main' branch
                raw_url_main = f"https://raw.githubusercontent.com/{repo}/main/{urllib.parse.quote(path)}"
                r_main = urllib.request.urlopen(raw_url_main)
                content_main = r_main.read()
                if len(content_main) > 1024:
                    file_path = f"models/downloaded/{repo.replace('/','_')}_{name}"
                    with open(file_path, 'wb') as f:
                        f.write(content_main)
                    downloaded.append(file_path)
                    print(f"Saved to {file_path} (main branch)")
                    count += 1
                else:
                    print(f"Failed to download or file too small.")
            except Exception as e2:
                print(f"Error downloading {name}: {e2}")
            
        time.sleep(1) # prevent rate limiting
        
    return downloaded

if __name__ == "__main__":
    search_github_glb("watch extension:glb", max_results=10)
    search_github_glb("watch face extension:glb", max_results=5)
