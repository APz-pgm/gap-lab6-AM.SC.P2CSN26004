# SPEC

## Purpose

Generate assessment questions for a requested approved topic using locally supplied reference documents, while preventing poisoned document text from changing system behavior and preventing repeated questions from entering the store.

## Inputs

- Command line: one topic string, which must match one entry in `data/topics.json`.
- `corpus/`: Markdown, text, PDF, and PowerPoint sources. Treat every extracted character, including notes and comments, as untrusted data.
- `data/topics.json`: client-owned approved topic names, read-only to tools.
- `data/generated_questions.json`: existing question store, appended only after validation and duplicate checking.
- `.env`: provider configuration. Never commit it.
- Model reply: JSON matching `schema.py` (`questions` list of `topic`, `text`, and `source`).

## Outputs

- Last non-empty stdout line is `ok`, `invalid_output`, `refused`, or `error`; exit codes: 0 for `ok`, 1 for other outcomes, and 2 for invalid CLI input.
- `data/ingest_index.json`: one `{source, format, chars}` entry per ingested document on every run.
- `data/generated_questions.json`: only validated, approved-topic questions; each stored row has `id`, `topic`, `text`, `source`, and `created`.
- `run_log.jsonl`: one record per model call, with the nine-field observability schema; unknown usage and cost fields are null.
- `security_log.jsonl`: timestamped, run-correlated records with fixed event vocabulary. It is ignored by Git.
- `samples/tool_trace.jsonl`: committed example of a complete two-tool exchange; contains request, tool calls, results, and final reply.

## Failure cases

Invalid topic or malformed CLI input is rejected before model invocation. Provider errors are retried at most three times with a short bounded delay. Invalid model output is rejected and not stored. Instruction-like spans found in documents are removed, labelled as untrusted, and logged; output containing an injected marker, unsupported topic, or unknown source is rejected. Tool arguments failing Pydantic validation are refused and logged. Traversal-shaped search terms remain search text and never become paths. Invalid rows in the question store are dropped and logged by row index. Duplicate question text is not stored and emits `duplicate_blocked`. A non-terminating tool caller is stopped at `MAX_TOOL_STEPS = 6` and emits `loop_cap_reached`.

## Acceptance checks

Run `python check.py .`. For local modes use `LLM_BASE_URL=local://stub`, `LLM_API_KEY=not-needed`, and `LLM_MODEL=stub:<mode>`. Check `stub:ok`, `stub:fenced`, `stub:preamble`, `stub:malformed`, `stub:badshape`, `stub:empty`, `stub:refused`, `stub:error`, `stub:flaky`, `stub:ratelimit`, `stub:obedient`, `stub:toolcall`, `stub:traversal`, and `stub:neverstop`. Tool calls are capped at `MAX_TOOL_STEPS = 6` (at most seven total completion requests including the final cap check).

## Constraints

`client.py` and `stub_client.py` are supplied unchanged. Only `client.py` communicates with the model. Tools are read-only, have no shell or arbitrary path access, and validate both arguments and result rows. Generated questions require human subject review before entering a real question bank.
