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
ALLOWED_TYPES = {'heading', 'subheading', 'paragraph', 'quote', 'list', 'image'}
ALLOWED_IMAGES = {'.png', '.jpg', '.jpeg', '.webp', '.svg'}


def validate(data, slug):
    if not isinstance(data, dict):
        raise ValueError('Utkastet ska vara ett JSON-objekt.')
    if data.get('slug') not in (None, slug):
        raise ValueError('Utkastets slug matchar inte det valda filnamnet.')
    for field, minimum in [('title', 12), ('description', 40), ('category', 3)]:
        if not isinstance(data.get(field), str) or len(data[field].strip()) < minimum:
            raise ValueError(f'{field} ska vara minst {minimum} tecken.')
    if not isinstance(data.get('content'), list) or len(data['content']) < 6:
        raise ValueError('content ska innehålla minst sex block.')
    for n, block in enumerate(data['content'], start=1):
        if not isinstance(block, dict) or block.get('type') not in ALLOWED_TYPES:
            raise ValueError(f'Felaktig blocktyp i innehållsblock {n}.')
        if block['type'] == 'list':
            if not isinstance(block.get('items'), list) or len(block['items']) < 2:
                raise ValueError(f'Listan i block {n} måste ha minst två punkter.')
        elif block['type'] != 'image' and not isinstance(block.get('text'), str):
            raise ValueError(f'Block {n} saknar text.')
    if not isinstance(data.get('sources', []), list):
        raise ValueError('sources ska vara en lista.')


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
        validate(data, args.slug)
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
        data['slug'] = args.slug
        data['image'] = {
            'src': f'images/{image_dest.name}',
            'alt': data.get('image', {}).get('alt') or f'Bild till artikeln {data["title"]}'
        }
        if args.kontrollera:
            print(f'OK att publicera: {args.slug}; inga filer ändrades.')
            return
        ARTICLES.mkdir(parents=True, exist_ok=True)
        IMAGES.mkdir(parents=True, exist_ok=True)
        if image_source:
            shutil.copyfile(image_source, image_dest)
        else:
            image_dest.write_text(make_svg(data['title']), encoding='utf-8')
        try:
            with json_dest.open('x', encoding='utf-8') as output:
                json.dump(data, output, ensure_ascii=False, indent=2)
                output.write('\n')
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
