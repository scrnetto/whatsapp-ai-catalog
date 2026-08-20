# WhatsApp → Catalogo strumenti AI/Dev + skill Claude Code

Sistema che legge i reel/link salvati nella chat WhatsApp personale (chat "con te stesso"),
ne estrae **repository GitHub** e **siti/servizi web** di strumenti AI e dev, verifica lo stato
di attività su GitHub, e mantiene un **catalogo consultabile da Claude Code in qualsiasi progetto**
tramite una skill globale.

## Cosa contiene il catalogo
- **69 repository GitHub** + **17 siti web**, in 10 categorie operative (Coding/Claude Code, LLM locali,
  RAG/memoria, OCR, generazione media, sicurezza, dev tools, finanza/trading, ricerca AI) + 1 non-dev.
- Per ogni voce: cosa fa, *quando usarlo*, e stato di attività (⭐ stelle, ultimo push, licenza).
- Versione leggibile: [`CATALOGO-AI-TOOLS.md`](CATALOGO-AI-TOOLS.md). Dati: `catalogo-unificato.json`.

## Installare la skill su un altro PC con Claude Code
```bash
git clone <URL-di-questo-repo> whatsapp-ai-catalog
cd whatsapp-ai-catalog
./install-skill.sh          # Linux/macOS
.\install-skill.ps1         # Windows (PowerShell)
```
Lo script copia la skill in `~/.claude/skills/ai-tools-catalog/` e rigenera il catalogo dai dati del
repo. Da quel momento, in **qualsiasi progetto** Claude Code, puoi chiedere ad es.
*"che libreria open-source uso per fare OCR su PDF?"* e la skill propone le voci pertinenti con stato.

> Richiede solo `python3` (libreria standard). Non serve token/credenziali.

## Aggiornare il catalogo (sul PC principale)
Serve il browser con WhatsApp Web loggato (e Instagram loggato per il monitoraggio profili).
- Da Claude Code: **`/aggiorna-catalogo`** (lancia l'agente `whatsapp-catalog-updater`).
- L'agente: legge la chat, controlla i profili Instagram dei creator già noti per reel nuovi,
  estrae/verifica i repo, e rigenera catalogo + skill. Vedi [`PIPELINE.md`](PIPELINE.md).

### Solo rigenerare il catalogo (senza rileggere WhatsApp)
```bash
python3 scripts/fetch_gh_meta.py   # aggiorna stelle/ultimo push (API GitHub, opzionale)
python3 scripts/build_catalog.py   # rigenera CATALOGO + catalogo.json e aggiorna la skill
```

## Struttura
| Percorso | Ruolo |
|---|---|
| `config.example.json` | Schema di configurazione: da copiare in `config.json` (gitignorato) |
| `github-repos.json` | Repo catalogati (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Siti web non-repo |
| `gh-meta.json` | Metadati attività GitHub per id |
| `instagram-profili.json` | Stato monitoraggio profili (reel già visti per handle) |
| `scripts/` | `fetch_gh_meta.py`, `build_catalog.py` |
| `skill/SKILL.md` | Definizione della skill (ridistribuibile) |
| `.claude/agents/` · `.claude/commands/` | Agente e slash command di aggiornamento |
| `install-skill.sh` | Installa la skill su un nuovo PC (Linux/macOS) |
| `install-skill.ps1` | Installa la skill su un nuovo PC (Windows) |

## Configurare la sorgente
La chat da leggere non è cablata nel codice: sta in `config.json`, che è **gitignorato**.

```bash
cp config.example.json config.json     # poi metti il nome della tua chat
```

| Campo | Effetto |
|---|---|
| `whatsapp.enabled` | `false` → salta del tutto la lettura di WhatsApp (usa solo i profili Instagram) |
| `whatsapp.chat` | Nome esatto della chat, come appare in WhatsApp Web |
| `whatsapp.self_chat` | `true` se è la chat "con te stesso" |
| `instagram.enabled` | `false` → salta il monitoraggio dei profili |
| `catalogo.titolo` / `catalogo.fonte` | Intestazione del catalogo generato |

Per una singola esecuzione puoi anche fare `/aggiorna-catalogo "Altra Chat"` oppure
`/aggiorna-catalogo --solo-instagram`, senza toccare la config.

**Il repo funziona anche senza WhatsApp**: con `whatsapp.enabled: false` resta un catalogo
alimentato dai profili Instagram in `instagram-profili.json`.

## Privacy
I file con i **messaggi WhatsApp personali** (CSV grezzo, riassunti, screenshot di login, snapshot
delle pagine), `config.json` e le voci non-dev (`siti-personali.json`) sono esclusi dal repo via
`.gitignore` e restano solo in locale. Nel repo finiscono solo il catalogo dei tool e il tooling.
Le voci taggate `macro: "Z"` (contenuti personali) vengono inoltre scartate da `build_catalog.py`
prima di generare gli output.
