import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from art import *

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ES = {}

def T(key, en, es, tag=None, cls=None, attrs=""):
    """Translatable text. Returns element markup if tag given, else a span-less attribute pair helper."""
    if key in ES and ES[key] != es:
        raise SystemExit("dup key with different text: " + key)
    ES[key] = es
    if tag:
        c = f' class="{cls}"' if cls else ""
        return f'<{tag}{c} data-i18n="{key}"{attrs}>{en}</{tag}>'
    return en

def tk(key, en, es):
    """Only register, return attribute string for an element whose inner text is en."""
    ES[key] = es
    return f'data-i18n="{key}"'

def ph(key, en, es):
    ES[key] = es
    return f'placeholder="{en}" data-i18n-ph="{key}"'

CHECK = '<svg width="18" height="18" viewBox="0 0 20 20" aria-hidden="true"><path d="M4 10.5l4 4 8-9" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
ARROW = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'
GLOBE = '<svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2.2"/><path d="M3 12h18M12 3c3 3.5 3 14.5 0 18M12 3c-3 3.5-3 14.5 0 18" fill="none" stroke="currentColor" stroke-width="2"/></svg>'
SQUIG = '<svg viewBox="0 0 200 20" preserveAspectRatio="none" aria-hidden="true"><path d="M2 14C30 2 50 18 80 10s50-8 70 0 40 4 48-2" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round"/></svg>'
MAIL = "mailto:david@webdesigncny.com?subject=Free%20sample%20for%20my%20business"

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Nunito:wght@400;600;700;800&family=Caveat:wght@700&display=swap">'

SCHEMA = {
  "@context": "https://schema.org", "@type": "ProfessionalService", "@id": "https://webdesigncny.com/#business",
  "name": "Web Design CNY", "url": "https://webdesigncny.com/", "email": "david@webdesigncny.com",
  "image": "https://webdesigncny.com/og-image.png", "logo": "https://webdesigncny.com/apple-touch-icon.png",
  "description": "Friendly, affordable websites and graphic design for small shops and side hustles in Utica and Central New York. Free sample first, flat prices, no monthly fee.",
  "priceRange": "$100-$300",
  "address": {"@type": "PostalAddress", "addressLocality": "Utica", "addressRegion": "NY", "addressCountry": "US"},
  "areaServed": [{"@type": "City", "name": n} for n in ["Utica, NY","Rome, NY","New Hartford, NY","Whitesboro, NY","Yorkville, NY","New York Mills, NY"]] +
                [{"@type": "AdministrativeArea", "name": "Oneida County, NY"}, {"@type": "AdministrativeArea", "name": "Central New York"}],
  "knowsLanguage": ["en", "es"],
  "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Websites and small business design", "itemListElement": [
    {"@type": "Offer", "name": "Small business website", "price": "200", "priceCurrency": "USD"},
    {"@type": "Offer", "name": "Hustler package: one-page site, Google profile, business card and flyer design", "price": "150", "priceCurrency": "USD"},
    {"@type": "Offer", "name": "Entrepreneur package: website, Google listing cleanup, review QR card, flyer and business card design", "price": "300", "priceCurrency": "USD"},
    {"@type": "Offer", "name": "Flyer design", "price": "30", "priceCurrency": "USD"},
    {"@type": "Offer", "name": "Business card design", "price": "25", "priceCurrency": "USD"}]}
}

def head(page, title, desc, extra=""):
    url = "https://webdesigncny.com/" + ("" if page == "index" else page + ".html")
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Web Design CNY">
<meta property="og:url" content="{url}">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://webdesigncny.com/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FFC23D">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
{FONTS}
<link rel="stylesheet" href="assets/style.css">
<script>document.documentElement.classList.add("js")</script>
{extra}
</head>
<body>
<a class="skip" href="#main" {tk("c.skip","Skip to content","Saltar al contenido")}>Skip to content</a>
'''

def header(page):
    def nav(p, key, en, es):
        cur = ' aria-current="page"' if p == page else ""
        return f'<a class="txt" href="{"./" if p=="index" else p+".html"}"{cur} {tk(key,en,es)}>{en}</a>'
    return f'''<header class="top">
  <div class="wrap">
    <a class="logo" href="./" aria-label="Web Design CNY, home">{LOGO}<span class="w"><b>Web Design CNY</b><small {tk("c.tag","your neighborhood web guy","tu vecino diseñador web")}>your neighborhood web guy</small></span></a>
    <nav class="nav" id="nav" aria-label="Main">
      {nav("index","n.home","Home","Inicio")}
      {nav("services","n.services","Services &amp; prices","Servicios y precios")}
      {nav("about","n.about","About","Quién soy")}
      {nav("contact","n.contact","Contact","Contacto")}
    </nav>
    <div class="lang" id="lang">
      <button class="lang-btn" type="button" aria-haspopup="true" aria-expanded="false" aria-label="Language / Idioma">{GLOBE}<span class="lname">English</span></button>
      <div class="lang-menu" role="menu"></div>
    </div>
    <a class="btn btn-red hdr-cta" href="contact.html" {tk("c.hdrcta","Free sample","Muestra gratis")}>Free sample</a>
    <button class="menu-btn" type="button" aria-controls="nav" aria-expanded="false" aria-label="Menu"><svg width="22" height="22" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" stroke="currentColor" stroke-width="2.6" stroke-linecap="round"/></svg></button>
  </div>
</header>
<main id="main">
'''

def bigcta():
    return f'''
  <section class="bigcta band-sun edge-top">
    <div class="wrap reveal">
      <span class="hand" style="color:var(--ink)" {tk("cta.hand","no strings attached","sin compromiso")}>no strings attached</span>
      <h2 {tk("cta.h","Let's get your shop online.","Pongamos tu negocio en internet.")}>Let's get your shop online.</h2>
      <p {tk("cta.p","Tell me your business name. I'll make a free sample homepage and send it to you, usually within a couple of days.","Dime el nombre de tu negocio. Te hago una página de muestra gratis y te la envío, normalmente en un par de días.")}>Tell me your business name. I'll make a free sample homepage and send it to you, usually within a couple of days.</p>
      <div class="cta" style="justify-content:center"><a class="btn btn-red" href="contact.html"><span {tk("c.cta","Get my free sample","Quiero mi muestra gratis")}>Get my free sample</span>{ARROW}</a><a class="btn" href="{MAIL}">david@webdesigncny.com</a></div>
    </div>
  </section>
'''

def footer():
    return f'''</main>

<footer>
  {TOWN}
  <div class="wrap">
    <div class="cols">
      <div>
        <a class="logo" href="./" aria-label="Web Design CNY, home">{LOGO}<span class="w"><b>Web Design CNY</b><small {tk("c.tag","your neighborhood web guy","tu vecino diseñador web")}>your neighborhood web guy</small></span></a>
        <p class="areas" {tk("f.areas","Websites and graphic design for small shops and side hustles in Utica, West Utica, East Utica, North Utica, New Hartford, Whitesboro, Yorkville, New York Mills, Rome and all of Oneida County.","Sitios web y diseño gráfico para pequeños negocios y emprendedores en Utica, West Utica, East Utica, North Utica, New Hartford, Whitesboro, Yorkville, New York Mills, Rome y todo el condado de Oneida.")}>Websites and graphic design for small shops and side hustles in Utica, West Utica, East Utica, North Utica, New Hartford, Whitesboro, Yorkville, New York Mills, Rome and all of Oneida County.</p>
      </div>
      <div>
        <h3 {tk("f.pages","Pages","Páginas")}>Pages</h3>
        <ul>
          <li><a href="./" {tk("n.home","Home","Inicio")}>Home</a></li>
          <li><a href="services.html" {tk("n.services","Services &amp; prices","Servicios y precios")}>Services &amp; prices</a></li>
          <li><a href="about.html" {tk("n.about","About","Quién soy")}>About</a></li>
          <li><a href="contact.html" {tk("n.contact","Contact","Contacto")}>Contact</a></li>
        </ul>
      </div>
      <div>
        <h3 {tk("f.say","Say hi","Saluda")}>Say hi</h3>
        <ul>
          <li><a href="{MAIL}">david@webdesigncny.com</a></li>
          <li {tk("f.based","Based in Utica, NY","Desde Utica, NY")}>Based in Utica, NY</li>
        </ul>
      </div>
    </div>
    <div class="legal"><span>© 2026 Web Design CNY</span><span {tk("f.made","Made in Utica, with help from two good dogs.","Hecho en Utica, con ayuda de dos buenos perros.")}>Made in Utica, with help from two good dogs.</span></div>
  </div>
</footer>

<div class="dock">
  <a class="btn btn-red" href="contact.html" {tk("c.cta","Get my free sample","Quiero mi muestra gratis")}>Get my free sample</a>
  <a class="btn btn-email" href="{MAIL}" aria-label="Email David" {tk("c.email","Email","Email")}>Email</a>
</div>

<script src="assets/i18n.js"></script>
<script src="assets/site.js"></script>
</body>
</html>
'''

def ticks(items):
    return "<ul class=\"ticks\">" + "".join(f'<li {tk(k,en,es)}>{en}</li>' for k,en,es in items) + "</ul>"

# ---------- shared blocks ----------
def plans_block(full=True):
    def plan(cls, tier_k, tier_en, tier_es, h_k, h_en, h_es, price, was, who_k, who_en, who_es, rows, save_k, save_en, save_es, btn_k, btn_en, btn_es, plan_val, ribbon=""):
        lis = "".join(f'<li><span><span {tk(k,en,es)}>{en}</span>{f"<small {tk(k+chr(46)+chr(110),n_en,n_es)}>{n_en}</small>" if n_en else ""}</span><span>{amt}</span></li>' for k,en,es,n_en,n_es,amt in rows)
        wasb = f'<s>${was}</s>' if was else ""
        return f'''<div class="plan {cls} reveal">{ribbon}
          <span class="tier" {tk(tier_k,tier_en,tier_es)}>{tier_en}</span>
          <h3 {tk(h_k,h_en,h_es)}>{h_en}</h3>
          <div class="price"><b>${price}</b>{wasb}</div>
          <p class="who" {tk(who_k,who_en,who_es)}>{who_en}</p>
          <ul>{lis}</ul>
          <span class="save" {tk(save_k,save_en,save_es)}>{save_en}</span>
          <a class="btn {"btn-red" if cls=="star" else ""}" href="contact.html?plan={plan_val}" {tk(btn_k,btn_en,btn_es)}>{btn_en}</a>
        </div>'''
    rib = f'<span class="ribbon" {tk("pl.rib","Best value for shops","Mejor valor para negocios")}>Best value for shops</span>'
    return f'''<div class="plans">
        {plan("", "pl.h.tier","Hustler package","Paquete Hustler", "pl.h.h","Starting a side hustle?","¿Empezando un negocio propio?", 150, 205,
              "pl.h.who","For braiders, nail techs, cleaners, handymen, home bakers and tutors who want to look official.","Para trenzadoras, manicuristas, limpiadoras, técnicos, reposteros caseros y tutores que quieren verse profesionales.",
              [("pl.h.1",'One-page "hire me" site','Sitio de una página "contrátame"',"Services, prices, photos, text or book button","Servicios, precios, fotos, botón para escribir o reservar","$100"),
               ("pl.h.2","Google profile setup","Perfil de Google","Your home address stays hidden","Tu dirección de casa queda oculta","$50"),
               ("pl.h.3","Business card design","Diseño de tarjeta de presentación","","","$25"),
               ("pl.h.4","Flyer design","Diseño de volante","","","$30")],
              "pl.h.save","You save $55","Ahorras $55","pl.h.btn","Choose Hustler","Elegir Hustler","hustler")}
        {plan("", "pl.w.tier","Website","Sitio web", "pl.w.h","Just the website","Solo el sitio web", 200, None,
              "pl.w.who","A full website for your shop, linked from your Google listing. Most shops start here.","Un sitio web completo para tu negocio, enlazado desde tu perfil de Google. La mayoría empieza aquí.",
              [("pl.w.1","Works great on phones","Se ve bien en celulares","","","✓"),
               ("pl.w.2","Hours, map &amp; call button","Horario, mapa y botón para llamar","","","✓"),
               ("pl.w.3","Menu, services or prices","Menú, servicios o precios","","","✓"),
               ("pl.w.4","Linked from your Google listing","Enlazado desde tu perfil de Google","","","✓"),
               ("pl.w.5","Hosting","Hospedaje","","","$0/mo")],
              "pl.w.save","Small fixes free for the first month","Cambios pequeños gratis el primer mes","pl.w.btn","Choose website","Elegir sitio web","website")}
        {plan("star", "pl.e.tier","Entrepreneur package","Paquete Emprendedor", "pl.e.h","Running a shop?","¿Tienes un negocio?", 300, 360,
              "pl.e.who","For delis, cafes, barbershops, auto shops and corner stores that want to be found, trusted and visited.","Para delis, cafés, barberías, talleres y tiendas de esquina que quieren que los encuentren, confíen en ellos y los visiten.",
              [("pl.e.1","Small business website","Sitio web para negocio","","","$200"),
               ("pl.e.2","Google listing cleanup","Arreglo del perfil de Google","","","$75"),
               ("pl.e.3","Review QR card design","Tarjeta QR para reseñas","Counter card that asks for Google reviews","Tarjeta de mostrador que pide reseñas en Google","$35"),
               ("pl.e.4","Flyer + business card design","Volante + tarjeta de presentación","","","$50")],
              "pl.e.save","You save $60","Ahorras $60","pl.e.btn","Choose Entrepreneur","Elegir Emprendedor","entrepreneur", rib)}
      </div>'''

def kinds_chips():
    chips = [("deli","Deli","Deli"),("barber","Barbershop","Barbería"),("auto","Auto shop","Taller"),("salon","Salon","Salón"),("hustle","Side hustle","Emprendimiento")]
    return "".join(f'<button class="chip" type="button" data-kind="{k}" aria-pressed="{"true" if i==0 else "false"}" {tk("k."+k,en,es)}>{en}</button>' for i,(k,en,es) in enumerate(chips))

PHONE = '''<div class="phone" id="phone" role="img" aria-label="Example small business website on a phone">
          <div class="tag" data-i18n="k.tag">Example</div>
          <div class="p-nav swap"><span data-f="name">Your Deli</span><i></i></div>
          <div class="p-hero swap">
            <strong data-f="head">Hot subs, pizza &amp; groceries</strong>
            <small data-f="sub">Your corner deli. Order ahead or stop by.</small>
            <div class="p-btn"><svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.57 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.57 3.57a1 1 0 01-.25 1z"/></svg><span data-f="btn">Call to order</span></div>
          </div>
          <div class="p-photo swap" data-f="photo">Your food photo</div>
          <div class="p-rows swap" data-f="rows"><b>Mon–Fri</b><span>8 AM – 10 PM</span><b>Sat</b><span>9 AM – 10 PM</span><b>Sun</b><span>9 AM – 8 PM</span></div>
        </div>'''
ES["k.tag"] = "Ejemplo"

HELLOS = ["Hello","Hola","Ciao","Zdravo","Cześć","Привіт","مرحبا","Xin chào","नमस्ते","မင်္ဂလာပါ","Bonjour","Jambo"]

# ---------- HOME ----------
def home():
    marquee = "".join(f'<span lang="und">{h}</span>' for h in HELLOS) * 2
    svc = lambda art, k, h_en, h_es, p_en, p_es, price_en, price_es, d: f'''<div class="svc reveal" style="--rd:{d}s">
          <div class="art">{art}</div>
          <h3 {tk(k+".h",h_en,h_es)}>{h_en}</h3>
          <p {tk(k+".p",p_en,p_es)}>{p_en}</p>
          <div class="from"><span {tk(k+".f",price_en,price_es)}>{price_en}</span><a href="services.html" {tk("home.svc.more","See prices","Ver precios")}>See prices</a></div>
        </div>'''
    return head("index", "Web Design CNY · Friendly websites for small businesses in Utica, NY",
                "Friendly, affordable websites and graphic design for small shops and side hustles in Utica and Central New York. Free sample first, flat prices, no monthly fee.",
                '<script type="application/ld+json">' + json.dumps(SCHEMA) + '</script>') + header("index") + f'''
  <section class="hero">
    <div class="wrap">
      <div class="hero-copy">
        <span class="hand-note" {tk("home.hand","Hey neighbor!","¡Hola, vecino!")}>Hey neighbor!</span>
        <h1 {tk("home.h1","Your shop deserves a <span class=\"accent\">real website.</span>","Tu negocio merece un <span class=\"accent\">sitio web de verdad.</span>")}>Your shop deserves a <span class="accent">real website.</span></h1>
        <p class="lede" {tk("home.lede","I'm David, from West Utica. I design bright, simple websites, flyers and cards for the delis, barbers, salons, auto shops and side hustles that make this town great. I'll make you a free sample first, so you see it before you spend a dollar.","Soy David, de West Utica. Diseño sitios web, volantes y tarjetas sencillos y llamativos para los delis, barberías, salones, talleres y emprendedores que hacen grande a esta ciudad. Primero te hago una muestra gratis, para que la veas antes de gastar un dólar.")}>I'm David, from West Utica. I design bright, simple websites, flyers and cards for the delis, barbers, salons, auto shops and side hustles that make this town great. I'll make you a free sample first, so you see it before you spend a dollar.</p>
        <div class="cta">
          <a class="btn btn-red" href="contact.html"><span {tk("c.cta","Get my free sample","Quiero mi muestra gratis")}>Get my free sample</span>{ARROW}</a>
          <a class="btn" href="services.html" {tk("home.seeprices","See prices","Ver precios")}>See prices</a>
        </div>
        <ul class="assure">
          <li><i></i><span {tk("as.1","Free sample","Muestra gratis")}>Free sample</span></li>
          <li><i></i><span {tk("as.2","No monthly fee","Sin pago mensual")}>No monthly fee</span></li>
          <li><i></i><span {tk("as.3","You own it","Es tuyo")}>You own it</span></li>
        </ul>
      </div>
      <div class="scene" id="scene">
        {HERO_STICKERS}
        {STREET}
      </div>
    </div>
  </section>

  <div class="marquee" aria-label="Hello in many of the languages spoken in Utica"><div class="track">{marquee}</div></div>

  <section>
    <div class="wrap">
      <div class="head reveal">
        <span class="kicker" {tk("home.what.k","What I do","Lo que hago")}>What I do</span>
        <h2 {tk("home.what.h","Web design <em>and</em> graphic design, made for small shops","Diseño web <em>y</em> diseño gráfico, hecho para pequeños negocios")}>Web design <em>and</em> graphic design, made for small shops</h2>
        <p {tk("home.what.p","Everything you need to look good, get found and get called, from one person you can actually reach.","Todo lo que necesitas para verte bien, que te encuentren y te llamen, de una sola persona a quien sí puedes contactar.")}>Everything you need to look good, get found and get called, from one person you can actually reach.</p>
      </div>
      <div class="svc-grid">
        {svc(SVC_WEB,"svc.web","Websites","Sitios web","A bright, simple site that works great on phones, with your hours, menu or services, photos and a call button.","Un sitio sencillo y llamativo que funciona muy bien en celulares, con tu horario, menú o servicios, fotos y un botón para llamar.","From $100","Desde $100",0)}
        {svc(SVC_PRINT,"svc.print","Flyers &amp; cards","Volantes y tarjetas","Flyers, business cards and review QR cards that match your site, sent as print-ready files.","Volantes, tarjetas de presentación y tarjetas QR para reseñas que combinan con tu sitio, listos para imprimir.","From $25","Desde $25",.12)}
        {svc(SVC_GOOGLE,"svc.google","Get found on Google","Que te encuentren en Google","Your Google listing set up or cleaned up: right hours, photos, categories and a website button.","Tu perfil de Google creado o arreglado: horario correcto, fotos, categorías y botón al sitio web.","From $50","Desde $50",.24)}
      </div>
    </div>
  </section>

  <section class="band-sky edge-top edge-bot">
    <div class="wrap demo-wrap">
      <div class="stack reveal">
        <span class="kicker" {tk("home.demo.k","Try it","Pruébalo")}>Try it</span>
        <h2 {tk("home.demo.h","What would <span class=\"hl\">your</span> site look like?","¿Cómo se vería <span class=\"hl\">tu</span> sitio?")}>What would <span class="hl">your</span> site look like?</h2>
        <p class="lede" {tk("home.demo.p","Tap a type of business. Your free sample uses your real name, hours, prices and photos.","Toca un tipo de negocio. Tu muestra gratis usa tu nombre, horario, precios y fotos reales.")}>Tap a type of business. Your free sample uses your real name, hours, prices and photos.</p>
        <div class="chips" role="group" aria-label="Business type">{kinds_chips()}</div>
      </div>
      <div class="demo reveal" style="--rd:.15s">{PHONE}</div>
    </div>
  </section>

  <section>
    <div class="wrap why-grid">
      <div class="stack reveal">
        <span class="kicker" {tk("why.k","Why it matters","Por qué importa")}>Why it matters</span>
        <h2 {tk("why.h","When someone searches \"near me,\" who do they pick?","Cuando alguien busca \"cerca de mí\", ¿a quién escoge?")}>When someone searches "near me," who do they pick?</h2>
        <p class="lede" {tk("why.p","New customers look you up on their phone before they walk in. If your listing has no website, they see less about you, and they often tap the shop next door instead.","Los clientes nuevos te buscan en el celular antes de llegar. Si tu perfil no tiene sitio web, ven menos de ti y muchas veces escogen el negocio de al lado.")}>New customers look you up on their phone before they walk in. If your listing has no website, they see less about you, and they often tap the shop next door instead.</p>
        {ticks([("why.t1","Your menu, prices and hours, right where people look","Tu menú, precios y horario, justo donde la gente busca"),("why.t2","A website button on your Google listing","Un botón de sitio web en tu perfil de Google"),("why.t3","One link for your flyers, cards, Facebook and Instagram","Un solo enlace para tus volantes, tarjetas, Facebook e Instagram")])}
      </div>
      <div class="serp reveal" style="--rd:.15s" role="img" aria-label="Illustration of two search results: one shop has a website, the other does not">
        <div class="q"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="11" cy="11" r="7" stroke="currentColor" stroke-width="2.4"/><path d="M20 20l-4-4" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg><span {tk("serp.q","barbershop near me","barbería cerca de mí")}>barbershop near me</span></div>
        <div class="res good"><span class="flag" {tk("serp.g","With a website","Con sitio web")}>With a website</span><div class="nm" {tk("serp.n1","Your Shop","Tu Negocio")}>Your Shop</div><div class="meta" {tk("serp.m1","Barbershop · Open until 7 PM · Prices on website","Barbería · Abierto hasta las 7 PM · Precios en el sitio")}>Barbershop · Open until 7 PM · Prices on website</div><div class="acts"><span class="web" {tk("serp.web","Website","Sitio web")}>Website</span><span {tk("serp.dir","Directions","Cómo llegar")}>Directions</span><span {tk("serp.call","Call","Llamar")}>Call</span></div></div>
        <div class="res bad"><span class="flag" {tk("serp.b","Without","Sin sitio")}>Without</span><div class="nm" {tk("serp.n2","The shop down the street","El negocio de la otra cuadra")}>The shop down the street</div><div class="meta" {tk("serp.m2","Barbershop · Hours may differ","Barbería · El horario puede variar")}>Barbershop · Hours may differ</div><div class="acts"><span class="none" {tk("serp.none","No website","Sin sitio web")}>No website</span><span {tk("serp.dir","Directions","Cómo llegar")}>Directions</span><span {tk("serp.call","Call","Llamar")}>Call</span></div></div>
        <div class="note" {tk("serp.note","Illustration. Not real businesses.","Ilustración. No son negocios reales.")}>Illustration. Not real businesses.</div>
      </div>
    </div>
  </section>

  <section class="band-ink">
    <div class="wrap">
      <div class="head reveal">
        <span class="kicker" {tk("how.k","How it works","Cómo funciona")}>How it works</span>
        <h2 {tk("how.h","From free sample to live in about a week","De la muestra gratis a estar en línea en una semana")}>From free sample to live in about a week</h2>
        <p {tk("how.p","You never pay for something you haven't seen.","Nunca pagas por algo que no has visto.")}>You never pay for something you haven't seen.</p>
      </div>
      <ol class="steps" style="color:var(--ink)">
        <li class="reveal"><h3 {tk("st.1h","I make a free sample","Te hago una muestra gratis")}>I make a free sample</h3><p {tk("st.1p","A homepage built from your Google listing, usually within a couple of days.","Una página de inicio hecha con tu perfil de Google, normalmente en un par de días.")}>A homepage built from your Google listing, usually within a couple of days.</p><span class="pay" {tk("st.1$","You pay: $0","Pagas: $0")}>You pay: $0</span></li>
        <li class="reveal" style="--rd:.1s"><h3 {tk("st.2h","You say yes","Dices que sí")}>You say yes</h3><p {tk("st.2p","Like it? Pay half to start, and send your menu or services, prices and a few phone photos.","¿Te gusta? Pagas la mitad para empezar y me mandas tu menú o servicios, precios y unas fotos del celular.")}>Like it? Pay half to start, and send your menu or services, prices and a few phone photos.</p><span class="pay" {tk("st.2$","You pay: half","Pagas: la mitad")}>You pay: half</span></li>
        <li class="reveal" style="--rd:.2s"><h3 {tk("st.3h","You approve it","Lo apruebas")}>You approve it</h3><p {tk("st.3p","I build the full site and show you. We change things until it looks right.","Hago el sitio completo y te lo muestro. Cambiamos lo que haga falta hasta que quede bien.")}>I build the full site and show you. We change things until it looks right.</p><span class="pay" {tk("st.3$","You pay: $0","Pagas: $0")}>You pay: $0</span></li>
        <li class="reveal" style="--rd:.3s"><h3 {tk("st.4h","It goes live","Sale en línea")}>It goes live</h3><p {tk("st.4p","It goes up on your own web address and gets linked from your Google listing.","Se publica en tu propia dirección web y se enlaza desde tu perfil de Google.")}>It goes up on your own web address and gets linked from your Google listing.</p><span class="pay" {tk("st.4$","You pay: the other half","Pagas: la otra mitad")}>You pay: the other half</span></li>
      </ol>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="head center reveal">
        <span class="kicker" {tk("pr.k","Simple prices","Precios sencillos")}>Simple prices</span>
        <h2 {tk("pr.h","Pick what fits. Pay once.","Escoge lo que te sirva. Pagas una vez.")}>Pick what fits. Pay once.</h2>
        <p {tk("pr.p","Half to start, half when you approve. No monthly fee.","La mitad para empezar, la mitad cuando lo apruebes. Sin pago mensual.")}>Half to start, half when you approve. No monthly fee.</p>
      </div>
      {plans_block()}
      <p class="plan-note" style="text-align:center;margin-inline:auto"><a href="services.html" {tk("pr.more","Build your own, add-ons and questions →","Arma tu propio paquete, extras y preguntas →")}>Build your own, add-ons and questions →</a></p>
    </div>
  </section>

  <section class="band-sky edge-top">
    <div class="wrap crew">
      <div class="crew-art reveal">{CREW}<span class="cap" {tk("crew.cap","West Utica HQ","Sede en West Utica")}>West Utica HQ</span></div>
      <div class="stack reveal" style="--rd:.15s">
        <span class="kicker" {tk("crew.k","Meet the crew","Conoce al equipo")}>Meet the crew</span>
        <h2 {tk("crew.h","A neighbor, not an agency","Un vecino, no una agencia")}>A neighbor, not an agency</h2>
        <p {tk("crew.p","I live in West Utica and walk these streets every day with my two dogs, the official Web Design CNY mascots. We pass a lot of great local businesses that people can't find online. I want to fix that, at a price a small shop can afford.","Vivo en West Utica y camino estas calles todos los días con mis dos perros, las mascotas oficiales de Web Design CNY. Pasamos por muchos negocios locales buenísimos que la gente no encuentra en internet. Quiero arreglar eso, a un precio que un negocio pequeño pueda pagar.")}>I live in West Utica and walk these streets every day with my two dogs, the official Web Design CNY mascots. We pass a lot of great local businesses that people can't find online. I want to fix that, at a price a small shop can afford.</p>
        <div class="cta"><a class="btn btn-teal" href="about.html"><span {tk("crew.btn","More about us","Más sobre nosotros")}>More about us</span>{ARROW}</a></div>
      </div>
    </div>
  </section>
''' + bigcta() + footer()

# ---------- SERVICES ----------
def services():
    opts = [("site",200,"b.site","Small business website","Sitio web para negocio","Full site for a shop, linked from Google","Sitio completo para un negocio, enlazado desde Google"),
            ("onepage",100,"b.one",'One-page "hire me" site','Sitio de una página "contrátame"',"For side hustles: services, prices, photos","Para emprendedores: servicios, precios, fotos"),
            ("gprofile",50,"b.gp","Google profile setup","Perfil de Google","New listing on Google Maps, home address hidden","Perfil nuevo en Google Maps, dirección de casa oculta"),
            ("gclean",75,"b.gc","Google listing cleanup","Arreglo del perfil de Google","Fix hours, photos, categories and website link","Arreglo de horario, fotos, categorías y enlace al sitio"),
            ("qr",35,"b.qr","Review QR card design","Tarjeta QR para reseñas","Counter card that asks happy customers for a review","Tarjeta de mostrador que pide reseñas a clientes contentos"),
            ("flyer",30,"b.fl","Flyer design","Diseño de volante","Print-ready file that matches your site","Archivo listo para imprimir que combina con tu sitio"),
            ("card",25,"b.cd","Business card design","Diseño de tarjeta de presentación","Print-ready file. Flyer + card together: $50","Archivo listo para imprimir. Volante + tarjeta juntos: $50")]
    optsh = "".join(f'<label class="opt"><input type="checkbox" value="{v}" data-price="{p}" data-k="{k}"><span><b {tk(k,en,es)}>{en}</b><small {tk(k+".s",s_en,s_es)}>{s_en}</small></span><span class="p">${p}</span></label>' for v,p,k,en,es,s_en,s_es in opts)
    inc = [("M6 2h12v20H6zM11 18h2","i.1","Made for phones","Hecho para celulares","Looks right on the phone in your customer's hand, and on computers too.","Se ve bien en el celular de tu cliente, y también en computadoras."),
           ("M22 16.9v3a2 2 0 01-2.2 2 19.8 19.8 0 01-8.6-3.1 19.5 19.5 0 01-6-6A19.8 19.8 0 012.1 4.2 2 2 0 014.1 2h3a2 2 0 012 1.7c.1 1 .4 1.9.7 2.8a2 2 0 01-.5 2.1L8 9.9a16 16 0 006 6l1.3-1.3a2 2 0 012.1-.4c.9.3 1.8.6 2.8.7a2 2 0 011.7 2z","i.2","Tap to call","Toca para llamar","A big button that calls or texts you, plus directions in one tap.","Un botón grande para llamarte o escribirte, y cómo llegar con un toque."),
           ("M12 3a9 9 0 100 18 9 9 0 000-18zM12 7v5l3 2","i.3","Hours &amp; map","Horario y mapa","Your hours, address and a map, so nobody shows up to a locked door.","Tu horario, dirección y mapa, para que nadie llegue a una puerta cerrada."),
           ("M4 6h16M4 12h16M4 18h10","i.4","Menu or services","Menú o servicios","Your menu, services and prices, with your own photos.","Tu menú, servicios y precios, con tus propias fotos."),
           ("M11 4a7 7 0 100 14 7 7 0 000-14zM20 20l-4-4","i.5","Ready for Google","Listo para Google","Set up so Google understands what you do and where.","Preparado para que Google entienda qué haces y dónde."),
           ("M13 2L4 14h7l-1 8 9-12h-7z","i.6","Fast to load","Carga rápido","Light pages that open quickly, even on a weak signal.","Páginas ligeras que abren rápido, aunque haya poca señal."),
           ("M3 12h18M12 3a14 14 0 010 18M12 3a14 14 0 000 18M12 3a9 9 0 100 18 9 9 0 000-18z","i.7","Your languages","Tus idiomas","English, Spanish or the language your customers speak, on the same site.","Inglés, español o el idioma de tus clientes, en el mismo sitio."),
           ("M10 13a5 5 0 007.5.5l3-3a5 5 0 00-7-7l-1.7 1.7M14 11a5 5 0 00-7.5-.5l-3 3a5 5 0 007 7l1.7-1.7","i.8","Links you already use","Tus enlaces de siempre","Online ordering, booking, Facebook and Instagram, all in one spot.","Pedidos en línea, reservas, Facebook e Instagram, todo en un lugar.")]
    inch = "".join(f'<div class="inc reveal" style="--rd:{(i%4)*0.08:.2f}s"><span class="ic"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1D1A33" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="{d}"/></svg></span><h3 {tk(k+".h",h_en,h_es)}>{h_en}</h3><p {tk(k+".p",p_en,p_es)}>{p_en}</p></div>' for i,(d,k,h_en,h_es,p_en,p_es) in enumerate(inc))
    faqs = [("q1","Is there a monthly fee?","¿Hay un pago mensual?","No. You pay once. The only other cost is your web address, about $10–20 a year, paid to the company that registers it, in your name.","No. Pagas una sola vez. El único otro costo es tu dirección web, unos $10–20 al año, que pagas a la compañía que la registra, a tu nombre."),
            ("q2","What if I don't like the free sample?","¿Y si no me gusta la muestra gratis?","Then you owe nothing. The sample is free and there's no contract. You only pay once you decide to go ahead.","Entonces no debes nada. La muestra es gratis y no hay contrato. Solo pagas cuando decides seguir adelante."),
            ("q3","Who owns the site?","¿De quién es el sitio?","You do. The web address and your accounts are in your name. I only get helper access.","Tuyo. La dirección web y tus cuentas están a tu nombre. Yo solo tengo acceso para ayudarte."),
            ("q4","I already have a Facebook page.","Ya tengo una página de Facebook.","Keep it. Your site links to it. A website shows up on Google for people who don't use Facebook, and gives your Google listing a website button.","Quédatela. Tu sitio la enlaza. Un sitio web aparece en Google para la gente que no usa Facebook y le da a tu perfil de Google un botón de sitio web."),
            ("q5","What do you need from me?","¿Qué necesitas de mí?","Your menu or list of services, prices, a few photos and how you take orders or bookings. Photos from your phone are fine.","Tu menú o lista de servicios, precios, unas fotos y cómo recibes pedidos o citas. Las fotos del celular sirven."),
            ("q6","How long does it take?","¿Cuánto tiempo toma?","The free sample usually takes a couple of days. The full site is usually live about a week after I get your information.","La muestra gratis normalmente toma un par de días. El sitio completo suele estar en línea una semana después de recibir tu información."),
            ("q7","Can I change things later?","¿Puedo cambiar cosas después?","Yes. Small fixes in the first month are free; after that I'll tell you the price before I do anything.","Sí. Los cambios pequeños del primer mes son gratis; después te digo el precio antes de hacer cualquier cosa."),
            ("q8","Do you print flyers and cards?","¿Imprimes volantes y tarjetas?","I design them and send you print-ready files. You take them to any print shop and pay them directly, so there's no markup.","Yo los diseño y te mando archivos listos para imprimir. Los llevas a cualquier imprenta y les pagas directamente, sin recargos."),
            ("q9","Can my site be in another language?","¿Mi sitio puede estar en otro idioma?","Yes. Utica speaks a lot of languages. Your site can have English plus the language your customers speak, and you check the wording before it goes live.","Sí. En Utica se hablan muchos idiomas. Tu sitio puede tener inglés y el idioma de tus clientes, y tú revisas el texto antes de publicarlo."),
            ("q10","Do you work outside Utica?","¿Trabajas fuera de Utica?","Yes. Most of the work happens by email and text, so anywhere in Central New York works: Rome, New Hartford, Whitesboro, Yorkville, New York Mills and beyond.","Sí. Casi todo se hace por email y mensajes, así que cualquier lugar del Centro de Nueva York funciona: Rome, New Hartford, Whitesboro, Yorkville, New York Mills y más.")]
    faqh = "".join(f'<details{" open" if i==0 else ""}><summary {tk("faq."+k,q_en,q_es)}>{q_en}</summary><p {tk("faq."+k+"a",a_en,a_es)}>{a_en}</p></details>' for i,(k,q_en,q_es,a_en,a_es) in enumerate(faqs))
    faq_schema = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for _,q,_,a,_ in faqs]}
    return head("services", "Services & prices · Web Design CNY · Utica, NY",
                "Flat, one-time prices for small business websites, flyers, business cards and Google listing help in Utica, NY. Packages from $150. No monthly fee.",
                '<script type="application/ld+json">' + json.dumps(faq_schema) + '</script>') + header("services") + f'''
  <section class="phero">
    <div class="wrap">
      <div class="stack">
        <span class="kicker" {tk("sv.k","Services &amp; prices","Servicios y precios")}>Services &amp; prices</span>
        <h1 {tk("sv.h1","Fair prices, <span class=\"squiggle\">written down</span>.","Precios justos, <span class=\"squiggle\">por escrito</span>.")}>Fair prices, <span class="squiggle">written down{SQUIG}</span>.</h1>
        <p class="lede" {tk("sv.lede","Websites, flyers, cards and Google help for small shops and side hustles. Pay once, half to start and half when you approve. No monthly fee, ever.","Sitios web, volantes, tarjetas y ayuda con Google para pequeños negocios y emprendedores. Pagas una vez: la mitad al empezar y la mitad cuando apruebes. Nunca hay pago mensual.")}>Websites, flyers, cards and Google help for small shops and side hustles. Pay once, half to start and half when you approve. No monthly fee, ever.</p>
      </div>
      <div class="art scene" id="scene" style="aspect-ratio:1/0.8">
        <div class="sticker" style="top:6%;left:6%;--rot:-8deg;--dy:-140px;--spin:-20deg" aria-hidden="true">{STICKERS["browser"]}</div>
        <div class="sticker" style="top:44%;left:44%;--rot:7deg;--dy:-200px;--spin:25deg;--d:.7s" aria-hidden="true">{STICKERS["card"]}</div>
        <div class="sticker" style="top:2%;right:6%;--rot:12deg;--dy:-120px;--spin:60deg;--d:1.1s" aria-hidden="true">{STICKERS["star"]}</div>
        <div class="sticker" style="top:52%;left:2%;--rot:-4deg;--dy:-170px;--spin:-30deg;--d:.4s" aria-hidden="true">{STICKERS["palette"]}</div>
      </div>
    </div>
  </section>
  <div class="awning-stripe" aria-hidden="true"></div>

  <section>
    <div class="wrap">
      <div class="head center reveal">
        <span class="kicker" {tk("pr.k2","Packages","Paquetes")}>Packages</span>
        <h2 {tk("pr.h","Pick what fits. Pay once.","Escoge lo que te sirva. Pagas una vez.")}>Pick what fits. Pay once.</h2>
      </div>
      {plans_block()}
      <p class="plan-note" {tk("pr.note","Your web address costs about $10–20 a year, paid to the registrar in your name. Designs come as print-ready files; printing isn't included, and you pay the print shop directly.","Tu dirección web cuesta unos $10–20 al año, que pagas al registrador a tu nombre. Los diseños vienen listos para imprimir; la impresión no está incluida y le pagas directamente a la imprenta.")}>Your web address costs about $10–20 a year, paid to the registrar in your name. Designs come as print-ready files; printing isn't included, and you pay the print shop directly.</p>
    </div>
  </section>

  <section class="band-sky edge-top edge-bot" id="build">
    <div class="wrap builder-grid">
      <div>
        <div class="head reveal" style="margin-bottom:28px">
          <span class="kicker" {tk("b.k","Build your own","Arma el tuyo")}>Build your own</span>
          <h2 {tk("b.h","Only need one thing?","¿Solo necesitas una cosa?")}>Only need one thing?</h2>
          <p {tk("b.p","Tick what you want and see the total. If a package is cheaper, I'll tell you.","Marca lo que quieres y mira el total. Si un paquete sale más barato, te aviso.")}>Tick what you want and see the total. If a package is cheaper, I'll tell you.</p>
        </div>
        <fieldset class="opts"><legend class="skip" style="position:absolute;left:-9999px" {tk("b.legend","Pick services","Escoge servicios")}>Pick services</legend>
          {optsh}
          <div class="opt ask"><span></span><span><b {tk("b.ask","Social pages, menus, updates","Redes sociales, menús, cambios")}>Social pages, menus, updates</b><small {tk("b.ask.s","Facebook or Instagram setup, menu or price-list design, changes after the first month. I'll tell you the price first.","Configurar Facebook o Instagram, diseño de menú o lista de precios, cambios después del primer mes. Te digo el precio primero.")}>Facebook or Instagram setup, menu or price-list design, changes after the first month. I'll tell you the price first.</small></span><span class="p" {tk("b.askp","Ask","Pregunta")}>Ask</span></div>
        </fieldset>
      </div>
      <aside class="sum" aria-live="polite">
        <span class="kicker" {tk("b.tot.k","Your total","Tu total")}>Your total</span>
        <div class="lines" id="lines"></div>
        <div class="tot"><span {tk("b.once","One time","Una vez")}>One time</span><b id="total">$0</b></div>
        <div class="tip" id="tip" hidden></div>
        <a class="btn btn-red" id="build-cta" href="contact.html" {tk("b.cta","Ask for these","Pedir esto")}>Ask for these</a>
        <p class="fine" {tk("b.fine","Half to start, half when you approve. The free sample is always free.","La mitad al empezar, la mitad cuando apruebes. La muestra siempre es gratis.")}>Half to start, half when you approve. The free sample is always free.</p>
      </aside>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="head reveal">
        <span class="kicker" {tk("i.k","Every website includes","Todo sitio web incluye")}>Every website includes</span>
        <h2 {tk("i.h","Everything a customer looks for, in one place","Todo lo que un cliente busca, en un solo lugar")}>Everything a customer looks for, in one place</h2>
      </div>
      <div class="inc-grid">{inch}</div>
    </div>
  </section>

  <section class="band-sky edge-top" id="faq">
    <div class="wrap faq-grid">
      <div class="head reveal">
        <span class="kicker" {tk("faq.k","Questions owners ask","Preguntas frecuentes")}>Questions owners ask</span>
        <h2 {tk("faq.h","Straight answers","Respuestas claras")}>Straight answers</h2>
        <p {tk("faq.p","Something else on your mind? <a href=\"mailto:david@webdesigncny.com\">Email me</a>.","¿Tienes otra pregunta? <a href=\"mailto:david@webdesigncny.com\">Escríbeme</a>.")}>Something else on your mind? <a href="mailto:david@webdesigncny.com">Email me</a>.</p>
      </div>
      <div class="qs reveal">{faqh}</div>
    </div>
  </section>
''' + bigcta() + footer()

# ---------- ABOUT ----------
def about():
    prom = [("pm.1","You see it before you pay","La ves antes de pagar","The sample is free. If it's not for you, you owe nothing.","La muestra es gratis. Si no es para ti, no debes nada."),
            ("pm.2","Prices in writing, up front","Precios por escrito, desde el inicio","No surprise bills. If something isn't listed, I tell you the price before I start.","Sin cobros sorpresa. Si algo no está en la lista, te digo el precio antes de empezar."),
            ("pm.3","Everything stays in your name","Todo queda a tu nombre","Your web address and accounts are yours. I only get helper access.","Tu dirección web y tus cuentas son tuyas. Yo solo tengo acceso para ayudarte."),
            ("pm.4","No fake reviews, ever","Nunca reseñas falsas","I'll help you ask real customers for reviews. I never write or buy them.","Te ayudo a pedir reseñas a clientes reales. Nunca las escribo ni las compro.")]
    promh = "".join(f'<li class="reveal" style="--rd:{i*0.08:.2f}s"><span class="n">{i+1}</span><b {tk(k,b_en,b_es)}>{b_en}</b><span {tk(k+".s",s_en,s_es)}>{s_en}</span></li>' for i,(k,b_en,b_es,s_en,s_es) in enumerate(prom))
    return head("about", "About David & the crew · Web Design CNY · Utica, NY",
                "Web Design CNY is David from West Utica and his two dogs: a neighbor who makes friendly, affordable websites and graphics for local shops.") + header("about") + f'''
  <section class="phero">
    <div class="wrap">
      <div class="stack">
        <span class="kicker" {tk("ab.k","About","Quién soy")}>About</span>
        <h1 {tk("ab.h1","Hi! I'm David. My dogs are my <span class=\"squiggle\">coworkers</span>.","¡Hola! Soy David. Mis perros son mis <span class=\"squiggle\">compañeros</span>.")}>Hi! I'm David. My dogs are my <span class="squiggle">coworkers{SQUIG}</span>.</h1>
        <p class="lede" {tk("ab.lede","Web Design CNY is me and my two dogs, working out of West Utica. I make websites and graphics for the small shops and side hustles we walk past every day.","Web Design CNY somos yo y mis dos perros, desde West Utica. Hago sitios web y diseños para los pequeños negocios y emprendedores por los que pasamos todos los días.")}>Web Design CNY is me and my two dogs, working out of West Utica. I make websites and graphics for the small shops and side hustles we walk past every day.</p>
      </div>
      <div class="crew-art">{CREW}<span class="cap" {tk("crew.cap","West Utica HQ","Sede en West Utica")}>West Utica HQ</span></div>
    </div>
  </section>
  <div class="awning-stripe" aria-hidden="true"></div>

  <section>
    <div class="wrap crew" style="align-items:start">
      <div class="stack reveal">
        <span class="kicker" {tk("ab.why.k","Why I do this","Por qué lo hago")}>Why I do this</span>
        <h2 {tk("crew.h","A neighbor, not an agency","Un vecino, no una agencia")}>A neighbor, not an agency</h2>
      </div>
      <div class="stack reveal" style="--rd:.12s">
        <p {tk("ab.p1","Utica is full of great small businesses: family delis, barbershops, salons, bakeries, markets and auto shops run by people from all over the world. A lot of them have a Facebook page or nothing at all, and no website button on their Google listing.","Utica está llena de pequeños negocios buenísimos: delis familiares, barberías, salones, panaderías, mercados y talleres de gente de todo el mundo. Muchos tienen una página de Facebook o nada, y no tienen botón de sitio web en su perfil de Google.")}>Utica is full of great small businesses: family delis, barbershops, salons, bakeries, markets and auto shops run by people from all over the world. A lot of them have a Facebook page or nothing at all, and no website button on their Google listing.</p>
        <p {tk("ab.p2","Agencies charge agency prices. I keep it simple: a fair flat price, a site you own, and a real person nearby you can reach when something needs changing.","Las agencias cobran precios de agencia. Yo lo mantengo sencillo: un precio justo y fijo, un sitio que es tuyo, y una persona real y cercana a quien puedes contactar cuando necesites un cambio.")}>Agencies charge agency prices. I keep it simple: a fair flat price, a site you own, and a real person nearby you can reach when something needs changing.</p>
        <p {tk("ab.p3","And the dogs? They supervise. Every website gets their approval before it goes live.","¿Y los perros? Ellos supervisan. Cada sitio web pasa por su aprobación antes de publicarse.")}>And the dogs? They supervise. Every website gets their approval before it goes live.</p>
      </div>
    </div>
  </section>

  <section class="band-ink">
    <div class="wrap">
      <div class="head reveal">
        <span class="kicker" {tk("pm.k","My promises","Mis promesas")}>My promises</span>
        <h2 {tk("pm.h","How I work with every shop","Cómo trabajo con cada negocio")}>How I work with every shop</h2>
      </div>
      <ul class="promises">{promh}</ul>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="head reveal">
        <span class="kicker" {tk("ar.k","Where I work","Dónde trabajo")}>Where I work</span>
        <h2 {tk("ar.h","All over Utica and Central New York","En todo Utica y el Centro de Nueva York")}>All over Utica and Central New York</h2>
        <p {tk("ar.p","West Utica, East Utica, North Utica, Cornhill, Bagg's Square, New Hartford, Whitesboro, Yorkville, New York Mills, Rome and anywhere else in Oneida County. Most of the work happens by email and text.","West Utica, East Utica, North Utica, Cornhill, Bagg's Square, New Hartford, Whitesboro, Yorkville, New York Mills, Rome y cualquier otro lugar del condado de Oneida. Casi todo se hace por email y mensajes.")}>West Utica, East Utica, North Utica, Cornhill, Bagg's Square, New Hartford, Whitesboro, Yorkville, New York Mills, Rome and anywhere else in Oneida County. Most of the work happens by email and text.</p>
      </div>
    </div>
  </section>
''' + bigcta() + footer()

# ---------- CONTACT ----------
def contact():
    kinds = [("Restaurant, deli or cafe","Restaurante, deli o café"),("Barbershop or salon","Barbería o salón"),("Auto shop","Taller mecánico"),("Contractor or trades","Contratista u oficios"),("Store or market","Tienda o mercado"),("Side hustle","Emprendimiento"),("Something else","Otro")]
    kopts = "".join(f'<option value="{en}" {tk("ct.kind."+str(i),en,es)}>{en}</option>' for i,(en,es) in enumerate(kinds))
    plans = [("sample","Just the free sample for now","Solo la muestra gratis por ahora"),("website","Small business website ($200)","Sitio web para negocio ($200)"),("hustler","Hustler package ($150)","Paquete Hustler ($150)"),("entrepreneur","Entrepreneur package ($300)","Paquete Emprendedor ($300)"),("custom","Something from Build your own","Algo de Arma el tuyo"),("unsure","Not sure yet","Todavía no sé")]
    popts = "".join(f'<option value="{v}" {tk("ct.plan."+v,en,es)}>{en}</option>' for v,en,es in plans)
    return head("contact", "Get a free sample · Web Design CNY · Utica, NY",
                "Ask for a free sample homepage for your Utica-area business. No cost, no contract. Email david@webdesigncny.com.") + header("contact") + f'''
  <section class="phero" style="padding-bottom:40px">
    <div class="wrap" style="grid-template-columns:minmax(0,1fr)">
      <div class="stack">
        <span class="kicker" {tk("ct.k","Free sample","Muestra gratis")}>Free sample</span>
        <h1 {tk("ct.h1","Want to see <span class=\"squiggle\">yours</span>?","¿Quieres ver <span class=\"squiggle\">el tuyo</span>?")}>Want to see <span class="squiggle">yours{SQUIG}</span>?</h1>
        <p class="lede" {tk("ct.lede","Tell me about your business. I'll build a free sample homepage and send it to you, usually within a couple of days. No cost, no contract.","Cuéntame de tu negocio. Te hago una página de muestra gratis y te la envío, normalmente en un par de días. Sin costo y sin contrato.")}>Tell me about your business. I'll build a free sample homepage and send it to you, usually within a couple of days. No cost, no contract.</p>
      </div>
    </div>
  </section>

  <section style="padding-top:20px">
    <div class="wrap contact-grid">
      <div class="direct reveal">
        <div class="card"><span class="k" {tk("ct.em","Email","Email")}>Email</span><a class="v" href="{MAIL}">david@webdesigncny.com</a></div>
        <div class="card"><span class="k" {tk("ct.based","Based in","Ubicación")}>Based in</span><span class="v" {tk("ct.wu","West Utica, NY","West Utica, NY")}>West Utica, NY</span></div>
        <div class="card"><span class="k" {tk("ct.lang","Languages","Idiomas")}>Languages</span><span class="v" style="font-size:19px" {tk("ct.langv","Write in your language. I use translation tools and will answer in yours.","Escríbeme en tu idioma. Uso herramientas de traducción y te respondo en el tuyo.")}>Write in your language. I use translation tools and will answer in yours.</span></div>
        <div class="crew-art" style="margin-top:10px">{CREW}</div>
      </div>
      <form class="form reveal" style="--rd:.12s" id="sample-form" action="mailto:david@webdesigncny.com" method="post" enctype="text/plain">
        <label class="full"><span {tk("ct.f.biz","Business name","Nombre del negocio")}>Business name</span><input name="business" required autocomplete="organization" {ph("ct.f.bizph","e.g. Main Street Deli","p. ej. Deli de la calle Main")}></label>
        <label><span {tk("ct.f.kind","Type of business","Tipo de negocio")}>Type of business</span><select name="kind">{kopts}</select></label>
        <label><span {tk("ct.f.name","Your name","Tu nombre")}>Your name</span><input name="name" autocomplete="name"></label>
        <label class="full"><span {tk("ct.f.reach","Best way to reach you","Cómo contactarte")}>Best way to reach you</span><small {tk("ct.f.reachs","Phone or email","Teléfono o email")}>Phone or email</small><input name="reach" autocomplete="tel"></label>
        <label class="full"><span {tk("ct.f.plan","I'm interested in","Me interesa")}>I'm interested in</span><select name="plan" id="plan">{popts}</select></label>
        <label class="full"><span {tk("ct.f.note","Anything else?","¿Algo más?")}>Anything else?</span><small {tk("ct.f.opt","Optional","Opcional")}>Optional</small><textarea name="note" id="note" {ph("ct.f.noteph","Your Facebook page, Google listing, or what you need","Tu página de Facebook, perfil de Google o lo que necesitas")}></textarea></label>
        <div class="full"><button class="btn btn-red" type="submit"><span {tk("ct.f.send","Send my free sample request","Enviar mi solicitud de muestra")}>Send my free sample request</span>{ARROW}</button></div>
        <p class="full fine" {tk("ct.f.fine","This opens your email app with everything filled in. Nothing is sent until you press send.","Esto abre tu app de email con todo ya escrito. No se envía nada hasta que presiones enviar.")}>This opens your email app with everything filled in. Nothing is sent until you press send.</p>
      </form>
    </div>
  </section>
''' + footer()

# JS-only strings
JS_ES = {
 "js.empty":"Todavía no has escogido nada.", "js.combo":"Volante + tarjeta juntos",
 "js.tipH":"El paquete Hustler incluye todo esto por $150. Ahorrarías ${n}.",
 "js.tipE":"El paquete Emprendedor incluye todo esto por $300. Ahorrarías ${n}.",
 "js.tipBoth":"Solo necesitas un sitio web. El de una página es para emprendedores; el completo es para negocios.",
 "js.noteprefix":"Me interesa: ",
 "js.mail.hi":"Hola David,", "js.mail.want":"Quisiera una muestra gratis para mi negocio.",
 "js.mail.biz":"Negocio", "js.mail.type":"Tipo", "js.mail.name":"Mi nombre", "js.mail.reach":"Cómo contactarme", "js.mail.plan":"Me interesa",
 "js.mail.subj":"Muestra gratis",
 # phone demo
 "d.deli.name":"Tu Deli","d.deli.head":"Sándwiches, pizza y abarrotes","d.deli.sub":"Tu deli de la esquina. Pide antes o pasa.","d.deli.btn":"Llama para ordenar","d.deli.photo":"Foto de tu comida",
 "d.barber.name":"Tu Barbería","d.barber.head":"Cortes frescos. Sin cita.","d.barber.sub":"Fades, barba y cortes para niños.","d.barber.btn":"Reserva tu silla","d.barber.photo":"Tu mejor corte",
 "d.auto.name":"Tu Taller","d.auto.head":"Reparaciones honestas y bien hechas","d.auto.sub":"Frenos, cambio de aceite, llantas e inspecciones.","d.auto.btn":"Llama para cotizar","d.auto.photo":"Tu taller",
 "d.salon.name":"Tu Salón","d.salon.head":"Color, cortes y peinados","d.salon.sub":"Reserva tu cita en un minuto.","d.salon.btn":"Reservar","d.salon.photo":"Tu trabajo",
 "d.hustle.name":"Tu Nombre · Limpieza","d.hustle.head":"Limpieza de casa en la que puedes confiar","d.hustle.sub":"Semanal, cada dos semanas o una vez.","d.hustle.btn":"Escríbeme para cotizar","d.hustle.photo":"Antes y después",
 "d.mf":"Lun–Vie","d.sat":"Sáb","d.sun":"Dom","d.closed":"Cerrado","d.ask":"Pregunta","d.from":"desde",
 "d.r.haircut":"Corte","d.r.fade":"Fade + barba","d.r.kids":"Corte niño","d.r.cut":"Corte y peinado","d.r.color":"Color","d.r.blow":"Secado","d.r.apt":"Apartamento","d.r.house":"Casa","d.r.move":"Mudanza",
}

pages = {"index.html": home(), "services.html": services(), "about.html": about(), "contact.html": contact()}
for name, html in pages.items():
    open(os.path.join(REPO, name), "w").write(html)
ES.update(JS_ES)
import re
for k,v in list(ES.items()):
    ES[k]=re.sub(r'(<span class="squiggle">)(.*?)(</span>)', lambda m: m.group(1)+m.group(2)+SQUIG+m.group(3), v)
langs = [{"code":"en","name":"English","sub":""},{"code":"es","name":"Español","sub":"Spanish"}]
with open(os.path.join(REPO, "assets/i18n.js"), "w") as f:
    f.write("/* Translations. English lives in the HTML; other languages are keyed by data-i18n ids.\n   Machine-assisted translations: have a native speaker check before relying on them. */\n")
    f.write("window.WDC_LANGS = " + json.dumps(langs, ensure_ascii=False) + ";\n")
    f.write("window.WDC_I18N = " + json.dumps({"es": ES}, ensure_ascii=False, indent=0) + ";\n")
print("keys", len(ES))
