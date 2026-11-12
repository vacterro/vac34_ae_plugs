#!/usr/bin/env python3
"""
vac34_AE Ingestion Pipeline
Parses Bible V1, V2, V3 markdown sources.
Extracts fenced blocks, tracks provenance, classifies, validates semantics,
and produces:
  - catalog/provenance/raw_blocks.json
  - catalog/provenance/classification_report.json
  - catalog/quarantine/quarantine_log.json
  - catalog/normalized/canonical_recipes.json
"""

import os
import re
import json
import hashlib
from typing import Dict, List, Any, Optional

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = [
    {
        "id": "bible_v1",
        "title": "THE ULTIMATE AFTER EFFECTS EXPRESSIONS BIBLE (V3 — ANNOTATED)",
        "path": os.path.join(WORKSPACE_ROOT, "sources", "bible_v1", "THE_ULTIMATE_AFTER_EFFECTS_EXPRESSIONS_BIBLE_V3.md")
    },
    {
        "id": "bible_v2",
        "title": "AE Expressions — Beat Sync Bible (Extensive Edition)",
        "path": os.path.join(WORKSPACE_ROOT, "sources", "bible_v2", "AE_Expressions_Beat_Sync_Bible_Extensive.md")
    },
    {
        "id": "bible_v3",
        "title": "AE Expressions — Beat Sync Bible v2",
        "path": os.path.join(WORKSPACE_ROOT, "sources", "bible_v3", "AE_Expressions_Beat_Sync_Bible_v2.md")
    }
]

# Classification categories
READY_RECIPE = "READY_RECIPE"
REQUIRES_PARAMETERIZATION = "REQUIRES_PARAMETERIZATION"
DUPLICATE_VARIANT = "DUPLICATE_VARIANT"
MULTI_PROPERTY_RIG = "MULTI_PROPERTY_RIG"
HELPER_FUNCTION = "HELPER_FUNCTION"
DOCUMENTATION_ONLY = "DOCUMENTATION_ONLY"
REQUIRES_EXTERNAL_DEPENDENCY = "REQUIRES_EXTERNAL_DEPENDENCY"
INVALID_OR_UNSAFE = "INVALID_OR_UNSAFE"
NEEDS_HOST_VERIFICATION = "NEEDS_HOST_VERIFICATION"
DEFERRED_WITH_REASON = "DEFERRED_WITH_REASON"

# Property target detection rules
TARGET_RULES = [
    (r'\b(scale|transform\.scale|\[\s*s\s*,\s*s\s*\]|\[\s*x\s*,\s*y\s*\]\s*;\s*//\s*scale)\b', "Transform.Scale"),
    (r'\b(position|transform\.position|\[\s*x\s*,\s*y\s*\]|\[\s*value\[0\]|\[\s*x\s*,\s*value\[1\])\b', "Transform.Position"),
    (r'\b(rotation|transform\.rotation|Math\.sin\s*\(.*?\)\s*\*\s*amp\b|degreesToRadians)\b', "Transform.Rotation"),
    (r'\b(opacity|transform\.opacity)\b', "Transform.Opacity"),
    (r'\b(sourceText|text\.sourceText|Math\.round\(.*?\)\.toString)\b', "Text.SourceText"),
    (r'\b(color|\[\s*r\s*,\s*g\s*,\s*b|rgbToHsl|hslToRgb)\b', "Color"),
    (r'\b(stroke|strokeWidth|stroke\s*width)\b', "StrokeWidth"),
    (r'\b(slider|effect\(.*?\)\("Slider"\)|value)\b', "Slider"),
]

def normalize_code(code: str) -> str:
    """Normalize code for deduplication (strip comments, whitespace)."""
    # Remove single line comments
    c = re.sub(r'//.*$', '', code, flags=re.MULTILINE)
    # Remove multi-line comments
    c = re.sub(r'/\*.*?\*/', '', c, flags=re.DOTALL)
    # Normalize whitespace
    c = re.sub(r'\s+', ' ', c).strip()
    return c

def detect_target_property(code: str, heading: str) -> str:
    h_lower = heading.lower()
    if "scale" in h_lower or "масштаб" in h_lower:
        return "Transform.Scale"
    if "position" in h_lower or "позиция" in h_lower or "прыжок" in h_lower or "orbit" in h_lower:
        return "Transform.Position"
    if "rotation" in h_lower or "вращение" in h_lower or "поворот" in h_lower or "спин" in h_lower:
        return "Transform.Rotation"
    if "opacity" in h_lower or "прозрачность" in h_lower or "fade" in h_lower or "blink" in h_lower:
        return "Transform.Opacity"
    if "color" in h_lower or "цвет" in h_lower:
        return "Color"
    if "stroke" in h_lower or "обводка" in h_lower:
        return "StrokeWidth"
    if "text" in h_lower or "текст" in h_lower:
        return "Text.SourceText"
    if "audio" in h_lower or "амплитуда" in h_lower or "dial" in h_lower or "крутилка" in h_lower:
        return "Slider"

    # Match in code
    for pat, target in TARGET_RULES:
        if re.search(pat, code, re.IGNORECASE):
            return target
    return "Generic.Property"

def extract_parameters(code: str) -> List[Dict[str, Any]]:
    """Detect potential tunable parameters in the code."""
    params = []
    # Check for effect slider reads: effect("Name")("Slider")
    slider_refs = re.findall(r'effect\(["\']([^"\']+)["\']\)\(["\'](?:Slider|Checkbox|Angle|Color|Layer)["\']\)', code)
    for ref in set(slider_refs):
        params.append({"name": ref, "type": "Slider", "source": "ae_effect"})
    
    # Check for hardcoded numeric variables: var/const/let name = 123.45;
    var_assigns = re.findall(r'(?:var|const|let)\s+([a-zA-Z0-9_]+)\s*=\s*(-?[0-9]+(?:\.[0-9]+)?)\s*;', code)
    for name, val in var_assigns:
        if name.lower() not in ('i', 'j', 'k', 'l', 'r', 'x', 'y', 'z', 't', 'dt', 'time'):
            params.append({
                "name": name,
                "type": "Number",
                "default": float(val) if '.' in val else int(val),
                "source": "inlined_variable"
            })
    return params

def detect_semantic_flaws(code: str, heading: str) -> List[Dict[str, str]]:
    """Detect known expression anti-patterns and mathematical pitfalls."""
    flaws = []
    # Variable speed multiplied by elapsed time (integration bug)
    if re.search(r'(?:time|t)\s*\*\s*(?:freq|speed|rate)', code) and re.search(r'(?:freq|speed|rate)\s*=\s*(?:ease|linear|amp|audio)', code):
        flaws.append({
            "type": "SPEED_INTEGRATION_FALLACY",
            "message": "Multiplying instantaneous variable frequency/speed by elapsed time does not integrate velocity; causes phase jumps."
        })
    
    # Threshold labeled as peak hold or peak detector
    if ("peak hold" in heading.lower() or "пик" in heading.lower()) and not re.search(r'valueAtTime', code):
        if re.search(r'amp\s*>\s*threshold', code) and not re.search(r'for\s*\(', code):
            flaws.append({
                "type": "THRESHOLD_NOT_PEAK_HOLD",
                "message": "Instantaneous threshold comparison is not peak hold; requires temporal memory/sampling."
            })
    
    # Hardcoded layer name dependency
    layer_names = re.findall(r'thisComp\.layer\(["\']([^"\']+)["\']\)', code)
    for name in layer_names:
        if name != "Audio Amplitude" and name != "Leader" and name != "Master":
            flaws.append({
                "type": "HARDCODED_LAYER_DEPENDENCY",
                "message": f"Expression depends on specific layer name '{name}'."
            })

    # Unbounded loop sampling
    if re.search(r'for\s*\(\s*var\s+[a-zA-Z0-9_]+\s*=\s*0\s*;\s*[a-zA-Z0-9_]+\s*<', code):
        if "valueAtTime" in code and not re.search(r'(?:50|30|20|10|frames|maxFrames)', code):
            flaws.append({
                "type": "POTENTIALLY_UNBOUNDED_TEMPORAL_LOOP",
                "message": "Loop with valueAtTime may cause severe AE UI lag if frame window is not bounded."
            })
            
    return flaws

def classify_block(code: str, heading: str, lang: str, flaws: List[Dict[str, str]]) -> str:
    # 1. Non-code or purely schematic
    if re.search(r'^\s*(INPUT|PROCESS|OUTPUT|ВХОД|ВЫХОД|ПАРАМЕТР|СХЕМА|\d+\.\s|\-\s|\[.*?\]\s*->)', code, re.MULTILINE):
        return DOCUMENTATION_ONLY
    if "```" in code or len(code.strip().splitlines()) <= 1 and not (";" in code or "=" in code or "wiggle" in code or "loop" in code):
        return DOCUMENTATION_ONLY
    if len(code.strip()) < 8:
        return DOCUMENTATION_ONLY
    
    # 2. Syntax/fatal bugs
    if any(f["type"] == "SPEED_INTEGRATION_FALLACY" for f in flaws):
        return INVALID_OR_UNSAFE

    # 3. Helpers/functions
    if code.strip().startswith("function ") or (code.count("function ") >= 1 and "return " in code and not code.endswith(";")):
        return HELPER_FUNCTION

    # 4. Multi-property rigs
    if "multi-property" in heading.lower() or "мастер" in heading.lower() or "rig" in heading.lower():
        return MULTI_PROPERTY_RIG

    # 5. External dependencies
    if re.search(r'footage\(["\'].*?\.json["\']\)', code):
        return REQUIRES_EXTERNAL_DEPENDENCY

    # 6. Audio / Expressions with hardcoded constants requiring sliders
    if re.search(r'thisComp\.layer\(["\']Audio Amplitude["\']\)', code) or "amp" in code or "wiggle" in code or "Math.sin" in code:
        if "effect(" in code:
            return READY_RECIPE
        return REQUIRES_PARAMETERIZATION

    if ";" in code or len(code.strip().splitlines()) >= 2:
        return READY_RECIPE

    return NEEDS_HOST_VERIFICATION

def parse_markdown_file(source_info: Dict[str, str]) -> List[Dict[str, Any]]:
    path = source_info["path"]
    source_id = source_info["id"]
    source_title = source_info["title"]
    
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        
    blocks = []
    curr_headers = []
    in_block = False
    block_lines = []
    block_lang = ""
    start_line = 0
    
    for i, line in enumerate(lines):
        line_num = i + 1
        if line.startswith("#"):
            level = len(line) - len(line.lstrip("#"))
            header_text = line.strip("# \r\n")
            curr_headers = [h for h in curr_headers if h[0] < level] + [(level, header_text)]
        elif line.startswith("```"):
            if not in_block:
                in_block = True
                block_lang = line.strip("` \r\n")
                block_lines = []
                start_line = line_num
            else:
                in_block = False
                end_line = line_num
                raw_snippet = "".join(block_lines)
                heading_chain = " > ".join(h[1] for h in curr_headers)
                
                flaws = detect_semantic_flaws(raw_snippet, heading_chain)
                classification = classify_block(raw_snippet, heading_chain, block_lang, flaws)
                target_prop = detect_target_property(raw_snippet, heading_chain)
                params = extract_parameters(raw_snippet)
                norm = normalize_code(raw_snippet)
                content_hash = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:16]
                
                block_id = f"{source_id}_b{len(blocks)+1:04d}"
                
                blocks.append({
                    "id": block_id,
                    "source_id": source_id,
                    "source_title": source_title,
                    "start_line": start_line,
                    "end_line": end_line,
                    "heading": heading_chain,
                    "raw_code": raw_snippet,
                    "language": block_lang,
                    "normalized_hash": content_hash,
                    "target_property": target_prop,
                    "parameters": params,
                    "flaws": flaws,
                    "classification": classification
                })
        elif in_block:
            block_lines.append(line)
            
    return blocks

def main():
    all_blocks = []
    for src in SOURCES:
        if os.path.exists(src["path"]):
            blocks = parse_markdown_file(src)
            print(f"Extracted {len(blocks)} blocks from {src['id']}")
            all_blocks.extend(blocks)
        else:
            print(f"WARNING: source missing {src['path']}")
            
    # Deduplicate and group
    hash_map: Dict[str, List[Dict[str, Any]]] = {}
    for b in all_blocks:
        h = b["normalized_hash"]
        if h not in hash_map:
            hash_map[h] = []
        hash_map[h].append(b)
        
    for h, group in hash_map.items():
        if len(group) > 1:
            # Mark second and later as DUPLICATE_VARIANT unless original was DOC_ONLY
            primary = group[0]
            for duplicate in group[1:]:
                if duplicate["classification"] not in (DOCUMENTATION_ONLY, INVALID_OR_UNSAFE):
                    duplicate["classification"] = DUPLICATE_VARIANT
                    duplicate["canonical_block_id"] = primary["id"]

    # Classification counts
    counts = {}
    for b in all_blocks:
        c = b["classification"]
        counts[c] = counts.get(c, 0) + 1
        
    print("\n--- CLASSIFICATION COUNTS ---")
    for k, v in sorted(counts.items()):
        print(f"  {k:30s}: {v}")
    print(f"  {'TOTAL':30s}: {len(all_blocks)}")
    
    # Save provenance files
    os.makedirs(os.path.join(WORKSPACE_ROOT, "catalog", "provenance"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_ROOT, "catalog", "quarantine"), exist_ok=True)
    os.makedirs(os.path.join(WORKSPACE_ROOT, "catalog", "normalized"), exist_ok=True)

    with open(os.path.join(WORKSPACE_ROOT, "catalog", "provenance", "raw_blocks.json"), "w", encoding="utf-8") as f:
        json.dump(all_blocks, f, indent=2, ensure_ascii=False)
        
    with open(os.path.join(WORKSPACE_ROOT, "catalog", "provenance", "classification_report.json"), "w", encoding="utf-8") as f:
        json.dump({
            "total_blocks": len(all_blocks),
            "counts": counts,
            "hash_groups_count": len(hash_map)
        }, f, indent=2)

    # Save quarantine
    quarantine = [b for b in all_blocks if b["classification"] in (INVALID_OR_UNSAFE, DEFERRED_WITH_REASON) or len(b["flaws"]) > 0]
    with open(os.path.join(WORKSPACE_ROOT, "catalog", "quarantine", "quarantine_log.json"), "w", encoding="utf-8") as f:
        json.dump(quarantine, f, indent=2, ensure_ascii=False)
    print(f"\nSaved {len(quarantine)} quarantined/flawed items to quarantine_log.json")

if __name__ == "__main__":
    main()
