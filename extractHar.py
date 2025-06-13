import json
import os
import sys
import base64
from urllib.parse import urlparse, unquote

def sanitize_filename(url, default_ext):
    """Extract a safe filename from a URL"""
    parsed = urlparse(url)
    path = unquote(parsed.path)
    name = os.path.basename(path) or "index"
    if '.' not in name:
        name += default_ext
    return name.replace('/', '_').replace('\\', '_')

def extract_from_har(har_file):
    if not os.path.isfile(har_file):
        print(f"[!] File not found: {har_file}")
        return

    base_name = os.path.splitext(os.path.basename(har_file))[0]
    out_dir = os.path.join(os.getcwd(), f"{base_name}_extracted")
    os.makedirs(out_dir, exist_ok=True)

    with open(har_file, 'r', encoding='utf-8') as f:
        har_data = json.load(f)

    entries = har_data.get("log", {}).get("entries", [])
    for i, entry in enumerate(entries):
        req = entry.get("request", {})
        res = entry.get("response", {})
        url = req.get("url", "")
        req_method = req.get("method", "")
        req_body = req.get("postData", {}).get("text", "")
        res_body = res.get("content", {}).get("text", "")
        res_mime = res.get("content", {}).get("mimeType", "")
        res_encoding = res.get("content", {}).get("encoding", "")
        
        safe_filename = sanitize_filename(url, ".txt")
        file_prefix = f"{i:04d}_{safe_filename}"
        
        req_path = os.path.join(out_dir, f"{file_prefix}_request.txt")
        with open(req_path, 'w', encoding='utf-8') as f_req:
            f_req.write(f"{req_method} {url}\n\n{req_body}")
        
        res_path = os.path.join(out_dir, f"{file_prefix}_response.txt")
        if res_body:
            try:
                if res_encoding == "base64":
                    with open(res_path, 'wb') as f_res:
                        f_res.write(base64.b64decode(res_body))
                else:
                    with open(res_path, 'w', encoding='utf-8', errors='ignore') as f_res:
                        f_res.write(res_body)
            except Exception as e:
                print(f"[!] Failed to write response for {url}: {e}")

        if any(x in res_mime for x in ["javascript", "css", "font", "image", "svg", "json", "xml"]):
            asset_path = os.path.join(out_dir, f"{file_prefix}_asset")
            try:
                if res_encoding == "base64":
                    with open(asset_path, 'wb') as f_asset:
                        f_asset.write(base64.b64decode(res_body))
                else:
                    with open(asset_path, 'w', encoding='utf-8', errors='ignore') as f_asset:
                        f_asset.write(res_body)
            except Exception as e:
                print(f"[!] Failed to write asset for {url}: {e}")

    print(f"[+] Extracted {len(entries)} entries to: {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extractHar.py <source.har>")
        sys.exit(1)

    extract_from_har(sys.argv[1])
