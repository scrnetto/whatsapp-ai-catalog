#!/usr/bin/env python3
"""
Fetch GitHub metadata (stars, last push, archived, license, language) for every repo in
github-repos.json and store it in gh-meta.json.

Usage:
    python3 scripts/fetch_gh_meta.py                # only repos with no metadata yet (default)
    python3 scripts/fetch_gh_meta.py --refresh      # re-fetch everything, oldest data first
    python3 scripts/fetch_gh_meta.py --refresh 30   # re-fetch only what was checked >30 days ago
    python3 scripts/fetch_gh_meta.py --limit 50     # stop after 50 repos
    python3 scripts/fetch_gh_meta.py --token TOKEN  # or set GITHUB_TOKEN in the environment

Rate limits: 60 requests/hour per IP unauthenticated, 5000/hour with a token. A full refresh of a
catalog larger than 60 repos therefore cannot finish in one unauthenticated run — so refreshes are
processed oldest-first and existing data is never discarded on failure. Re-running later resumes
where the previous run stopped; each entry carries a `fetched` date so progress is tracked.
"""
import json, re, time, urllib.request, urllib.error, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS = os.path.join(ROOT, 'github-repos.json')
META  = os.path.join(ROOT, 'gh-meta.json')

def slug(u):
    m = re.search(r'github\.com/([^/]+/[^/?#]+)', u)
    return '/'.join(m.group(1).rstrip('/').split('/')[:2]) if m else None

def parse_args(argv):
    """--refresh [GIORNI] / --limit N / --token T. Argomenti sconosciuti -> errore esplicito,
    cosi' un typo non viene scambiato per il comportamento di default."""
    opts = {'refresh': False, 'max_age': None, 'limit': None,
            'token': os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in ('--refresh', '-r'):
            opts['refresh'] = True
            if i + 1 < len(argv) and argv[i + 1].isdigit():
                opts['max_age'] = int(argv[i + 1]); i += 1
        elif a in ('--limit', '-n') and i + 1 < len(argv):
            opts['limit'] = int(argv[i + 1]); i += 1
        elif a == '--token' and i + 1 < len(argv):
            opts['token'] = argv[i + 1]; i += 1
        elif a in ('--help', '-h'):
            print(__doc__); sys.exit(0)
        else:
            print(f"Unknown argument: {a}", file=sys.stderr)
            print(__doc__, file=sys.stderr)
            sys.exit(2)
        i += 1
    return opts

def eta(entry):
    """Giorni dall'ultimo fetch. Le voci senza `fetched` sono anteriori a questo campo:
    valgono come infinitamente vecchie, cosi' il primo --refresh le prende per prime."""
    d = (entry or {}).get('fetched')
    if not d:
        return float('inf')
    try:
        return (datetime.date.today() - datetime.date.fromisoformat(d)).days
    except ValueError:
        return float('inf')

def da_fare(repos, meta, opts):
    """Repo da interrogare, nell'ordine in cui vanno interrogati."""
    def senza_meta(r):
        k = str(r['id'])
        return k not in meta or 'error' in meta.get(k, {})

    mancanti = [r for r in repos if senza_meta(r)]
    if not opts['refresh']:
        return mancanti, []
    vecchi = [r for r in repos if not senza_meta(r)
              and (opts['max_age'] is None or eta(meta.get(str(r['id']))) > opts['max_age'])]
    # i mancanti prima, poi i piu' stantii: se il rate limit taglia la run, taglia
    # la parte meno urgente
    vecchi.sort(key=lambda r: -eta(meta.get(str(r['id']))))
    return mancanti, vecchi

def fetch(s, token):
    """Ritorna (dati, quota_residua). GitHub dichiara la quota negli header di OGNI risposta:
    leggerla permette di fermarsi con l'ultima chiamata utile invece di sbattere nel 403."""
    headers = {'User-Agent': 'wa-catalog', 'Accept': 'application/vnd.github+json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    req = urllib.request.Request(f"https://api.github.com/repos/{s}", headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        d = json.load(resp)
        try:
            resta = int(resp.headers.get('X-RateLimit-Remaining'))
        except (TypeError, ValueError):
            resta = None
        return d, resta

def quando_riprende():
    """Ora locale in cui la quota si ricarica, chiesta a GitHub (costa 0 richieste)."""
    try:
        req = urllib.request.Request('https://api.github.com/rate_limit',
                                     headers={'User-Agent': 'wa-catalog'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            ts = json.load(resp)['resources']['core']['reset']
        return datetime.datetime.fromtimestamp(ts).strftime('%H:%M')
    except Exception:
        return None

def main():
    opts  = parse_args(sys.argv[1:])
    repos = json.load(open(REPOS, encoding='utf-8'))
    meta  = json.load(open(META, encoding='utf-8')) if os.path.exists(META) else {}
    oggi  = datetime.date.today().isoformat()

    mancanti, vecchi = da_fare(repos, meta, opts)
    coda = mancanti + vecchi
    if opts['limit']:
        coda = coda[:opts['limit']]

    if not coda:
        eta_msg = f" newer than {opts['max_age']} days" if opts['max_age'] else ""
        print(f"Nothing to do: all {len(repos)} repos already have metadata{eta_msg}.")
        return

    auth = 'token' if opts['token'] else 'anonymous (60 req/h)'
    print(f"Queue: {len(coda)} repos "
          f"({len(mancanti)} missing, {len(coda) - len(mancanti)} to refresh) · auth: {auth}")

    nuovi = rinfrescati = falliti = 0
    interrotto = False
    for r in coda:
        k, s = str(r['id']), slug(r['url'])
        if not s:
            continue
        era_presente = k in meta and 'error' not in meta[k]
        try:
            d, resta = fetch(s, opts['token'])
            meta[k] = {
                'slug': s, 'stars': d.get('stargazers_count'),
                'pushed': (d.get('pushed_at') or '')[:10],
                'archived': d.get('archived'), 'lang': d.get('language'),
                'license': (d.get('license') or {}).get('spdx_id'),
                'open_issues': d.get('open_issues_count'), 'desc': d.get('description'),
                'fetched': oggi}
            if era_presente:
                rinfrescati += 1
            else:
                nuovi += 1
            if resta is not None and resta <= 0:
                # quota esaurita: ci fermiamo con l'ultimo dato buono salvato, il resto
                # tocchera' al prossimo giro (la coda e' ordinata, quindi riparte dai piu' vecchi)
                interrotto = True
                break
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"⚠️  GitHub rate limit hit after {nuovi + rinfrescati} repos. "
                      "Re-run later to resume, or pass --token / set GITHUB_TOKEN.",
                      file=sys.stderr)
                interrotto = True
                break
            # 404 su un repo che avevamo: sparito o rinominato, va segnalato. Ma un errore
            # NON deve mai cancellare metadati validi gia' in archivio.
            if era_presente:
                meta[k]['last_error'] = e.code
                print(f"⚠️  {s}: HTTP {e.code} — keeping existing data", file=sys.stderr)
            else:
                meta[k] = {'slug': s, 'error': e.code}
            falliti += 1
        except Exception as e:
            if era_presente:
                meta[k]['last_error'] = str(e)[:50]
            else:
                meta[k] = {'slug': s, 'error': str(e)[:50]}
            falliti += 1
        time.sleep(0.0 if opts['token'] else 0.4)

    json.dump(meta, open(META, 'w', encoding='utf-8'), indent=1, ensure_ascii=False)

    missing = [str(r['id']) for r in repos
               if str(r['id']) not in meta or 'error' in meta.get(str(r['id']), {})]
    print(f"Fetched: {nuovi} new, {rinfrescati} refreshed, {falliti} failed | "
          f"with metadata: {len(repos) - len(missing)}/{len(repos)}")
    if missing:
        print("IDs without metadata (complete via browser HTML scraping):", ",".join(missing))
    if interrotto:
        rimasti = len(coda) - (nuovi + rinfrescati + falliti)
        reset = quando_riprende()
        quando = f" Quota resets around {reset}." if reset else ""
        print(f"Stopped early: {rimasti} repos left in the queue.{quando} "
              "Re-run to continue — the queue restarts from the stalest entries.")

if __name__ == '__main__':
    main()
