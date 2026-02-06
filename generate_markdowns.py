from __future__ import annotations

import argparse
import datetime as dt
import re
from pathlib import Path


HEADING_L2 = re.compile(r"^##\s+(?P<title>.+?)\s*$")
HEADING_L3 = re.compile(r"^###\s+(?P<title>.+?)\s*$")
HEADING_L4 = re.compile(r"^####\s+(?P<title>.+?)\s*$")
ITEM_WITH_DESC = re.compile(r"^-\s+\[(?P<title>.+?)\]\((?P<url>[^)]+)\)\s+-\s+(?P<desc>.+?)\s*$")
ITEM_NO_DESC = re.compile(r"^-\s+\[(?P<title>.+?)\]\((?P<url>[^)]+)\)\s*$")


def slugify(text: str) -> str:
	cleaned = re.sub(r"[^a-zA-Z0-9]+", "-", text.strip().lower())
	cleaned = cleaned.strip("-")
	return cleaned or "item"


def parse_godot_version(title: str) -> str | None:
	if not title.lower().startswith("godot"):
		return None
	suffix = title[len("godot"):].strip().lower()
	if "unknown" in suffix:
		return "unknown"
	match = re.search(r"\b(\d+)\b", suffix)
	if match:
		return match.group(1)
	return None


def should_use_genre(title: str | None) -> bool:
	return title in {"2D", "3D", "XR"}


def yaml_escape(value: str) -> str:
	escaped = value.replace("\\", "\\\\").replace('"', '\\"')
	return f'"{escaped}"'


def write_entry(
	output_dir: Path,
	title: str,
	url: str,
	description: str,
	category: str,
	genre: str | None,
	godot_version: str | None,
	force: bool,
) -> Path:
	slug = slugify(title)
	target = output_dir / f"{slug}.md"
	counter = 2
	while target.exists() and not force:
		target = output_dir / f"{slug}-{counter}.md"
		counter += 1

	now = dt.datetime.now().strftime("%Y-%m-%d")
	category_list = f"[{yaml_escape(category)}]"
	genre_list = f"[{yaml_escape(genre)}]" if genre else "[]"
	version_list = f"[{yaml_escape(godot_version)}]" if godot_version else "[]"

	content = "\n".join(
		[
			"---",
			f"title: {yaml_escape(title)}",
			f"date: {now}",
			"draft: false",
			f"external_link: {yaml_escape(url)}",
			f"godot_version: {version_list}",
			f"genre: {genre_list}",
			f"category: {category_list}",
			f"description: {yaml_escape(description)}",
			"build:",
			"  render: \"never\"",
			"  list: \"always\"",
			"---",
			"",
		]
	)

	output_dir.mkdir(parents=True, exist_ok=True)
	target.write_text(content, encoding="utf-8")
	return target


def main() -> int:
	parser = argparse.ArgumentParser(description="Generate hub markdown entries from awesome-godot.txt")
	parser.add_argument("--input", default="awesome-godot.txt")
	parser.add_argument("--output", default="content/hub")
	parser.add_argument("--force", action="store_true", help="Overwrite existing files")
	args = parser.parse_args()

	input_path = Path(args.input)
	output_dir = Path(args.output)

	if not input_path.exists():
		raise SystemExit(f"Input file not found: {input_path}")

	section = None
	heading3 = None
	heading4 = None
	created = 0

	for raw_line in input_path.read_text(encoding="utf-8").splitlines():
		line = raw_line.rstrip()

		match = HEADING_L2.match(line)
		if match:
			section = match.group("title").strip()
			heading3 = None
			heading4 = None
			continue

		match = HEADING_L3.match(line)
		if match:
			heading3 = match.group("title").strip()
			heading4 = None
			continue

		match = HEADING_L4.match(line)
		if match:
			heading4 = match.group("title").strip()
			continue

		match = ITEM_WITH_DESC.match(line) or ITEM_NO_DESC.match(line)
		if not match or not section:
			continue

		title = match.group("title").strip()
		url = match.group("url").strip()
		description = match.groupdict().get("desc") or ""
		description = description.strip() if description else ""

		genre = heading3 if should_use_genre(heading3) else None
		godot_version = parse_godot_version(heading4 or "")

		write_entry(
			output_dir=output_dir,
			title=title,
			url=url,
			description=description,
			category=section,
			genre=genre,
			godot_version=godot_version,
			force=args.force,
		)
		created += 1

	print(f"Created {created} entries in {output_dir}")
	return 0


if __name__ == "__main__":
	raise SystemExit(main())
