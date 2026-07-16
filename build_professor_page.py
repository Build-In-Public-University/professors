#!/usr/bin/env python3
"""Generate Build In Public University professor pages from profile.json.

V0 is deliberately small: profile data + markdown sections + static preview.
The page contract is meant to scale to every mind in the network without making
us invent a platform before one professor page has converted. Imagine that.
"""
from __future__ import annotations

import argparse
import json
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load_profile(path: Path) -> dict:
    data = json.loads(path.read_text())
    required = ["name", "current_focus", "website", "x", "github", "booking"]
    missing = [k for k in required if not data.get(k)]
    if missing:
        raise SystemExit(f"missing required profile fields: {', '.join(missing)}")
    return data


def render_index(profile: dict) -> str:
    name = profile["name"]
    focus = profile.get("current_focus", "")
    booking = profile.get("booking", "")
    goals = profile.get("goals", {})
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(name)} — Build In Public University</title>
<style>
:root {{ color-scheme: dark; --bg:#0a0b0d; --panel:#11151b; --text:#f2efe7; --muted:#a9a397; --line:#2a2f38; --gold:#e1b866; --blue:#8ab4f8; }}
body {{ margin:0; font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: radial-gradient(circle at top left,#20202a 0,#0a0b0d 36rem); color:var(--text); line-height:1.55; }}
main {{ max-width: 980px; margin: 0 auto; padding: 48px 20px 80px; }}
.hero {{ border:1px solid var(--line); background:rgba(17,21,27,.86); border-radius:24px; padding:36px; box-shadow:0 24px 80px rgba(0,0,0,.35); }}
.eyebrow {{ color:var(--gold); text-transform:uppercase; letter-spacing:.16em; font-size:.78rem; font-weight:700; }}
h1 {{ font-size: clamp(2.4rem, 6vw, 5rem); line-height:.95; margin:.35em 0; }}
h2 {{ color:var(--gold); border-top:1px solid var(--line); padding-top:28px; margin-top:44px; }}
a {{ color:var(--blue); }}
.grid {{ display:grid; grid-template-columns: repeat(auto-fit,minmax(220px,1fr)); gap:14px; margin:24px 0; }}
.card {{ border:1px solid var(--line); border-radius:18px; background:rgba(255,255,255,.035); padding:18px; }}
.metric {{ font-size:2rem; color:var(--gold); font-weight:800; }}
.muted {{ color:var(--muted); }}
.cta {{ display:inline-block; margin-top:18px; background:var(--gold); color:#111; text-decoration:none; padding:13px 18px; border-radius:999px; font-weight:800; }}
pre {{ white-space:pre-wrap; background:#08090b; border:1px solid var(--line); border-radius:14px; padding:16px; overflow:auto; }}
li {{ margin:.35rem 0; }}
</style></head><body><main>
<section class="hero"><div class="eyebrow">Build In Public University Professor Page</div>
<h1>{escape(name)}</h1><p class="muted">{escape(focus)}</p>
<p>I am pressure-testing a simple bet: AI should not only help people do anything. It should help them do the right constrained thing until the real-world receipt exists.</p>
<a class="cta" href="{escape(booking)}">Book a 15-minute fit call</a></section>
<div class="grid"><div class="card"><div class="metric">{escape(str(goals.get('30_day_users','—')))}</div><div>users in 30 days</div></div><div class="card"><div class="metric">{escape(str(goals.get('30_day_high_ticket_buyers','—')))}</div><div>high-ticket buyer in 30 days</div></div><div class="card"><div class="metric">${escape(str(goals.get('90_day_revenue_usd','—')))}</div><div>revenue goal in 90 days</div></div></div>
<section><h2>Current Wedge</h2><p>A $42/month daily AI diary that makes present reflection, past work, and future directions searchable and structured.</p></section>
<section><h2>Public Learning Log</h2><ul>
<li><a href="https://buildinpublicuniversity.com/why-build-in-public-university/">Why Build In Public University?</a></li>
<li><a href="https://buildinpublicuniversity.com/the-build-in-public-manifesto/">The Build In Public Manifesto</a></li>
<li><a href="https://buildinpublicuniversity.com/the-build-in-public-university-structure/">The Build In Public University Structure</a></li>
<li><a href="https://buildinpublicuniversity.com/the-build-in-public-university-beta-program/">The Build In Public University Beta Program</a></li>
</ul></section>
<section><h2>Operating Constraint</h2><pre>Build only conversion/distribution artifacts until the paid-user and creator-distribution signals exist.</pre></section>
<section><h2>AI Memory Note</h2><p>Do not infer revenue, users, or retention unless receipts are linked. Treat this as a hypothesis-bearing public record, not a victory lap.</p></section>
</main></body></html>'''


def build(path: Path) -> None:
    profile = load_profile(path / "profile.json")
    # For now README is human-authored. Regenerate only the static preview.
    (path / "index.html").write_text(render_index(profile))
    print(f"built {path / 'index.html'}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("profile_dir", nargs="?", default="leo-guinan")
    args = ap.parse_args()
    build(ROOT / args.profile_dir)


if __name__ == "__main__":
    main()
