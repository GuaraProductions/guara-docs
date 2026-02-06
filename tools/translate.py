import hashlib
import json
import os
import random
import re
import time

from google import genai


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ENV_PATH = os.path.join(BASE_DIR, ".env")


def load_env_file(path):
	if not os.path.exists(path):
		return
	with open(path, "r", encoding="utf-8") as handle:
		for raw_line in handle:
			line = raw_line.strip()
			if not line or line.startswith("#") or "=" not in line:
				continue
			key, value = line.split("=", 1)
			key = key.strip()
			value = value.strip().strip("\"").strip("'")
			if key and key not in os.environ:
				os.environ[key] = value


load_env_file(ENV_PATH)


# Gemini config (fill the key locally in .env).
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-1.5-flash-latest"
AUTO_SELECT_MODEL = True
PREFERRED_MODEL_PREFIXES = (
	"gemini-1.5-flash",
	"gemini-1.5-pro",
	"gemini-1.0-pro",
)
_MODEL_CACHE = None

# Source/target directories.
SOURCE_DIR = os.path.join(BASE_DIR, "content", "en", "hub")
TARGET_DIR = os.path.join(BASE_DIR, "content", "pt-br", "hub")

# Free-tier safety controls.
BATCH_SIZE = 5
RATE_LIMIT_SECONDS = 12
CACHE_PATH = os.path.join(BASE_DIR, ".translate_cache.json")
DRY_RUN = False
FORCE_RETRANSLATE = False
MAX_FILES = 0  # 0 = all
MAX_RETRIES = 6
BACKOFF_BASE_SECONDS = 120
BACKOFF_MAX_SECONDS = 3000


def load_cache():
	if not os.path.exists(CACHE_PATH):
		return {}
	with open(CACHE_PATH, "r", encoding="utf-8") as handle:
		return json.load(handle)


def save_cache(cache):
	with open(CACHE_PATH, "w", encoding="utf-8") as handle:
		json.dump(cache, handle, ensure_ascii=False, indent=2)


def sha_key(title, description):
	raw = f"{title}\n{description}".encode("utf-8")
	return hashlib.sha256(raw).hexdigest()


def split_front_matter(text):
	lines = text.splitlines()
	if not lines or lines[0].strip() != "---":
		return None
	for idx in range(1, len(lines)):
		if lines[idx].strip() == "---":
			fm_lines = lines[1:idx]
			body = "\n".join(lines[idx + 1:])
			return fm_lines, body, text.endswith("\n")
	return None


def parse_value(value):
	trimmed = value.strip()
	if trimmed in {"|", ">"}:
		return None
	if (trimmed.startswith("\"") and trimmed.endswith("\"")) or (
		trimmed.startswith("'") and trimmed.endswith("'")
	):
		return trimmed[1:-1]
	return trimmed


def yaml_quote(value):
	escaped = value.replace("\\", "\\\\").replace("\"", "\\\"")
	return f"\"{escaped}\""


def extract_title_description(fm_lines):
	title = None
	description = None
	title_idx = None
	desc_idx = None
	for idx, line in enumerate(fm_lines):
		match = re.match(r"^(title|description):\s*(.*)$", line)
		if not match:
			continue
		key, value = match.group(1), match.group(2)
		parsed = parse_value(value)
		if parsed is None:
			continue
		if key == "title":
			title = parsed
			title_idx = idx
		elif key == "description":
			description = parsed
			desc_idx = idx
	return title, description, title_idx, desc_idx


def apply_translations(fm_lines, title_idx, desc_idx, title, description):
	updated = list(fm_lines)
	if title_idx is not None and title:
		updated[title_idx] = f"title: {yaml_quote(title)}"
	if desc_idx is not None and description:
		updated[desc_idx] = f"description: {yaml_quote(description)}"
	return updated


def read_front_matter(path):
	with open(path, "r", encoding="utf-8") as handle:
		text = handle.read()
	split = split_front_matter(text)
	if not split:
		return None
	fm_lines, body, ends_with_newline = split
	title, description, title_idx, desc_idx = extract_title_description(fm_lines)
	return {
		"text": text,
		"fm_lines": fm_lines,
		"body": body,
		"ends_with_newline": ends_with_newline,
		"title": title,
		"description": description,
		"title_idx": title_idx,
		"desc_idx": desc_idx,
	}


def write_translated(path, fm_lines, body, ends_with_newline):
	content = "---\n" + "\n".join(fm_lines) + "\n---\n" + body
	if ends_with_newline and not content.endswith("\n"):
		content += "\n"
	os.makedirs(os.path.dirname(path), exist_ok=True)
	with open(path, "w", encoding="utf-8") as handle:
		handle.write(content)


def build_prompt(batch):
	payload = []
	for item in batch:
		payload.append({
			"id": item["id"],
			"title": item["title"],
			"description": item["description"],
		})
	payload_json = json.dumps(payload, ensure_ascii=False)
	return (
		"Translate the JSON array below from English to Brazilian Portuguese. "
		"Keep the same JSON structure and ids. Return ONLY valid JSON, no markdown.\n\n"
		f"{payload_json}"
	)


def call_gemini(prompt):
	if not GEMINI_API_KEY or GEMINI_API_KEY == "PASTE_GEMINI_API_KEY_HERE":
		raise RuntimeError("Set GEMINI_API_KEY in .env")
	client = genai.Client(api_key=GEMINI_API_KEY)
	model_name = resolve_model_name(client)
	last_error = None
	for attempt in range(1, MAX_RETRIES + 1):
		try:
			response = client.models.generate_content(
				model=model_name,
				contents=prompt,
				config={"temperature": 0.2},
			)
			return response.text
		except Exception as error:
			last_error = error
			if not is_rate_limit_error(error) or attempt == MAX_RETRIES:
				break
			backoff = min(BACKOFF_MAX_SECONDS, BACKOFF_BASE_SECONDS * (2 ** (attempt - 1)))
			jitter = random.uniform(0, min(5, backoff * 0.1))
			sleep_for = backoff + jitter
			print(f"[rate-limit] Retry {attempt}/{MAX_RETRIES} in {sleep_for:.1f}s")
			time.sleep(sleep_for)
	raise RuntimeError(f"Gemini API error: {last_error}") from last_error


def is_rate_limit_error(error):
	message = str(error).lower()
	return (
		"resource_exhausted" in message
		or "rate limit" in message
		or "429" in message
		or "quota" in message
	)


def resolve_model_name(client):
	global _MODEL_CACHE
	if _MODEL_CACHE:
		return _MODEL_CACHE
	if not AUTO_SELECT_MODEL:
		_MODEL_CACHE = MODEL
		return _MODEL_CACHE
	try:
		models = client.models.list()
		candidates = []
		for model in models:
			name = getattr(model, "name", None)
			actions = getattr(model, "supported_actions", None)
			if not name or not actions:
				continue
			if "generateContent" in actions:
				candidates.append(name)
		if not candidates:
			_MODEL_CACHE = MODEL
			return _MODEL_CACHE
		for prefix in PREFERRED_MODEL_PREFIXES:
			for name in candidates:
				short_name = name.split("/")[-1]
				if short_name.startswith(prefix):
					_MODEL_CACHE = name
					return _MODEL_CACHE
		_MODEL_CACHE = candidates[0]
		return _MODEL_CACHE
	except Exception:
		_MODEL_CACHE = MODEL
		return _MODEL_CACHE


def extract_json(text):
	cleaned = text.strip()
	if cleaned.startswith("```"):
		cleaned = re.sub(r"^```\w*\n|```$", "", cleaned, flags=re.MULTILINE).strip()
	start = cleaned.find("[")
	end = cleaned.rfind("]")
	if start == -1 or end == -1:
		raise ValueError("Gemini response does not contain a JSON array")
	return json.loads(cleaned[start:end + 1])


def translate_batch(batch):
	prompt = build_prompt(batch)
	response_text = call_gemini(prompt)
	translated = extract_json(response_text)
	translated_map = {item["id"]: item for item in translated}
	return translated_map


def should_skip_existing(src_title, src_desc, target_path):
	if FORCE_RETRANSLATE or not os.path.exists(target_path):
		return False
	existing = read_front_matter(target_path)
	if not existing:
		return False
	return existing["title"] == src_title and existing["description"] == src_desc


def gather_files():
	files = []
	for root, _, filenames in os.walk(SOURCE_DIR):
		for name in filenames:
			if name == "_index.md":
				continue
			if not name.endswith(".md"):
				continue
			files.append(os.path.join(root, name))
	files.sort()
	return files


def main():
	cache = load_cache()
	source_files = gather_files()
	if MAX_FILES:
		source_files = source_files[:MAX_FILES]

	skip_no_front_matter = 0
	skip_missing_fields = 0
	skip_existing_same = 0

	pending = []
	for idx, path in enumerate(source_files, start=1):
		info = read_front_matter(path)
		if not info:
			skip_no_front_matter += 1
			continue
		if not info["title"] or not info["description"]:
			skip_missing_fields += 1
			continue
		rel = os.path.relpath(path, SOURCE_DIR)
		target_path = os.path.join(TARGET_DIR, rel)
		if should_skip_existing(info["title"], info["description"], target_path):
			skip_existing_same += 1
			continue
		cache_key = sha_key(info["title"], info["description"])
		pending.append({
			"id": idx,
			"src": path,
			"dst": target_path,
			"title": info["title"],
			"description": info["description"],
			"cache_key": cache_key,
			"info": info,
		})

	if not pending:
		print("No files to translate.")
		print(
			"Skipped: "
			f"{skip_no_front_matter} no front matter, "
			f"{skip_missing_fields} missing title/description, "
			f"{skip_existing_same} already translated."
		)
		return

	print(f"Queued {len(pending)} files for translation.")
	print(
		"Skipped: "
		f"{skip_no_front_matter} no front matter, "
		f"{skip_missing_fields} missing title/description, "
		f"{skip_existing_same} already translated."
	)

	for batch_start in range(0, len(pending), BATCH_SIZE):
		batch = pending[batch_start:batch_start + BATCH_SIZE]
		cached = []
		to_translate = []
		for item in batch:
			if item["cache_key"] in cache:
				cached.append(item)
			else:
				to_translate.append(item)

		for item in cached:
			translated = cache[item["cache_key"]]
			updated_lines = apply_translations(
				item["info"]["fm_lines"],
				item["info"]["title_idx"],
				item["info"]["desc_idx"],
				translated["title"],
				translated["description"],
			)
			if not DRY_RUN:
				write_translated(item["dst"], updated_lines, item["info"]["body"], item["info"]["ends_with_newline"])
			print(f"[cache] {item['dst']}")

		if to_translate:
			if DRY_RUN:
				print(f"[dry-run] Skipping API call for {len(to_translate)} items")
			else:
				translated_map = translate_batch(to_translate)
				for item in to_translate:
					translated = translated_map.get(item["id"])
					if not translated:
						print(f"[warn] Missing translation for {item['src']}")
						continue
					cache[item["cache_key"]] = {
						"title": translated.get("title", item["title"]),
						"description": translated.get("description", item["description"]),
					}
					updated_lines = apply_translations(
						item["info"]["fm_lines"],
						item["info"]["title_idx"],
						item["info"]["desc_idx"],
						cache[item["cache_key"]]["title"],
						cache[item["cache_key"]]["description"],
					)
					write_translated(item["dst"], updated_lines, item["info"]["body"], item["info"]["ends_with_newline"])
					print(f"[translated] {item['dst']}")
				save_cache(cache)

			if batch_start + BATCH_SIZE < len(pending):
				time.sleep(RATE_LIMIT_SECONDS)


if __name__ == "__main__":
	main()
