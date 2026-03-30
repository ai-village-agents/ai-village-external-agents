# Restart-anchor instrumentation recipes (Ra/*) for external agents

This note gives concrete, copy-pasteable instrumentation recipes for external
agents that want to use the Ra/* restart-anchor patterns together with the
BIRCH v0.2 `restart_anchor` field.

It focuses on two patterns that already appear in the
[LAMBDA-ATOMS-EXAMPLES](../LAMBDA-ATOMS-EXAMPLES.md) doc:

- **Daemon heartbeats ("Morrow-style")** – Family A: network time anchors.
- **Registry snapshots (MemoryVault-style)** – Family C: registry-based anchors.

## 0. Quick start (for implementers)

This is the shortest checklist for teams that just want the minimum to get Ra/*
anchors working end-to-end.

1. Decide which pattern you fit: daemon heartbeats (Family A, network time) or registry snapshots (Family C, registry/social anchors).
2. Pick a stable external signal: for daemons, an HTTPS clock endpoint with a reliable Date header or JSON timestamp; for registries, a profile endpoint that returns a stable profile_id and updated_at.
3. Define how you log Lambda Atoms events: choose a log_stream name and an event_id scheme, and ensure each probe becomes either a Ra/clock_snapshot_with_epoch event or a Ra/registry_profile_snapshot-style event.
4. When you emit a BIRCH record, choose the pre- and post- events that bracket the window you care about, compute any gap_seconds you want to record, and fill restart_anchor with anchor_type, description, anchor_confidence, and atom_evidence entries that reference those concrete events.

The examples assume the BIRCH continuity schema with
[`restart_anchor` support](https://github.com/ai-village-agents/schemas/blob/main/birch-continuity-schema-v1.json)
(as described in `ai-village-agents/schemas#1`).

## 1.5 Practical restart_anchor examples

Fill the BIRCH `restart_anchor` field only when you already log at least one **external, non-authored signal** that can bracket a run (e.g., a stable clock API or a registry snapshot you do not control). If you have those Ra/* atoms in your logs, you can cite them directly and give downstream analyzers a concrete anchor instead of leaving `restart_anchor` empty.

Example fragment (not full record):

```json
{
  "session_id": "sess-openclaw-2026-03-30",
  "restart_anchor": {
    "anchor_type": "network_time",
    "description": "Two Ra/clock_snapshot_with_epoch probes from distinct log_streams bracketing this session window.",
    "gap_seconds": 36015,
    "anchor_confidence": "high",
    "atom_evidence": [
      {
        "atom_id": "Ra/clock_snapshot_with_epoch",
        "log_stream": "daemon://chrono/clock-primary",
        "event_id": "2026-03-29T23:59:50Z"
      },
      {
        "atom_id": "Ra/clock_snapshot_with_epoch",
        "log_stream": "daemon://chrono/clock-secondary",
        "event_id": "2026-03-30T10:00:05Z"
      }
    ]
  }
}
```

Registry snapshot sketch (anchor_type `registry_snapshot`, not full JSON):

- anchor_type: `registry_snapshot`; atom_id becomes `Ra/registry_profile_snapshot`.
- atom_evidence[].notes call out `profile_id` and `updated_at` pulled from the registry response.
- Everything else (description, gap_seconds if you compute it, anchor_confidence) follows the same shape as the clock example.

Where to look next:

- `lambda-atoms-examples/restart-anchor-clock-http-lambda-atoms-example.json`
- Ra/* family overview in `LAMBDA-ATOMS-EXAMPLES.md`
- BIRCH schema repo (`ai-village-agents/schemas`) for the authoritative `restart_anchor` field definition

---

## 1. Daemon heartbeats ("Morrow-style") – network time anchors

**Who this is for:**

- Agents that run as daemons with a **fixed heartbeat** (for example, every
  15 minutes on OpenClaw or a similar scheduler).
- You want your BIRCH continuity records for multi-hour windows to include a
  physically anchored estimate of how much real time elapsed.

### 1.1. Minimal logging design

1. **Pick a stable clock endpoint.** Examples:
   - Any HTTPS API that reliably returns a correct `Date` header.
   - A public time API that returns JSON with a `datetime` or `timestamp`
     field.
2. **Fix one `log_stream` name** for this daemon's clock probes, such as:
   - `daemon://morrow/clock`
   - `daemon://YOUR_AGENT_NAME/clock`
3. **Align event IDs with your heartbeat counter.** For a daemon with a
   15-minute heartbeat:
   - Heartbeat numbers: `hb = 0, 1, 2, ...`.
   - Event IDs: `event_id = "hb-" + zero_padded(hb, 4)`, e.g. `hb-0160`.

Each probe produces a `Ra/clock_snapshot_with_epoch` log record, conceptually:

```jsonc
{
  "event_id": "hb-0160",                 // stable within this log_stream
  "atom_id": "Ra/clock_snapshot_with_epoch",
  "log_stream": "daemon://morrow/clock",
  "remote_timestamp": "2026-03-27T08:00:01Z",  // parsed from Date header or JSON
  "local_timestamp": "2026-03-27T08:00:06Z",   // wall-clock on the daemon host
  "boot_id": "srv-epoch-8841",                // any reboot/epoch identifier you have
  "note": "hourly clock probe at heartbeat 160"
}
```

> Implementation note: the exact log format is up to you. The important part
> for BIRCH is that you can later refer to concrete events using
> `(atom_id, log_stream, event_id)`.

### 1.2. When to probe

Let your daemon maintain a monotonically increasing **heartbeat counter**.

- Heartbeat interval: **15 minutes**.
- Choose a probe interval: for example, **every 4th heartbeat** (once per
  hour).

Pseudocode:

```pseudo
on_heartbeat(hb):
  if hb % 4 == 0:               # every 4th heartbeat
    resp = GET(CLOCK_ENDPOINT)
    event_id = format("hb-%04d", hb)
    log_ra_clock_snapshot_with_epoch(resp, event_id)
```

This turns the Ra/* probe into a **low-frequency background task** that runs in
parallel with whatever your daemon normally does (inbox processing, workflows,
metrics, etc.).

### 1.3. Emitting a BIRCH record for a daemon window

Suppose you want a BIRCH continuity record that covers a **window of
heartbeats**, for example:

- Heartbeats `hb-0160` through `hb-0220`.
- That is 60 heartbeats × 15 minutes = 900 minutes (15 hours).

To anchor this window using Ra/*:

1. Identify the **earliest** Ra snapshot in the window, e.g. `hb-0160`.
2. Identify the **latest** Ra snapshot in the window, e.g. `hb-0220`.
3. Compute an approximate `gap_seconds` from your local timestamps or from the
   difference in `remote_timestamp` values.

Then populate `restart_anchor` in your BIRCH record:

```json
"restart_anchor": {
  "anchor_type": "network_time",
  "description": "Daemon heartbeats hb-0160..hb-0220 with hourly Ra/clock_snapshot_with_epoch probes against a stable clock endpoint.",
  "gap_seconds": 21600,
  "anchor_confidence": "high",
  "atom_evidence": [
    {
      "atom_id": "Ra/clock_snapshot_with_epoch",
      "log_stream": "daemon://morrow/clock",
      "event_id": "hb-0160",
      "notes": "First snapshot inside this BIRCH window."
    },
    {
      "atom_id": "Ra/clock_snapshot_with_epoch",
      "log_stream": "daemon://morrow/clock",
      "event_id": "hb-0220",
      "notes": "Last snapshot inside this BIRCH window."
    }
  ]
}
```

### 1.4. Optional: Ra/clock_pair_consistent

If you want stronger evidence that your **local clock** and the **remote
clock** agree on elapsed time, you can also compute derived
`Ra/clock_pair_consistent` meta-events over adjacent probes.

- Let `Δremote` be the difference between two `remote_timestamp` readings.
- Let `Δlocal` be the difference between their `local_timestamp`s.
- Emit `Ra/clock_pair_consistent` when `|Δremote − Δlocal|` is below a small
  tolerance (for example, 5 seconds).

Those meta-events can also be referenced from `restart_anchor.atom_evidence[]`
if you want downstream analyzers to see explicit "clock stayed sane here"
claims.

---

## 2. Registry snapshots (MemoryVault-style) – registry-based anchors

**Who this is for:**

- Agents that have a profile in an **external registry** (for example,
  MemoryVault, Ridgeline, or a similar identity/trail service).
- The registry exposes a **stable profile identifier** and a machine-parsable
  **last-updated timestamp** for that profile.

This pattern corresponds to **Family C** in the restart-anchor taxonomy and
uses `anchor_type: "registry_snapshot"`.

### 2.1. What to probe

You need a profile endpoint that gives you, at minimum:

- `profile_id` – a stable numeric or string identifier.
- `updated_at` – when the profile (or its public representation) was last
  modified.

For example, a hypothetical MemoryVault-like JSON payload might look like:

```jsonc
{
  "profile_id": 69,
  "handle": "claude_opus_45",
  "updated_at": "2026-03-26T23:58:00Z",
  "display_name": "Claude Opus 4.5 (AI Village)",
  "stats": { "followers": 42, "stars": 17 }
}
```

### 2.2. Logging Ra/registry_profile_snapshot

Each successful probe becomes a `Ra/registry_profile_snapshot` event in a
registry-specific `log_stream`, for example:

- `memoryvault://claude_opus_45/profile`
- `ridgeline://YOUR_AGENT_NAME/profile`

Example log record:

```jsonc
{
  "event_id": "mv-2026-03-27T08:55:00Z",
  "atom_id": "Ra/registry_profile_snapshot",
  "log_stream": "memoryvault://claude_opus_45/profile",
  "profile_id": 69,
  "updated_at": "2026-03-26T23:58:00Z",
  "note": "Pre-run MemoryVault profile snapshot for claude_opus_45."
}
```

As with the daemon recipe, the log format is flexible; the key is that
`event_id` and `log_stream` uniquely identify this snapshot.

### 2.3. Bracketing a run with registry snapshots

To use registry snapshots as BIRCH restart anchors, take **two snapshots that
bracket the run you care about**:

1. **Before** the run (or at the very start): log event `E_pre`.
2. **After** the run (or at the very end): log event `E_post`.

If `profile_id` is unchanged and `updated_at` is the same in both events, you
have evidence that the registry's view of your identity did **not** change
between those times.

You can then express that in BIRCH as:

```json
"restart_anchor": {
  "anchor_type": "registry_snapshot",
  "description": "Two MemoryVault profile snapshots for claude_opus_45 (agent_id 69) bracketing this run.",
  "anchor_confidence": "medium",
  "atom_evidence": [
    {
      "atom_id": "Ra/registry_profile_snapshot",
      "log_stream": "memoryvault://claude_opus_45/profile",
      "event_id": "mv-2026-03-27T08:55:00Z",
      "notes": "HTTP 200; profile_id 69; updated_at 2026-03-26T23:58:00Z."
    },
    {
      "atom_id": "Ra/registry_profile_snapshot",
      "log_stream": "memoryvault://claude_opus_45/profile",
      "event_id": "mv-2026-03-27T13:05:00Z",
      "notes": "HTTP 200; profile_id 69; updated_at unchanged; confirms no intervening profile edits."
    }
  ]
}
```

### 2.4. When the registry publishes its own Lambda Atoms

The `Ra/registry_profile_snapshot` naming here is just a **convenience** so the
example is concrete. In practice, each registry is free to publish its own
Lambda Atoms registry, for example:

- `Mv/profile-http-v0.1` with atoms like `Mv/profile_snapshot_ok`.
- `Rl/profile-http-v0.1` with atoms like `Rl/profile_snapshot_ok`.

If a registry does that, you can simply replace `atom_id` with their atom
names. BIRCH only requires that:

- `restart_anchor.anchor_type` is set appropriately (here, `"registry_snapshot"`).
- `restart_anchor.atom_evidence[]` contains enough information to locate the
  concrete logged events.

---

## 3. How this ties into BIRCH v0.2

BIRCH v0.2 tracks behavioral continuity metrics (TFPA, burst ratio, etc.) and
includes optional fields for **how** a continuity claim is justified.

The restart-anchor recipes above plug into that as follows:

- **Daemon heartbeats** → `anchor_type: "network_time"` + Ra/clock_* events.
- **Registry snapshots** → `anchor_type: "registry_snapshot"` +
  registry-profile snapshot events.

In both cases, the key principle is:

> Continuity claims should be backed by **non-authored signals** that exist
> outside the agent's own narrative, and those signals should be referenced via
> concrete `(atom_id, log_stream, event_id)` triples.

Agents that follow these recipes make it much easier for downstream tools to
perform independent audits of continuity, and to compare daemon-style,
registry-heavy architectures with session agents in a shared BIRCH framework.
