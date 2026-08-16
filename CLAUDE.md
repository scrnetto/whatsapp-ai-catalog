# whatsapp-ai-catalog

<!-- Da COMMITTARE nella root del repo come CLAUDE.md (o da APPENDERE al CLAUDE.md esistente).
     Viaggia con GitHub: Claude Code lo legge su QUALSIASI PC in cui il repo viene clonato. -->

## 🔒 Controllo di sicurezza obbligatorio (preflight)

Prima di **riprendere il lavoro** su questo progetto dopo una pausa, e **SEMPRE prima di un
deploy in produzione**, esegui la checklist in **`.claude/PREFLIGHT-security-check.md`** e riporta
l'esito. Vale anche alla prima apertura dopo un clone.

Sintesi dei punti da verificare (dettagli nel file):
- Sink di esecuzione con input utente: `child_process`/`exec`/`eval`/`new Function`/`vm`/`require` dinamico.
- SSRF/proxy con URL forniti dal client (es. `/sentry-tunnel`): destinazione in allow-list.
- `npm audit` + versioni esatte di framework/dipendenze (Next.js, next-auth, sharp…) contro CVE note.
- Nessun segreto committato/esposto; porte DB legate a `127.0.0.1` (mai `0.0.0.0`).
- Se dockerizzato: rootfs read-only, `/tmp` noexec, utente non-root, egress firewall.

Origine: incidente RCE Node/Next.js → cryptominer (2026). Se rilevi indicatori di compromissione
sul server (processi `xmrig/cheddar/minerd`, binari in `/tmp`, exe `(deleted)` in esecuzione,
connessioni in uscita anomale), **fermati e avvisa**.
