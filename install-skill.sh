#!/usr/bin/env bash
#
# Installa la skill Claude Code "ai-tools-catalog" su questo computer.
# Funziona su qualsiasi PC dove è presente Claude Code (richiede python3).
#
# Uso:
#   git clone <questo-repo> && cd <repo> && ./install-skill.sh
#
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.claude/skills/ai-tools-catalog"

echo "→ Installo la skill in: ${DEST}"
mkdir -p "${DEST}"

# 1) definizione della skill (statica)
cp "${SRC}/skill/SKILL.md" "${DEST}/SKILL.md"

# 2) rigenera catalogo dai dati del repo e popola la skill (CATALOGO-AI-TOOLS.md + catalogo.json)
if command -v python3 >/dev/null 2>&1; then
  python3 "${SRC}/scripts/build_catalog.py"
else
  echo "⚠️  python3 non trovato: copio i file già generati senza rigenerarli."
  cp "${SRC}/CATALOGO-AI-TOOLS.md" "${DEST}/CATALOGO-AI-TOOLS.md"
  cp "${SRC}/catalogo-unificato.json" "${DEST}/catalogo.json"
fi

echo "✅ Skill 'ai-tools-catalog' installata."
echo "   Da qualsiasi progetto Claude Code chiedi p.es.: \"che tool open-source esiste per fare OCR?\""
