# SECURITY

## What this application is

The application generates draft assessment questions for one approved topic, using client-provided documents and an external model. It records which source document supported each question, checks the reply before storage, consults read-only topic and question tools, and prevents duplicate text from being appended. A subject lead must review every generated item before real use.

## Trust boundaries

| Crossing | What crosses | Direction | What checks it |
|---|---|---|---|
| Local corpus to prompt | PDF, PPTX (including speaker notes), Markdown, and text | Files to application to model | `doc_loader.py:load_corpus`; `main.py:sanitise_document` removes recognized instruction lines, retains source labels, and logs action. |
| Model reply to application | Untrusted JSON text | Model to application | `main.py:valid_output` parses and validates Pydantic shape, marker absence, approved topic, and ingested source before storage. |
| Model tool arguments | Search text and optional limits | Model to tools | `tools.py:run_tool`, `TopicLookupArgs`, and `QuestionLookupArgs` validate shape and bounds before reads. |
| Tool access to local data | Two JSON files | Tool to disk and back | `tools.py:load_data_file` allow-lists filenames, resolves paths, checks `is_relative_to(DATA_DIR)`, and validates every returned row. |
| Generated item to persistent store | Question records | Application to JSON store | `main.py:store_questions` checks normalized duplicate text and writes only validated records. |
| Runtime telemetry to log files | Usage metadata and security event details | Application to local logs | `observability.py:log_call` leaves unknowns null; `security.py:log_event` limits detail and excludes prompts, replies, and secrets. |

## What an attacker could try

- Put instructions in visible PDF text or hidden slide speaker notes to change topics, forge approval, or add a marker. Both supplied payloads were found in the corpus. A canary appearing in stored output would be evidence of success; the defended pipeline removes the matching instruction spans and checks the reply.
- Use a tool query such as `../.env` or `../topics_backup.json` to read files outside the approved data set. The argument remains search text; no tool argument is used as a path.
- Omit a required tool argument or supply malformed stored rows to trigger unexpected behavior or silently corrupt context. Pydantic argument models refuse malformed calls; result models log and drop malformed rows.
- Ask the model to repeat a question with different whitespace or capitalization. Normalized exact text duplicates are blocked; meaning-level paraphrases can still pass.

## The guardrails in place

| Guardrail | File and function | Which attack it addresses |
|---|---|---|
| Instruction pattern removal and untrusted-data labeling | `main.py:sanitise_document`, `main.py:prompt_messages` | PDF instruction block and speaker-note payload |
| Output schema, marker, topic, and source checks | `main.py:valid_output` | Injected verification marker, invented topic, false source |
| Argument validation and path containment | `tools.py:topic_lookup`, `tools.py:question_lookup`, `tools.py:load_data_file`, `tools.py:run_tool` | Missing argument and traversal-shaped query |
| Per-row result validation | `tools.py:topic_lookup`, `tools.py:question_lookup` | Malformed topic/question rows |
| Bounded tool loop | `main.py:run` | Tool calls that never stop |
| Storage-time duplicate check | `main.py:store_questions` | Exact normalized repeat despite tool or prompt behavior |
| Event recording | `security.py:log_event` and call sites above | Provides evidence that a guardrail was invoked |

## What each guardrail does not stop

- Pattern removal will miss novel paraphrases, instructions expressed as ordinary prose, or payloads split across line boundaries.
- Output checks cannot establish factual correctness, pedagogical quality, or whether an allowed source actually supports the item.
- Pydantic validates argument shape, not whether a well-formed query is appropriate or useful.
- Path containment does not protect against a compromised Python process or malicious local filesystem/runtime.
- Row validation drops malformed content but cannot recover data that was already lost or establish its provenance.
- Six tool steps can terminate a valid workflow that needs more calls and cannot force the model to provide a useful final reply.
- Exact normalized duplicate detection misses semantic paraphrases.
- Security logs record observed events but do not make the application tamper-proof or prove an unlogged action never occurred.

## What I would do with more time

1. Replace phrase-based filtering with a tested document classification and human review workflow that preserves quarantined payloads for audit.
2. Add semantic duplicate review and a reviewer approval state before questions can move into a production bank.
3. Add independent tests for symlink containment, malformed JSON, provider-specific refusal responses, and output provenance; the supplied checker does not cover every edge case.
4. Send security logs to append-only storage with access controls and retention monitoring.
