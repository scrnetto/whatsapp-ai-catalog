# Preflight Security Check — Node/Next.js RCE & Cryptominer

> Origine: incidente reale su `terris-geospatial` (terrisgeospatial.it), 2026-08-16 — RCE nel
> processo Next.js → reverse shell → miner XMRig. Report completo: `~/.claude/security/INCIDENT-terris-geospatial.md`.

**Quando eseguire questo controllo:**
- Quando si **riprende a lavorare** su un progetto dopo una pausa.
- **SEMPRE prima di una messa in produzione / deploy.**
- Su **ogni progetto clonato o iniziato da zero**, la prima volta che ci si lavora.

Applica soprattutto a web app Node/Next.js/Express, ma i punti 4–6 valgono per qualunque stack.

---

## A) Verifica se il progetto è VULNERABILE (audit del codice)

1. **Sink di esecuzione con input utente** — cerca e verifica che NON ricevano dati non fidati:
   ```
   grep -rnE "child_process|exec\(|execSync|spawn|eval\(|new Function|vm\.|require\([^'\"]" src app pages server 2>/dev/null
   ```
2. **SSRF / proxy** — endpoint che inoltrano richieste a URL forniti dal client (es. `/sentry-tunnel`,
   image proxy, webhook relay). L'URL/destinazione deve essere **allow-list**, mai arbitrario.
   ```
   grep -rniE "sentry-tunnel|fetch\(|axios|got\(|http\.request|url\.parse" app pages src 2>/dev/null | grep -i tunnel
   ```
3. **Dipendenze vulnerabili**:
   ```
   npm audit --omit=dev ; npm ls next next-auth sharp 2>/dev/null
   ```
   Controllare CVE note per la versione ESATTA di Next.js / next-auth / sharp in uso.
4. **Segreti**: nessun segreto committato; env non esposto a route pubbliche; pronti a **ruotare**
   se il server è stato compromesso.
5. **Esposizione porte**: in `docker-compose*.yml` i DB e i servizi interni devono legarsi a
   `127.0.0.1`, MAI `0.0.0.0`/porta pubblica. (`ports: - "127.0.0.1:5432:5432"`)
6. **Hardening container** (se dockerizzato): rootfs read-only, `/tmp` con `noexec`, utente non-root,
   egress firewall (blocca reverse shell e mining pool).

## B) Verifica se un SERVER è già COMPROMESSO (IOC — indicatori di compromissione)

```
# processi/binari sospetti in /tmp e cwd anomale
ps aux | grep -iE "cheddar|xmrig|minerd|/tmp/" | grep -v grep
ls -la /tmp /var/tmp /dev/shm 2>/dev/null
# binari cancellati ma in esecuzione (classico occultamento)
sudo ls -l /proc/*/exe 2>/dev/null | grep -i deleted
# connessioni in uscita verso pool/C2
sudo ss -tnp | grep -vE ':22|:80|:443|:5432|127.0.0.1' | head
# load anomalo / molti processi identici come utente di servizio
uptime; top -bn1 | head -20
```

**IOC noti da questo incidente** (da cercare ovunque):
- C2 reverse shell: `185.177.72.3:20015`
- Pool mining: `xmproxy.scrap-transport-musical-hospital-brainstorm.com` (porte 10028–10036)
- XMRig BuildID: `c746d5445679e29ea09a8ae5bdc7fbbbf3720c44`
- Nomi file: `cheddar`, `.n`, `system-check`, `npm_update`, `batch5`, `virtuoso`,
  `pls_pak_choi`, `HelloMrMeeseeks`, `YELLOWMRMEESEEKS`, `niggastuna`, `safenet-client-alpine-amd64`

## C) Se trovi compromissione
Non riavviare l'app com'è. Contieni (ferma container/servizio), estrai le prove (`docker diff`,
`/tmp`, `/var/tmp`), **ruota tutti i segreti**, ricostruisci da sorgente pulito, chiudi il vettore
d'ingresso trovato in (A). Vedi il report terris per la procedura dettagliata.
