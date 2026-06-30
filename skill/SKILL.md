---
name: ai-tools-catalog
description: >-
  Catalogo curato di 68 repository GitHub e 17 siti/servizi web di strumenti AI e dev
  (coding agent & Claude Code, LLM e inferenza locale, RAG/memoria, OCR, generazione media
  video/immagini/3D/voce, sicurezza & supply-chain, dev tools, finanza/trading AI, ricerca AI),
  ciascuno con descrizione funzionale, stato di attività verificato su GitHub (stelle, ultimo
  push) e suggerimento d'uso. Usa questa skill quando l'utente cerca uno strumento, libreria,
  modello o repo per un progetto ("che tool esiste per X", "c'è un'alternativa open-source a Y",
  "come faccio OCR/RAG/TTS/fine-tuning", "un agente per Z"), vuole valutare alternative, o chiede
  se un progetto è ancora attivo/manutenuto. Fonte: chat WhatsApp personale di Marco Scarlino.
---

# Catalogo strumenti AI & Dev (Marco Scarlino)

Catalogo operativo di strumenti AI/dev raccolti dai reel Instagram e dai messaggi salvati in una
chat WhatsApp personale, ripuliti e arricchiti con metadati GitHub reali.

## File in questa skill
- **`CATALOGO-AI-TOOLS.md`** — versione leggibile completa, organizzata per categoria con tabelle
  (Progetto · Cosa fa · Quando usarlo · Stato). **Leggi questo file** per rispondere all'utente.
- **`catalogo.json`** — stessi dati in forma strutturata (1 oggetto per voce). Usalo quando devi
  **filtrare/cercare programmaticamente** (per categoria `macro`, per `tipo` repo/sito, per stato,
  per stelle). Campi: `tipo, macro, macro_nome, nome, cosa_fa, quando_usarlo, url, stelle,
  ultimo_push, attivita, licenza, linguaggio, fonte`.

## Come usarla
1. Quando l'utente cerca uno strumento o chiede "cosa esiste per fare X", **apri
   `CATALOGO-AI-TOOLS.md`** (o filtra `catalogo.json`) e proponi le voci pertinenti.
2. Cita sempre **stato di attività** (🟢/🟡/🔴, stelle, ultimo push) e **licenza** se rilevante per
   l'uso nel progetto dell'utente.
3. Se nessuna voce calza, dillo chiaramente: il catalogo è una raccolta personale, non esaustivo.
4. I dati di attività sono stati verificati il **2026-06-30**: se serve precisione attuale,
   ricontrolla il repo (le stelle/push cambiano nel tempo).

## Categorie e contenuto (indice rapido)
- **A · Coding Agent, Claude Code & sviluppo AI-assistito**: CLI-Anything, Spec Kit, Everything Claude Code, Pixel Agents, BMAD-METHOD, Vibe Kanban, Claude SEO, cc-blender-skill, blender-mcp, BMAD-Speckit-SDD-Flow, Ralph Loop, ai-website-cloner-template, Dyad, Google Stitch
- **B · Framework Agenti AI & assistenti personali**: NanoBot, Parlant, OpenClaw, PicoClaw, J.A.R.V.I.S, JARVIS-PA-Lovable, MiroFish, SwarmClaw, Proactor.ai, agentskills.io
- **C · LLM, modelli & inferenza locale**: Unsloth AI, Heretic, Kimi K2.5, Qwen3-Coder, NanoChat, IQuest-Coder-V1, AirLLM, whichllm, DwarfStar (ds4), SpikingBrain-7B
- **D · RAG, memoria agenti & knowledge base**: Easy Dataset, VideoRAG, last30days-skill, MinerU, Memvid, Headroom, TencentDB-Agent-Memory
- **E · OCR & parsing documenti**: GLM-OCR, Unlimited-OCR (vedi anche MinerU in D)
- **F · Generazione media (video, immagini, 3D, voce)**: TRELLIS, Qwen3-TTS, SAM Audio, Z-Image, VibeVoice, GLM-Image, Seedance 2.0, GenieRedux, Pusa V1.0, Supertonic, Deep-Live-Cam, Voxtral (Mistral)
- **G · Sicurezza & supply-chain**: Anthropic-Cybersecurity-Skills, flowsint, Trivy, SkillSpector (NVIDIA), Bumblebee (Perplexity)
- **H · Dev tools, produttività & librerie**: Stirling-PDF, Tolaria, Pake, supervision (Roboflow), CuPy, LibreTranslate, TestSprite, Google Code Wiki, Render
- **I · Finanza & trading AI**: Kronos, ai-hedge-fund, TradingAgents
- **J · Ricerca AI, world models & dati vettoriali**: AutoResearchClaw, zvec, SEAL, Jina AI, Google EmbeddingGemma
- **Z · Contenuti personali / non-dev**: voci non rilevanti per i progetti (salute, ricette, social) — ignorabili.

## Aggiornare il catalogo
La sorgente è la chat WhatsApp "Marco Scarlino" (file di lavoro in `~/progetti/whatsapp/`:
`github-repos.json`, `marco-scarlino-siti-web.json`, `marco-scarlino-catalogo-completo.csv`).
Quando arrivano nuovi reel/link, rigenera da lì e ricopia `CATALOGO-AI-TOOLS.md` e `catalogo.json`
in questa cartella.
