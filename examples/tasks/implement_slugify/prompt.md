Implement `slugify(text: str, max_length: int | None = None) -> str`.

Requirements:
- Lowercase text.
- Convert runs of non-alphanumeric characters to a single hyphen.
- Strip leading/trailing hyphens.
- Preserve ASCII letters and digits.
- Normalize common accented Latin characters to ASCII when possible.
- If `max_length` is provided, the returned slug must be at most that length and must not end with a hyphen.
- Empty or punctuation-only input should return "n-a".
