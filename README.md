# WhatsApp → AI/Dev tools catalog + Claude Code skill

Reads the reels and links you save in a WhatsApp chat (typically the "message yourself" chat),
extracts **GitHub repositories** and **websites/services** for AI and dev tooling, checks how alive
each project is on GitHub, and keeps a **catalog that Claude Code can query from any project**
through a global skill.

> The tooling and docs are in English; the catalog *entries* are in Italian, because that is the
> language of the reels they come from. Section headings and status labels follow
> `catalogo.lingua` in your config — see [Configuration](#configuration).

## What the catalog holds
- **132 GitHub repositories** + **15 websites**, in 10 practical categories (coding agents/Claude
  Code, local LLMs, RAG/memory, OCR, media generation, security, dev tools, finance/trading, AI
  research). Counts are regenerated on every build.
- Per entry: what it does, *when to use it*, and activity status (⭐ stars, last push, license).
- Human-readable output: [`CATALOGO-AI-TOOLS.md`](CATALOGO-AI-TOOLS.md). Structured data:
  `catalogo-unificato.json`.

## Install the skill on another machine
```bash
git clone https://github.com/scrnetto/whatsapp-ai-catalog.git
cd whatsapp-ai-catalog
./install-skill.sh          # Linux/macOS
.\install-skill.ps1         # Windows (PowerShell)
```
The script copies the skill into `~/.claude/skills/ai-tools-catalog/` and rebuilds the catalog from
the data in the repo. From then on, in **any** Claude Code project, you can ask things like *"which
open-source library should I use for OCR on PDFs?"* and the skill surfaces the relevant entries with
their activity status.

> Needs only `python3` (standard library). No tokens or credentials required.

## Configuration
The chat to read is not hardcoded — it lives in `config.json`, which is **gitignored**:

```bash
cp config.example.json config.json     # then set your own chat
```

| Field | Effect |
|---|---|
| `whatsapp.enabled` | `false` → skip WhatsApp entirely (run on Instagram profiles alone) |
| `whatsapp.chat` | Exact chat name, as it appears in WhatsApp Web |
| `whatsapp.self_chat` | `true` if it is the "message yourself" chat |
| `instagram.enabled` | `false` → skip profile monitoring |
| `catalogo.titolo` / `catalogo.fonte` | Heading and source line of the generated catalog |
| `catalogo.lingua` | `it` (default) or `en` — language of category names, status labels and generated prose |

For a one-off run you can also use `/aggiorna-catalogo "Another Chat"` or
`/aggiorna-catalogo --solo-instagram` without touching the config.

**The project works without WhatsApp**: with `whatsapp.enabled: false` you still get a catalog fed
by the Instagram profiles tracked in `instagram-profili.json`.

Adding a language means adding one entry to `LOCALI` in `scripts/build_catalog.py`. Note that only
the *scaffolding* is translated — entry descriptions stay in whatever language they were written in,
and the prose of `skill/SKILL.md` is not generated, so it keeps its own language.

## Updating the catalog
Requires a browser with WhatsApp Web logged in (and Instagram logged in for profile monitoring).
- From Claude Code: **`/aggiorna-catalogo`** (runs the `whatsapp-catalog-updater` agent).
- The agent reads the chat, checks known creators' Instagram profiles for new reels, extracts and
  verifies the repos, then rebuilds the catalog and the skill. See [`PIPELINE.md`](PIPELINE.md).

### Rebuild only, without re-reading WhatsApp
```bash
python3 scripts/fetch_gh_meta.py   # refresh stars/last push (GitHub API, optional)
python3 scripts/build_catalog.py   # rebuild CATALOGO + catalogo.json and update the skill
```

## Layout
| Path | Role |
|---|---|
| `config.example.json` | Configuration schema — copy to `config.json` (gitignored) |
| `github-repos.json` | Catalogued repos (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Non-repo websites |
| `gh-meta.json` | GitHub activity metadata, keyed by repo id |
| `instagram-profili.json` | Profile-monitoring state (reels already seen, per handle) |
| `scripts/` | `fetch_gh_meta.py`, `build_catalog.py` |
| `skill/SKILL.md` | Skill definition (redistributable) |
| `.claude/agents/` · `.claude/commands/` | Update agent and slash command |
| `install-skill.sh` · `install-skill.ps1` | Install the skill on a new machine |

## Privacy
Files holding **personal WhatsApp content** (raw message dump, summaries, login screenshots, page
snapshots), `config.json`, and non-dev entries (`siti-personali.json`) are kept out of the repo via
`.gitignore` and stay local. Only the tool catalog and the tooling are committed.

Entries tagged `macro: "Z"` (personal content) are additionally dropped by `build_catalog.py` before
the outputs are generated — a second line of defence, so a personal entry that slips into a tracked
file still never reaches the published catalog.
