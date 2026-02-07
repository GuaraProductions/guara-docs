import argparse
import json
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DEFAULT_SOURCE_DIR = os.path.join(BASE_DIR, "content", "en", "hub")
DEFAULT_TARGET_DIR = os.path.join(BASE_DIR, "content", "pt-br", "hub")
DEFAULT_MERGED_FILE = os.path.join(BASE_DIR, "merged-hub.md")
DEFAULT_ORDER_FILE = os.path.join(BASE_DIR, "merged-hub-order.json")

START_MARKER = "<!-- BEGIN FILE: {path} -->"
END_MARKER = "<!-- END FILE -->"


def gather_files(source_dir, include_index):
	files = []
	for root, _, filenames in os.walk(source_dir):
		for name in filenames:
			if not name.endswith(".md"):
				continue
			if not include_index and name == "_index.md":
				continue
			files.append(os.path.join(root, name))
	files.sort()
	return files


def merge_documents(source_dir, merged_file, include_index, order_file):
	files = gather_files(source_dir, include_index)
	if not files:
		raise RuntimeError("No markdown files found to merge.")
	lines = []
	order = []
	for path in files:
		rel = os.path.relpath(path, source_dir)
		order.append(rel)
		with open(path, "r", encoding="utf-8") as handle:
			content = handle.read()
		lines.append(content.rstrip("\n"))
		lines.append("")
	merged_content = "\n".join(lines).rstrip() + "\n"
	with open(merged_file, "w", encoding="utf-8") as handle:
		handle.write(merged_content)
	with open(order_file, "w", encoding="utf-8") as handle:
		json.dump(order, handle, ensure_ascii=False, indent=2)
	print(f"Merged {len(files)} files into {merged_file}")
	print(f"Wrote order file to {order_file}")


def split_documents(merged_file, target_dir, order_file):
	if not os.path.exists(merged_file):
		raise RuntimeError(f"Merged file not found: {merged_file}")
	with open(merged_file, "r", encoding="utf-8") as handle:
		all_lines = handle.read().splitlines()

	current_path = None
	buffer = []
	count = 0

	def flush():
		nonlocal count
		if current_path is None:
			return
		out_path = os.path.join(target_dir, current_path)
		os.makedirs(os.path.dirname(out_path), exist_ok=True)
		content = "\n".join(buffer).rstrip("\n") + "\n"
		with open(out_path, "w", encoding="utf-8") as out_handle:
			out_handle.write(content)
		count += 1

	for line in all_lines:
		if line.startswith("<!-- BEGIN FILE:") and line.endswith("-->"):
			flush()
			current_path = line.replace("<!-- BEGIN FILE:", "").replace("-->", "").strip()
			buffer = []
			continue
		if line == END_MARKER:
			flush()
			current_path = None
			buffer = []
			continue
		if current_path is not None:
			buffer.append(line)

	flush()
	if count:
		print(f"Split into {count} files under {target_dir}")
		return

	if not os.path.exists(order_file):
		raise RuntimeError("Order file is required when markers are missing.")
	with open(order_file, "r", encoding="utf-8") as handle:
		order = json.load(handle)

	blocks = split_by_front_matter(all_lines)
	if len(blocks) != len(order):
		raise RuntimeError(
			"Block count does not match order file: "
			f"{len(blocks)} blocks vs {len(order)} paths."
		)

	for path, content in zip(order, blocks):
		out_path = os.path.join(target_dir, path)
		os.makedirs(os.path.dirname(out_path), exist_ok=True)
		with open(out_path, "w", encoding="utf-8") as out_handle:
			out_handle.write(content)
	count = len(order)
	print(f"Split into {count} files under {target_dir}")


def split_by_front_matter(lines):
	blocks = []
	start_indices = []

	def next_non_empty(idx):
		while idx < len(lines) and lines[idx].strip() == "":
			idx += 1
		return idx

	for idx, line in enumerate(lines):
		if line.strip() != "---":
			continue
		next_idx = next_non_empty(idx + 1)
		if next_idx >= len(lines):
			continue
		next_line = lines[next_idx]
		if next_line.startswith("title:") or next_line.startswith("date:") or next_line.startswith("draft:"):
			start_indices.append(idx)

	for i, start in enumerate(start_indices):
		end = start_indices[i + 1] if i + 1 < len(start_indices) else len(lines)
		block_lines = lines[start:end]
		blocks.append("\n".join(block_lines).rstrip("\n") + "\n")

	return blocks


def validate_source_dir(source_dir, include_index):
	if not os.path.isdir(source_dir):
		raise RuntimeError(f"Source directory does not exist: {source_dir}")
	files = gather_files(source_dir, include_index)
	if not files:
		raise RuntimeError(f"No markdown files found in source directory: {source_dir}")


def validate_merged_file(merged_file):
	if not os.path.exists(merged_file):
		raise RuntimeError(f"Merged file not found: {merged_file}")


def build_parser():
	parser = argparse.ArgumentParser(description="Merge or split hub markdown files.")
	subparsers = parser.add_subparsers(dest="command", required=True)

	merge_parser = subparsers.add_parser("merge", help="Merge markdown files into one.")
	merge_parser.add_argument("--lang", default="en", help="Language folder to read from (e.g., en, pt-br).")
	merge_parser.add_argument("--source-dir", default=None, help="Optional explicit source directory (overrides --lang)")
	merge_parser.add_argument("--merged-file", default=DEFAULT_MERGED_FILE)
	merge_parser.add_argument("--order-file", default=DEFAULT_ORDER_FILE)
	merge_parser.add_argument("--include-index", action="store_true")

	split_parser = subparsers.add_parser("split", help="Split a merged file into markdown files.")
	split_parser.add_argument("--lang", default="pt-br", help="Language folder to write to (e.g., en, pt-br).")
	split_parser.add_argument("--merged-file", default=DEFAULT_MERGED_FILE)
	split_parser.add_argument("--target-dir", default=None, help="Optional explicit target directory (overrides --lang)")
	split_parser.add_argument("--order-file", default=DEFAULT_ORDER_FILE)

	return parser


def main():
	parser = build_parser()
	args = parser.parse_args()
	if args.command == "merge":
		if args.source_dir is None:
			source_dir = os.path.join(BASE_DIR, "content", args.lang, "hub")
		else:
			source_dir = args.source_dir
		validate_source_dir(source_dir, args.include_index)
		merge_documents(source_dir, args.merged_file, args.include_index, args.order_file)
	elif args.command == "split":
		if args.target_dir is None:
			target_dir = os.path.join(BASE_DIR, "content", args.lang, "hub")
		else:
			target_dir = args.target_dir
		validate_merged_file(args.merged_file)
		split_documents(args.merged_file, target_dir, args.order_file)


if __name__ == "__main__":
	main()
