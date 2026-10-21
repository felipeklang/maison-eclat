// Huvudnavigation: tillgänglig mobilmeny som också fungerar med tangentbord.
const menuToggle = document.querySelector('#menuToggle');
const mainNav = document.querySelector('#mainNav');
if (menuToggle && mainNav) {
  menuToggle.addEventListener('click', () => {
    const isOpen = mainNav.classList.toggle('open');
    menuToggle.setAttribute('aria-expanded', String(isOpen));
    menuToggle.setAttribute('aria-label', isOpen ? 'Stäng menyn' : 'Öppna menyn');
  });
  mainNav.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    mainNav.classList.remove('open');
    menuToggle.setAttribute('aria-expanded', 'false');
    menuToggle.setAttribute('aria-label', 'Öppna menyn');
  }));
}

// Produktväljaren byter till fem riktiga bildfiler som finns i images-mappen.
const variants = {
  brut: { image: 'images/brut-reserve.webp', name: 'BRUT RÉSERVE', alt: 'Maison Éclat Brut Réserve med gyllengul etikett' },
  blanc: { image: 'images/blanc-de-blancs.webp', name: 'BLANC DE BLANCS', alt: 'Maison Éclat Blanc de Blancs med vit etikett' },
  rose: { image: 'images/rose-elegance.webp', name: 'ROSÉ ÉLÉGANCE', alt: 'Maison Éclat Rosé Élégance med rosa etikett' },
  verte: { image: 'images/reserve-verte.webp', name: 'RÉSERVE VERTE', alt: 'Maison Éclat Réserve Verte med grön etikett' },
  turquoise: { image: 'images/cuvee-turquoise.webp', name: 'CUVÉE TURQUOISE', alt: 'Maison Éclat Cuvée Turquoise med turkos etikett' }
};
const heroBottle = document.querySelector('#heroBottle');
const heroVariantName = document.querySelector('#heroVariantName');
const variantCount = document.querySelector('.hero-note-number');
const selectors = Array.from(document.querySelectorAll('[data-bottle]'));
let currentVariant = 'brut';
function showVariant(key) {
  if (!variants[key] || !heroBottle || key === currentVariant) return;
  const chosen = variants[key];
  // Preladda bilden för att undvika att den gamla bilden försvinner vid långsam uppkoppling.
  const preloaded = new Image();
  preloaded.onload = () => {
    heroBottle.classList.add('changing');
    heroBottle.src = chosen.image;
    heroBottle.alt = chosen.alt;
    heroVariantName.textContent = chosen.name;
    variantCount.textContent = `${String(Object.keys(variants).indexOf(key) + 1).padStart(2, '0')} / 05`;
    selectors.forEach(button => {
      const selected = button.dataset.bottle === key;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-pressed', String(selected));
    });
    currentVariant = key;
    requestAnimationFrame(() => heroBottle.classList.remove('changing'));
  };
  preloaded.src = chosen.image;
}
selectors.forEach(button => button.addEventListener('click', () => showVariant(button.dataset.bottle)));
// Knapparna vid produktkorten väljer respektive flaska och hoppar upp till presentationen.
document.querySelectorAll('[data-preview]').forEach(button => button.addEventListener('click', () => {
  showVariant(button.dataset.preview);
  document.querySelector('.hero').scrollIntoView({ behavior: 'smooth' });
}));

// Formulärkravet: skapa ett NYTT HTML-element via JavaScript när användaren skickar formuläret.
const newsletterForm = document.querySelector('#newsletterForm');
newsletterForm?.addEventListener('submit', event => {
  event.preventDefault();
  const feedback = document.querySelector('#formFeedback');
  if (!feedback) return;
  feedback.replaceChildren();
  const message = document.createElement('p');
  message.textContent = 'Merci! ✨ Tack för ditt intresse. Detta är en demo – ingen adress har sparats eller skickats.';
  feedback.appendChild(message);
  newsletterForm.reset();
});
