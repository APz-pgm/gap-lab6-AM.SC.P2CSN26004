# Lab 6 run report

## Scope

The uploaded materials included the Lab 6 assignment brief and `Lab6_Starter.zip`. No Lab 5 repository or Lab 5 files were present. The runtime and documentation absent from the starter were reconstructed from the brief and fixed interfaces in the supplied starter. The Lab 5 `REPORT.md`, prior decision history, original nine observability field names, and `samples/run_log_sample.jsonl` could not be carried forward. `observability.py` therefore provides a documented nine-field reconstruction; compare it with your Lab 5 version and restore its original field names if available.

## Verification performed

`python check.py .` completed in self-check mode against the submission folder. Result: 8.5 / 8.5 automated marks passed. The checker also reported repository-state gates separately; the tag gate is not satisfied because no GitHub repository was supplied.

The check exercised corpus ingestion, both injected documents, invalid output, tool schema generation, traversal input, malformed tool arguments, malformed stored question rows, non-terminating tool calls, duplicate blocking, and trace structure. The output was also run directly with `stub:obedient` in a disposable copy; the security log recorded input and output guardrail events, and zero stored question rows contained the marker.

A disposable baseline copy with the relevant input and output checks disabled was run with `stub:obedient`. It printed `ok` while storing the generated marker. This is evidence from an explicitly vulnerable baseline, not from the defended implementation.

## Limits

No real provider credentials were supplied or used. No real-model quality, cost, or factuality claim is made. The checker does not prove protection against unseen injection phrasings, semantic duplicates, or all parser and filesystem edge cases. GitHub collaborator status, remote push, and tag publication must be completed in the user's private repository.
