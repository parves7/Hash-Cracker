import hashlib
import requests
import sys
import os
from typing import Iterable, Optional
# Raw URL to the SecLists top-10M (raw content)
DEFAULT_GITHUB_RAW_URL = (
    "https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/"
    "Common-Credentials/Pwdb_top-10000000.txt"
)
def url_wordlist(raw_url: str) -> Optional[Iterable[str]]:
    try:
        resp = requests.get(raw_url, stream=True, timeout=15)
        resp.raise_for_status()
        # resp.iter_lines yields bytes; decode and yield text lines
        for raw_line in resp.iter_lines(decode_unicode=True):
            if raw_line is None:
                continue
            yield raw_line
    except requests.RequestException as e:
        print(f"[-] Failed to fetch remote wordlist: {e}")
        return None
def file_wordlist(path: str) -> Optional[Iterable[str]]:
    """Yield lines from a local file. Returns None on failure."""
    if not os.path.isfile(path):
        print(f"[-] Local file not found: {path}")
        return None
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                yield line
    except Exception as e:
        print(f"[-] Failed to open local file: {e}")
        return None
def is_hex_string(s: str) -> bool:
    """Quick check for a hex string (0-9a-f)"""
    try:
        int(s, 16)
        return True
    except ValueError:
        return False
def crack_hash(target_hash: str, word_lines: Iterable[str], algorithm: str) -> Optional[str]:
    algorithm = algorithm.lower()
    # Validate algorithm availability
    if algorithm not in hashlib.algorithms_available:
        print(f"[-] Algorithm '{algorithm}' not available on this system.")
        print("    Available examples:", ", ".join(sorted(list(hashlib.algorithms_available)[:10])) + ", ...")
        return None

    target_hash = target_hash.strip().lower()
    if not target_hash:
        print("[-] Empty target hash provided.")
        return None

    print(f"[+] Attempting to crack hash (first 16 chars): {target_hash[:16]}... using {algorithm}")

    count = 0
    try:
        for line in word_lines:
            count += 1
            word = line.rstrip("\n\r")
            if not word:
                continue

            # try the plain form
            h = hashlib.new(algorithm)
            h.update(word.encode("utf-8"))
            if h.hexdigest() == target_hash:
                print(f"[!] Found (line {count}): {word}")
                return word

            # try the stripped whitespace variant (common)
            stripped = word.strip()
            if stripped != word:
                h = hashlib.new(algorithm)
                h.update(stripped.encode("utf-8"))
                if h.hexdigest() == target_hash:
                    print(f"[!] Found (line {count}, stripped): {stripped}")
                    return stripped

            # periodic status update every 100000 lines (adjust if needed)
            if count % 100000 == 0:
                print(f"[i] Tried {count} candidates...")

    except GeneratorExit:
        raise
    except Exception as e:
        print(f"[-] Unexpected error during cracking loop: {e}")
        return None

    print(f"[-] Exhausted source (tried {count} candidates). No match found.")
    return None
def main():
    try:
        target_hash_input = input("Enter the target hash (hex): ").strip().lower()
        if not target_hash_input:
            print("[-] No hash provided, exiting.")
            return

        algorithm_input = input("Enter the hash algorithm (e.g., md5, sha1, sha256): ").strip().lower()
        if not algorithm_input:
            print("[-] No algorithm provided, exiting.")
            return

        choice = input("Use default (remote) wordlist? (y/n): ").strip().lower()
        line_source = None

        if choice == "y":
            print(f"[+] Streaming remote wordlist from {DEFAULT_GITHUB_RAW_URL}")
            line_source = url_wordlist(DEFAULT_GITHUB_RAW_URL)
            if line_source is None:
                print("[-] Could not load the remote wordlist; aborting.")
                return

        elif choice == "n":
            local_path = input("Enter path to local wordlist: ").strip()
            line_source = file_wordlist(local_path)
            if line_source is None:
                print("[-] Could not load the local file; aborting.")
                return
        else:
            print("[-] Invalid choice; exiting.")
            return

        # run the cracker
        result = crack_hash(target_hash_input, line_source, algorithm_input)
        if result:
            print(f"[+] SUCCESS: password = {result}")
        else:
            print("[-] No password recovered from provided source.")

    except KeyboardInterrupt:
        print("\n[!] Interrupted by user. Exiting.")
    except Exception as e:
        print(f"[-] Fatal error: {e}")
if __name__ == "__main__":
    main()
