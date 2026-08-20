# Pipeline catalogo WhatsApp → skill `ai-tools-catalog`

Automatizza ciò che è stato fatto a mano: leggere la **chat WhatsApp configurata in `config.json`**, catalogare
repo GitHub e siti web condivisi (per lo più reel Instagram di AI/coding), e tenere aggiornata la
**skill globale Claude Code** consultabile da ogni progetto.

## Come si avvia
- **Slash command:** `/aggiorna-catalogo`  (richiede WhatsApp Web loggato nel browser)
- **Oppure** chiedendo: *"aggiorna il catalogo / controlla i nuovi reel"* →
  parte l'agente **`whatsapp-catalog-updater`** (`.claude/agents/`).

## Cosa fa l'agente (in breve)
**Fase A — Chat WhatsApp** *(saltata se `whatsapp.enabled: false`)*
1. Apre WhatsApp Web, apre la chat indicata da `whatsapp.chat` e raccoglie tutti i messaggi (scroll + dedup).
2. Confronta con il catalogo esistente e isola i **link nuovi**.

**Fase B — Monitoraggio profili Instagram** *(richiede Instagram loggato)*
- Ricava gli handle degli autori dei reel già catalogati (dal campo `fonte`), apre
  `instagram.com/{handle}/reels/` e scorre la griglia per scoprire **reel nuovi** pubblicati da quei
  creator. Stato tracciato in `instagram-profili.json` (controllo incrementale: si ferma quando trova
  reel già visti). Senza login Instagram questa fase viene saltata (login wall) e segnalata.

**Fasi comuni**
3. Per ogni nuovo reel (A o B) legge la **caption Instagram** (meta tag) e ne ricava il repo GitHub
   (esplicito o verificato via web) oppure il sito web; cataloga solo i reel tool-related; gli incerti
   restano segnalati.
4. Scrive i nuovi record (con `macro` + `uso`) in `github-repos.json` / `siti-web.json`.
5. Recupera i metadati di attività e **rigenera** catalogo + skill.

## Configurazione (`config.json`)
Il file è **gitignorato** perché contiene il nome della tua chat; lo schema tracciato è
`config.example.json`. Chi clona il repo copia l'example e mette la propria sorgente.

| Campo | Effetto |
|---|---|
| `whatsapp.enabled` | `false` → Fase A saltata del tutto (nessuna apertura di WhatsApp Web) |
| `whatsapp.chat` | Nome esatto della chat da aprire |
| `whatsapp.self_chat` | `true` = chat "con te stesso"; `false` = cercala per nome nella lista |
| `instagram.enabled` | `false` → Fase B (monitoraggio profili) saltata |
| `catalogo.titolo` / `catalogo.fonte` | Intestazione di `CATALOGO-AI-TOOLS.md` |

Override una tantum dal comando: `/aggiorna-catalogo "Nome Chat"`, `--solo-instagram`,
`--solo-whatsapp`. Senza `config.json`, l'agente chiede il nome della chat e `build_catalog.py`
usa i default neutri.

## File
| File | Ruolo |
|---|---|
| `config.json` / `config.example.json` | Configurazione locale (gitignorata) / schema tracciato |
| `github-repos.json` | Repo catalogati (`id, progetto, descrizione, url, categoria, fonte, macro, uso`) |
| `siti-web.json` | Siti web non-repo (stessi campi, `sito` al posto di `progetto`) |
| `gh-meta.json` | Metadati GitHub (stelle, ultimo push, licenza) per id |
| `instagram-profili.json` | Stato monitoraggio profili (handle → reel già visti/catalogati, ultimo controllo) |
| `chat-messaggi.csv` | Dump grezzo dei messaggi |
| `catalogo-unificato.json` / `CATALOGO-AI-TOOLS.md` | Output generati |
| `scripts/fetch_gh_meta.py` | Recupera metadati attività (merge incrementale) |
| `scripts/build_catalog.py` | Genera catalogo e aggiorna `~/.claude/skills/ai-tools-catalog/` |

## Rigenerare solo il catalogo (senza rileggere WhatsApp)
```bash
python3 scripts/fetch_gh_meta.py     # aggiorna stelle/push (opzionale)
python3 scripts/build_catalog.py     # rigenera MD+JSON e aggiorna la skill
```

## Note
- Macro-categorie (`macro`): A Coding/Claude Code · B Agenti AI · C LLM locali · D RAG/memoria ·
  E OCR · F Generazione media · G Sicurezza · H Dev tools · I Finanza/trading · J Ricerca AI · Z non-dev.
- L'API GitHub non autenticata limita a 60 richieste/ora: per i repo eccedenti l'agente usa lo
  scraping HTML same-origin dal browser (vedi prompt dell'agente).
- Principio guida: **non inventare URL**; gli elementi non verificabili vanno segnalati, non forzati.
