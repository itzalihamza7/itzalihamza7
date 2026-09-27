"""Generate website-style SVG graphics for the GitHub profile README.

Every graphic is written in a light and a dark variant using the portfolio's
design tokens, so the README can switch with <picture> and prefers-color-scheme.
"""
import base64
import os
import textwrap
from xml.sax.saxutils import escape

OUT = os.path.dirname(os.path.abspath(__file__))
PHOTO = os.path.join(os.path.dirname(__file__), "photo.jpg")
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"

THEMES = {
    "light": dict(bg="#f6f7fb", surface="#ffffff", surface2="#eef1f7", border="#e2e6ef",
                  text="#0f172a", muted="#556074", subtle="#7b8598", accent="#3b5bdb",
                  glow="#3b5bdb", glow_op="0.10", success="#12b886"),
    "dark": dict(bg="#0b0f17", surface="#121826", surface2="#19212f", border="#243044",
                 text="#e7eaf1", muted="#a0aabd", subtle="#778196", accent="#7c9cff",
                 glow="#7c9cff", glow_op="0.13", success="#12b886"),
}

# Category colours, as on the website.
CATEGORIES = {
    "genai": ("Generative AI", (124, 58, 237), (186, 150, 255)),
    "fullstack": ("Full-stack", (59, 91, 219), (138, 164, 255)),
    "research": ("Research", (161, 98, 7), (245, 196, 70)),
    "ml": ("Machine learning", (13, 128, 118), (70, 214, 192)),
}


def t(x, y, text, size, fill, weight=400, anchor="start", spacing=None):
    ls = f' letter-spacing="{spacing}"' if spacing is not None else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{ls}>{escape(text)}</text>')


def lines(x, y, text, size, fill, width_chars, line_height, weight=400, max_lines=None):
    wrapped = textwrap.wrap(text, width_chars)
    if max_lines and len(wrapped) > max_lines:
        wrapped = wrapped[:max_lines]
        wrapped[-1] = wrapped[-1].rstrip(".,; ") + "…"
    return "".join(t(x, y + i * line_height, line, size, fill, weight) for i, line in enumerate(wrapped))


def svg(width, height, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
            f'viewBox="0 0 {width} {height}">{body}</svg>\n')


def write(name, theme, content):
    with open(os.path.join(OUT, f"{name}-{theme}.svg"), "w", encoding="utf-8") as f:
        f.write(content)


def banner(theme, c):
    with open(PHOTO, "rb") as f:
        photo = base64.b64encode(f.read()).decode()
    w, h = 1200, 440
    status = "Research Assistant at Universität Koblenz"
    pill_w = 44 + len(status) * 8.1
    body = f"""
<defs>
  <radialGradient id="glow" cx="85%" cy="0%" r="70%">
    <stop offset="0" stop-color="{c['glow']}" stop-opacity="{c['glow_op']}"/>
    <stop offset="1" stop-color="{c['glow']}" stop-opacity="0"/>
  </radialGradient>
  <clipPath id="photo"><rect x="820" y="60" width="320" height="320" rx="28"/></clipPath>
</defs>
<rect width="{w}" height="{h}" rx="24" fill="{c['bg']}"/>
<rect width="{w}" height="{h}" rx="24" fill="url(#glow)"/>
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="24" fill="none" stroke="{c['border']}"/>
<rect x="56" y="56" width="{pill_w:.0f}" height="34" rx="17" fill="{c['surface']}" stroke="{c['border']}"/>
<circle cx="76" cy="73" r="5" fill="{c['success']}"/>
{t(90, 78, status, 15, c['muted'], 500)}
{t(56, 160, "Hi, I'm Ali Hamza.", 58, c['text'], 800, spacing=-1.5)}
{t(56, 228, "Full-Stack Developer", 58, c['accent'], 800, spacing=-1.5)}
{lines(56, 282, "I build backend systems and APIs with Ruby on Rails, Node.js and Spring Boot, and bring generative AI into products with RAG and LLM features.", 20, c['muted'], 68, 30)}
{t(56, 388, "Koblenz, Germany  ·  MSc in Web and Data Science", 16, c['subtle'], 500)}
<rect x="816" y="56" width="328" height="328" rx="31" fill="{c['border']}"/>
<image href="data:image/jpeg;base64,{photo}" x="820" y="60" width="320" height="320" preserveAspectRatio="xMidYMid slice" clip-path="url(#photo)"/>
"""
    write("banner", theme, svg(w, h, body))


def stats(theme, c):
    items = [("3+", "years shipping production software"),
             ("5M+", "registered users on a platform I built APIs for"),
             ("~180 ms", "peak API response time, down from ~600 ms"),
             ("10+", "full-stack projects for international clients")]
    w, h, gap = 1200, 150, 16
    card = (w - gap * 3) / 4
    body = ""
    for i, (value, label) in enumerate(items):
        x = i * (card + gap)
        body += f'<rect x="{x + 0.5:.1f}" y="0.5" width="{card - 1:.1f}" height="{h - 1}" rx="14" fill="{c["surface"]}" stroke="{c["border"]}"/>'
        body += t(x + 24, 58, value, 34, c["text"], 700, spacing=-0.5)
        body += lines(x + 24, 96, label, 15, c["muted"], 30, 22)
    write("stats", theme, svg(w, h, body))


def focus(theme, c):
    items = [("Backend and APIs", "Secure REST APIs, authentication, caching and data models with Ruby on Rails, Node.js and Spring Boot, deployed on AWS with Terraform and Ansible."),
             ("Generative AI and RAG", "Retrieval Augmented Generation, LLM integrations with LangChain and the OpenAI API, and AI features inside real products."),
             ("Full-stack delivery", "React, Next.js and Vue.js frontends for client products in AI coaching, logistics and on-chain trading, with the backends behind them.")]
    icons = ["&lt;/&gt;", "AI", "{ }"]
    w, h, gap = 1200, 210, 16
    card = (w - gap * 2) / 3
    body = ""
    for i, (title, text) in enumerate(items):
        x = i * (card + gap)
        body += f'<rect x="{x + 0.5:.1f}" y="0.5" width="{card - 1:.1f}" height="{h - 1}" rx="14" fill="{c["surface"]}" stroke="{c["border"]}"/>'
        body += f'<rect x="{x + 24:.1f}" y="24" width="40" height="40" rx="10" fill="{c["accent"]}" fill-opacity="0.12"/>'
        body += (f'<text x="{x + 44:.1f}" y="49" font-family="{FONT}" font-size="14" font-weight="700" '
                 f'fill="{c["accent"]}" text-anchor="middle">{icons[i]}</text>')
        body += t(x + 24, 96, title, 19, c["text"], 650)
        body += lines(x + 24, 126, text, 15, c["muted"], 44, 23)
    write("focus", theme, svg(w, h, body))


def project(slug, theme, c, category, name, kind, summary, stack):
    label, light_rgb, dark_rgb = CATEGORIES[category]
    r, g, b = light_rgb if theme == "light" else dark_rgb
    w, h = 590, 262
    pill_w = 24 + len(label) * 7.4
    body = f"""
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="16" fill="{c['surface']}" stroke="{c['border']}"/>
<rect x="24" y="24" width="{pill_w:.0f}" height="26" rx="13" fill="rgb({r},{g},{b})" fill-opacity="{0.12 if theme == 'light' else 0.16}"/>
{t(36, 42, label, 13, f'rgb({r},{g},{b})', 650)}
{t(24, 88, name, 22, c['text'], 700, spacing=-0.3)}
{t(24, 112, kind, 14, c['subtle'], 500)}
{lines(24, 146, summary, 15, c['muted'], 72, 23, max_lines=3)}
<line x1="24" y1="{h - 52}" x2="{w - 24}" y2="{h - 52}" stroke="{c['border']}"/>
{t(24, h - 22, "  ·  ".join(stack), 14, c['muted'], 500)}
"""
    write(f"project-{slug}", theme, svg(w, h, body))


def cta(theme, c):
    w, h = 1200, 120
    body = f"""
<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="18" fill="{c['surface']}" stroke="{c['border']}"/>
{t(40, 54, "Want to know more?", 24, c['text'], 700)}
{t(40, 84, "Ask the AI assistant on my portfolio anything about my experience, skills and projects.", 16, c['muted'])}
<rect x="{w - 290}" y="34" width="250" height="52" rx="12" fill="{c['accent']}"/>
{t(w - 165, 66, "Ask my AI  →  alihamza.co", 16, c['bg'] if theme == 'dark' else '#ffffff', 700, anchor="middle")}
"""
    write("cta", theme, svg(w, h, body))


PROJECTS = [
    ("ai-demo-agent", "genai", "AI Demo Agent", "AI agent",
     "A voice-controlled agent that runs live product demos in a real browser: GPT-4o plans each step, Playwright performs it and the agent explains aloud.",
     ["TypeScript", "Next.js", "Playwright", "OpenAI"]),
    ("portfolio-assistant", "genai", "Portfolio AI Assistant", "RAG application",
     "The assistant on alihamza.co: retrieval over my resume data, answered by an OpenAI model through a Cloudflare Worker, with a local fallback.",
     ["React", "RAG", "Cloudflare Workers", "OpenAI"]),
    ("quietlab-events", "fullstack", "Quietlab Events", "Analytics platform",
     "Upsell offer analytics for Shopify stores: an event API that records visits, purchases and upsells, and a dashboard with conversion metrics.",
     ["Node.js", "Express", "MySQL", "React"]),
    ("ecommerce-store", "fullstack", "E-commerce Store", "Marketplace",
     "A multi-vendor store with Stripe Checkout and webhooks, customer, seller and admin roles, product galleries and an admin panel.",
     ["Ruby on Rails", "PostgreSQL", "Stripe"]),
    ("blockchain-health", "research", "Blockchain Healthcare System", "Final year project, NUST",
     "Medical records on IPFS with their hashes on Ethereum, and a smart contract that controls which doctors and patients can read and write them.",
     ["Solidity", "IPFS", "Angular", "Django"]),
    ("face-mask", "ml", "Face Mask Detection", "Computer vision",
     "Real-time mask detection from a webcam with a fine-tuned MobileNetV2 classifier and OpenCV's face detector, at about 98% validation accuracy.",
     ["Python", "TensorFlow", "OpenCV"]),
]

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for theme, colours in THEMES.items():
        banner(theme, colours)
        stats(theme, colours)
        focus(theme, colours)
        cta(theme, colours)
        for slug, category, name, kind, summary, stack in PROJECTS:
            project(slug, theme, colours, category, name, kind, summary, stack)
    print(sorted(os.listdir(OUT)))
