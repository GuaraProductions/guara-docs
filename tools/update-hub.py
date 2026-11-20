#!/usr/bin/env python3
"""Weekly Hub maintenance: prune dead/archived entries and discover Godot 4 plugins via Gemini."""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EN_HUB = REPO_ROOT / "content" / "en" / "hub"
PT_HUB = REPO_ROOT / "content" / "pt-br" / "hub"

GITHUB_REPO_RE = re.compile(r"^https?://(?:www\.)?github\.com/([^/]+)/([^/#?]+)")
ALLOWED_CATEGORIES = {
    "Plugins and scripts",
    "Modules",
    "Tools",
    "Editor integrations",
    "Importer/Exporter",
    "Assets",
    "Themes",
    "GDScript/C# editor support",
    "CI/CD",
    "Automation",
    "Networking",
    "Audio",
    "Physics",
    "UI",
    "Localization",
    "Testing",
    "Performance",
    "Bash scripts",
    "Other",
    "Examples",
}
ALLOWED_VERSIONS = {"4", "both", "gde", "module"}


def parse_inline_list(raw: str) -> list[str]:
    """Parse a YAML inline list into a list of strings."""
    inner = raw.strip()
    if inner.startswith("[") and inner.endswith("]"):
        inner = inner[1:-1]
    return [m[0] or m[1] for m in re.findall(r'"([^"]*)"|\'([^\']*)\'', inner) if (m[0] or m[1])]


def parse_frontmatter(path: Path) -> dict[str, object]:
    """Extract frontmatter fields from a Hub markdown file."""
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    data: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if ":" not in line or line.startswith((" ", "\t")):
            continue
        key, val = line.split(":", 1)
        key, val = key.strip(), val.strip()
        if key in {"godot_version", "category", "genre"}:
            data[key] = parse_inline_list(val)
        elif key in {"title", "external_link", "date"}:
            data[key] = val.strip('"').strip("'")
    return data


def http_json(
    url: str,
    *,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    body: dict[str, object] | None = None,
    retries: int = 2,
    timeout: int = 20,
) -> tuple[int, dict[str, object]]:
    """Perform an HTTP JSON request with simple retry on 429/5xx/timeouts."""
    req_headers = {"Accept": "application/json", "User-Agent": "guara-docs-hub-updater"}
    if headers:
        req_headers.update(headers)
    data = json.dumps(body).encode("utf-8") if body is not None else None
    if data is not None:
        req_headers["Content-Type"] = "application/json"

    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=req_headers, method=method)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            if err.code in {429, 500, 502, 503, 504} and attempt < retries:
                time.sleep(2 ** (attempt + 1))
                continue
            return err.code, {}
        except (urllib.error.URLError, TimeoutError):
            if attempt < retries:
                time.sleep(2)
                continue
            return 0, {}
    return 0, {}


def github_headers() -> dict[str, str]:
    """Build GitHub API headers using GITHUB_TOKEN if present."""
    headers = {"Accept": "application/vnd.github+json"}
    token = os.environ.get("GITHUB_TOKEN", "").strip()
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def normalize_url(url: str) -> str:
    """Normalize a GitHub repository URL for deduplication."""
    return url.strip().rstrip("/").removesuffix(".git").lower()


def slugify(name: str) -> str:
    """Convert a plugin name into a filesystem-safe slug."""
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return slug or "godot-plugin"


def prune_entries(dry_run: bool) -> list[str]:
    """Remove 404, archived, or >24m inactive unknown-version GitHub entries."""
    removed: list[str] = []
    cutoff = datetime.now(timezone.utc) - timedelta(days=730)
    headers = github_headers()

    for en_path in sorted(EN_HUB.glob("*.md")):
        if en_path.name == "_index.md":
            continue
        meta = parse_frontmatter(en_path)
        categories = set(meta.get("category") or [])
        link = str(meta.get("external_link") or "")
        if "Contents" in categories or link.startswith("#"):
            continue

        match = GITHUB_REPO_RE.match(link)
        if not match:
            continue
        owner, repo = match.group(1), match.group(2).removesuffix(".git")
        status, payload = http_json(f"https://api.github.com/repos/{owner}/{repo}", headers=headers)

        reason = ""
        if status == 404:
            reason = "HTTP 404"
        elif status == 200:
            if payload.get("archived"):
                reason = "archived"
            else:
                versions = set(meta.get("godot_version") or [])
                pushed_raw = str(payload.get("pushed_at") or "")
                if "unknown" in versions and pushed_raw:
                    pushed_at = datetime.fromisoformat(pushed_raw.replace("Z", "+00:00"))
                    if pushed_at < cutoff:
                        reason = "unknown & >24m inactive"

        if reason:
            removed.append(f"{en_path.stem} ({reason})")
            if not dry_run:
                en_path.unlink(missing_ok=True)
                (PT_HUB / en_path.name).unlink(missing_ok=True)
    return removed


def fetch_readme_snippet(owner: str, repo: str, headers: dict[str, str]) -> str:
    """Fetch and truncate the repository README to ~1200 characters."""
    status, payload = http_json(f"https://api.github.com/repos/{owner}/{repo}/readme", headers=headers)
    if status != 200 or not payload.get("content"):
        return ""
    try:
        decoded = base64.b64decode(str(payload["content"])).decode("utf-8", errors="ignore")
        return re.sub(r"\s+", " ", decoded)[:1200]
    except Exception:
        return ""


def discover_candidates(existing_urls: set[str], existing_slugs: set[str]) -> list[dict[str, object]]:
    """Search GitHub for recently active, open-source Godot 4 plugins."""
    headers = github_headers()
    since = (datetime.now(timezone.utc) - timedelta(days=90)).strftime("%Y-%m-%d")
    queries = [
        f"topic:godot4 pushed:>{since} archived:false",
        f"topic:godot-addon pushed:>{since} archived:false",
        f"topic:gdextension pushed:>{since} archived:false",
    ]
    seen_repos: set[str] = set()
    candidates: list[dict[str, object]] = []

    for query in queries:
        encoded = urllib.parse.quote(query)
        url = f"https://api.github.com/search/repositories?q={encoded}&sort=stars&order=desc&per_page=15"
        status, payload = http_json(url, headers=headers)
        if status != 200:
            continue
        for item in payload.get("items") or []:
            html_url = str(item.get("html_url") or "")
            lic = (item.get("license") or {}).get("spdx_id")
            if not html_url or not lic or lic == "NOASSERTION":
                continue
            norm = normalize_url(html_url)
            if norm in existing_urls or norm in seen_repos:
                continue
            seen_repos.add(norm)
            full_name = str(item.get("full_name") or "")
            owner, repo = full_name.split("/", 1)
            slug = slugify(repo)
            if slug in existing_slugs:
                continue
            candidates.append(
                {
                    "name": item.get("name"),
                    "slug": slug,
                    "url": html_url,
                    "stars": item.get("stargazers_count"),
                    "license": lic,
                    "pushed_at": str(item.get("pushed_at") or "")[:10],
                    "description": item.get("description") or "",
                    "readme_snippet": fetch_readme_snippet(owner, repo, headers),
                }
            )
            if len(candidates) >= 12:
                return candidates
    return candidates


def select_gemini_models(api_key: str) -> list[str]:
    """Return an ordered list of available Gemini Flash models supporting generateContent."""
    preferred = [
        "gemini-flash-latest",
        "gemini-3.8-flash",
        "gemini-3.7-flash",
        "gemini-3.6-flash",
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-flash-lite-latest",
    ]
    status, payload = http_json(
        f"https://generativelanguage.googleapis.com/v1beta/models?key={urllib.parse.quote(api_key)}"
    )
    if status != 200:
        return preferred[:3]

    excluded = ("preview", "omni", "tts", "image", "transcribe", "robotics", "computer-use")
    available: set[str] = set()
    for model in payload.get("models") or []:
        name = str(model.get("name") or "").removeprefix("models/")
        methods = model.get("supportedGenerationMethods") or []
        if "generateContent" in methods and "flash" in name and not any(x in name for x in excluded):
            available.add(name)

    ordered = [m for m in preferred if m in available]
    for m in sorted(available, reverse=True):
        if m not in ordered:
            ordered.append(m)
    return ordered or preferred[:3]


def curate_with_gemini(candidates: list[dict[str, object]]) -> list[dict[str, object]]:
    """Use Gemini API (free tier compatible) to select and translate top Godot 4 plugins."""
    api_key = os.environ.get("GEMINI_API_KEY", "").strip()
    if not api_key or not candidates:
        return []

    prompt = (
        "You are curating a bilingual (English + Brazilian Portuguese) Godot 4 plugin Hub.\n"
        "From the JSON candidates below, select up to 5 genuinely useful, active Godot 4 plugins, "
        "GDExtensions, or developer tools (skip raw games, empty templates, or Godot 3-only repos).\n"
        f"Allowed godot_version tags: {sorted(ALLOWED_VERSIONS)}\n"
        f"Allowed category tags: {sorted(ALLOWED_CATEGORIES)}\n"
        "Return ONLY valid JSON: {\"selected\": [{\"slug\": str, \"title\": str, \"url\": str, "
        "\"godot_version\": [str], \"category\": [str], \"description_en\": str, \"description_pt_br\": str}]}.\n"
        "Keep descriptions concise (one line, <= 140 chars).\n\n"
        f"Candidates:\n{json.dumps(candidates, ensure_ascii=False)}"
    )

    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"responseMimeType": "application/json", "temperature": 0.2},
    }

    for model_name in select_gemini_models(api_key)[:4]:
        print(f"Trying Gemini model: {model_name} ({len(candidates)} candidates)")
        endpoint = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            f"{urllib.parse.quote(model_name)}:generateContent?key={urllib.parse.quote(api_key)}"
        )
        status, payload = http_json(endpoint, method="POST", body=body, retries=1, timeout=60)
        if status == 200:
            try:
                text = payload["candidates"][0]["content"]["parts"][0]["text"]
                parsed = json.loads(text)
                return list(parsed.get("selected") or [])
            except (KeyError, IndexError, json.JSONDecodeError, TypeError):
                print(f"Failed to parse JSON from {model_name}; trying next model.")
                continue
        print(f"Gemini model {model_name} returned HTTP {status}; trying next model.")

    print("All Gemini candidate models failed; skipping discovery additions.")
    return []

    try:
        text = payload["candidates"][0]["content"]["parts"][0]["text"]
        parsed = json.loads(text)
        return list(parsed.get("selected") or [])
    except (KeyError, IndexError, json.JSONDecodeError, TypeError):
        print("Failed to parse Gemini JSON response; skipping discovery additions.")
        return []


def render_entry(
    *,
    title: str,
    date_str: str,
    external_link: str,
    godot_version: list[str],
    category: list[str],
    description: str,
) -> str:
    """Render a Hub markdown entry matching archetypes/resources.md."""
    safe_title = title.replace('"', '\\"')
    safe_desc = description.replace('"', '\\"').replace("\n", " ").strip()
    gv_json = json.dumps(godot_version)
    cat_json = json.dumps(category)
    return (
        "---\n"
        f'title: "{safe_title}"\n'
        f"date: {date_str}\n"
        "draft: false\n"
        f'external_link: "{external_link}"\n'
        f"godot_version: {gv_json}\n"
        "genre: []\n"
        f"category: {cat_json}\n"
        f'description: "{safe_desc}"\n'
        "build:\n"
        '  render: "never"\n'
        '  list: "always"\n'
        "---\n"
    )


def add_selected_entries(
    selected: list[dict[str, object]],
    candidates: list[dict[str, object]],
    dry_run: bool,
) -> list[str]:
    """Write validated bilingual Hub markdown pairs for selected plugins."""
    added: list[str] = []
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    candidate_urls = {normalize_url(str(c.get("url") or "")) for c in candidates}

    for item in selected:
        slug = slugify(str(item.get("slug") or item.get("title") or ""))
        title = str(item.get("title") or "").strip()
        url = str(item.get("url") or "").strip()
        desc_en = str(item.get("description_en") or "").strip()
        desc_pt = str(item.get("description_pt_br") or "").strip()
        versions = [v for v in (item.get("godot_version") or []) if v in ALLOWED_VERSIONS] or ["4"]
        categories = [c for c in (item.get("category") or []) if c in ALLOWED_CATEGORIES] or ["Plugins and scripts"]

        if not title or not url or not desc_en or not desc_pt:
            continue
        if normalize_url(url) not in candidate_urls:
            continue
        en_path = EN_HUB / f"{slug}.md"
        pt_path = PT_HUB / f"{slug}.md"
        if en_path.exists() or pt_path.exists():
            continue

        added.append(f"{slug} ({url})")
        if not dry_run:
            en_path.write_text(
                render_entry(
                    title=title,
                    date_str=today,
                    external_link=url,
                    godot_version=versions,
                    category=categories,
                    description=desc_en,
                ),
                encoding="utf-8",
            )
            pt_path.write_text(
                render_entry(
                    title=title,
                    date_str=today,
                    external_link=url,
                    godot_version=versions,
                    category=categories,
                    description=desc_pt,
                ),
                encoding="utf-8",
            )
    return added


def verify_parity() -> None:
    """Ensure 1:1 filename parity between en and pt-br Hub directories."""
    en_files = {p.name for p in EN_HUB.glob("*.md")}
    pt_files = {p.name for p in PT_HUB.glob("*.md")}
    if en_files != pt_files:
        raise RuntimeError(f"Parity mismatch: en-only={en_files - pt_files}, pt-only={pt_files - en_files}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune and discover Hub entries.")
    parser.add_argument("--dry-run", action="store_true", help="Report changes without writing files.")
    args = parser.parse_args()

    removed = prune_entries(args.dry_run)

    existing_urls: set[str] = set()
    existing_slugs: set[str] = set()
    for p in EN_HUB.glob("*.md"):
        existing_slugs.add(p.stem)
        link = str(parse_frontmatter(p).get("external_link") or "")
        if link:
            existing_urls.add(normalize_url(link))

    candidates = discover_candidates(existing_urls, existing_slugs)
    selected = curate_with_gemini(candidates)
    added = add_selected_entries(selected, candidates, args.dry_run)

    verify_parity()

    print(f"Pruned: {len(removed)}")
    for r in removed:
        print(f"  - {r}")
    print(f"Added: {len(added)}")
    for a in added:
        print(f"  + {a}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
