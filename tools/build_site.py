#!/usr/bin/env python3
"""Build the ODIRAH concept site into site/.

Every page shares one header, menu, footer and bag, written here once.
Run from the repository root:  python3 tools/build_site.py
"""
import html
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
SRC = ROOT / "tools" / "src"

WORDMARK = re.search(r' d="([^"]+)"', (SITE / "assets/brand/odirah-wordmark.svg").read_text()).group(1)
VB = "0 0 1104.91 221.00"
ARROW = '<svg aria-hidden="true"><use href="#arrow"/></svg>'

ARCH = [
    dict(id="silk-and-ashes", n="I", arch="The Maiden", name="Silk & Ashes", tone="#EDE5E1",
         story="Silver morning light on silk. The self before the world arrived.",
         text="Before the world asks anything of her, there is a quiet room, silver light and the soft weight of silk. Silk & Ashes holds the first breath of the day: the self that exists before any role begins, unhurried and entirely her own.",
         world="An oval mirror, ivory silk, white lilies and a strand of pearls, in the pale light of early morning."),
    dict(id="skin-and-shadow", n="II", arch="The Lover", name="Skin & Shadow", tone="#E8DCD2",
         story="Warm skin, a shadow on the wall, the hour no one else sees.",
         text="The hour when the door is closed and the light is low. Skin & Shadow is warmth carried close to the body: the intimacy that needs no audience, the part of you that only one person knows.",
         world="Bronze satin, the shadow of leaves on a warm wall, and the low glow of late evening."),
    dict(id="ember-and-desire", n="III", arch="The Seductress", name="Ember & Desire", tone="#EBD9D3",
         story="Velvet, ember and a mirror that keeps your secret.",
         text="A curtain drawn, a glow that does not go out. Ember & Desire is the part of you that knows its own pull and does not apologise for it: certain, warm and impossible to overlook.",
         world="Red velvet, a gilded mirror, a ruby decanter and an iris, lit by the colour of embers."),
    dict(id="stars-and-whisper", n="IV", arch="The Wanderer", name="Stars & Whisper", tone="#E4E0E2",
         story="A tent of light under the open sky. Home is where you breathe.",
         text="A night in the open, a lantern, a horizon that keeps moving. Stars & Whisper is for the self that feels most at home while travelling, carrying a small light through very large spaces.",
         world="A desert under the Milky Way, a crescent moon and a single tent glowing with lantern light."),
    dict(id="velvet-and-poise", n="V", arch="The Queen", name="Velvet & Poise", tone="#E9E0DD",
         story="Stillness, gold, and a key she has always held.",
         text="Stillness as a form of power. Velvet & Poise carries the composure of someone who has always held the key and never needed to show it: unhurried, generous and entirely sure of her ground.",
         world="A palace balcony over the river, purple velvet, a sealed scroll, a golden key and a white lily."),
    dict(id="rain-and-solace", n="VI", arch="The Healer", name="Rain & Solace", tone="#E5E4DA",
         story="Rain on old stone. The quiet that puts you back together.",
         text="Rain over old stone and a garden slowly taking back its ruins. Rain & Solace is the quiet that gathers you up and puts you back together, the part of you that tends to others and, at last, to herself.",
         world="An overgrown archway after rain, moss, white wildflowers and clear water over old steps."),
]

NAV = [("collection.html", "Fragrances"), ("discovery-kit.html", "Discovery Kit"),
       ("the-house.html", "The House"), ("the-house.html#manifesto", "Manifesto"), ("shop.html", "Shop")]


def e(s):
    return html.escape(s, quote=True)


def img(base, name, alt, sizes, small=640, large=1200, w=1200, h=1490, lazy=True):
    return (f'<img src="{base}assets/img/{name}-{small}.webp" srcset="{base}assets/img/{name}-{small}.webp {small}w, '
            f'{base}assets/img/{name}-{large}.webp {large}w" sizes="{sizes}" width="{w}" height="{h}"'
            f'{" loading=\"lazy\"" if lazy else ""} decoding="async" alt="{e(alt)}">')


def page(path, title, description, body, current=None, has_hero=False, extra_end=""):
    depth = path.count("/")
    base = "../" * depth
    links = "".join(
        f'<li><a href="{base}{href}"{" aria-current=\"page\"" if current == href else ""}>{label}</a></li>'
        for href, label in NAV)
    menu_links = "".join(f'<a href="{base}{h}" data-close-menu>{l}</a>' for h, l in
                         [("collection.html", "The Archetypes: HER"), ("discovery-kit.html", "Discovery Kit"),
                          ("shop.html", "Shop"), ("the-house.html", "The House")])
    doc = f"""<!doctype html>
<html lang="en" data-base="{base}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<meta name="theme-color" content="#301E15">
<link rel="icon" href="{base}assets/brand/odirah-wordmark.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Cormorant+SC:wght@500;600&family=Pinyon+Script&display=swap">
<link rel="stylesheet" href="{base}assets/css/odirah.css">
<script src="{base}assets/js/odirah.js" defer></script>
</head>
<body{' class="has-hero"' if has_hero else ''}>
<a class="skip" href="#main">Skip to content</a>
<svg width="0" height="0" style="position:absolute" aria-hidden="true">
  <symbol id="wordmark" viewBox="{VB}"><path fill="currentColor" d="{WORDMARK}"/></symbol>
  <symbol id="arrow" viewBox="0 0 14 10"><path d="M0 5h12.5M8.5 1l4 4-4 4" fill="none" stroke="currentColor" stroke-width="1.2"/></symbol>
</svg>

<header class="site-header" id="top">
  <div class="nav">
    <button class="menu-btn" type="button" aria-controls="menu" aria-expanded="false" data-open-menu>Menu</button>
    <a class="logo" href="{base}index.html" aria-label="ODIRAH, home"><svg viewBox="{VB}" aria-hidden="true"><use href="#wordmark"/></svg></a>
    <ul class="nav-links">{links}</ul>
    <div class="nav-end">
      <a class="hide-m" href="{base}shop.html">Search</a>
      <a class="hide-m" href="#account" data-soon="Accounts arrive with the Shopify build.">Account</a>
      <button type="button" data-open-bag aria-controls="bag">Bag (<span data-count>0</span>)</button>
    </div>
  </div>
</header>

<div class="menu" id="menu" aria-label="Menu" role="dialog" aria-modal="true">
  <div class="menu-top">
    <button type="button" class="label" data-close-menu>Close</button>
    <span class="logo" style="width:108px"><svg viewBox="{VB}" aria-hidden="true"><use href="#wordmark"/></svg></span>
    <button type="button" class="label" data-open-bag>Bag</button>
  </div>
  <nav aria-label="Main">{menu_links}</nav>
  <div class="utility label"><a href="{base}shop.html">Search</a><a href="#account" data-soon="Accounts arrive with the Shopify build.">Account</a><a href="{base}contact.html">Contact</a></div>
</div>

<main id="main">
{body.replace("{B}", base)}
</main>

<footer class="mosaic footer" id="contact">
  <div class="panel foot-news">
    <span class="logo"><svg viewBox="{VB}" role="img" aria-label="ODIRAH"><use href="#wordmark"/></svg></span>
    <p>Letters from the house. New worlds, first.</p>
    <form data-news novalidate>
      <label for="news-email" class="sr">Email address</label>
      <input id="news-email" name="email" type="email" placeholder="Email address" autocomplete="email" required>
      <button type="submit">Join</button>
    </form>
    <p class="msg" aria-live="polite" data-news-msg></p>
  </div>
  <div class="panel links"><h3>Shop</h3><ul><li><a href="{base}shop.html">All fragrances</a></li><li><a href="{base}collection.html">The Archetypes: HER</a></li><li><a href="{base}discovery-kit.html">Discovery Kit</a></li></ul></div>
  <div class="panel links"><h3>House</h3><ul><li><a href="{base}the-house.html">The House</a></li><li><a href="{base}the-house.html#manifesto">Manifesto</a></li><li><a href="{base}contact.html">Contact</a></li></ul></div>
  <div class="panel links"><h3>Help</h3><ul><li><a href="{base}contact.html#help">Shipping &amp; returns</a></li><li><a href="{base}contact.html#help">FAQ</a></li><li><a href="{base}contact.html#legal">Legal</a></li></ul></div>
  <div class="panel foot-base"><span>© 2026 ODIRAH. All rights reserved.</span><span>Concept preview. Prices, vial size and fragrance copy to be confirmed.</span></div>
</footer>

<div class="scrim" data-scrim></div>
<aside class="bag" id="bag" role="dialog" aria-modal="true" aria-labelledby="bag-title">
  <header><h2 id="bag-title">Your bag</h2><button type="button" class="label" data-close-bag>Close</button></header>
  <div class="items" data-items></div>
  <footer>
    <div class="row"><span class="label">Subtotal</span><span>Price on launch</span></div>
    <p class="note">Shipping and taxes are calculated at checkout.</p>
    <button type="button" class="btn btn--dark" data-checkout>Checkout</button>
    <p class="note" data-checkout-msg aria-live="polite"></p>
  </footer>
</aside>
{extra_end}
</body>
</html>
"""
    out = SITE / path
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc)
    return out


KIT_SPLIT = """
  <section class="mosaic split rev" aria-labelledby="kit-title">
    <div class="panel text-panel kit-panel">
      <div class="reveal">
        <h2 id="kit-title">Meet all six before you choose.</h2>
        <p class="lede">Wear one archetype a day, on skin, not paper. Notice which one stays with you into the evening. That is usually her.</p>
      </div>
      <div class="panel-foot reveal">
        <ul class="spec">
          <li><span>Inside</span><span>All six fragrances</span></li>
          <li><span>Vials</span><span>6 × 7 or 10 ml</span></li>
          <li><span>Box</span><span>Dedicated Discovery Kit box</span></li>
        </ul>
        <div style="display:flex;flex-wrap:wrap;gap:10px">
          <button type="button" class="btn btn--light" data-add="kit">Add the kit to bag""" + ARROW + """</button>
          <a class="btn" style="color:var(--blush)" href="{B}discovery-kit.html">View the kit</a>
        </div>
      </div>
    </div>
    <figure class="panel media wide" style="margin:0"><img src="{B}assets/img/discovery-kit-1600.webp" srcset="{B}assets/img/discovery-kit-800.webp 800w, {B}assets/img/discovery-kit-1600.webp 1600w" sizes="(max-width:860px) 100vw, 66vw" width="1600" height="1200" loading="lazy" decoding="async" alt="The Discovery Kit: an open brown linen box holding six slim glass vials of amber fragrance with stone caps."></figure>
  </section>"""


def build_home():
    main = (SRC / "home-main.html").read_text()
    main = main[len('<main id="main">'):-len("</main>")]
    main = main.replace('src="assets/', 'src="{B}assets/').replace('srcset="assets/', 'srcset="{B}assets/') \
               .replace(', assets/', ', {B}assets/').replace('data-src-small="assets/', 'data-src-small="{B}assets/') \
               .replace('<source src="assets/', '<source src="{B}assets/')
    main = main.replace('href="#fragrances">Shop the collection', 'href="{B}shop.html">Shop the collection')
    main = main.replace('href="#house">Explore', 'href="{B}the-house.html">Explore')
    main = main.replace('href="#manifesto">Our vision', 'href="{B}the-house.html">Our vision')
    main = main.replace(
        '<button type="button" class="btn btn--light" data-add="kit">Add the kit to bag' + ARROW + '</button>',
        '<div style="display:flex;flex-wrap:wrap;gap:10px"><button type="button" class="btn btn--light" data-add="kit">Add the kit to bag'
        + ARROW + '</button><a class="btn" style="color:var(--blush)" href="{B}discovery-kit.html">View the kit</a></div>')
    page("index.html", "ODIRAH · Intimately you",
         "ODIRAH is a house of fragrance. The Archetypes: HER, six fragrances for the worlds within you.",
         main, has_hero=True)


def build_collection():
    idx = "".join(f'<li><a href="#{a["id"]}"><span class="label">{a["n"]}</span><span class="script">{e(a["name"])}</span>'
                  f'<span class="label">{a["arch"]}</span></a></li>' for a in ARCH)
    body = f"""
  <section class="mosaic split rev" aria-labelledby="col-title">
    <div class="panel text-panel">
      <div>
        <h1 id="col-title" style="font-size:clamp(2.8rem,1.8rem + 3.4vw,5rem)">The Archetypes: HER</h1>
        <p style="margin-top:20px;max-width:26rem;color:var(--brown)">Six fragrances, six feminine archetypes. Each one gives voice to a different part of the inner world, so that several sides of you can coexist.</p>
      </div>
      <ul class="index-list">{idx}</ul>
    </div>
    <figure class="panel media" style="margin:0">{img("{B}", "mirror-monolith", "A woman in white stands before a tall mirror in a red rock desert, her reflection looking back.", "(max-width:860px) 100vw, 66vw", lazy=False)}</figure>
  </section>
"""
    for i, a in enumerate(ARCH):
        rev = i % 2 == 1
        media = f'<figure class="panel media tall" style="margin:0">{img("{B}", a["id"], "Painterly illustration for " + a["name"] + ": " + a["world"], "(max-width:860px) 100vw, 66vw")}</figure>'
        text = f"""<div class="panel text-panel" style="--tone:{a['tone']}">
      <span class="label corner">{a['n']}</span>
      <div class="reveal">
        <h2 class="script">{e(a['name'])}</h2>
        <p class="arch-name label">{a['arch']}</p>
        <p class="story">{a['story']}</p>
        <p class="dense">{e(a['text'])}</p>
      </div>
      <div class="buy-row reveal">
        <span class="meta">Eau de parfum · 100 ml</span>
        <span class="acts"><button type="button" class="btn btn--dark" data-add="{a['id']}">Add to bag</button><a class="btn btn--line" href="{{B}}fragrances/{a['id']}.html">Discover{ARROW}</a></span>
      </div>
    </div>"""
        body += f"""
  <section class="mosaic split chapter{' rev' if rev else ''}" id="{a['id']}" aria-label="{e(a['name'])}, {a['arch']}" style="scroll-margin-top:90px">
    {text + media if rev else media + text}
  </section>"""
    body += KIT_SPLIT
    page("collection.html", "The Archetypes: HER · ODIRAH",
         "Six fragrances, six feminine archetypes: The Maiden, The Lover, The Seductress, The Wanderer, The Queen and The Healer.",
         body, current="collection.html")


def build_fragrance(a):
    others = a["id"]
    body = f"""
  <section class="mosaic pdp" aria-labelledby="p-title">
    <div class="gallery">
      <figure class="panel" style="margin:0">{img("{B}", "bottle-on-stone", "The ODIRAH bottle: amber eau de parfum with a round stone stopper, on sandstone.", "(max-width:960px) 50vw, 33vw", lazy=False)}</figure>
      <figure class="panel" style="margin:0">{img("{B}", a["id"], "Painterly illustration for " + a["name"] + ": " + a["world"], "(max-width:960px) 50vw, 33vw", lazy=False)}</figure>
      <figure class="panel wide" style="margin:0"><img src="{{B}}assets/img/terracotta-velvet-1600.webp" width="1600" height="905" loading="lazy" decoding="async" alt="Close-up of terracotta velvet, the texture of the ODIRAH packaging."></figure>
    </div>
    <div class="panel buy-panel">
      <span class="label corner">{a['n']}</span>
      <div>
        <h1 id="p-title">{e(a['name'])}</h1>
        <p class="arch-name label">{a['arch']}</p>
      </div>
      <p class="story">{a['story']}</p>
      <div>
        <div class="price-row"><span>Eau de parfum · 100 ml</span><span class="price">Price on launch</span></div>
      </div>
      <button type="button" class="btn btn--dark" data-add="{a['id']}" data-main-add>Add to bag{ARROW}</button>
      <a class="kit-link" href="{{B}}discovery-kit.html"><span>Not sure yet? Try all six in the Discovery Kit.</span>{ARROW}</a>
      <div class="acc">
        <details><summary>Olfactory notes</summary><p>Top, heart and base notes will be published with the launch.</p></details>
        <details><summary>Ingredients</summary><p>The full ingredient list will be published with the launch.</p></details>
        <details><summary>Delivery &amp; returns</summary><p>Delivery options and costs are shown at checkout. Unopened bottles can be returned; the full policy will be published with the launch.</p></details>
      </div>
    </div>
  </section>

  <section class="mosaic split" aria-labelledby="world-title">
    <figure class="panel media" style="margin:0">{img("{B}", a["id"], a["world"], "(max-width:860px) 100vw, 66vw")}</figure>
    <div class="panel story-panel" style="background:{a['tone']}">
      <h2 id="world-title" class="reveal">Her world</h2>
      <p class="dense reveal">{e(a['text'])} {e(a['world'])}</p>
    </div>
  </section>

  <section class="mosaic three" aria-label="Olfactory profile">
    <div class="panel"><span class="label corner">I</span><div><h3>Top</h3><p class="tba">Notes to be announced with the launch.</p></div></div>
    <div class="panel"><span class="label corner">II</span><div><h3>Heart</h3><p class="tba">Notes to be announced with the launch.</p></div></div>
    <div class="panel"><span class="label corner">III</span><div><h3>Base</h3><p class="tba">Notes to be announced with the launch.</p></div></div>
  </section>

  <section class="mosaic" aria-labelledby="others-title">
    <div class="panel title-panel" style="min-height:0">
      <h2 id="others-title" style="font-size:clamp(2rem,1.5rem + 1.8vw,3.2rem)">The other archetypes</h2>
      <p>Each archetype is a different part of the same inner world. Compare them, or meet all six in the Discovery Kit.</p>
    </div>
  </section>
  <section class="mosaic tiles five" aria-label="The other five fragrances" data-tiles data-exclude="{others}" data-sizes="(max-width:600px) 60vw, (max-width:1200px) 25vw, 14vw"></section>
"""
    sticky = f"""<div class="sticky-buy" data-sticky-buy aria-hidden="false"><span class="script">{e(a['name'])}</span><button type="button" class="btn btn--dark" data-add="{a['id']}">Add to bag</button></div>"""
    page(f"fragrances/{a['id']}.html", f"{a['name']} · {a['arch']} · ODIRAH",
         f"{a['name']}, {a['arch']}. Eau de parfum, 100 ml, from The Archetypes: HER by ODIRAH. {a['story']}",
         body, current="collection.html", extra_end=sticky)


def build_kit():
    vials = "".join(f"""<article class="panel tile" style="--tone:{a['tone']}">
      <div class="tile-top"><span class="label">{a['n']}</span></div>
      <a class="arch" href="{{B}}fragrances/{a['id']}.html" aria-label="{e(a['name'])}">{img("{B}", a["id"], "", "(max-width:600px) 52vw, 20vw")}</a>
      <div class="tile-name"><h3><a href="{{B}}fragrances/{a['id']}.html" style="text-decoration:none">{e(a['name'])}</a></h3><span class="vol">7/10 ml</span></div>
      <p class="arch-name label">{a['arch']}</p>
      <p class="story">{a['story']}</p>
    </article>""" for a in ARCH)
    body = f"""
  <section class="mosaic pdp" aria-labelledby="kit-h1">
    <div class="gallery">
      <figure class="panel wide" style="margin:0"><img src="{{B}}assets/img/discovery-kit-1600.webp" srcset="{{B}}assets/img/discovery-kit-800.webp 800w, {{B}}assets/img/discovery-kit-1600.webp 1600w" sizes="(max-width:960px) 100vw, 66vw" width="1600" height="1200" decoding="async" alt="The Discovery Kit: an open brown linen box holding six slim glass vials of amber fragrance with stone caps."></figure>
    </div>
    <div class="panel buy-panel" style="min-height:0">
      <div>
        <h1 id="kit-h1" style="font-family:var(--f-serif);font-weight:500;font-size:clamp(2.8rem,2rem + 2.4vw,4.4rem)">Discovery Kit</h1>
        <p class="arch-name label">The Archetypes: HER</p>
      </div>
      <p class="story">All six archetypes in one box, so you can meet each of them before choosing a full size.</p>
      <ul class="spec" style="border-color:var(--line)">
        <li style="border-color:var(--line)"><span style="color:var(--brown)">Inside</span><span>All six fragrances</span></li>
        <li style="border-color:var(--line)"><span style="color:var(--brown)">Vials</span><span>6 × 7 or 10 ml (to be confirmed)</span></li>
        <li style="border-color:var(--line)"><span style="color:var(--brown)">Box</span><span>Dedicated Discovery Kit box</span></li>
      </ul>
      <div class="price-row"><span>Complete set</span><span class="price">Price on launch</span></div>
      <button type="button" class="btn btn--dark" data-add="kit" data-main-add>Add to bag{ARROW}</button>
    </div>
  </section>

  <section class="mosaic" aria-labelledby="inside-title">
    <div class="panel title-panel" style="min-height:0">
      <h2 id="inside-title" style="font-size:clamp(2rem,1.5rem + 1.8vw,3.2rem)">What’s inside</h2>
      <p>One vial of each archetype. Every vial leads to its full-size fragrance.</p>
    </div>
  </section>
  <section class="mosaic tiles" aria-label="The six vials">{vials}</section>

  <section class="mosaic three" aria-label="How to choose your full size">
    <div class="panel"><span class="label corner">1</span><div><h3>Wear one a day</h3><p>On skin, not paper. Give each archetype a whole day to unfold.</p></div></div>
    <div class="panel"><span class="label corner">2</span><div><h3>Notice which one stays</h3><p>The one you think about in the evening is usually the one.</p></div></div>
    <div class="panel"><span class="label corner">3</span><div><h3>Choose her in 100 ml</h3><p>Every vial in the box leads to its full-size fragrance page.</p></div></div>
  </section>

  <section class="mosaic split rev" aria-labelledby="kit-faq">
    <div class="panel text-panel">
      <h2 id="kit-faq" style="font-size:clamp(2rem,1.5rem + 1.8vw,3.2rem)">Questions about the kit</h2>
      <div class="acc">
        <details><summary>Can I buy a single vial?</summary><p>No. The Discovery Kit is sold as a complete set of all six fragrances.</p></details>
        <details><summary>How large are the vials?</summary><p>Each vial holds 7 or 10 ml. The final size will be confirmed before launch.</p></details>
        <details><summary>Does the kit count towards a full size?</summary><p>To be confirmed by the house before launch.</p></details>
      </div>
    </div>
    <figure class="panel media wide" style="margin:0">{img("{B}", "bottle-on-stone", "The full-size ODIRAH bottle on sandstone.", "(max-width:860px) 100vw, 66vw")}</figure>
  </section>
"""
    sticky = f"""<div class="sticky-buy" data-sticky-buy><span class="label">Discovery Kit</span><button type="button" class="btn btn--dark" data-add="kit">Add to bag</button></div>"""
    page("discovery-kit.html", "Discovery Kit · The Archetypes: HER · ODIRAH",
         "All six ODIRAH fragrances in one Discovery Kit, so you can meet each archetype before choosing a full size.",
         body, current="discovery-kit.html", extra_end=sticky)


def build_shop():
    body = """
  <section class="mosaic" aria-labelledby="shop-title">
    <div class="panel title-panel">
      <h1 id="shop-title">Shop</h1>
      <div style="display:grid;gap:18px;justify-items:start">
        <p>Every fragrance and the Discovery Kit, with sizes up front. Prices will be shown at launch.</p>
        <div class="chips" role="group" aria-label="Filter products">
          <button type="button" class="chip" data-filter="all" aria-pressed="true">All <span>7</span></button>
          <button type="button" class="chip" data-filter="fragrance" aria-pressed="false">Fragrances <span>6</span></button>
          <button type="button" class="chip" data-filter="kit" aria-pressed="false">Discovery Kit <span>1</span></button>
        </div>
      </div>
    </div>
  </section>
  <section class="mosaic tiles four" aria-label="All products" data-tiles data-with-kit data-sizes="(max-width:600px) 60vw, (max-width:1060px) 30vw, 16vw"></section>
""" + KIT_SPLIT
    page("shop.html", "Shop · ODIRAH", "Shop all six fragrances from The Archetypes: HER and the Discovery Kit.",
         body, current="shop.html")


def build_house():
    lines = ["To the invisible self.",
             "To the many layers of the human experience, shaped by memory, instinct, desire, time and circumstance.",
             "To the worlds we carry within us.",
             "Some are quiet. Some hold fire. Some are softly lit.",
             "Some remain closed until we are ready to enter them again.",
             "We are ever-changing. We do not belong to one narrative.",
             "We move through time without losing the essence of who we are.",
             "Within us lives a strength that can be fierce, unyielding and certain, yet fluid enough to move freely through the world.",
             "Not to perform. Not to play a role. But to feel fully alive.",
             "ODIRAH exists as a house for those worlds.",
             "Each fragrance is not a character to become, but a passage into a world already within you."]
    lines_html = "".join(f'<span class="reveal">{e(l)}</span>' for l in lines)
    body = f"""
  <section class="mosaic split" aria-labelledby="house-title">
    <figure class="panel media tall" style="margin:0">{img("{B}", "mirror-monolith", "A woman in white stands before a tall mirror in a red rock desert, her reflection looking back.", "(max-width:860px) 100vw, 66vw", lazy=False)}</figure>
    <div class="panel text-panel">
      <h1 id="house-title" style="font-size:clamp(2.8rem,1.8rem + 3.4vw,5rem)">A mirror of the self</h1>
      <div class="reveal" style="display:grid;gap:22px">
        <p style="font-style:italic;font-size:clamp(1.3rem,1.1rem + .8vw,1.8rem);line-height:1.35">To create a fragrance collection that transcends trends and becomes a mirror of the self.</p>
        <p class="dense">ODIRAH is an artistic exploration of the human inner world: memory, intimacy, desire and mystery, translated into scent. Fragrance here is not an accessory. It is a way to explore the worlds within us.</p>
      </div>
    </div>
  </section>

  <section class="mosaic three" aria-label="What ODIRAH stands for">
    <div class="panel"><span class="label corner">1</span><div><h3>Mirror of the soul</h3><p>Our fragrances give expression to feelings and experiences that are deeply personal.</p></div></div>
    <div class="panel"><span class="label corner">2</span><div><h3>Inner archetypes</h3><p>Each scent explores a different part of our inner world, allowing several sides of ourselves to coexist.</p></div></div>
    <div class="panel"><span class="label corner">3</span><div><h3>Self-discovery</h3><p>Choosing a fragrance becomes a moment of recognition: finding something of yourself in a scent.</p></div></div>
  </section>

  <section class="mosaic" id="manifesto" aria-labelledby="man-title" style="scroll-margin-top:84px">
    <div class="panel manifesto-panel">
      <h2 id="man-title" class="reveal">Here’s to the unseen.</h2>
      <p class="lines">{lines_html}<span class="reveal last">You are not one version of yourself.</span></p>
    </div>
  </section>

  <section class="mosaic split" aria-label="Tagline">
    <figure class="panel media" style="margin:0"><img src="{{B}}assets/img/hero-desert-1280.webp" srcset="{{B}}assets/img/hero-desert-1280.webp 1280w, {{B}}assets/img/hero-desert-2400.webp 2400w" sizes="(max-width:860px) 100vw, 66vw" width="2400" height="1357" loading="lazy" decoding="async" alt="A woman wrapped in sand-coloured silk on a dune at dusk."></figure>
    <div class="panel tag-panel">
      <p class="big reveal">Intimately you<sup>TM</sup></p>
      <p class="sub reveal">“Intimately you” expresses the personal relationship between fragrance and identity: a promise to bring you closer to the many parts of yourself.</p>
      <p class="reveal" style="margin-top:24px"><a class="btn btn--light" href="{{B}}collection.html">Meet the six archetypes{ARROW}</a></p>
    </div>
  </section>
"""
    page("the-house.html", "The House · ODIRAH",
         "ODIRAH is a house of fragrance: an artistic exploration of the human inner world. Our vision, positioning and manifesto.",
         body, current="the-house.html")


def build_contact():
    body = f"""
  <section class="mosaic split rev" aria-labelledby="c-title">
    <div class="panel text-panel">
      <div>
        <h1 id="c-title" style="font-size:clamp(2.8rem,1.8rem + 3.4vw,5rem)">Contact</h1>
        <p style="margin-top:18px;max-width:24rem;color:var(--brown)">For questions about the fragrances, an order or the house, write to us. We reply within two working days.</p>
      </div>
      <div class="copy-line"><span>office@odirah.com</span><button type="button" data-copy="office@odirah.com">Copy</button></div>
    </div>
    <div class="panel text-panel" style="justify-content:flex-start">
      <form class="form" data-contact novalidate>
        <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" autocomplete="name"></div>
        <div class="field"><label for="c-email">Email</label><input id="c-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field"><label for="c-topic">Topic</label><select id="c-topic" name="topic"><option>A fragrance</option><option>An order</option><option>The Discovery Kit</option><option>Press and partnerships</option><option>Something else</option></select></div>
        <div class="field"><label for="c-message">Message</label><textarea id="c-message" name="message" required></textarea></div>
        <div><button type="submit" class="btn btn--dark">Send message{ARROW}</button></div>
        <p class="msg" aria-live="polite" data-contact-msg></p>
      </form>
    </div>
  </section>

  <section class="mosaic three" id="help" aria-label="Help" style="scroll-margin-top:84px">
    <div class="panel"><div><h3>Shipping</h3><p>Delivery options, costs and times are shown at checkout once markets are confirmed.</p></div></div>
    <div class="panel"><div><h3>Returns</h3><p>Unopened bottles can be returned. The full returns policy will be published with the launch.</p></div></div>
    <div class="panel" id="legal" style="scroll-margin-top:84px"><div><h3>Legal</h3><p>Terms of sale, privacy policy and cookie policy will be published with the launch.</p></div></div>
  </section>
"""
    page("contact.html", "Contact · ODIRAH", "Contact the house of ODIRAH, with help on shipping, returns and legal information.",
         body, current=None)


def build_404():
    body = """
  <section class="mosaic" aria-labelledby="nf">
    <div class="panel lost">
      <h1 id="nf">This world is closed for now.</h1>
      <p style="color:var(--brown);max-width:28rem">The page you were looking for does not exist, or has moved. The six archetypes are still here.</p>
      <a class="btn btn--dark" href="{B}collection.html">Meet the archetypes</a>
    </div>
  </section>"""
    page("404.html", "Page not found · ODIRAH", "Page not found.", body)


if __name__ == "__main__":
    build_home()
    build_collection()
    for a in ARCH:
        build_fragrance(a)
    build_kit()
    build_shop()
    build_house()
    build_contact()
    build_404()
    for p in sorted(SITE.rglob("*.html")):
        print(p.relative_to(ROOT))
