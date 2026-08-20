---
description: Legge i nuovi messaggi della chat WhatsApp configurata, cataloga repo/siti e aggiorna la skill ai-tools-catalog
---

Lancia l'agente **whatsapp-catalog-updater** per eseguire l'intero workflow di aggiornamento del
catalogo: leggere la chat WhatsApp configurata, trovare i reel/link nuovi, estrarne i repository
GitHub e i siti web, verificarli, recuperare lo stato di attività e rigenerare il catalogo
aggiornando la skill globale `ai-tools-catalog`.

**Sorgente:** definita in `config.json` (`whatsapp.chat`, `whatsapp.enabled`, `instagram.enabled`).
Se `config.json` non esiste, l'agente chiede il nome della chat invece di indovinarlo.

**Argomento opzionale:** un nome di chat passato qui sovrascrive `whatsapp.chat` per questa sola
esecuzione — utile per catalogare una chat diversa senza toccare la config. Passa `--solo-instagram`
per saltare la Fase A anche se `whatsapp.enabled` è `true`.

Prerequisito: WhatsApp Web aperto e loggato nel browser (non serve se la Fase A è disattivata).

$ARGUMENTS
