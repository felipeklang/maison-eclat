# AGENTS.md – Maison Éclat

Detta är **bruksanvisningen för AI-agenten**, inte en fil som visas på webbplatsen.

## Projektets mappar
- `webbplats/`: själva webbplatsen; `index.html`, `style.css`, `script.js`, `artikel.html`, `artikel.css` och `artikel.js`.
- `webbplats/artiklar/`: JSON-filer där filnamnet är artikelns slug.
- `webbplats/images/`: lokala flaskbilder och artikelbilder.
- `.agents/skills/skapa-champagneartikel/SKILL.md`: **AI-skillen** för artikelproduktion.
- `.agents/skills/skapa-champagneartikel/scripts/publicera_artikel.py`: validator + säker publicering.
- `README.md`: mänskliga instruktioner och uppföljning.

## Ordning för nya artiklar
1. Läs detta dokument.
2. Läs `.agents/skills/skapa-champagneartikel/SKILL.md`.
3. Utför research, källgranskning och skriv ett nytt artikelutkast i JSON utanför `webbplats`.
4. Ta fram eller välj en bild och skriv en relevant alt-text.
5. Be människan granska och godkänna både fakta, innehåll, SEO och bild.
6. Validera med publiceringsskriptets `--kontrollera`.
7. Publicera som ny JSON och en ny bild med publiceringsskriptet.
8. Testa artikelmallen i Live Server och be om återkoppling.
9. Föreslå endast att människan **manuellt** lägger in länken `artikel.html?id=slug` på startsidan.

## Regler för alla artiklar
- Varumärket är **fiktivt** – hitta inte på autentiska företagsfakta, priser eller medaljer.
- Välj ett konkret ämne om champagne och skriv huvudsakligen på svenska.
- Ge läsaren nytta: praktiska exempel, korrekt rubrikhierarki (blocktyperna `h1`, `h2`, `h3`).
- Följ `webbplats/artiklar/test-artikel.json`: JSON har `title` och `content`, med rubriker, stycken och listor som egna block.
- Lägg bilden i ett `img`-block med `src` och beskrivande `alt`. Publiceringsskriptet sätter en lokal bildväg under `images/`.
- Slug får endast innehålla gemener a–z, siffror och bindestreck; t.ex. `champagne-till-maten`.
- Kontrollera sakpåståenden och ange källor där sådana behövs. Följ användarens feedback nästa gång.
- **AI får aldrig ändra befintliga filer i `webbplats`.** Skriv bara nya artikelfiler och bilder via det skyddade skriptet.
- Publicera aldrig lösenord eller API-nycklar.
