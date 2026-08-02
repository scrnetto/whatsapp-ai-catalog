#!/usr/bin/env python3
"""
Genera il catalogo unificato (repo GitHub + siti web) e aggiorna la skill globale
Claude Code 'ai-tools-catalog'.

Input  (nella root del progetto):
    github-repos.json          -> ogni repo deve avere: id, progetto, descrizione, url,
                                   categoria, fonte, macro (A..Z), uso
    marco-scarlino-siti-web.json -> ogni sito: id, sito, url, descrizione, fonte, macro, uso
    gh-meta.json               -> metadati attività per id repo (da fetch_gh_meta.py + scraping)

Output:
    catalogo-unificato.json    (root progetto)
    CATALOGO-AI-TOOLS.md       (root progetto)
    skill/SKILL.md             (root progetto: conteggi, data di verifica e indice categorie
                                rigenerati dai dati reali; il resto della prosa resta invariato)
    e copia dei tre (json -> catalogo.json) in ~/.claude/skills/ai-tools-catalog/

Uso:
    python3 scripts/build_catalog.py
"""
import json, os, re, datetime

ROOT  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.expanduser('~/.claude/skills/ai-tools-catalog')
SKILL_SRC = os.path.join(ROOT, 'skill', 'SKILL.md')

MACRO = {
 'A': 'Coding Agent, Claude Code & sviluppo AI-assistito',
 'B': 'Framework Agenti AI & assistenti personali',
 'C': 'LLM, modelli & inferenza locale',
 'D': 'RAG, memoria agenti & knowledge base',
 'E': 'OCR & parsing documenti',
 'F': 'Generazione media (video, immagini, 3D, voce)',
 'G': 'Sicurezza & supply-chain',
 'H': 'Dev tools, produttività & librerie',
 'I': 'Finanza & trading AI',
 'J': 'Ricerca AI, world models & dati vettoriali',
 'Z': 'Contenuti personali / non-dev',
}
ORDER = list("ABCDEFGHIJZ")

def today():
    return datetime.date.today()

def stato(m):
    if not m or m.get('archived'):
        return ('⚫', 'archiviato')
    p = (m.get('pushed') or '')[:10]
    if not p:
        return ('⚪', 'n/d')
    try:
        dt = datetime.date.fromisoformat(p)
    except Exception:
        return ('⚪', 'n/d')
    mo = (today() - dt).days / 30
    if mo <= 3:  return ('🟢', 'molto attivo')
    if mo <= 12: return ('🟢', 'attivo')
    if mo <= 24: return ('🟡', 'rallentato')
    return ('🔴', 'fermo')

def kfmt(n):
    if n is None: return 'n/d'
    return (f"{n/1000:.1f}k".replace('.0k', 'k')) if n >= 1000 else str(n)

def load(name):
    return json.load(open(os.path.join(ROOT, name), encoding='utf-8'))

def indice_categorie(unified):
    """Righe dell'indice rapido di SKILL.md: una per macro-categoria non vuota."""
    out = []
    for c in ORDER:
        items = [u for u in unified if u['macro'] == c]
        if not items: continue
        if c == 'Z':
            out.append(f"- **{c} · {MACRO[c]}** ({len(items)}): voci non rilevanti per i progetti "
                       "(salute, ricette, social) — ignorabili.")
            continue
        # stesso ordine delle tabelle nel markdown: repo per stelle desc, poi siti
        repos_c = sorted([u for u in items if u['tipo'] == 'repo'], key=lambda x: -(x['stelle'] or 0))
        sites_c = [u for u in items if u['tipo'] == 'sito']
        nomi = ', '.join(u['nome'] for u in repos_c + sites_c)
        out.append(f"- **{c} · {MACRO[c]}** ({len(items)}): {nomi}")
    return out

def sync_skill_md(unified, n_repo, n_sito):
    """Riallinea le parti dinamiche di skill/SKILL.md (conteggi nella description, data di
    verifica, indice categorie). E' la `description` a decidere quando Claude invoca la skill:
    se resta indietro il catalogo risulta sottodimensionato. Le sostituzioni che non trovano
    esattamente un match vengono segnalate invece di fallire in silenzio."""
    if not os.path.isfile(SKILL_SRC):
        return None, [f"⚠️ {SKILL_SRC} non trovato: SKILL.md non aggiornato"]

    txt, warn = open(SKILL_SRC, encoding='utf-8').read(), []

    def sub(pattern, repl, cosa, flags=0):
        nonlocal txt
        txt, n = re.subn(pattern, lambda m: repl(m), txt, flags=flags)
        if n != 1:
            warn.append(f"⚠️ SKILL.md: {cosa} non aggiornato ({n} match, atteso 1) — "
                        "il pattern non corrisponde più, correggi build_catalog.py o SKILL.md")

    sub(r'Catalogo curato di \d+ repository GitHub e \d+ siti/servizi web',
        lambda m: f'Catalogo curato di {n_repo} repository GitHub e {n_sito} siti/servizi web',
        'conteggi nella description')
    sub(r'verificati il \*\*\d{4}-\d{2}-\d{2}\*\*',
        lambda m: f'verificati il **{today().isoformat()}**', 'data di verifica')
    blocco = '\n'.join(indice_categorie(unified))
    sub(r'^(## Categorie e contenuto \(indice rapido\)\n).*?(?=^## )',
        lambda m: m.group(1) + blocco + '\n\n', 'indice categorie', flags=re.M | re.S)

    open(SKILL_SRC, 'w', encoding='utf-8').write(txt)
    return txt, warn

def main():
    repos = load('github-repos.json')
    siti  = load('marco-scarlino-siti-web.json')
    meta  = load('gh-meta.json')

    unified = []
    for r in repos:
        m = meta.get(str(r['id']), {})
        em, lab = stato(m)
        unified.append({
            'tipo': 'repo', 'macro': r.get('macro', 'H'), 'macro_nome': MACRO.get(r.get('macro', 'H')),
            'nome': r['progetto'], 'cosa_fa': r['descrizione'], 'quando_usarlo': r.get('uso', ''),
            'url': r['url'], 'stelle': m.get('stars'), 'ultimo_push': (m.get('pushed') or '')[:10],
            'attivita': lab, 'attivita_emoji': em, 'licenza': m.get('license'),
            'linguaggio': m.get('lang'), 'fonte': r.get('fonte', '')})
    for s in siti:
        c = s.get('macro', 'Z')
        unified.append({
            'tipo': 'sito', 'macro': c, 'macro_nome': MACRO.get(c),
            'nome': s['sito'], 'cosa_fa': s['descrizione'], 'quando_usarlo': s.get('uso', ''),
            'url': s['url'], 'stelle': None, 'ultimo_push': None, 'attivita': 'sito web',
            'attivita_emoji': '🌐', 'licenza': None, 'linguaggio': None, 'fonte': s.get('fonte', '')})

    json.dump(unified, open(os.path.join(ROOT, 'catalogo-unificato.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    # --- Markdown ---
    n_repo = sum(1 for u in unified if u['tipo'] == 'repo')
    n_sito = sum(1 for u in unified if u['tipo'] == 'sito')
    L = []
    L.append('# 📚 Catalogo strumenti AI & Dev — da chat "Marco Scarlino"')
    L.append('')
    L.append('> Catalogo unificato di **repository GitHub** e **siti/servizi web** raccolti dai reel Instagram')
    L.append('> e dai messaggi salvati nella chat WhatsApp personale di Marco Scarlino.')
    L.append(f'> **{n_repo} repository** + **{n_sito} siti web**, organizzati per categoria operativa.')
    L.append(f'> Stato attività verificato il **{today().isoformat()}**. '
             'Legenda: 🟢 attivo (push ≤12 mesi) · 🟡 rallentato · 🔴 fermo · ⚫ archiviato · 🌐 sito web.')
    L.append('')
    L.append('## Indice')
    for c in ORDER:
        n = sum(1 for u in unified if u['macro'] == c)
        if n: L.append(f"- **{MACRO[c]}** ({n})")
    L.append('')
    for c in ORDER:
        items = [u for u in unified if u['macro'] == c]
        if not items: continue
        repos_c = sorted([u for u in items if u['tipo'] == 'repo'], key=lambda x: -(x['stelle'] or 0))
        sites_c = [u for u in items if u['tipo'] == 'sito']
        L.append(f"## {MACRO[c]}")
        L.append('')
        L.append('| Progetto | Cosa fa | Quando usarlo | Stato |')
        L.append('|---|---|---|---|')
        for u in repos_c + sites_c:
            nome = f"[{u['nome']}]({u['url']})"
            cosa = (u['cosa_fa'] or '').replace('|', '/')
            quando = (u['quando_usarlo'] or '').replace('|', '/')
            if u['tipo'] == 'sito':
                stato_cell = '🌐 sito'
            else:
                lic = f" · {u['licenza']}" if u.get('licenza') and u['licenza'] != 'NOASSERTION' else ''
                stato_cell = f"{u['attivita_emoji']} ⭐{kfmt(u['stelle'])} · {u['ultimo_push'] or 'n/d'}{lic}"
            L.append(f"| {nome} | {cosa} | {quando} | {stato_cell} |")
        L.append('')
    md = '\n'.join(L) + '\n'
    open(os.path.join(ROOT, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md)

    # --- SKILL.md: riallinea conteggi, data e indice ---
    skill_md, warn = sync_skill_md(unified, n_repo, n_sito)

    # --- copia nella skill globale ---
    if os.path.isdir(SKILL):
        open(os.path.join(SKILL, 'CATALOGO-AI-TOOLS.md'), 'w', encoding='utf-8').write(md)
        json.dump(unified, open(os.path.join(SKILL, 'catalogo.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
        if skill_md is not None:
            open(os.path.join(SKILL, 'SKILL.md'), 'w', encoding='utf-8').write(skill_md)
        skill_msg = f"skill aggiornata: {SKILL}"
    else:
        skill_msg = f"⚠️ skill non trovata in {SKILL} (catalogo generato solo nel progetto)"

    by_cat = {c: sum(1 for u in unified if u['macro'] == c) for c in ORDER}
    print(f"Catalogo generato: {len(unified)} voci ({n_repo} repo + {n_sito} siti)")
    print("Per categoria:", {c: n for c, n in by_cat.items() if n})
    print(skill_msg)
    for w in warn:
        print(w)

if __name__ == '__main__':
    main()
