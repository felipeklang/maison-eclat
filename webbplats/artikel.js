// Denna artikelmall används av alla JSON-artiklar: artikel.html?id=artikelns-slug.
// OBS: lärarens externa Gist-exempel behöver fortfarande jämföras med detta format.
const container = document.querySelector('#artikel');
const params = new URLSearchParams(window.location.search);
const slug = params.get('id');

// Mobilmenyn i artikelmallen fungerar på samma sätt som menyn på startsidan.
const menuToggle = document.querySelector('#menuToggle');
const menu = document.querySelector('#mainNav');
menuToggle?.addEventListener('click', () => {
  const open = menu.classList.toggle('open');
  menuToggle.setAttribute('aria-expanded', String(open));
  menuToggle.setAttribute('aria-label', open ? 'Stäng menyn' : 'Öppna menyn');
});
menu?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
  menu.classList.remove('open');
  menuToggle.setAttribute('aria-expanded', 'false');
}));

// Säker DOM-byggare: textContent ser till att JSON-text inte tolkas som körbar HTML.
function node(tag, className, text) {
  const element = document.createElement(tag);
  if (className) element.className = className;
  if (text !== undefined) element.textContent = String(text);
  return element;
}
function safeImage(image) {
  if (!image || typeof image.src !== 'string' || !/^images\/[a-z0-9-]+\.(?:webp|png|jpg|jpeg|svg)$/i.test(image.src)) return null;
  const img = node('img');
  img.src = image.src;
  img.alt = image.alt || 'Illustration till artikel';
  img.loading = 'lazy';
  return img;
}
function renderBlock(block, parent) {
  if (!block || typeof block !== 'object') return;
  const type = block.type;
  if (type === 'heading') parent.append(node('h2', '', block.text || ''));
  else if (type === 'subheading') parent.append(node('h3', '', block.text || ''));
  else if (type === 'paragraph') parent.append(node('p', '', block.text || ''));
  else if (type === 'quote') parent.append(node('blockquote', '', block.text || ''));
  else if (type === 'list' && Array.isArray(block.items)) {
    const list = node(block.ordered ? 'ol' : 'ul');
    block.items.forEach(item => list.append(node('li', '', item)));
    parent.append(list);
  } else if (type === 'image') {
    const image = safeImage({ src: block.src, alt: block.alt });
    if (!image) return;
    const figure = node('figure');
    figure.append(image);
    if (block.caption) figure.append(node('figcaption', '', block.caption));
    parent.append(figure);
  }
}
function showArticle(data) {
  if (!data || typeof data.title !== 'string' || !Array.isArray(data.content)) throw new Error('Ogiltig artikeldata');
  const fragment = document.createDocumentFragment();
  const header = node('header', 'article-head');
  header.append(node('p', 'article-category', data.category || 'MAISON ÉCLAT JOURNAL'));
  header.append(node('h1', '', data.title));
  if (data.description) header.append(node('p', 'article-deck', data.description));
  header.append(node('p', 'article-byline', `${data.author || 'Maison Éclat'} · ${data.date || '2026'}`));
  fragment.append(header);
  const cover = safeImage(data.image);
  if (cover) {
    const figure = node('figure', 'article-figure');
    figure.append(cover);
    if (data.image.caption) figure.append(node('figcaption', '', data.image.caption));
    fragment.append(figure);
  }
  const body = node('div', 'article-body');
  data.content.forEach(block => renderBlock(block, body));
  if (Array.isArray(data.sources) && data.sources.length) {
    const sources = node('div', 'article-sources');
    sources.append(node('strong', '', 'Källor och vidare läsning'));
    const list = node('ul');
    data.sources.forEach(item => {
      const entry = node('li');
      if (typeof item === 'string') entry.textContent = item;
      else if (item && /^https:\/\//.test(item.url || '')) {
        const a = node('a', '', item.name || item.url);
        a.href = item.url;
        a.rel = 'noopener noreferrer';
        a.target = '_blank';
        entry.append(a);
      }
      list.append(entry);
    });
    sources.append(list);
    body.append(sources);
  }
  fragment.append(body);
  container.replaceChildren(fragment);
  document.title = `${data.title} | Maison Éclat`;
  const desc = document.querySelector('meta[name="description"]');
  if (desc && data.description) desc.content = data.description.slice(0, 160);
}
function showError(message) {
  const error = node('div', 'article-error');
  error.append(node('h1', '', 'Artikeln kunde inte visas'), node('p', '', message));
  container.replaceChildren(error);
}
// Begränsa id till säkra filnamn utan å, ä eller ö. Inga API-nycklar behövs.
async function loadArticle() {
  if (!slug || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(slug)) return showError('Länken saknar ett giltigt artikel-id.');
  try {
    const response = await fetch(`artiklar/${slug}.json`);
    if (!response.ok) throw new Error('Hittar inte filen');
    const data = await response.json();
    showArticle(data);
  } catch (error) {
    showError('Starta webbplatsen via Live Server i VS Code och kontrollera att artikelns JSON-fil finns i artiklar-mappen.');
  }
}
loadArticle();
