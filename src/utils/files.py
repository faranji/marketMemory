"""Small raw-cache helpers."""
from pathlib import Path
import json

def ensure_directory(path:Path)->Path:
    path.mkdir(parents=True,exist_ok=True);return path

def write_json(path:Path,data:dict|list)->None:
    ensure_directory(path.parent)
    path.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')

def append_jsonl(path:Path,record:dict)->None:
    # JSONL keeps one independent record per line and survives partial runs.
    ensure_directory(path.parent)
    with path.open('a',encoding='utf-8') as f:f.write(json.dumps(record,ensure_ascii=False)+'\n')
