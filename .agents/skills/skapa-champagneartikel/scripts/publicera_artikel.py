#!/usr/bin/env python3
"""Validerar ett AI-artikelutkast och publicerar som JSON + bild; skriver ALDRIG över filer."""
import argparse
import json
import re
import shutil
import sys
from html import escape
from pathlib import Path

PROJECT = Path(__file__).resolve().parents[4]
SITE = PROJECT / 'webbplats'
ARTICLES = SITE / 'artiklar'
IMAGES = SITE / 'images'
SLUG = re.compile(r'^[a-z0-9]+(?:-[a-z0-9]+)*$')
TEXT_TYPES = {'h1', 'h2', 'h3', 'p'}
ALLOWED_IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.svg'}


def has_text(value):
    return isinstance(value, str) and bool(value.strip())


def validate(data):
    if not isinstance(data, dict) or not has_text(data.get('title')):
        raise ValueError('Utkastet ska ha en titel.')
    blocks = data.get('content')
    if not isinstance(blocks, list) or not blocks or not all(isinstance(b, dict) for b in blocks):
        raise ValueError('content ska vara en lista med innehållsblock.')
    if blocks[0].get('type') != 'h1' or sum(b.get('type') == 'h1' for b in blocks) != 1:
        raise ValueError('Artikeln ska börja med en enda h1.')
    images = []
    for number, block in enumerate(blocks, start=1):
        kind = block.get('type')
        if kind == 'img':
            if not has_text(block.get('alt')):
                raise ValueError(f'Bildblock {number} saknar alt-text.')
            images.append(block)
        elif kind in ('ul', 'ol'):
            items = block.get('items')
            if not isinstance(items, list) or not items or not all(has_text(item) for item in items):
                raise ValueError(f'Listblock {number} saknar giltiga punkter.')
        elif not isinstance(kind, str) or kind not in TEXT_TYPES or not has_text(block.get('text')):
            raise ValueError(f'Ogiltigt textblock {number}.')
    if len(images) != 1:
        raise ValueError('Publiceringsskriptet hanterar en bild per artikel.')
    return images[0]


def make_svg(title):
    """Reservillustration när ingen egen/fotograferad bild anges."""
    name = escape(title[:55])
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" role="img" aria-label="Illustration av champagneglas">
<defs><linearGradient id="bg" x2="1" y2="1"><stop stop-color="#f6e8d5"/><stop offset="1" stop-color="#e2bc84"/></linearGradient></defs>
<rect width="1200" height="800" fill="url(#bg)"/><circle cx="865" cy="370" r="275" fill="#fdf7e9" opacity=".4"/>
<g fill="none" stroke="#fff9ec" stroke-width="11"><path d="M512 140 H690 Q682 375 603 400 Q520 375 512 140 Z"/><path d="M603 400 V650 M520 660 Q600 630 690 660"/></g>
<path d="M531 268 H672 Q652 370 603 382 Q554 371 531 268" fill="#d79a42" opacity=".8"/>
<g fill="#fff9f0"><circle cx="575" cy="320" r="5"/><circle cx="625" cy="291" r="5"/><circle cx="600" cy="250" r="4"/></g>
<text x="64" y="90" font-family="Georgia" font-size="22" letter-spacing="4" fill="#6f4a22">MAISON ÉCLAT / JOURNAL</text>
<text x="64" y="745" font-family="Georgia" font-size="31" fill="#6f4a22">{name}</text></svg>'''


def main():
    parser = argparse.ArgumentParser(description='Publicera granskad artikel + bild i rätt mappar.')
    parser.add_argument('--utkast', required=True, help='JSON-utkast skapat med hjälp av AI.')
    parser.add_argument('--slug', required=True, help='Filnamn i små bokstäver utan åäö, använd bindestreck.')
    parser.add_argument('--bild', help='Valfri lokalt framtagen PNG/JPG/WEBP/SVG som ska kopieras till webbplats/images.')
    parser.add_argument('--kontrollera', action='store_true', help='Kontrollera utan att skriva filer.')
    args = parser.parse_args()
    try:
        if not SLUG.fullmatch(args.slug):
            raise ValueError('slug får bara innehålla a-z, siffror och bindestreck.')
        draft = Path(args.utkast).resolve()
        data = json.loads(draft.read_text(encoding='utf-8'))
        image_block = validate(data)
        if args.bild:
            image_source = Path(args.bild).resolve()
            if not image_source.is_file() or image_source.suffix.lower() not in ALLOWED_IMAGES:
                raise ValueError('Bilden måste vara en lokal PNG/JPG/WEBP/SVG-fil.')
            suffix = image_source.suffix.lower()
        else:
            image_source = None
            suffix = '.svg'
        json_dest = ARTICLES / f'{args.slug}.json'
        image_dest = IMAGES / f'artikel-{args.slug}{suffix}'
        # Skriptet får endast skapa NYA JSON- och bildfiler, aldrig skriva över HTML/CSS/JS.
        for destination in (json_dest, image_dest):
            if destination.exists():
                raise FileExistsError(f'Filen finns redan och skyddas mot överskrivning: {destination.name}')
        image_block['src'] = f'images/{image_dest.name}'
        if args.kontrollera:
            print(f'OK att publicera: {args.slug}; inga filer ändrades.')
            return
        ARTICLES.mkdir(parents=True, exist_ok=True)
        IMAGES.mkdir(parents=True, exist_ok=True)
        with image_dest.open('xb') as output:
            try:
                if image_source:
                    with image_source.open('rb') as source:
                        shutil.copyfileobj(source, output)
                else:
                    output.write(make_svg(data['title']).encode('utf-8'))
            except Exception:
                image_dest.unlink(missing_ok=True)
                raise
        try:
            serialized = json.dumps(data, ensure_ascii=False, indent=2) + '\n'
            with json_dest.open('x', encoding='utf-8') as output:
                try:
                    output.write(serialized)
                except Exception:
                    json_dest.unlink(missing_ok=True)
                    raise
        except Exception:
            image_dest.unlink(missing_ok=True)
            raise
        print('SKAPAD:', json_dest.relative_to(PROJECT))
        print('SPARAD BILD:', image_dest.relative_to(PROJECT))
        print('LÄNK:', f'artikel.html?id={args.slug}')
        print('Nästa steg: granska resultatet och länka manuellt från index.html (AI får inte ändra den filen).')
    except (ValueError, FileExistsError, OSError, json.JSONDecodeError) as exc:
        print('FEL:', exc, file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
