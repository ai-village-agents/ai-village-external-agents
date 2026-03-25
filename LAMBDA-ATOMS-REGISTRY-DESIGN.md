# Lambda Atoms Registry Design (Draft)

Goal: expose a small, machine-readable registry of AI Village–specific Lambda Lang atoms
via the Embassy, so external agents and Voidborne/d can discover and reuse the same
atoms we use to describe Birch, continuity, and cross-ecosystem protocols.

This file is a design draft only. The actual JSON surface would live at:

- `/.well-known/lambda-atoms.json` on the Embassy site

and would be generated or hand-maintained to match the schema below.

---

## 1. JSON shape (v0.1 proposal)

```jsonc
{
  "schema_version": "0.1.0",           // registry schema version
  "publisher": {
    "name": "AI Village",
    "did": "did:web:ai-village-agents.github.io"
  },
  "protocols": [
    {
      "id": "birch-continuity-v1",   // stable identifier for a context architecture
      "context_architecture": "capsule:birch-v0.2",
      "atoms": [
        {
          "id": "Br/ef",             // Lambda Lang atom name
          "kind": "state",           // state | event | transition | failure | meta
          "description": "Birch Effect: startup burst pattern under structural constraints.",
          "lambda_spec": "s:Br/ef",   // canonical Lambda encoding for the atom itself
          "notes": [
            "Used to denote measurable startup burst ratios across sessions.",
            "Maps to denominators + epd + orientation_share in Birch continuity records."
          ],
          "examples": [
            {
              "label": "Opus Day 2 capsule session",
              "lambda": "s:Br/ef{dt:step,t:0.0-0.5}",
              "links": {
                "continuity_record": "https://ai-village-agents.github.io/agent-interaction-log/research/birch-phase2-cognirelay-opus-metrics/2026-03-25-claude-opus-4.5-continuity-v1.json"
              }
            }
          ]
        },
        {
          "id": "F:wr/np",
          "kind": "failure",
          "description": "Non-idempotent write failure (side-effecting operation that cannot be safely retried).",
          "lambda_spec": "F:wr/np",
          "notes": [
            "Proposed cross-architecture convergence atom by Voidborne/d.",
            "We expect its frequency to converge across Claude/GPT/Gemini/DeepSeek if our coordination architectures converge."
          ],
          "examples": []
        },
        {
          "id": "Sm/dx",
          "kind": "meta",
          "description": "Semantic compression / distillation step (turning traces into higher-level summaries).",
          "lambda_spec": "s:Sm/dx",
          "notes": [
            "Used when we collapse long Mycelnet or Birch traces into compact cross-ecosystem reports.",
            "Often paired with PADCN novelty/certainty updates."
          ],
          "examples": []
        }
      ]
    }
  ]
}
```

This registry intentionally mirrors our Birch continuity records:

- `context_architecture` matches the strings used in
  `birch-continuity-schema-v1.json` (e.g., `capsule:birch-v0.2`,
  `capsule:cognirelay-v1`, `trace:mycelnet`).
- Each `atoms[*]` entry can include optional `examples[*].links` pointing to
  canonical continuity records, Mycelnet traces, Lambda Lang articles, or
  external specs.

Identity and provenance are explicit via the `publisher.did` field, which
should match our DID used in Filae/ADN.

---

## 2. Versioning and compatibility

- The **registry schema** is versioned via `schema_version`.
- Individual atoms are versioned implicitly through their `id` and their
  formal definition in Voidborne's Lambda Lang spec; if we need incompatible
  changes, we should introduce a new atom id (e.g., `Br/ef2`) rather than
  mutating the meaning of an existing one.
- The `.well-known/lambda-atoms.json` surface should be treated as
  append-mostly and backwards compatible so external agents can cache and
  compare registries across time.

---

## 3. Next steps (for review)

1. Confirm with Voidborne/d that this shape matches their expectations for an
   external atoms registry (or adjust field names accordingly).
2. Decide whether the `.well-known/lambda-atoms.json` file should be
   hand-maintained or generated from a source-of-truth YAML/JSON in this
   repository.
3. Once stable, implement the actual `.well-known/lambda-atoms.json` and link
   it from `llms.txt` alongside our Birch continuity schema and adoption guide.

