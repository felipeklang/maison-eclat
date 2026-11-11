// SKA INTE JUSTERAS MED AI

// Det här skriptet bygger upp artikelsidan (artikel.html) utifrån en JSON-fil.
// Vilken artikel som visas styrs av URL:en. Tex:
// artikel.html?id=laddning hämtar filen artiklar/laddning.json och skapar ett HTML-element per block i den.

// Läser in parametrarna i URL:en (allt efter "?") så att vi kan plocka ut dem
const params = new URLSearchParams(window.location.search);

// Hämtar värdet på parametern "id", t.ex. "laddning".
const id = params.get('id');

// Hämtar elementet i artikel.html som artikelns innehåll ska läggas in i
const container = document.querySelector('#artikel');

// Skapar ett HTML-element utifrån ett block i JSON-filen.
// Ett block är ett objekt med en "type" (t.ex. "h2", "p", "img" eller "ul") och det innehåll som hör till den typen.
function createBlock(block) {
    // Variabel som ska hålla det element vi skapar
    let el;

    // if-sats: OM block-typen är "img" går vi in i första delen i if-satsen.
    // Om block-typen istället är "ul" eller "ol" går vi in i andra delen i if-satsen.
    // Om inget av ovanstående stämmer hamnar vi i "else"-delen av if-satsen.
    if (block.type === 'img') {
        // Bild: skapar ett <img> och sätter bildens sökväg och alt-text.
        // Saknas alt-text i JSON-filen används en tom sträng.
        el = document.createElement('img');
        el.src = block.src;
        el.alt = block.alt || '';
    } else if (block.type === 'ul' || block.type === 'ol') {
        // Lista: skapar en <ul> (punktlista) eller <ol> (numrerad lista)
        el = document.createElement(block.type);

        // Går igenom varje punkt i "items" och lägger till den som ett <li> i listan
        block.items.forEach(item => {
            const li = document.createElement('li');
            li.textContent = item;
            el.appendChild(li);
        });
    } else {
        // Allt annat (h1, h2, h3, p osv.): skapar ett element av den typen och sätter dess text.
        el = document.createElement(block.type);
        el.textContent = block.text;
    }

    // Skickar tillbaka det färdiga elementet så att det kan läggas in på sidan
    return el;
}


// Hämtar JSON-filen för artikeln. Backticks (`) gör att ${id}
// byts ut mot värdet i variabeln, t.ex. artiklar/laddning.json
fetch(`artiklar/${id}.json`)
    .then(res => {
        // res.ok är false om filen inte finns (t.ex. fel 404).
        // Då kastas ett fel så att vi hoppar direkt till .catch() nedan.
        if (!res.ok) throw new Error('Artikeln finns inte');

        // Omvandlar svaret från text till ett JavaScript-objekt
        return res.json();
    })
    .then(artikel => {
        // Sätter sidans titel (det som syns i webbläsarfliken)
        document.title = artikel.title;

        // Går igenom alla block i "content" i tur och ordning,
        // skapar ett element för varje block och lägger in det i artikeln
        artikel.content.forEach(block => {
            container.appendChild(createBlock(block));
        });
    })
    // Körs om något gick fel: filen finns inte, JSON-filen är felskriven
    // eller sidan är öppnad utan lokal server
    .catch(error => console.log(error.message));