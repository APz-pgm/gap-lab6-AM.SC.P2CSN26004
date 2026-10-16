# DECISIONS

## 2026-10-16 — Remove instruction-like document spans before prompting

I chose to remove complete lines matching instruction phrasings in the fixed injected payloads, label all remaining source text as untrusted reference data, and record both input and ignored-instruction events. I rejected relying on a system prompt alone because a model can still follow text quoted in the user context. This catches the supplied visible block and hidden speaker note; it will not recognize every paraphrase or malicious content expressed as ordinary factual prose.

## 2026-10-16 — Tools accept search terms, never locations

I kept `query` as a bounded search string and hard-coded the two approved data filenames inside `load_data_file`. I rejected a model-supplied path with a string filter because normalization, symlinks, and future wiring mistakes make string checks fragile. Resolution plus `is_relative_to(DATA_DIR)` is a second containment check. The tools still trust local file contents enough to parse JSON, so malformed rows are validated and logged.

## 2026-10-16 — Validate and deduplicate before storage

I chose strict Pydantic output validation plus an allow-list check for topic and source, and a normalized text comparison before appending. I rejected relying on the model's duplicate search tool because a model can omit a tool call or ignore its result. The check blocks exact normalized-text repeats, but does not detect semantic paraphrases.

## 2026-10-16 — Bound tool round trips

I kept the supplied `MAX_TOOL_STEPS = 6` and stop with an error outcome when the model continues tool requests past that budget. I rejected an unbounded loop because a model may never return a final answer. This bounds model-call cost but can stop a legitimate multi-step workflow that needs more than six calls.
