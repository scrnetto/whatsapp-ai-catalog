# WhatsApp catalog pipeline → `ai-tools-catalog` skill

Automates what used to be done by hand: read the **WhatsApp chat configured in `config.json`**,
catalog the GitHub repos and websites shared there (mostly Instagram reels about AI/coding), and
keep the **global Claude Code skill** — queryable from any project — up to date.

## How to run it
- **Slash command:** `/aggiorna-catalogo` (needs WhatsApp Web logged in, unless Phase A is disabled)
- **Or** just ask: *"update the catalog / check for new reels"* → this starts the
  **`whatsapp-catalog-updater`** agent (`.claude/agents/`).

## What the agent does
**Phase A — WhatsApp chat** *(skipped when `whatsapp.enabled: false`)*
1. Opens WhatsApp Web, opens the chat named by `whatsapp.chat`, and collects every message
   (scroll + dedup — WhatsApp virtualises the DOM, so messages are gathered *during* the scroll).
2. Diffs against the existing catalog and isolates the **new links**.

**Phase B — Instagram profile monitoring** *(skipped when `instagram.enabled: false`; needs Instagram logged in)*
- Derives the handles of creators whose reels are already catalogued (from the `fonte` field), opens
  `instagram.com/{handle}/reels/` and scans the grid for **new reels** from those creators. State is
  tracked in `instagram-profili.json` — the check is incremental and stops at the first reel already
  seen. Without an Instagram login this phase hits the login wall, gets skipped, and is reported.

**Both phases**
3. For each new reel, reads the **Instagram caption** (meta tag) and derives the GitHub repo (explicit
   or verified via web search) or the website. Only tool-related reels are catalogued; anything
   uncertain is reported rather than guessed.
4. Writes the new records (with `macro` + `uso`) into `github-repos.json` / `siti-web.json`.
5. Fetches activity metadata and **rebuilds** the catalog and the skill.

## Configuration (`config.json`)
The file is **gitignored** because it holds the name of your chat; the tracked schema is
`config.example.json`. Anyone cloning the repo copies the example and points it at their own source.

| Field | Effect |
|---|---|
| `whatsapp.enabled` | `false` → Phase A skipped entirely (WhatsApp Web never opened) |
| `whatsapp.chat` | Exact name of the chat to open |
| `whatsapp.self_chat` | `true` = the "message yourself" chat; `false` = look it up by name in the list |
| `instagram.enabled` | `false` → Phase B (profile monitoring) skipped |
| `catalogo.titolo` / `catalogo.fonte` | Heading and source line of `CATALOGO-AI-TOOLS.md` |
| `catalogo.lingua` | `it` (default) or `en` — language of category names, status labels and generated prose |

One-off overrides from the command: `/aggiorna-catalogo "Chat Name"`, `--solo-instagram`,
`--solo-whatsapp`. With no `config.json`, the agent asks which chat to read and `build_catalog.py`
falls back to neutral defaults.

## Files
| File | Role |
|---|---|
| `config.json` / `config.example.json` | Local configuration (gitignored) / tracked schema |
| `github-repos.json` | Catalogued repos (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Non-repo websites (same fields, `sito` instead of `progetto`) |
| `gh-meta.json` | GitHub metadata (stars, last push, license) by repo id |
| `instagram-profili.json` | Profile-monitoring state (handle → reels seen/catalogued, last check) |
| `chat-messaggi.csv` | Raw message dump (gitignored) |
| `catalogo-unificato.json` / `CATALOGO-AI-TOOLS.md` | Generated outputs |
| `siti-personali.json` | Non-dev entries, kept out of the repo (gitignored) |
| `scripts/fetch_gh_meta.py` | Fetches activity metadata (incremental merge) |
| `scripts/build_catalog.py` | Builds the catalog and updates `~/.claude/skills/ai-tools-catalog/` |

## Rebuild only, without re-reading WhatsApp
```bash
python3 scripts/fetch_gh_meta.py     # refresh stars/push (optional)
python3 scripts/build_catalog.py     # rebuild MD+JSON and update the skill
```

## Notes
- Macro categories (`macro`): A coding/Claude Code · B AI agents · C local LLMs · D RAG/memory ·
  E OCR · F media generation · G security · H dev tools · I finance/trading · J AI research ·
  **Z personal/non-dev → private file, never committed**.
- Unauthenticated GitHub API is capped at 60 requests/hour: for repos beyond that the agent falls
  back to same-origin HTML scraping from the browser (see the agent prompt).
- Guiding principle: **never invent URLs**. Anything unverifiable is reported, not forced.
