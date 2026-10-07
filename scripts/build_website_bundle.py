"""
Build script to package the JugaadLang compiler and stdlib for the browser website.
Produces website/assets/jugaad_bundle.js containing a base64-encoded zip archive.
"""

from __future__ import annotations

import base64
import io
import os
import zipfile

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
JUGAADLANG_DIR = os.path.join(ROOT_DIR, "jugaadlang")
OUTPUT_FILE = os.path.join(ROOT_DIR, "website", "assets", "jugaad_bundle.js")


def build_bundle() -> None:
    buf = io.BytesIO()
    file_count = 0

    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(JUGAADLANG_DIR):
            # Exclude pycache and hidden dirs
            dirs[:] = [d for d in dirs if not d.startswith(".") and d != "__pycache__"]
            for f in sorted(files):
                if f.endswith(".py"):
                    full_path = os.path.join(root, f)
                    rel_path = os.path.relpath(full_path, ROOT_DIR).replace("\\", "/")
                    zf.write(full_path, rel_path)
                    file_count += 1

    zip_bytes = buf.getvalue()
    b64_str = base64.b64encode(zip_bytes).decode("ascii")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        out.write("// Auto-generated JugaadLang browser bundle for online compiler\n")
        out.write("// Run 'python scripts/build_website_bundle.py' to regenerate.\n")
        out.write(f'window.JUGAADLANG_ZIP_BASE64 = "{b64_str}";\n')

    print(
        f"[OK] Bundled {file_count} JugaadLang Python files ({len(zip_bytes)} bytes zipped, {len(b64_str)} b64 chars) -> {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    build_bundle()
