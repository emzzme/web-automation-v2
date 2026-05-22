from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import zipfile


@dataclass(slots=True)
class IcdBundle:
    raw_text: str
    found_tokens: list[str]


def extract_docx_text(docx_path: Path) -> str:
    with zipfile.ZipFile(docx_path) as zf:
        xml = zf.read("word/document.xml").decode("utf-8", "ignore")
    tokens = re.findall(r"<w:t[^>]*>(.*?)</w:t>", xml)
    return "\n".join(tokens)


def parse_icd(docx_path: Path) -> IcdBundle:
    text = extract_docx_text(docx_path)
    key_patterns = [
        "Ethernet", "USB", "SCPI", "TTL", "Trigger", "Encoder", "Limit", "Home", "E-Stop",
        "220 VAC", "X", "Z", "VNA",
    ]
    found = sorted({k for k in key_patterns if k.lower() in text.lower()})
    return IcdBundle(raw_text=text, found_tokens=found)


def save_icd_snapshot(bundle: IcdBundle, out_json: Path) -> None:
    payload = {
        "found_tokens": bundle.found_tokens,
        "raw_excerpt": bundle.raw_text[:12000],
    }
    out_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
