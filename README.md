# Hash Cracker

A small command-line tool to attempt cracking hashes by comparing them against a wordlist. It supports streaming a large remote wordlist or reading a local file and can use any hash algorithm supported by the Python `hashlib` module.

---

## Features

* Stream a remote wordlist hosted on GitHub (default) to avoid storing large files locally.
* Read a local wordlist (one password per line) when desired.
* Try both raw lines and `strip()`-ped variants of each candidate (common whitespace variants).
* Uses Python's `hashlib` so any algorithm available on your platform is supported (e.g., `md5`, `sha1`, `sha256`, etc.).
* Lightweight; only external dependency is `requests`.

---

## Files

* `hash_cracker.py` — The main Python script (your provided code).
* `requirements.txt` — External Python packages required to run the script (only `requests`).
* `README.md` — This file.
* Optional: `my_wordlist.txt` — Local wordlist file (one candidate per line) if you choose not to stream the remote list.

---

## Requirements

* Python 3.8+ recommended.
* Install dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` should contain:

```
requests>=2.31.0,<3.0.0
```

---

## Usage

Run the script from a terminal:

```bash
python hash_cracker.py
```

The script will prompt for:

1. **Target hash (hex)** — paste the hex-encoded hash you want to crack.
2. **Hash algorithm** — algorithm name supported by `hashlib` (e.g., `md5`, `sha1`, `sha256`).
3. **Use default (remote) wordlist? (y/n)** — choose `y` to stream the SecLists file from GitHub, or `n` to provide a local file path.

If you choose `n`, provide the path to your local wordlist when prompted.

Example interactive session:

```
Enter the target hash (hex): 5f4dcc3b5aa765d61d8327deb882cf99
Enter the hash algorithm (e.g., md5, sha1, sha256): md5
Use default (remote) wordlist? (y/n): n
Enter path to local wordlist: my_wordlist.txt
```

---

## Tips & Notes

* The script prints periodic status updates every 100,000 lines. Adjust that frequency in the source if you want more/less noisy progress.
* If the algorithm you specified is not available on your platform, the script will print the availability and exit. On most systems `md5`, `sha1`, `sha256`, and `sha512` are available.
* For very large wordlists, streaming (remote) avoids downloading large files to disk but depends on a stable network connection.
* Ensure your local wordlist is encoded in UTF-8 or use `errors="ignore"` (the script already uses this when opening local files).

---

## Security & Ethics

This tool is intended for **authorized** password recovery, auditing, and educational use only. Do **not** use it against systems, accounts, or data that you do not own or for which you do not have explicit permission.

Unauthorized use may be illegal and unethical. Always obtain written permission before performing any cracking, auditing, or security testing activity.

---

## Troubleshooting

* **Requests timeout / remote fetch fails**: check network connectivity and consider using a local wordlist instead.
* **`Algorithm 'xyz' not available`**: verify the algorithm name and availability by running a small test in Python:

```python
import hashlib
print(sorted(hashlib.algorithms_available))
```

* **Script runs slowly**: cracking is CPU-bound — try a smaller wordlist, or use optimized tools (e.g., Hashcat) for large-scale cracking.

---

## Contributing

Small fixes and improvements are welcome. Consider adding:

* A CLI interface (via `argparse`) for non-interactive usage.
* Resume/duplicate-detection when using local files.
* Multi-threading or multiprocessing (careful with I/O and GIL) or integration with tools like Hashcat.

---

## License

This repository is provided as-is for educational and auditing purposes. No warranty is provided. Use responsibly.

---
