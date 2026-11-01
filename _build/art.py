# SVG illustrations for the Web Design CNY site
INK = "#1D1A33"

LOGO = '''<svg viewBox="0 0 48 48" aria-hidden="true"><rect x="2" y="2" width="44" height="44" rx="12" fill="#FFC23D" stroke="#1D1A33" stroke-width="2.5"/><path d="M6 17h36l-2 6H8z" fill="#EE5236" stroke="#1D1A33" stroke-width="2.2" stroke-linejoin="round"/><path d="M8 23c2 3 6 3 8 0 2 3 6 3 8 0 2 3 6 3 8 0 2 3 6 3 8 0" fill="#fff" stroke="#1D1A33" stroke-width="2.2" stroke-linejoin="round"/><rect x="11" y="28" width="26" height="13" rx="2.5" fill="#fff" stroke="#1D1A33" stroke-width="2.2"/><path d="M15 34.5h9M15 37.5h6" stroke="#0E8A7E" stroke-width="2.2" stroke-linecap="round"/><circle cx="31" cy="35" r="2.6" fill="#EE5236"/><path d="M14 11h20" stroke="#1D1A33" stroke-width="2.4" stroke-linecap="round"/></svg>'''

def awning(x, w, c1, c2, y=120, h=34):
    n = 6
    sw = w / n
    out = []
    for i in range(n):
        out.append(f'<rect x="{x+i*sw:.1f}" y="{y}" width="{sw:.1f}" height="{h}" fill="{c1 if i%2==0 else c2}"/>')
    # scallops
    for i in range(n):
        cx = x + i*sw + sw/2
        out.append(f'<path d="M{x+i*sw:.1f} {y+h} a{sw/2:.1f} {sw/2.4:.1f} 0 0 0 {sw:.1f} 0" fill="{c1 if i%2==0 else c2}" stroke="{INK}" stroke-width="2.5"/>')
    out.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="2.5"/>')
    return "".join(out)

def shop(x, wall, c1, c2, sign, signbg, signink, extra=""):
    w = 136
    s = []
    s.append(f'<rect x="{x}" y="60" width="{w}" height="300" fill="{wall}" stroke="{INK}" stroke-width="2.5"/>')
    # roof cornice
    s.append(f'<rect x="{x-6}" y="52" width="{w+12}" height="14" rx="3" fill="{INK}"/>')
    # upper windows
    for wx in (x+18, x+76):
        s.append(f'<rect x="{wx}" y="78" width="42" height="30" rx="4" fill="#DDF2FB" stroke="{INK}" stroke-width="2.5"/><path d="M{wx+21} 78v30" stroke="{INK}" stroke-width="2"/>')
    s.append(awning(x-4, w+8, c1, c2, y=168))
    # sign board
    s.append(f'<rect x="{x+14}" y="130" width="{w-28}" height="30" rx="6" fill="{signbg}" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<text x="{x+w/2}" y="151.5" text-anchor="middle" font-family="Bricolage Grotesque, Arial, sans-serif" font-weight="800" font-size="17" fill="{signink}" letter-spacing="1">{sign}</text>')
    # shop window + door
    s.append(f'<rect x="{x+12}" y="226" width="66" height="74" rx="5" fill="#DDF2FB" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<path d="M{x+20} 236l14 -0M{x+20} 244l24 0" stroke="#fff" stroke-width="4" stroke-linecap="round"/>')
    s.append(f'<rect x="{x+88}" y="226" width="36" height="134" rx="4" fill="{c1}" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<rect x="{x+94}" y="236" width="24" height="36" rx="3" fill="#DDF2FB" stroke="{INK}" stroke-width="2"/>')
    s.append(f'<circle cx="{x+117}" cy="300" r="3" fill="{INK}"/>')
    s.append(f'<rect x="{x+12}" y="306" width="66" height="54" fill="{wall}" stroke="{INK}" stroke-width="2.5"/>')
    s.append(extra)
    return "".join(s)

def street():
    parts = [f'<svg class="street" viewBox="0 0 600 420" role="img" aria-label="Illustration of a Utica main street with a deli, a barbershop, a salon and an auto shop">']
    parts.append('<circle cx="520" cy="48" r="34" fill="#FFC23D" stroke="#1D1A33" stroke-width="2.5"/>')
    parts.append(shop(14, "#FFD9CF", "#EE5236", "#FFFFFF", "DELI", "#FFFFFF", "#EE5236"))
    pole = '<rect x="268" y="228" width="12" height="54" rx="6" fill="#fff" stroke="#1D1A33" stroke-width="2.2"/><path d="M268 236l12 -6M268 248l12 -6M268 260l12 -6M268 272l12 -6" stroke="#EE5236" stroke-width="3.5"/>'
    parts.append(shop(158, "#9ED8F2", "#0E8A7E", "#FFFFFF", "CUTS", "#1D1A33", "#FFC23D", pole))
    parts.append(shop(302, "#C9EFD9", "#6D4AA8", "#FFFFFF", "SALON", "#FFFFFF", "#6D4AA8"))
    parts.append(shop(446, "#FFE8A8", "#FFC23D", "#1D1A33", "AUTO", "#EE5236", "#FFFFFF"))
    # sidewalk
    parts.append('<rect x="0" y="360" width="600" height="60" fill="#E8DCC6" stroke="#1D1A33" stroke-width="2.5"/>')
    parts.append('<path d="M0 384h600" stroke="#1D1A33" stroke-width="2" stroke-dasharray="2 28"/>')
    # planters
    for px in (126, 270, 414):
        parts.append(f'<rect x="{px-14}" y="336" width="28" height="24" rx="4" fill="#EE5236" stroke="#1D1A33" stroke-width="2.2"/><circle cx="{px-6}" cy="330" r="10" fill="#0E8A7E" stroke="#1D1A33" stroke-width="2.2"/><circle cx="{px+7}" cy="327" r="12" fill="#0E8A7E" stroke="#1D1A33" stroke-width="2.2"/>')
    parts.append('</svg>')
    return "".join(parts)

STREET = street()

# Floating "design" stickers for the hero
STICKERS = {
"browser": '''<svg width="190" height="132" viewBox="0 0 190 132"><rect x="2" y="2" width="186" height="128" rx="14" fill="#fff" stroke="#1D1A33" stroke-width="3"/><path d="M2 28h186" stroke="#1D1A33" stroke-width="3"/><circle cx="18" cy="15" r="5" fill="#EE5236"/><circle cx="34" cy="15" r="5" fill="#FFC23D"/><circle cx="50" cy="15" r="5" fill="#0E8A7E"/><rect x="16" y="42" width="96" height="14" rx="7" fill="#1D1A33"/><rect x="16" y="64" width="70" height="9" rx="4.5" fill="#C9C3DD"/><rect x="16" y="80" width="84" height="9" rx="4.5" fill="#C9C3DD"/><rect x="16" y="100" width="62" height="20" rx="10" fill="#EE5236"/><rect x="124" y="42" width="50" height="78" rx="8" fill="#9ED8F2" stroke="#1D1A33" stroke-width="2.5"/><circle cx="149" cy="70" r="11" fill="#FFC23D" stroke="#1D1A33" stroke-width="2.5"/><path d="M124 108l18-16 14 12 18-14v28h-50z" fill="#0E8A7E" stroke="#1D1A33" stroke-width="2.5" stroke-linejoin="round"/></svg>''',
"palette": '''<svg width="118" height="118" viewBox="0 0 118 118"><path d="M59 4C28 4 4 27 4 56c0 27 20 44 38 44 10 0 12-8 9-14-4-8 1-15 10-15h18c20 0 35-12 35-31C114 20 90 4 59 4z" fill="#FFFDF8" stroke="#1D1A33" stroke-width="3"/><circle cx="34" cy="40" r="10" fill="#EE5236" stroke="#1D1A33" stroke-width="2.5"/><circle cx="60" cy="26" r="10" fill="#FFC23D" stroke="#1D1A33" stroke-width="2.5"/><circle cx="86" cy="36" r="10" fill="#0E8A7E" stroke="#1D1A33" stroke-width="2.5"/><circle cx="30" cy="70" r="10" fill="#6D4AA8" stroke="#1D1A33" stroke-width="2.5"/></svg>''',
"phone": '''<svg width="92" height="160" viewBox="0 0 92 160"><rect x="3" y="3" width="86" height="154" rx="16" fill="#1D1A33"/><rect x="10" y="14" width="72" height="132" rx="9" fill="#fff"/><rect x="18" y="26" width="44" height="9" rx="4.5" fill="#1D1A33"/><rect x="18" y="42" width="56" height="34" rx="6" fill="#FFD9CF"/><rect x="18" y="84" width="40" height="6" rx="3" fill="#C9C3DD"/><rect x="18" y="95" width="50" height="6" rx="3" fill="#C9C3DD"/><rect x="18" y="114" width="56" height="20" rx="10" fill="#0E8A7E"/><path d="M38 124h16" stroke="#fff" stroke-width="3" stroke-linecap="round"/></svg>''',
"pen": '''<svg width="150" height="96" viewBox="0 0 150 96"><path d="M10 80C40 10 100 10 140 60" fill="none" stroke="#1D1A33" stroke-width="3.5" stroke-linecap="round"/><path d="M10 80L52 18M140 60L104 8" stroke="#6D4AA8" stroke-width="2" stroke-dasharray="4 4"/><rect x="2" y="72" width="16" height="16" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><rect x="132" y="52" width="16" height="16" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><circle cx="52" cy="18" r="7" fill="#6D4AA8" stroke="#1D1A33" stroke-width="2.5"/><circle cx="104" cy="8" r="6" fill="#6D4AA8" stroke="#1D1A33" stroke-width="2.5"/></svg>''',
"cursor": '''<svg width="56" height="64" viewBox="0 0 56 64"><path d="M6 4l42 26-18 4 10 20-9 5-10-20-15 12z" fill="#EE5236" stroke="#1D1A33" stroke-width="3" stroke-linejoin="round"/></svg>''',
"open": '''<svg width="120" height="104" viewBox="0 0 120 104"><path d="M60 4L22 44M60 4l38 40" stroke="#1D1A33" stroke-width="3" fill="none"/><circle cx="60" cy="6" r="5" fill="#FFC23D" stroke="#1D1A33" stroke-width="2.5"/><rect x="6" y="40" width="108" height="58" rx="12" fill="#0E8A7E" stroke="#1D1A33" stroke-width="3"/><text x="60" y="80" text-anchor="middle" font-family="Bricolage Grotesque, Arial, sans-serif" font-weight="800" font-size="30" fill="#fff" letter-spacing="2">OPEN</text></svg>''',
"star": '''<svg width="58" height="58" viewBox="0 0 58 58"><path d="M29 3l6 18 19 1-15 12 5 19-15-11-16 11 6-19L4 22l19-1z" fill="#FFC23D" stroke="#1D1A33" stroke-width="3" stroke-linejoin="round"/></svg>''',
"card": '''<svg width="140" height="86" viewBox="0 0 140 86"><rect x="3" y="3" width="134" height="80" rx="10" fill="#EE5236" stroke="#1D1A33" stroke-width="3"/><rect x="14" y="16" width="62" height="11" rx="5.5" fill="#fff"/><rect x="14" y="34" width="44" height="7" rx="3.5" fill="#FFD9CF"/><rect x="14" y="56" width="54" height="7" rx="3.5" fill="#FFD9CF"/><rect x="92" y="16" width="34" height="34" rx="4" fill="#fff" stroke="#1D1A33" stroke-width="2"/><path d="M98 22h8v8h-8zM112 22h8v8h-8zM98 36h8v8h-8zM114 38h4v4h-4z" fill="#1D1A33"/></svg>''',
}

def sticker(name, style):
    return f'<div class="sticker" style="{style}" aria-hidden="true">{STICKERS[name]}</div>'

HERO_STICKERS = "".join([
    sticker("palette", "top:-7%;left:-5%;--rot:-10deg;--dy:-160px;--spin:-40deg;--d:0s"),
    sticker("open",    "top:-9%;right:-4%;--rot:8deg;--dy:-200px;--spin:90deg;--d:.7s"),
    sticker("cursor",  "bottom:-4%;right:4%;--rot:-12deg;--dy:-240px;--spin:-30deg;--d:1.3s"),
])

# Service card art
SVC_WEB = '''<svg viewBox="0 0 240 130" width="100%" height="100%" aria-hidden="true"><rect width="240" height="130" fill="#DDF2FB"/><rect x="34" y="18" width="150" height="100" rx="10" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><path d="M34 36h150" stroke="#1D1A33" stroke-width="2.5"/><circle cx="46" cy="27" r="3.5" fill="#EE5236"/><circle cx="57" cy="27" r="3.5" fill="#FFC23D"/><circle cx="68" cy="27" r="3.5" fill="#0E8A7E"/><rect x="46" y="48" width="70" height="10" rx="5" fill="#1D1A33"/><rect x="46" y="64" width="54" height="6" rx="3" fill="#C9C3DD"/><rect x="46" y="94" width="44" height="14" rx="7" fill="#EE5236"/><rect x="126" y="48" width="46" height="58" rx="6" fill="#FFC23D" stroke="#1D1A33" stroke-width="2"/><rect x="168" y="50" width="40" height="72" rx="9" fill="#1D1A33"/><rect x="173" y="58" width="30" height="56" rx="4" fill="#fff"/><rect x="177" y="98" width="22" height="9" rx="4.5" fill="#0E8A7E"/></svg>'''
SVC_PRINT = '''<svg viewBox="0 0 240 130" width="100%" height="100%" aria-hidden="true"><rect width="240" height="130" fill="#FFE8A8"/><g transform="rotate(-8 80 70)"><rect x="40" y="16" width="80" height="104" rx="6" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><rect x="50" y="26" width="60" height="34" rx="4" fill="#EE5236"/><rect x="50" y="68" width="48" height="7" rx="3.5" fill="#1D1A33"/><rect x="50" y="80" width="56" height="5" rx="2.5" fill="#C9C3DD"/><path d="M50 106h60" stroke="#1D1A33" stroke-width="2" stroke-dasharray="3 5"/></g><g transform="rotate(6 170 80)"><rect x="128" y="52" width="88" height="54" rx="6" fill="#0E8A7E" stroke="#1D1A33" stroke-width="2.5"/><rect x="138" y="62" width="40" height="8" rx="4" fill="#fff"/><rect x="138" y="76" width="30" height="5" rx="2.5" fill="#C9EFD9"/><rect x="190" y="62" width="18" height="18" rx="2" fill="#fff"/></g></svg>'''
SVC_GOOGLE = '''<svg viewBox="0 0 240 130" width="100%" height="100%" aria-hidden="true"><rect width="240" height="130" fill="#C9EFD9"/><path d="M0 92h240M70 0v130M170 0v130" stroke="#fff" stroke-width="10"/><path d="M0 40 L240 70" stroke="#fff" stroke-width="7"/><path d="M120 16c-17 0-30 13-30 29 0 22 30 52 30 52s30-30 30-52c0-16-13-29-30-29z" fill="#EE5236" stroke="#1D1A33" stroke-width="2.5"/><circle cx="120" cy="45" r="11" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><rect x="150" y="80" width="78" height="34" rx="17" fill="#fff" stroke="#1D1A33" stroke-width="2.5"/><path d="M164 97l6 6 12-12" stroke="#0E8A7E" stroke-width="3.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/><rect x="188" y="92" width="30" height="9" rx="4.5" fill="#1D1A33"/></svg>'''

# Crew placeholder: a cartoon guy (no face details) walking two dogs. To be replaced once David sends dog photos.
CREW = ('<svg viewBox="0 0 600 470" role="img" aria-label="Illustration of a West Utica street with paw prints along the sidewalk"><rect width="600" height="470" fill="#DDF2FB"/><g transform="translate(0 10)">' + STREET.replace('<svg class="street" viewBox="0 0 600 420" role="img" aria-label="Illustration of a Utica main street with a deli, a barbershop, a salon and an auto shop">','').replace('</svg>','') + '</g><rect x="0" y="430" width="600" height="40" fill="#E8DCC6"/><g transform="translate(40 395) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(78 382) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(118 398) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(156 384) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(196 400) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(236 386) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(276 402) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(316 388) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(356 404) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(396 390) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(436 406) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(476 392) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g><g transform="translate(516 408) rotate(80)" fill="#1D1A33" opacity=".75"><ellipse cx="0" cy="6" rx="7" ry="6"/><circle cx="-7" cy="-4" r="3"/><circle cx="-2" cy="-8" r="3"/><circle cx="3" cy="-8" r="3"/><circle cx="8" cy="-4" r="3"/></g></svg>')

# Little town skyline for the footer top edge (filled with the footer ink, sitting on cream)
TOWN = '''<svg class="town" viewBox="0 0 1200 90" preserveAspectRatio="none" aria-hidden="true"><path fill="currentColor" d="M0 90V62h60V40h40v-14h50v14h30v22h40V30l30-20 30 20v32h50V44h70v18h30V20h16V8h12v12h16v42h60V36h90v26h40V48l30-18 30 18v14h60V28h80v34h40V44h50v18h60V36h40v-10h30v10h20v26h80V40h60v22h30v28z"/></svg>'''
