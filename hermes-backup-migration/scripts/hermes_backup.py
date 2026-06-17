"""
Hermes Backup Script
Run from repo root. Creates compressed backups of ~/.hermes/ with API keys masked.
Usage: python hermes_backup.py [--output-dir ./backup]
"""
import os
import shutil
import zipfile
import json
import re
import argparse
from datetime import datetime


def mask_api_keys_yaml(content: str) -> str:
    content = re.sub(r"(api_key:\s*)['\"]?[\w\-]+['\"]?", r"\1'YOUR_API_KEY'", content)
    content = re.sub(r"(token:\s*)['\"]?[\w\-]+['\"]?", r"\1'YOUR_TOKEN'", content)
    return content


def mask_api_keys_json(content: str) -> str:
    data = json.loads(content)
    def _mask(obj):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k in ('api_key', 'token', 'secret', 'password') and isinstance(v, str) and len(v) > 10:
                    obj[k] = 'YOUR_' + k.upper()
                else:
                    _mask(v)
        elif isinstance(obj, list):
            for item in obj:
                _mask(item)
    _mask(data)
    return json.dumps(data, indent=2, ensure_ascii=False)


def compress_directory(src_dir: str, zip_path: str, skip_dirs: set = None) -> int:
    skip_dirs = skip_dirs or set()
    count = 0
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(src_dir):
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            for f in files:
                filepath = os.path.join(root, f)
                arcname = os.path.relpath(filepath, os.path.dirname(src_dir))
                zf.write(filepath, arcname)
                count += 1
                if count % 500 == 0:
                    print(f"  Compressed {count} files...")
    return count


def backup_hermes(output_dir: str):
    home = os.path.expanduser("~")
    hermes_dir = os.path.join(home, ".hermes")
    today = datetime.now().strftime("%Y-%m-%d")

    os.makedirs(output_dir, exist_ok=True)

    # 1. Core config (masked)
    print("=== Copying core config ===")
    config_dst = os.path.join(output_dir, "hermes-config")
    os.makedirs(config_dst, exist_ok=True)

    # config.yaml
    with open(os.path.join(hermes_dir, "config.yaml"), 'r', encoding='utf-8') as f:
        content = f.read()
    with open(os.path.join(config_dst, "config.yaml"), 'w', encoding='utf-8') as f:
        f.write(mask_api_keys_yaml(content))
    print("  config.yaml (masked)")

    # auth.json
    with open(os.path.join(hermes_dir, "auth.json"), 'r', encoding='utf-8') as f:
        content = f.read()
    with open(os.path.join(config_dst, "auth.json"), 'w', encoding='utf-8') as f:
        f.write(mask_api_keys_json(content))
    print("  auth.json (masked)")

    # .env -> .env.template
    with open(os.path.join(hermes_dir, ".env"), 'r', encoding='utf-8') as f:
        content = f.read()
    with open(os.path.join(config_dst, ".env.template"), 'w', encoding='utf-8') as f:
        f.write(re.sub(r"=[\w\-]{20,}", "=YOUR_KEY_HERE", content))
    print("  .env -> .env.template (masked)")

    # 2. Copy auxiliary dirs
    for dirname in ["memories", "plugins", "cron", "scripts", "references", "monitoring", "hindsight"]:
        src = os.path.join(hermes_dir, dirname)
        if os.path.exists(src):
            shutil.copytree(src, os.path.join(config_dst, dirname), dirs_exist_ok=True)
            print(f"  {dirname}/")

    # 3. Compress large dirs
    print("\n=== Compressing skills ===")
    n = compress_directory(
        os.path.join(hermes_dir, "skills"),
        os.path.join(output_dir, "hermes-skills.zip")
    )
    print(f"  skills: {n} files")

    print("\n=== Compressing sessions ===")
    n = compress_directory(
        os.path.join(hermes_dir, "sessions"),
        os.path.join(output_dir, "hermes-sessions.zip")
    )
    print(f"  sessions: {n} files")

    print("\n=== Compressing state.db ===")
    with zipfile.ZipFile(os.path.join(output_dir, "state.db.zip"), 'w', zipfile.ZIP_DEFLATED) as zf:
        zf.write(os.path.join(hermes_dir, "state.db"), "state.db")
    print("  state.db compressed")

    print("\n=== Compressing logs ===")
    n = compress_directory(
        os.path.join(hermes_dir, "logs"),
        os.path.join(output_dir, "hermes-logs.zip")
    )
    print(f"  logs: {n} files")

    # 4. Copy small DB files directly
    for db in ["kanban.db", "memory_store.db"]:
        src = os.path.join(hermes_dir, db)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(output_dir, db))
            print(f"  {db}")

    print(f"\n=== Backup complete: {output_dir} ===")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="./hermes-backup")
    args = parser.parse_args()
    backup_hermes(args.output_dir)
