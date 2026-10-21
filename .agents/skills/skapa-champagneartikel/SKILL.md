---
name: skapa-champagneartikel
description: Skapa en faktagranskad champagneartikel med AI, korrekt JSON-schema, lokal bild och säker publicering utan att skriva över webbplatskod.
---

# Skapa champagneartikel – agent skill

Använd denna skill när användaren ber om en ny artikel till Maison Éclat. Arbeta i denna ordning:

1. **Ämne och mål:** fråga efter ämne, tänkt läsare och fokusfråga om det saknas. Formulera en saklig artikelidé och sökord, inte bara reklamspråk.
2. **Research:** kontrollera påståenden mot pålitliga källor, helst flera oberoende. Markera osäkra uppgifter. Skriv inte påhittade historiska fakta om Maison Éclat – varumärket är fiktivt.
3. **AI-utkast:** skriv ett nytt JSON-utkast i valfri mapp **utanför `webbplats`**. Följ schemat nedan. Svenska, informativt, välskrivet, korrekt rubrikhierarki och normalt 350–650 ord. Inga markdownkodstaket inne i JSON.
4. **Bild:** använd en egen eller AI-skapad bild sparad lokalt (.png/.jpg/.webp/.svg). Bilden ska avbilda det artikeln faktiskt handlar om; skriv en konkret alt-text.
5. **Mänsklig kontroll:** låt användaren läsa, granska, rätta påståenden och godkänna artikeln + eventuell bild innan publicering. Undvik att AI skapar vilseledande källor, copyright-problem eller påståenden om att en fiktiv produkt finns till försäljning.
6. **Validera och publicera:** kör `publicera_artikel.py` med ett unikt slug och den godkända bildfilen. Först `--kontrollera`, sedan utan flaggan efter godkännande.
7. **Granska webbplatsen:** öppna `artikel.html?id=slug` i Live Server. Lägg till en länk från startsidan **manuellt** efter kontroll – AI-skillen får inte ändra den existerande HTML-filen.
8. **Lärande:** notera användarens feedback om SEO, ton, bild och faktakvalitet; förbättra nästa artikel utan att skriva över tidigare publicerat innehåll.

## Struktur på artikelutkastet

```json
{
  "slug": "ny-champagneartikel",
  "title": "En informativ rubrik om champagne",
  "description": "En konkret ingress på minst fyrtio tecken om vad läsaren får veta.",
  "category": "GUIDE",
  "author": "Maison Éclat",
  "date": "20 oktober 2026",
  "image": { "alt": "En konkret och beskrivande text om den valda bilden" },
  "content": [
    { "type": "paragraph", "text": "Inledning." },
    { "type": "heading", "text": "Första mellanrubriken" },
    { "type": "paragraph", "text": "Fördjupning." },
    { "type": "subheading", "text": "En underrubrik" },
    { "type": "list", "items": ["Första tipset", "Andra tipset"] },
    { "type": "paragraph", "text": "Avslutning." }
  ],
  "sources": ["Författarens egna redaktionella råd; kontrollera sakpåståenden"]
}
```

Tillåtna blocktyper: `paragraph`, `heading` (blir h2), `subheading` (blir h3), `list`, `quote`, `image`. Endast en h1 per artikelsida: den kommer automatiskt från `title`.

## Körning

Från projektets rotmapp:

```bash
python .agents/skills/skapa-champagneartikel/scripts/publicera_artikel.py --utkast UTKAST.json --slug min-nya-artikel --bild MIN-BILD.webp --kontrollera
python .agents/skills/skapa-champagneartikel/scripts/publicera_artikel.py --utkast UTKAST.json --slug min-nya-artikel --bild MIN-BILD.webp
```

Utan `--bild` skapar skriptet en enkel illustrerad SVG i `webbplats/images`.

## Hårda skyddsregler

- Ändra **inte** redan befintliga filer i `webbplats`, inklusive `index.html`, `style.css`, `script.js`, `artikel.html`, `artikel.css`, `artikel.js` eller gamla artiklar och bilder.
- Skapa **endast** nya JSON-filer i `webbplats/artiklar` och nya bilder i `webbplats/images`.
- Filnamn ska vara små bokstäver a–z med bindestreck, utan åäö eller mellanslag.
- Spara aldrig API-nycklar, token eller lösenord i projektet. Skillen kräver ingen automatisk API-anslutning.
- Publicera aldrig utan mänsklig faktagranskning och beslut.
