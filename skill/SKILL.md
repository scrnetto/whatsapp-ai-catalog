---
name: ai-tools-catalog
description: >-
  Catalogo curato di 95 repository GitHub e 19 siti/servizi web di strumenti AI e dev
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
4. I dati di attività sono stati verificati il **2026-08-02**: se serve precisione attuale,
   ricontrolla il repo (le stelle/push cambiano nel tempo).

## Categorie e contenuto (indice rapido)
- **A · Coding Agent, Claude Code & sviluppo AI-assistito** (18): Everything Claude Code, gstack, Spec Kit, ponytail, BMAD-METHOD, CLI-Anything, Ralph Loop, ai-website-cloner-template, Vibe Kanban, blender-mcp, knowledge-work-plugins, Dyad, Claude SEO, Pixel Agents, cc-blender-skill, BMAD-Speckit-SDD-Flow, Google Stitch, GitReverse
- **B · Framework Agenti AI & assistenti personali** (13): OpenClaw, odysseus, MiroFish, Agent-Reach, NanoBot, PicoClaw, Parlant, agent-lightning, SwarmClaw, J.A.R.V.I.S, JARVIS-PA-Lovable, Proactor.ai, agentskills.io
- **C · LLM, modelli & inferenza locale** (11): Unsloth AI, NanoChat, timesfm, Heretic, AirLLM, DwarfStar (ds4), Qwen3-Coder, whichllm, Kimi K2.5, IQuest-Coder-V1, SpikingBrain-7B
- **D · RAG, memoria agenti & knowledge base** (9): MinerU, Headroom, last30days-skill, open-notebook, Memvid, Easy Dataset, TencentDB-Agent-Memory, PixelRAG, VideoRAG
- **E · OCR & parsing documenti** (3): markitdown, Unlimited-OCR, GLM-OCR
- **F · Generazione media (video, immagini, 3D, voce)** (19): Deep-Live-Cam, VibeVoice, hyperframes, chatterbox, video-use, Supertonic, TRELLIS, palmier-pro, Qwen3-TTS, Z-Image, SAM Audio, ASCILINE, GLM-Image, Pusa V1.0 (Pusa-VidGen), GenieRedux, Seedance 2.0, ByteDance Seedance 2.0, ByteDance Seed, Mistral AI - Voxtral
- **G · Sicurezza & supply-chain** (7): Trivy, maigret, Anthropic-Cybersecurity-Skills, simplex-chat, SkillSpector, flowsint, Bumblebee
- **H · Dev tools, produttività & librerie** (19): Stirling-PDF, Pake, Penpot, Win11Debloat, twenty, cypress, supervision, CasaOS, Tolaria, aisuite, LibreTranslate, CuPy, TREK, dicebear, fli, TestSprite, Google Code Wiki, Render, Codeberg
- **I · Finanza & trading AI** (3): TradingAgents, ai-hedge-fund, Kronos
- **J · Ricerca AI, world models & dati vettoriali** (6): awesome-generative-ai-guide, zvec, AutoResearchClaw, SEAL (Self-Adapting LM), Jina AI, Google EmbeddingGemma
- **Z · Contenuti personali / non-dev** (6): voci non rilevanti per i progetti (salute, ricette, social) — ignorabili.

## Aggiornare il catalogo
La sorgente è la chat WhatsApp "Marco Scarlino". File di lavoro in `C:\progetti\whatsapp-ai-catalog\`:
`github-repos.json`, `marco-scarlino-siti-web.json`, `marco-scarlino-catalogo-completo.csv`,
`instagram-profili.json` (stato monitoraggio profili), `gh-meta.json` (metadati attività).
Quando arrivano nuovi reel/link: aggiorna i JSON, poi esegui `python scripts/fetch_gh_meta.py` e
`python scripts/build_catalog.py`. Quest'ultimo rigenera `CATALOGO-AI-TOOLS.md` + `catalogo.json`
e riallinea da solo, in questo file, i **conteggi nella description**, la **data di verifica** e
l'**indice categorie** qui sopra: non modificarli a mano, verrebbero sovrascritti. Il resto della
prosa è libero. La sorgente versionata è `skill/SKILL.md` nel progetto, copiata poi in questa
cartella.
