#!/usr/bin/env python3
"""
Recupera i metadati GitHub (stelle, ultimo push, archived, licenza, linguaggio)
per tutti i repo in github-repos.json e li salva in gh-meta.json.

Uso:
    python3 scripts/fetch_gh_meta.py

API GitHub non autenticata: 60 richieste/ora per IP. Se il rate limit viene colpito,
i repo mancanti restano senza metadati: completarli con lo scraping HTML same-origin
dal browser (vedi PIPELINE.md) oppure ri-eseguire più tardi (lo script fa il merge,
NON ricomincia da capo se gh-meta.json esiste già).
"""
import json, re, time, urllib.request, urllib.error, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS = os.path.join(ROOT, 'github-repos.json')
META  = os.path.join(ROOT, 'gh-meta.json')

def slug(u):
    m = re.search(r'github\.com/([^/]+/[^/?#]+)', u)
    return '/'.join(m.group(1).rstrip('/').split('/')[:2]) if m else None

def main():
    repos = json.load(open(REPOS))
    meta = json.load(open(META)) if os.path.exists(META) else {}
    done = skipped = 0
    for r in repos:
        k = str(r['id'])
        if k in meta and 'error' not in meta[k]:
            skipped += 1; continue
        s = slug(r['url'])
        if not s:
            continue
        api = f"https://api.github.com/repos/{s}"
        try:
            req = urllib.request.Request(api, headers={'User-Agent': 'wa-catalog', 'Accept': 'application/vnd.github+json'})
            with urllib.request.urlopen(req, timeout=15) as resp:
                d = json.load(resp)
            meta[k] = {
                'slug': s, 'stars': d.get('stargazers_count'), 'pushed': (d.get('pushed_at') or '')[:10],
                'archived': d.get('archived'), 'lang': d.get('language'),
                'license': (d.get('license') or {}).get('spdx_id'),
                'open_issues': d.get('open_issues_count'), 'desc': d.get('description')}
            done += 1
        except urllib.error.HTTPError as e:
            meta[k] = {'slug': s, 'error': e.code}
            if e.code == 403:
                print(f"⚠️  Rate limit GitHub colpito dopo {done} repo. Restanti da completare via scraping HTML.", file=sys.stderr)
                break
        except Exception as e:
            meta[k] = {'slug': s, 'error': str(e)[:50]}
        time.sleep(0.4)
    json.dump(meta, open(META, 'w'), indent=1)
    missing = [str(r['id']) for r in repos if str(r['id']) not in meta or 'error' in meta.get(str(r['id']), {})]
    print(f"Recuperati ora: {done} | già presenti: {skipped} | totale con metadati: {len(repos)-len(missing)}/{len(repos)}")
    if missing:
        print("ID senza metadati (completare via scraping HTML browser):", ",".join(missing))

if __name__ == '__main__':
    main()
