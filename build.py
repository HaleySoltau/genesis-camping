#!/usr/bin/env python3
"""
Genesis Family Camping — site builder.

Usage:
    python3 build.py

Reads data/trips.json and regenerates:
    - index.html            (homepage, with a card per trip)
    - trips/<slug>.html     (one detail page per trip)

Run this after editing data/trips.json, then commit + push.
Photos: drop an image at assets/images/trips/<slug>.jpg and set
"photo": "assets/images/trips/<slug>.jpg" in trips.json for that trip.
"""
import json
import os
from datetime import date

ROOT = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(ROOT, "data", "trips.json")) as f:
    DATA = json.load(f)

TRIPS = DATA["trips"]

TODAY = date.today()

def trip_date(t):
    y, m, d = (int(x) for x in t["date_iso"].split("-"))
    return date(y, m, d)

# Trips still on the calendar, soonest first. A trip "falls off" the
# homepage timeline automatically once its date has passed — no manual
# cleanup needed, just leave it in trips.json (its detail page still exists
# for anyone who has the link, e.g. from a past newsletter).
UPCOMING_TRIPS = sorted(
    (t for t in TRIPS if trip_date(t) >= TODAY),
    key=trip_date,
)

STYLE = """
:root{
  --blue:#2bc3f7; --blue-deep:#0b9cd1; --blue-pale:#e7f8ff;
  --ink:#1a1a1a; --ink-soft:#4a4a4a; --paper:#ffffff; --paper-2:#f4f8fa;
  --line:rgba(26,26,26,0.1);
}
*{box-sizing:border-box;}
html{scroll-behavior:smooth;}
body{margin:0; background:var(--paper); color:var(--ink); font-family:'Work Sans', sans-serif; font-size:16px; line-height:1.6;}
h1,h2,h3,.display{font-family:'Fraunces', serif; font-weight:600; letter-spacing:-0.01em; color:var(--ink); margin:0;}
.eyebrow{font-family:'JetBrains Mono', monospace; text-transform:uppercase; letter-spacing:0.14em; font-size:0.72rem; color:var(--blue-deep); font-weight:500;}
a{color:inherit;}
img{max-width:100%; display:block;}
.wrap{max-width:1080px; margin:0 auto; padding:0 28px;}
.photo{width:100%; height:100%; object-fit:cover; display:block;}
.photo-slot{background:var(--paper-2); border:1px dashed rgba(26,26,26,0.25); display:flex; align-items:center; justify-content:center; color:rgba(26,26,26,0.4); font-family:'JetBrains Mono', monospace; font-size:0.72rem; text-align:center; padding:12px; overflow:hidden;}

nav{position:sticky; top:0; z-index:50; background:rgba(255,255,255,0.92); backdrop-filter:blur(6px); border-bottom:1px solid var(--line);}
.nav-inner{max-width:1080px; margin:0 auto; padding:14px 28px; display:flex; align-items:center; justify-content:space-between; flex-wrap:wrap; gap:12px;}
.brand{display:flex; align-items:center; gap:10px; text-decoration:none;}
.brand img{height:34px; width:auto;}
.brand-text{font-family:'Fraunces', serif; font-weight:700; font-size:1.05rem; color:var(--ink); letter-spacing:-0.01em;}
.nav-links{display:flex; gap:26px; list-style:none; margin:0; padding:0; flex-wrap:wrap;}
.nav-links a{text-decoration:none; font-size:0.88rem; font-weight:500; color:var(--ink-soft); padding:6px 0; border-bottom:2px solid transparent; transition:border-color 0.2s, color 0.2s;}
.nav-links a:hover{border-color:var(--blue); color:var(--ink);}

.hero{position:relative; overflow:hidden;}
.hero-media{position:relative; height:78vh; min-height:460px; max-height:720px; background:linear-gradient(160deg, var(--ink) 0%, #2a2a2a 100%);}
.hero-media .photo-slot{position:absolute; inset:0;}
.hero-media::after{content:""; position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.15) 0%, rgba(0,0,0,0.55) 100%);}
.hero-copy{position:absolute; left:0; right:0; bottom:0; z-index:2; padding:56px 28px; max-width:1080px; margin:0 auto;}
.hero-copy .eyebrow{color:var(--blue);}
.hero-copy h1{color:#fff; font-size:clamp(2.4rem, 5.6vw, 4rem); line-height:1.02; max-width:760px; margin-top:12px;}
.hero-copy p.lede{color:rgba(255,255,255,0.82); max-width:520px; margin-top:18px; font-size:1.05rem;}
.hero-cta{display:flex; gap:14px; margin-top:30px; flex-wrap:wrap;}

.trip-hero-media{position:relative; height:52vh; min-height:340px; max-height:520px; background:linear-gradient(160deg, var(--ink) 0%, #2a2a2a 100%);}
.trip-hero-media .photo-slot{position:absolute; inset:0;}
.trip-hero-media::after{content:""; position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,0.1) 0%, rgba(0,0,0,0.6) 100%);}
.crumb{position:absolute; top:24px; left:0; right:0; z-index:3;}
.crumb a{font-family:'JetBrains Mono', monospace; font-size:0.76rem; text-transform:uppercase; letter-spacing:0.06em; color:rgba(255,255,255,0.85); text-decoration:none;}
.crumb a:hover{color:var(--blue);}

.btn{display:inline-block; padding:13px 26px; border-radius:2px; font-family:'JetBrains Mono', monospace; font-size:0.78rem; text-transform:uppercase; letter-spacing:0.08em; font-weight:500; text-decoration:none; transition:transform 0.15s, background 0.15s, color 0.15s; border:1px solid transparent;}
.btn-primary{background:var(--blue); color:var(--ink);}
.btn-primary:hover{background:var(--blue-deep); color:#fff; transform:translateY(-1px);}
.btn-ghost{border-color:#fff; color:#fff;}
.btn-ghost:hover{background:#fff; color:var(--ink);}

section{padding:88px 0;}
.section-head{max-width:620px; margin-bottom:52px;}
.section-head h2{font-size:clamp(1.8rem, 3.4vw, 2.5rem); margin-top:10px;}
.section-head p{color:var(--ink-soft); margin-top:14px; font-size:1.02rem;}

.about{background:var(--paper-2); border-top:1px solid var(--line); border-bottom:1px solid var(--line);}
.about-grid{display:grid; grid-template-columns:0.9fr 1.3fr; gap:56px; align-items:start;}
.host-photo{aspect-ratio:4/5; border-radius:3px; overflow:hidden;}
.host-label{margin-top:16px;}
.host-label .name{font-family:'Fraunces', serif; font-weight:600; font-size:1.2rem;}
.host-label .role{font-family:'JetBrains Mono', monospace; font-size:0.7rem; text-transform:uppercase; letter-spacing:0.1em; color:var(--blue-deep); margin-top:2px;}
.about-copy p{margin:0 0 18px;}
.pull{font-family:'Fraunces', serif; font-style:italic; font-size:1.2rem; color:var(--ink); border-left:3px solid var(--blue); padding-left:20px; margin:26px 0;}

.trail-wrap{position:relative;}
.trail-line{position:absolute; left:24px; top:14px; bottom:14px; width:2px; background:repeating-linear-gradient(to bottom, var(--blue) 0 6px, transparent 6px 12px);}
@media(min-width:760px){ .trail-line{left:50%; transform:translateX(-1px);} }
.trip{position:relative; padding-left:64px; margin-bottom:44px;}
@media(min-width:760px){
  .trip{display:grid; grid-template-columns:1fr 1fr; gap:48px; align-items:center; padding-left:0;}
  .trip:nth-child(even) .trip-card{grid-column:2;}
  .trip:nth-child(even) .trip-date{grid-column:1; text-align:right;}
  .trip:nth-child(odd) .trip-card{grid-column:1;}
  .trip:nth-child(odd) .trip-date{grid-column:2;}
}
.trip-marker{position:absolute; left:16px; top:6px; width:18px; height:18px; border-radius:50%; background:var(--blue); border:3px solid var(--paper); box-shadow:0 0 0 2px var(--ink);}
@media(min-width:760px){ .trip-marker{left:50%; transform:translateX(-9px); top:calc(50% - 9px);} }
.trip-date{font-family:'JetBrains Mono', monospace; color:var(--ink-soft); font-size:0.85rem; margin-bottom:8px;}
@media(min-width:760px){ .trip-date{margin-bottom:0; align-self:center;} }
.trip-card{background:var(--paper); border:1px solid var(--line); border-radius:3px; overflow:hidden;}
.trip-card .trip-photo{aspect-ratio:16/9;}
.trip-card .trip-body{padding:22px 24px;}
.trip-card h3{font-size:1.3rem;}
.trip-card p{color:var(--ink-soft); margin:10px 0 16px; font-size:0.95rem;}
.trip-card a.detail-link{font-family:'JetBrains Mono', monospace; font-size:0.76rem; text-transform:uppercase; letter-spacing:0.06em; color:var(--blue-deep); text-decoration:none; font-weight:500;}
.trip-card a.detail-link:hover{text-decoration:underline;}

.individual{background:var(--ink); color:var(--paper);}
.individual .section-head h2{color:var(--paper);}
.individual .section-head p{color:rgba(255,255,255,0.65);}
.ind-grid{display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:24px;}
.ind-card{background:rgba(255,255,255,0.05); border:1px solid rgba(255,255,255,0.14); padding:26px; border-radius:3px;}
.ind-card .eyebrow{color:var(--blue);}
.ind-card h3{color:var(--paper); font-size:1.2rem; margin-top:10px;}
.ind-card p{color:rgba(255,255,255,0.62); font-size:0.94rem; margin:12px 0 18px;}
.ind-card a.btn{padding:11px 20px;}

.issue-featured{background:var(--paper-2); border:1px solid var(--line); border-radius:3px; padding:36px; margin-bottom:36px;}
.issue-featured h3{font-size:1.6rem; margin-top:10px;}
.issue-featured p{color:var(--ink); margin-top:14px; max-width:640px;}
.issue-list{list-style:none; margin:0; padding:0; border-top:1px solid var(--line);}
.issue-list li{display:flex; justify-content:space-between; align-items:baseline; padding:16px 0; border-bottom:1px solid var(--line); gap:16px; flex-wrap:wrap;}
.issue-list .issue-name{font-family:'Fraunces', serif; font-size:1.05rem;}
.issue-list .issue-tag{font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:var(--ink-soft); text-transform:uppercase; letter-spacing:0.06em;}

footer{background:var(--paper-2); color:var(--ink); padding:64px 0 40px; border-top:1px solid var(--line);}
.footer-top{display:flex; align-items:center; gap:12px; margin-bottom:36px;}
.footer-top img{height:30px; width:auto;}
.footer-grid{display:grid; grid-template-columns:1.2fr 1fr 1fr; gap:40px; margin-bottom:48px;}
footer h4{font-family:'JetBrains Mono', monospace; text-transform:uppercase; letter-spacing:0.1em; font-size:0.74rem; color:var(--blue-deep); margin-bottom:16px;}
footer p{color:var(--ink-soft); max-width:320px; font-size:0.94rem;}
footer ul{list-style:none; margin:0; padding:0;}
footer li{margin-bottom:10px;}
footer a{color:var(--ink-soft); text-decoration:none; font-size:0.92rem;}
footer a:hover{color:var(--blue-deep);}
.footer-bottom{border-top:1px solid var(--line); padding-top:24px; font-family:'JetBrains Mono', monospace; font-size:0.72rem; color:rgba(26,26,26,0.5); display:flex; justify-content:space-between; flex-wrap:wrap; gap:10px;}

.detail-grid{display:grid; grid-template-columns:1.4fr 0.9fr; gap:56px; align-items:start;}
.detail-copy p{margin:0 0 18px;}
.fact-card{background:var(--paper-2); border:1px solid var(--line); border-radius:3px; padding:28px;}
.fact-card h3{font-size:1.05rem; margin-bottom:18px;}
.fact-list{list-style:none; margin:0 0 24px; padding:0;}
.fact-list li{display:flex; justify-content:space-between; gap:12px; padding:10px 0; border-bottom:1px solid var(--line); font-size:0.92rem;}
.fact-list li:last-child{border-bottom:none;}
.fact-list .k{color:var(--ink-soft); font-family:'JetBrains Mono', monospace; font-size:0.72rem; text-transform:uppercase; letter-spacing:0.06em;}
.fact-list .v{text-align:right; font-weight:500;}
.note-box{background:var(--blue-pale); border:1px solid rgba(43,195,247,0.35); border-radius:3px; padding:18px 20px; font-size:0.9rem; color:var(--ink); margin-top:22px;}

@media(max-width:760px){
  .about-grid{grid-template-columns:1fr;}
  .footer-grid{grid-template-columns:1fr; gap:32px;}
  .detail-grid{grid-template-columns:1fr;}
}
"""

def head(title, depth=0):
    # depth=0 for pages at root, depth=1 for pages in /trips
    prefix = "../" if depth else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<link rel="icon" type="image/png" href="{prefix}assets/images/icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600;9..144,700&family=Work+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>{STYLE}</style>
</head>
<body>
"""

def nav(depth=0):
    prefix = "../" if depth else ""
    return f"""
<nav>
  <div class="nav-inner">
    <a class="brand" href="{prefix}index.html">
      <img src="{prefix}assets/images/icon.png" alt="Genesis Family Camping icon">
      <span class="brand-text">Genesis Family Camping</span>
    </a>
    <ul class="nav-links">
      <li><a href="{prefix}index.html#hosts">About</a></li>
      <li><a href="{prefix}index.html#trips">Group Trips</a></li>
      <li><a href="{prefix}index.html#individual">Individual Trips</a></li>
      <li><a href="{prefix}index.html#chronicles">Campfire Chronicles</a></li>
      <li><a href="{prefix}index.html#links">Links</a></li>
    </ul>
  </div>
</nav>
"""

def footer(depth=0):
    prefix = "../" if depth else ""
    return f"""
<footer id="links">
  <div class="wrap">
    <div class="footer-top">
      <img src="{prefix}assets/images/icon.png" alt="Genesis Family Camping icon">
      <span class="brand-text">Genesis Family Camping</span>
    </div>
    <div class="footer-grid">
      <div>
        <h4>About</h4>
        <p>A Genesis Church Orlando family group built on fellowship, the outdoors, and the occasional bioluminescent paddle board.</p>
      </div>
      <div>
        <h4>Get Involved</h4>
        <ul>
          <li><a href="https://forms.gle/m2KCsUUN74c58sTM6">Ideas &amp; Suggestions</a></li>
          <li><a href="https://forms.gle/ni3sjWrQRgKLFWsHA">Share Your Own Trip</a></li>
          <li><a href="https://genesischurchorlando.churchcenter.com/groups/adult-groups/family-camping">Join the Group</a></li>
        </ul>
      </div>
      <div>
        <h4>Explore</h4>
        <ul>
          <li><a href="https://genesis-camping.square.site/">Book a Trip (Shop)</a></li>
          <li><a href="{prefix}index.html#trips">Group Trips</a></li>
          <li><a href="{prefix}index.html#chronicles">Campfire Chronicles</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>Genesis Family Camping Group</span>
      <span>Creating memories one campsite at a time</span>
    </div>
  </div>
</footer>
</body>
</html>
"""

def trip_card_html(t):
    if t.get("photo"):
        media = f'<img class="photo" src="{t["photo"]}" alt="{t["name"]}">'
    else:
        media = f'<div class="photo-slot">PHOTO: {t["name"]}</div>'
    return f"""
      <div class="trip">
        <div class="trip-marker"></div>
        <div class="trip-date">{t['date_display']}</div>
        <div class="trip-card">
          <div class="trip-photo">{media}</div>
          <div class="trip-body">
            <h3>{t['name']}</h3>
            <p>{t['card_teaser']}</p>
            <a class="detail-link" href="trips/{t['slug']}.html">Get the details &rarr;</a>
          </div>
        </div>
      </div>"""

def build_index():
    if UPCOMING_TRIPS:
        trip_cards = "\n".join(trip_card_html(t) for t in UPCOMING_TRIPS)
    else:
        trip_cards = """
      <div style="padding:40px 0; color:var(--ink-soft); font-family:'JetBrains Mono', monospace; font-size:0.9rem;">
        Nothing on the calendar yet &mdash; check back soon, or suggest a trip below.
      </div>"""
    html = head("Genesis Family Camping") + nav() + f"""
<header class="hero" id="top">
  <div class="hero-media">
    <img class="photo" src="assets/images/hero.jpg" alt="Group gathered around the campfire" style="position:absolute; inset:0; object-position:50% 40%;">
    <div class="hero-copy">
      <p class="eyebrow">Genesis Church Orlando &middot; Family Camping Group</p>
      <h1>Fellowship, unplugged<br>and under the stars.</h1>
      <p class="lede">A group for anyone who wants to camp &mdash; solo campers, families of five with two dogs and a parrot, first-timers, and lifers. No sermons required, just good company and God's creation.</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="#trips">See upcoming trips</a>
        <a class="btn btn-ghost" href="https://genesischurchorlando.churchcenter.com/groups/adult-groups/family-camping">Join the group</a>
      </div>
    </div>
  </div>
</header>

<section class="about" id="hosts">
  <div class="wrap about-grid">
    <div>
      <div class="host-photo">
        <img class="photo" src="assets/images/host.jpg" alt="Haley and Evan Soltau" style="object-position:28% 35%;">
      </div>
      <div class="host-label">
        <div class="name">Haley &amp; Evan Soltau</div>
        <div class="role">Group Leaders</div>
      </div>
    </div>
    <div class="about-copy">
      <p class="eyebrow" style="margin-bottom:10px;">How it started</p>
      <h2 style="margin-bottom:18px;">Meet your hosts</h2>
      <p>My name is Haley Soltau, and my family has been with Genesis Church since the theater. While my husband doesn't camp, my son Evan and I love it. In 2024, I mentioned how I kept trying to camp at Jetty Park for beach baptisms, but it's always full. A friend I'd assumed wasn't into camping told me she'd love that too.</p>
      <p class="pull">"It's easy to make assumptions about who likes camping and who doesn't."</p>
      <p>So I talked with the pastors, and the Genesis Family Camping Group was born. Anyone is welcome &mdash; solo campers, families of five with two dogs and a parrot, seasoned campers, or someone trying it for the very first time.</p>
      <p>The purpose of this group is fellowship. There's something about camping together that brings people closer &mdash; a chance to unwind, talk, laugh, and eat. We won't have sermons at our events, but we encourage you to bring a devotional and dive deeper into His word while enjoying the world He created. When it's all over, you'll smile at the memories, because you simply had to be there.</p>
    </div>
  </div>
</section>

<section id="trips">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The route ahead</p>
      <h2>Upcoming group trips</h2>
      <p>You book your own site, then let us know which one you picked so we can add you to the group camping map.</p>
    </div>
    <div class="trail-wrap">
      <div class="trail-line"></div>
      {trip_cards}
    </div>
  </div>
</section>

<section class="individual" id="individual">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow" style="color:var(--blue);">Off the group calendar</p>
      <h2>Camping on your own time</h2>
      <p>Our members go camping all the time, and you don't have to wait for us to plan a trip to invite others along.</p>
    </div>
    <div class="ind-grid">
      <div class="ind-card">
        <p class="eyebrow">Browse</p>
        <h3>Upcoming individual trips</h3>
        <p>See what fellow campers already have booked, and find out how to join them.</p>
        <a class="btn btn-primary" href="https://docs.google.com/spreadsheets/d/e/2PACX-1vQ3CcSuv5lb9NlyxqQLfoCaz0OwNPtjZW8VwN6ZPobMOcGuw6vDpksIfjVOZIMbCPS77aehIfUQEnmm/pubhtml?gid=744332280&single=true">View trips</a>
      </div>
      <div class="ind-card">
        <p class="eyebrow">Contribute</p>
        <h3>Share your own trip</h3>
        <p>Got a trip booked already? Let the group know so others can tag along or send well-wishes.</p>
        <a class="btn btn-primary" href="https://forms.gle/ni3sjWrQRgKLFWsHA">Share a trip</a>
      </div>
      <div class="ind-card">
        <p class="eyebrow">Suggest</p>
        <h3>Ideas &amp; suggestions</h3>
        <p>Found a hidden-gem campground or a great day trip idea? Your recommendations shape what we plan next.</p>
        <a class="btn btn-primary" href="https://forms.gle/m2KCsUUN74c58sTM6">Submit an idea</a>
      </div>
    </div>
  </div>
</section>

<section class="chronicles" id="chronicles">
  <div class="wrap">
    <div class="section-head">
      <p class="eyebrow">The newsletter</p>
      <h2>Campfire Chronicles</h2>
      <p>The monthly update on where we're headed next and what the group's been up to.</p>
    </div>

    <div class="issue-featured">
      <p class="eyebrow">Latest issue &middot; November 2025</p>
      <h3>We are back!!!</h3>
      <p>Between flooded campgrounds, mission trips, and an epidemic of gallbladder removals&hellip; we're officially back, kicking things off with two new trips and a third in the works: Moss Park in December, Wickham Park in March, and Jetty Park returning in May.</p>
    </div>

    <ul class="issue-list">
      <li><span class="issue-name">October 2025</span><span class="issue-tag">Manatee Hammock &mdash; cancelled (flooding)</span></li>
      <li><span class="issue-name">August 2025</span><span class="issue-tag">Manatee Hammock trip announced</span></li>
      <li><span class="issue-name">July 2025</span><span class="issue-tag">The website launches</span></li>
      <li><span class="issue-name">June 2025</span><span class="issue-tag">Recap: Moss Park &amp; Jetty Park</span></li>
    </ul>
  </div>
</section>
""" + footer()

    with open(os.path.join(ROOT, "index.html"), "w") as f:
        f.write(html)
    print("wrote index.html")


def build_trip_page(t):
    if t.get("photo"):
        media = f'<img class="photo" src="../{t["photo"]}" alt="{t["name"]}" style="position:absolute; inset:0;">'
    else:
        media = f'<div class="photo-slot">PHOTO: {t["name"]}</div>'
    paras = "\n      ".join(f"<p>{p}</p>" for p in t["body_paragraphs"])
    fact_rows = "\n        ".join(
        f'<li><span class="k">{k}</span><span class="v">{v}</span></li>' for k, v in t["facts"]
    )
    html = head(f"{t['name']} — Genesis Family Camping", depth=1) + nav(depth=1) + f"""
<header class="hero">
  <div class="trip-hero-media">
    {media}
    <div class="crumb"><div class="wrap"><a href="../index.html#trips">&larr; Back to all trips</a></div></div>
    <div class="hero-copy" style="max-width:1080px; margin:0 auto;">
      <p class="eyebrow">{t['eyebrow']}</p>
      <h1 style="font-size:clamp(2.2rem, 5vw, 3.4rem);">{t['name']}</h1>
      <p class="lede">{t['intro']}</p>
      <div class="hero-cta">
        <a class="btn btn-primary" href="{t['reserve_url']}">{t['reserve_label']}</a>
        <a class="btn btn-ghost" href="../index.html#individual">Share your site number</a>
      </div>
    </div>
  </div>
</header>

<section>
  <div class="wrap detail-grid">
    <div class="detail-copy">
      <p class="eyebrow" style="margin-bottom:10px;">Trip details</p>
      <h2 style="margin-bottom:18px;">What to expect</h2>
      {paras}
    </div>
    <div class="fact-card">
      <h3>At a glance</h3>
      <ul class="fact-list">
        {fact_rows}
      </ul>
      <a class="btn btn-primary" style="width:100%; text-align:center;" href="{t['reserve_url']}">{t['reserve_label']}</a>
      <div class="note-box">{t['note']}</div>
    </div>
  </div>
</section>
""" + footer(depth=1)

    out_path = os.path.join(ROOT, "trips", f"{t['slug']}.html")
    with open(out_path, "w") as f:
        f.write(html)
    print("wrote trips/" + t["slug"] + ".html")


if __name__ == "__main__":
    build_index()
    for trip in TRIPS:
        build_trip_page(trip)
    print(f"\nDone. Built index.html + {len(TRIPS)} trip pages from data/trips.json.")
