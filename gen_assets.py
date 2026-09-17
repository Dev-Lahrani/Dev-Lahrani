#!/usr/bin/env python3
"""Generate CAD-blueprint style SVG assets for the Dev-Lahrani profile README."""
import math
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "Dev-Lahrani", "assets")
os.makedirs(OUT, exist_ok=True)

MONO = "ui-monospace,'JetBrains Mono',Menlo,Consolas,'Liberation Mono',monospace"

THEMES = {
    "light": dict(
        bg="#eef1ec", paper="#ffffff", ink="#15314a", ink2="#3f6178",
        ink3="#93a9b6", line="#15314a", accent="#ffb454", accent_ink="#15314a",
        grid="#15314a", soft_op="0.45",
    ),
    "dark": dict(
        bg="#0a2036", paper="#0e2c47", ink="#eaf4fb", ink2="#a8c8dd",
        ink3="#5e87a3", line="#66a9d6", accent="#ffb454", accent_ink="#0a2036",
        grid="#66a9d6", soft_op="0.45",
    ),
}


def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def grid_pattern(pid: str, t: dict) -> str:
    return (
        f'<pattern id="{pid}" width="30" height="30" patternUnits="userSpaceOnUse">'
        f'<path d="M30 0H0V30" fill="none" stroke="{t["grid"]}" stroke-opacity="0.10" stroke-width="1"/>'
        f"</pattern>"
    )


def cross(x: float, y: float, r: float, t: dict, sw: float = 1.4) -> str:
    return (
        f'<g stroke="{t["ink3"]}" stroke-width="{sw}" stroke-linecap="round">'
        f'<line x1="{x - r}" y1="{y}" x2="{x + r}" y2="{y}"/>'
        f'<line x1="{x}" y1="{y - r}" x2="{x}" y2="{y + r}"/></g>'
    )


def frame(w: float, h: float, t: dict, pid: str) -> str:
    return (
        f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>'
        f'<rect width="{w}" height="{h}" fill="url(#{pid})"/>'
        f'<rect x="8" y="8" width="{w - 16}" height="{h - 16}" fill="{t["paper"]}" stroke="{t["line"]}" stroke-width="2"/>'
        f'<rect x="14" y="14" width="{w - 28}" height="{h - 28}" fill="none" stroke="{t["line"]}" stroke-width="1" stroke-opacity="0.55"/>'
        + cross(8, 8, 7, t) + cross(w - 8, 8, 7, t)
        + cross(8, h - 8, 7, t) + cross(w - 8, h - 8, 7, t)
    )


def arrow_line(x1: float, x2: float, y: float, t: dict) -> str:
    """Horizontal dimension line with arrowheads on both ends."""
    d = 7
    return (
        f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{t["ink3"]}" stroke-width="1"/>'
        f'<path d="M{x1} {y} l{d} -3.5 v7 z" fill="{t["ink3"]}"/>'
        f'<path d="M{x2} {y} l-{d} -3.5 v7 z" fill="{t["ink3"]}"/>'
    )


# ---------------------------------------------------------------- banner
def banner(t: dict) -> str:
    w, h = 1200, 200
    tb_x, tb_y, tb_w, tb_h = 880, 30, 280, 140
    rows = [
        ("DWG NO.", "DL-2026-001"),
        ("SHEET", "1 / 1"),
        ("SCALE", "NTS &#183; REV 03"),
    ]
    body = frame(w, h, t, "bg")
    # left text block
    body += f'<text x="44" y="78" font-family="{MONO}" font-size="46" font-weight="700" letter-spacing="10" fill="{t["ink"]}">DEV LAHRANI</text>'
    body += f'<text x="46" y="108" font-family="{MONO}" font-size="16" letter-spacing="6" fill="{t["ink2"]}">CYBERSECURITY &amp; SYSTEMS</text>'
    body += f'<text x="46" y="130" font-family="{MONO}" font-size="11" letter-spacing="3" fill="{t["ink3"]}">B.TECH COMPUTER ENGINEERING &#183; VIT PUNE</text>'
    # status chip
    body += f'<rect x="44" y="144" width="222" height="26" rx="3" fill="{t["accent"]}"/>'
    body += f'<text x="155" y="161" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="2" fill="{t["accent_ink"]}" text-anchor="middle">&#9679; STATUS: OPERATIONAL</text>'
    # title block
    body += f'<rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="{tb_h}" fill="{t["paper"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
    body += f'<rect x="{tb_x}" y="{tb_y}" width="{tb_w}" height="30" fill="{t["line"]}"/>'
    body += f'<text x="{tb_x + 12}" y="{tb_y + 20}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="4" fill="{t["bg"]}">TITLE BLOCK</text>'
    rh = (tb_h - 30) / 3
    for i, (lab, val) in enumerate(rows):
        ry = tb_y + 30 + i * rh
        if i > 0:
            body += f'<line x1="{tb_x}" y1="{ry}" x2="{tb_x + tb_w}" y2="{ry}" stroke="{t["line"]}" stroke-opacity="0.5" stroke-width="1"/>'
        body += f'<text x="{tb_x + 12}" y="{ry + rh / 2 - 2}" font-family="{MONO}" font-size="9" letter-spacing="1.5" fill="{t["ink3"]}">{lab}</text>'
        body += f'<text x="{tb_x + 110}" y="{ry + rh / 2 + 8}" font-family="{MONO}" font-size="13" font-weight="700" fill="{t["ink"]}">{val}</text>'
    body += f'<line x1="{tb_x + 100}" y1="{tb_y + 30}" x2="{tb_x + 100}" y2="{tb_y + tb_h}" stroke="{t["line"]}" stroke-opacity="0.5" stroke-width="1"/>'
    # bottom dimension line
    body += arrow_line(44, 838, 180, t)
    body += f'<rect x="292" y="170" width="298" height="19" fill="{t["bg"]}"/>'
    body += f'<text x="441" y="183" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{t["ink3"]}" text-anchor="middle">FULL DRAWING SET &#183; 10 SHEETS &#183; NTS</text>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Dev Lahrani — cybersecurity and systems engineering drawing banner">'
        + f"<defs>{grid_pattern('bg', t)}</defs>" + body + "</svg>"
    )


# ---------------------------------------------------------------- status board
def status(t: dict) -> str:
    w, h = 1200, 232
    body = frame(w, h, t, "bg")
    body += f'<text x="36" y="46" font-family="{MONO}" font-size="13" font-weight="700" letter-spacing="5" fill="{t["ink2"]}">SYSTEM READOUT</text>'
    body += f'<text x="1164" y="46" font-family="{MONO}" font-size="10" letter-spacing="1.5" fill="{t["ink3"]}" text-anchor="end">REALTIME &#183; LAST SYNC 2026-09-17</text>'
    body += f'<line x1="36" y1="58" x2="1164" y2="58" stroke="{t["line"]}" stroke-width="1" stroke-opacity="0.6"/>'
    cells = [
        ("CGPA", "8.71", "/ 10 &#183; B.TECH C.E.", 0.87, t["ink"]),
        ("CTF FLAGS", "16+", "PICOCTF &#183; SOLVED", 0.80, t["ink"]),
        ("HACKTOVATE '26", "#2", "1ST RUNNER-UP &#183; CSI VIT", 0.66, t["ink"]),
        ("CERTS", "02", "CTI/IR SPEC. + OSINT", 0.66, t["ink"]),
        ("ROLES @ VIT", "03", "TREASURER &#183; CSA", 0.75, t["ink"]),
        ("STATUS", "OPEN", "SWE &amp; SEC INTERNSHIPS", 0.92, t["accent"]),
    ]
    cw = (1164 - 36) / len(cells)
    for i, (lab, val, sub, pct, col) in enumerate(cells):
        x0 = 36 + i * cw
        if i > 0:
            body += f'<line x1="{x0 - 10}" y1="74" x2="{x0 - 10}" y2="196" stroke="{t["line"]}" stroke-opacity="0.3" stroke-width="1"/>'
        body += f'<text x="{x0 + 6}" y="88" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{t["ink3"]}">{lab}</text>'
        body += f'<text x="{x0 + 6}" y="128" font-family="{MONO}" font-size="30" font-weight="700" fill="{col}">{val}</text>'
        body += f'<text x="{x0 + 6}" y="150" font-family="{MONO}" font-size="9" letter-spacing="1" fill="{t["ink2"]}">{sub}</text>'
        body += f'<rect x="{x0 + 6}" y="168" width="{cw - 40}" height="4" fill="none" stroke="{t["line"]}" stroke-opacity="0.35" stroke-width="1"/>'
        body += f'<rect x="{x0 + 6}" y="168" width="{(cw - 40) * pct:.0f}" height="4" fill="{t["accent"]}"/>'
    body += f'<text x="600" y="214" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{t["ink3"]}" text-anchor="middle">ALL VALUES SELF-REPORTED &#183; AUDIT TRAIL: DEVLAHRANI.SYSTEMS</text>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="System readout: CGPA 8.71, 16+ CTF flags, hackathon runner-up, 2 certifications, 3 campus roles, open to internships">'
        + f"<defs>{grid_pattern('bg', t)}</defs>" + body + "</svg>"
    )


# ---------------------------------------------------------------- divider
def divider(t: dict) -> str:
    w, h = 1200, 64
    y = 32
    body = f'<rect width="{w}" height="{h}" fill="none"/>'
    body += f'<line x1="40" y1="{y}" x2="1160" y2="{y}" stroke="{t["ink3"]}" stroke-width="1"/>'
    body += f'<line x1="40" y1="{y - 10}" x2="40" y2="{y + 10}" stroke="{t["ink3"]}" stroke-width="1"/>'
    body += f'<line x1="1160" y1="{y - 10}" x2="1160" y2="{y + 10}" stroke="{t["ink3"]}" stroke-width="1"/>'
    body += f'<path d="M40 {y} l9 -3.5 v7 z" fill="{t["ink3"]}"/>'
    body += f'<path d="M1160 {y} l-9 -3.5 v7 z" fill="{t["ink3"]}"/>'
    body += f'<rect x="470" y="{y - 12}" width="260" height="24" fill="var(--dl-bg, #eef1ec)"/>'
    body += f'<text x="600" y="{y + 4}" font-family="{MONO}" font-size="10" letter-spacing="3" fill="{t["ink2"]}" text-anchor="middle">MEASUREMENT BETWEEN SHEETS</text>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="divider">'
        + body + "</svg>"
    )


# ---------------------------------------------------------------- footer title block
def footer(t: dict) -> str:
    w, h = 1200, 170
    body = frame(w, h, t, "bg")
    x0, y0, tw, th = 36, 30, 1128, 110
    body += f'<rect x="{x0}" y="{y0}" width="{tw}" height="{th}" fill="{t["paper"]}" stroke="{t["line"]}" stroke-width="1.5"/>'
    body += f'<rect x="{x0}" y="{y0}" width="{tw}" height="26" fill="{t["line"]}"/>'
    body += f'<text x="{x0 + 12}" y="{y0 + 18}" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="4" fill="{t["bg"]}">TITLE BLOCK &#8212; IDENTIFICATION</text>'
    top = y0 + 26
    bh = th - 26
    # big project cell
    big_w = 360
    body += f'<text x="{x0 + 16}" y="{top + 34}" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{t["ink3"]}">PROJECT</text>'
    body += f'<text x="{x0 + 16}" y="{top + 62}" font-family="{MONO}" font-size="19" font-weight="700" fill="{t["ink"]}">DEV LAHRANI</text>'
    body += f'<text x="{x0 + 16}" y="{top + 80}" font-family="{MONO}" font-size="10" letter-spacing="1" fill="{t["ink2"]}">CYBERSECURITY &amp; SYSTEMS &#183; PUNE, IN &#183; devlahrani.systems</text>'
    # four cells
    small = [("DRAWN BY", "DEV LAHRANI"), ("CHECKED BY", "SELF"), ("APPROVED BY", "D. LAHRANI"), ("DATE", "2026-09-17")]
    cx = x0 + big_w
    cw = 130
    for lab, val in small:
        body += f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{y0 + th}" stroke="{t["line"]}" stroke-opacity="0.5" stroke-width="1"/>'
        body += f'<text x="{cx + 12}" y="{top + 30}" font-family="{MONO}" font-size="8" letter-spacing="1.5" fill="{t["ink3"]}">{lab}</text>'
        body += f'<text x="{cx + 12}" y="{top + 56}" font-family="{MONO}" font-size="12" font-weight="700" fill="{t["ink"]}">{val}</text>'
        cx += cw
    # mini rows cell
    mini_w = 150
    body += f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{y0 + th}" stroke="{t["line"]}" stroke-opacity="0.5" stroke-width="1"/>'
    mini = ["DWG NO.  DL-2026-001", "REV      03", "SCALE    NTS"]
    for i, m in enumerate(mini):
        ry = top + 22 + i * 21
        if i > 0:
            body += f'<line x1="{cx}" y1="{ry - 6}" x2="{cx + mini_w}" y2="{ry - 6}" stroke="{t["line"]}" stroke-opacity="0.35" stroke-width="1"/>'
        body += f'<text x="{cx + 12}" y="{ry + 4}" font-family="{MONO}" font-size="9" fill="{t["ink2"]}">{m}</text>'
    cx += mini_w
    # sheet cell
    body += f'<line x1="{cx}" y1="{top}" x2="{cx}" y2="{y0 + th}" stroke="{t["line"]}" stroke-opacity="0.5" stroke-width="1"/>'
    body += f'<text x="{cx + 12}" y="{top + 30}" font-family="{MONO}" font-size="8" letter-spacing="1.5" fill="{t["ink3"]}">SHEET</text>'
    body += f'<text x="{cx + 12}" y="{top + 62}" font-family="{MONO}" font-size="24" font-weight="700" fill="{t["ink"]}">1/1</text>'
    # bottom caption
    body += f'<text x="600" y="156" font-family="{MONO}" font-size="9" letter-spacing="2" fill="{t["ink3"]}" text-anchor="middle">&#169; 2026 &#8212; DEV LAHRANI &#183; DRAWN WITH CARE IN PUNE, IN &#183; END OF DRAWING SET</text>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Drawing title block: project Dev Lahrani, drawn by Dev Lahrani, drawing number DL-2026-001, revision 03">'
        + f"<defs>{grid_pattern('bg', t)}</defs>" + body + "</svg>"
    )


# ---------------------------------------------------------------- radar
def radar(t: dict) -> str:
    w, h = 520, 430
    cx, cy, R = 260, 240, 140
    axes = [
        ("SEC", 90), ("CRYPTO", 70), ("AI/ML", 62),
        ("OPS", 78), ("SYSTEMS", 75), ("BACKEND", 84),
    ]
    body = f'<rect width="{w}" height="{h}" fill="{t["paper"]}"/>'
    body += f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" fill="none" stroke="{t["line"]}" stroke-width="1.5"/>'
    body += f'<text x="20" y="34" font-family="{MONO}" font-size="10" fill="{t["ink3"]}">FIG. 06-A</text>'
    body += f'<text x="20" y="56" font-family="{MONO}" font-size="14" font-weight="700" letter-spacing="2" fill="{t["ink"]}">SYSTEM CAPABILITY SURVEY</text>'

    def pt(i: int, frac: float):
        a = math.radians(-90 + i * 60)
        return cx + R * frac * math.cos(a), cy + R * frac * math.sin(a)

    # rings
    for frac in (0.25, 0.5, 0.75, 1.0):
        pts = " ".join(f"{pt(i, frac)[0]:.1f},{pt(i, frac)[1]:.1f}" for i in range(6))
        body += f'<polygon points="{pts}" fill="none" stroke="{t["line"]}" stroke-opacity="{0.6 if frac == 1.0 else 0.22}" stroke-width="1"/>'
    # axes + labels
    for i, (lab, _v) in enumerate(axes):
        px, py = pt(i, 1.0)
        body += f'<line x1="{cx}" y1="{cy}" x2="{px:.1f}" y2="{py:.1f}" stroke="{t["line"]}" stroke-opacity="0.25" stroke-width="1" stroke-dasharray="3 4"/>'
        lx, ly = cx + (R + 24) * math.cos(math.radians(-90 + i * 60)), cy + (R + 24) * math.sin(math.radians(-90 + i * 60))
        c = math.cos(math.radians(-90 + i * 60))
        anchor = "middle" if abs(c) < 0.2 else ("start" if c > 0 else "end")
        body += f'<text x="{lx:.1f}" y="{ly + 4:.1f}" font-family="{MONO}" font-size="11" font-weight="700" letter-spacing="1.5" fill="{t["ink2"]}" text-anchor="{anchor}">{lab}</text>'
    # ring scale labels along top axis
    for frac, labv in ((0.25, "25"), (0.5, "50"), (0.75, "75"), (1.0, "100")):
        body += f'<text x="{cx + 4}" y="{cy - R * frac - 2:.1f}" font-family="{MONO}" font-size="7" fill="{t["ink3"]}">{labv}</text>'
    # data polygon
    pts = " ".join(f"{pt(i, v / 100.0)[0]:.1f},{pt(i, v / 100.0)[1]:.1f}" for i, (_l, v) in enumerate(axes))
    body += f'<polygon points="{pts}" fill="{t["accent"]}" fill-opacity="0.28" stroke="{t["accent"]}" stroke-width="2" stroke-linejoin="round"/>'
    for i, (_l, v) in enumerate(axes):
        px, py = pt(i, v / 100.0)
        body += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="3.5" fill="{t["accent"]}" stroke="{t["paper"]}" stroke-width="1.5"/>'
    body += f'<text x="{w - 20}" y="{h - 16}" font-family="{MONO}" font-size="8" letter-spacing="1.5" fill="{t["ink3"]}" text-anchor="end">N = SELF-ASSESSMENT &#183; NOT TO SCALE</text>'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="Capability radar: security 90, backend 84, ops 78, systems 75, crypto 70, AI/ML 62">'
        + body + "</svg>"
    )


GENERATORS = {
    "banner": banner,
    "status": status,
    "divider": divider,
    "footer": footer,
    "radar": radar,
}

for name, fn in GENERATORS.items():
    for theme, t in THEMES.items():
        svg = fn(t)
        path = os.path.join(OUT, f"{name}-{theme}.svg")
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print("wrote", path, len(svg), "bytes")
