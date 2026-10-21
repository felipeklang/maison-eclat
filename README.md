# Maison Éclat – HTML/CSS/JavaScript + AI-artikelplugin

**Individuell inlämningsuppgift, deadline 23 oktober 2026 kl. 23.59.**

Maison Éclat är ett **fiktivt champagnevarumärke** som används för att demonstrera webbutveckling, redaktionellt innehåll och ett AI-stött arbetsflöde. Det är ingen verklig butik och nyhetsbrevet skickar inga mejl. Fotografiska flaskbilderna är AI-genererade för skolprojektet.

## Starta webbplatsen

1. Packa upp hela ZIP-filen så att projektmappen `maison-eclat-ny` får behålla sin mappstruktur.
2. Öppna projektmappen i **Visual Studio Code**.
3. Installera tillägget **Live Server** om det saknas.
4. Högerklicka på `webbplats/index.html` och välj **Open with Live Server**. (Alternativt använd `python -m http.server 5500 --directory webbplats` från projektmappen.)
5. Prova att klicka på flaskorna, produkternas pilar och de tre artikellänkarna.
6. Testa formuläret längst ner. Ett nytt `p`-element skapas i JavaScript efter inskickning.
7. Testa även `webbplats/artikel.html?id=test-artikel` och en riktig artikel, till exempel `artikel.html?id=valj-ratt-champagneglas`.

**Obs:** Artikeldata läses med `fetch()`. Webbläsare blockerar ofta `fetch` från en lokal `file://`-adress, så kör via Live Server.

## Mappstruktur

```text
maison-eclat-ny/
├── AGENTS.md
├── README.md
├── .gitignore
├── .agents/
│   └── skills/
│       └── skapa-champagneartikel/
│           ├── SKILL.md
│           └── scripts/
│               └── publicera_artikel.py
└── webbplats/
    ├── index.html
    ├── style.css
    ├── script.js
    ├── artikel.html
    ├── artikel.css
    ├── artikel.js
    ├── artiklar/
    │   ├── test-artikel.json
    │   ├── valj-ratt-champagneglas.json
    │   ├── upptack-champagnens-aromer.json
    │   └── champagne-till-maten.json
    └── images/
        ├── brut-reserve.webp
        ├── blanc-de-blancs.webp
        ├── rose-elegance.webp
        ├── reserve-verte.webp
        ├── cuvee-turquoise.webp
        └── artikel-....webp (tre artikelbilder)
```

**Viktigt vid ZIP:** `.agents` är en dold mapp. Den **måste vara med** i inlämningen. ZIP-filen som följer med projektet innehåller den.

## Lärandemål och kravchecklista

### Del 1 – HTML/CSS/JavaScript
- Semantisk `<header>`, `<nav>`, `<main>`, `<section>`, `<article>` och `<footer>`.
- En **h1** på startsidan, **h2** för sektioner och **h3** för produkt-/artikelkort.
- Navigeringslänkar som går till verkliga sektioner på sidan.
- Ankarlänk till formuläret (`#newsletter`).
- Bilder i `images/` med alt-texter.
- Tre artikellänkar i formatet `artikel.html?id=slug`.
- Externa stilmallar (`style.css`, `artikel.css`).
- `script.js` skapar ett nytt tackmeddelande med `document.createElement('p')`.
- Sidtitel och metabeskrivning; koden har minst två förklarande kommentarer per HTML/CSS/JS-fil.

### Del 2 – JSON-artiklar
- Gemensam mall `artikel.html` med `<!-- Elementet som artikeln ska placeras i -->` och `<article id="artikel">`.
- Artikelmallen läser `id` från URL och hämtar `artiklar/<slug>.json`.
- Testartikel och tre riktiga artiklar med bilder och alt-texter.

### Del 3 – AI-skill / artikelautomation
- Agentens instruktioner finns i `AGENTS.md`.
- Skillen finns i `.agents/skills/skapa-champagneartikel/SKILL.md`.
- `publicera_artikel.py` tar ett AI-stött JSON-utkast och en bild och sparar **nya** filer i `webbplats/artiklar/` respektive `webbplats/images/`.
- Tre artiklar har skapats genom publiceringsskriptet och är länkade från startsidan.
- Skriptet validerar JSON och slug, kräver ingen API-nyckel och vägrar skriva över befintliga filer.
- **Människan granskar** fakta, språk, SEO, källor, bilder och alt-text innan publicering.

## Vad gör pluginet, och hur kör man det?

Pluginet är en **AI-agent-skill** med ett skyddat publiceringsskript. AI hjälper till med ämnesval, research, artikelstruktur, språk och bildbeskrivning. Python-skriptet är den tekniska delen som kontrollerar utkastet, kopierar bilden till rätt mapp och sparar artikel-JSON utan att röra webbplatsens kod.

Skriv ett nytt utkast enligt JSON-exemplet i `.agents/skills/skapa-champagneartikel/SKILL.md` i en separat arbetsmapp **utanför** `webbplats`. Skapa eller välj en egen bild. Gå sedan igenom innehållet själv. Kör från projektmappen:

```bash
python .agents/skills/skapa-champagneartikel/scripts/publicera_artikel.py --utkast /sokvag/till/ny-artikel.json --slug mitt-artikelnamn --bild /sokvag/till/bild.webp --kontrollera
python .agents/skills/skapa-champagneartikel/scripts/publicera_artikel.py --utkast /sokvag/till/ny-artikel.json --slug mitt-artikelnamn --bild /sokvag/till/bild.webp
```

Om man utelämnar `--bild` genereras en egen lokal SVG-illustration. Den kommer också ligga i `images/` och refereras av JSON.

Skriptet skriver ut en länk av typen `artikel.html?id=mitt-artikelnamn`. **Efter mänsklig granskning** lägger du in en ny länk på startsidan manuellt. Detta är medvetet: uppgiften säger att AI inte får ändra befintliga webbplatsfiler under artikelgenereringen.

### Feedback och förbättringar över tid (VG)

Arbetsflödet är: **ämnesval → research → AI-utkast → mänsklig granskning → validering → publicering → uppföljning**. Kontrollera om användarna förstår artikeln, om rubriken motsvarar deras sökintention och om bilder/alt-text stämmer med innehållet. Notera återkoppling och justera skillens skrivinstruktioner inför *nästa* artikel. Gamla publicerade filer skrivs inte över automatiskt. Research- och faktakontroll sker innan en artikel blir publik.

## Publicera på GitHub (VG)

Från projektmappen i terminalen:

```bash
git init
git add .
git commit -m "Skolprojekt: Maison Eclat"
```

Skapa sedan ett **nytt repository** på GitHub och följ instruktionerna som GitHub visar för `git remote add origin ...` och `git push -u origin main`. Kontrollera att även `.agents/skills/skapa-champagneartikel/SKILL.md` syns i repot. Ge läraren läsrättighet om repot är privat, eller använd ett publikt repo om skolan tillåter det.

## Viktig kontroll före inlämning

Lärarens två GitHub Gist-exempel gick **inte att öppna** i projektmiljön vid produktionen. `test-artikel.json` och `artikel.js` är därför **fungerande egna implementationer**, inte ordagranna kopior av lärarens exempel. Jämför dessa två filer med lärarens Gist och anpassa vid behov. Detta måste verifieras för att säkerställa full kravuppfyllelse.

Projektet är ännu **inte publicerat i användarens GitHub-repository**. Även GitHub-delen måste göras innan man hävdar att samtliga VG-krav är klara.
