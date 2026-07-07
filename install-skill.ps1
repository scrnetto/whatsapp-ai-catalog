#
# Installa la skill Claude Code "ai-tools-catalog" su questo computer.
# Funziona su qualsiasi PC Windows dove è presente Claude Code (richiede python3).
#
# Uso:
#   git clone <questo-repo>; cd <repo>; .\install-skill.ps1
#

$ErrorActionPreference = "Stop"

$SRC = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DEST = Join-Path $env:USERPROFILE ".claude\skills\ai-tools-catalog"

Write-Host "-> Installo la skill in: $DEST"
New-Item -ItemType Directory -Force -Path $DEST | Out-Null

# 1) definizione della skill (statica)
Copy-Item "$SRC\skill\SKILL.md" "$DEST\SKILL.md" -Force

# 2) rigenera catalogo dai dati del repo e popola la skill
$pythonExe = $null
foreach ($candidate in @("python3", "python")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") {
        $pythonExe = $cmd.Source
        break
    }
}
if (-not $pythonExe) {
    foreach ($path in @("C:\Python311\python.exe", "C:\Python312\python.exe", "C:\Python313\python.exe")) {
        if (Test-Path $path) { $pythonExe = $path; break }
    }
}

if ($pythonExe) {
    & $pythonExe "$SRC\scripts\build_catalog.py"
} else {
    Write-Host "ATTENZIONE: python non trovato: copio i file gia' generati senza rigenerarli."
    Copy-Item "$SRC\CATALOGO-AI-TOOLS.md" "$DEST\CATALOGO-AI-TOOLS.md" -Force
    Copy-Item "$SRC\catalogo-unificato.json" "$DEST\catalogo.json" -Force
}

Write-Host "Skill 'ai-tools-catalog' installata."
Write-Host "  Da qualsiasi progetto Claude Code chiedi p.es.: `"che tool open-source esiste per fare OCR?`""
