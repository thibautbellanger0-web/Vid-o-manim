from manim import *
import math

# =====================================================================
#  BOÎTE À OUTILS – vidéos de correction et de cours (Manim Community 0.22, rendu sur GitHub)
#  Base à copier en tête de chaque nouvelle vidéo : mise en forme, unités, puissances de 10,
#  rédaction (expression littérale encadrée, application numérique, phrase réponse),
#  calage sur le SRT (self.at), sous-titres (self.dire) pour les vidéos autonomes.
#  Pour une nouvelle vidéo : remplir T (débuts des passages lus, d'après le SRT) puis construct().
# =====================================================================

config.background_color = "#111318"

# ---------- Code couleur (identique dans toute la vidéo) ----------
CONC = "#58C4DD"     # concentrations (bleu)
VOL = "#83C167"      # volumes (vert)
MASSE = "#FF862F"    # masses (orange)
ABSO = "#F4D03F"     # absorbance (jaune)
KCOL = "#C77DFF"     # coefficient k, epsilon (violet)
RHO = "#FF6F91"      # masse volumique (rose)
RES = "#3BE07A"      # résultats / phrases réponses (vert vif)
BOX = "#FFD166"      # cadre « expression littérale » (or)
AN_C = "#8FB3FF"     # étiquette « application numérique »
UNIT = "#C8C8C8"     # unités (gris clair)
MAGENTA = "#E040FB"
SOFT = "#9AA0A6"     # textes secondaires
SOLUTE = "#E040FB"   # soluté (particules et solution colorée)
EAU = "#4FA3E0"      # eau / solvant
SPIN = "#4FC3F7"     # spin aligné
SPIN_D = "#B39DDB"   # spin désaligné
MCOL = "#FF7B54"     # aimantation
TCOL = "#F4D03F"     # température
BCOL = "#81C784"     # champ magnétique
LAMB = "#C77DFF"     # champ moléculaire / couplage
UPC = "#4FC3F7"      # état « haut » (aligné)
DNC = "#FF8A65"      # état « bas » (anti-aligné)
XCOL = "#CE93D8"     # paramètre x = μB / k_B T

# ---------- Zones de l'écran ----------
ZONE_BAS = -2.55     # bas de la zone de travail (en dessous : phrase réponse ou sous-titres)
LARGEUR = 13.2       # largeur utile


# =====================================================================
#  Outils de mise en forme
# =====================================================================
def tx(s, fs=28, c=WHITE, w=LARGEUR, bold=False):
    t = Text(s, font_size=fs, color=c, weight=BOLD if bold else NORMAL)
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def mx(s, c=WHITE, fs=40):
    return MathTex(s, color=c, font_size=fs)


def val(num, unit, c=WHITE, fs=40):
    """Valeur + unité. unit : texte LaTeX ou tuple de morceaux (pour barrer un morceau).
    val(...)[0] = nombre ; val(...)[1] = unité ; val(...)[1][i] = i-ème morceau de l'unité."""
    parts = unit if isinstance(unit, tuple) else (unit,)
    # une seule formule LaTeX : nombre et unités restent sur la même ligne de base (s⁻¹ à la bonne hauteur)
    m = MathTex(num + r"\,", *parts, font_size=fs)
    m[0].set_color(c)
    for k in range(1, len(parts) + 1):
        m[k].set_color(UNIT)
    return VGroup(m[0], VGroup(*[m[k] for k in range(1, len(parts) + 1)]))


def frac(n, d, c=WHITE):
    """Fraction construite à la main : [0] numérateur, [1] barre, [2] dénominateur."""
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=c, stroke_width=3)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.12)


def row(*m, buff=0.18):
    return VGroup(*m).arrange(RIGHT, buff=buff)


def barre(m, c="#FF5555"):
    return Line(m.get_corner(DL) + DL * 0.03, m.get_corner(UR) + UR * 0.03, color=c, stroke_width=5)


def txm(s, fs=26, c=WHITE, w=LARGEUR):
    """Texte avec formules en ligne entre $…$ (ex. « au-dessus de $T_C$ »)."""
    morceaux = s.split("$")
    parts = []
    for k, m in enumerate(morceaux):
        if not m.strip():
            continue
        parts.append(MathTex(m, color=c, font_size=fs * 1.45) if k % 2 else Text(m.strip(), font_size=fs, color=c))
    g = VGroup(*parts).arrange(RIGHT, buff=0.12)
    if g.width > w:
        g.scale_to_fit_width(w)
    return g


def ajuster(m, w=LARGEUR, h=None):
    """Réduit m s'il dépasse la largeur w ou la hauteur h (jamais d'agrandissement)."""
    if m.width > w:
        m.scale_to_fit_width(w)
    if h is not None and m.height > h:
        m.scale_to_fit_height(h)
    return m


def etiquette(s, c):
    """Petite étiquette arrondie (« Expression littérale », « Application numérique »…)."""
    t = Text(s, font_size=16, color=c)
    r = RoundedRectangle(corner_radius=0.08, width=t.width + 0.25, height=t.height + 0.16,
                         stroke_color=c, stroke_width=1.5, fill_color=c, fill_opacity=0.12)
    return VGroup(r, t.move_to(r))


def tableau(lignes, fs=24, couleurs_tetes=None, pad_x=0.28, pad_y=0.2, couleur_grille=SOFT):
    """Petit tableau : lignes = liste de listes de chaînes LaTeX. Retourne VGroup(cellules, grille)."""
    cells = [[mx(s, WHITE, fs) for s in ligne] for ligne in lignes]
    if couleurs_tetes:
        for i, c in enumerate(couleurs_tetes):
            cells[i][0].set_color(c)
    ncol = max(len(l) for l in cells)
    colw = [max(cells[i][j].width for i in range(len(cells)) if j < len(cells[i])) + 2 * pad_x for j in range(ncol)]
    rowh = [max(c.height for c in l) + 2 * pad_y for l in cells]
    W, H = sum(colw), sum(rowh)
    grp = VGroup()
    y = H / 2
    for i, l in enumerate(cells):
        x = -W / 2
        for j, c in enumerate(l):
            c.move_to([x + colw[j] / 2, y - rowh[i] / 2, 0])
            grp.add(c)
            x += colw[j]
        y -= rowh[i]
    grille = VGroup(Rectangle(width=W, height=H, stroke_color=couleur_grille, stroke_width=2))
    y = H / 2
    for i in range(len(rowh) - 1):
        y -= rowh[i]
        grille.add(Line([-W / 2, y, 0], [W / 2, y, 0], stroke_color=couleur_grille, stroke_width=1.5))
    x = -W / 2
    for j in range(ncol - 1):
        x += colw[j]
        grille.add(Line([x, H / 2, 0], [x, -H / 2, 0], stroke_color=couleur_grille, stroke_width=1.5))
    return VGroup(grp, grille)


def carte(titre, contenu, c=ABSO):
    """Document présenté comme une carte (cadre arrondi + titre)."""
    cadre = SurroundingRectangle(contenu, color=SOFT, buff=0.3, corner_radius=0.15, stroke_width=2)
    t = tx(titre, 22, c).next_to(cadre, UP, buff=0.12).align_to(cadre, LEFT).shift(RIGHT * 0.15)
    return VGroup(t, cadre, contenu)


def wl_color(wl):
    """Couleur approximative d'une longueur d'onde visible (nm)."""
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    f = 0.3 + 0.7 * (wl - 380) / 40 if wl < 420 else 1.0
    return "#%02X%02X%02X" % tuple(int(255 * max(0, min(1, x * f))) for x in (r, g, b))


def spectre(x):
    """Allure du spectre d'absorption de l'éosine (document 2)."""
    return (1.13 * math.exp(-((x - 528) / 15) ** 2) + 0.33 * math.exp(-((x - 498) / 15) ** 2)
            + 0.16 * math.exp(-((x - 312) / 14) ** 2) + 0.07 * math.exp(-((x - 346) / 7) ** 2))


def trace(ax, f, x0, x1, color=WHITE, sw=4, n=240):
    """Courbe construite point par point à partir de ax.c2p."""
    pts = [ax.c2p(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners(pts)
    return m


def aire(ax, f, x0, x1, color, op=0.5, n=12):
    pts = [ax.c2p(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    return Polygon(ax.c2p(x0, 0), *pts, ax.c2p(x1, 0), stroke_width=0, fill_color=color, fill_opacity=op)


def aire_couleurs(ax, f, x0=380, x1=645, pas=5, op=0.8):
    return VGroup(*[aire(ax, f, w, w + pas, wl_color(w + pas / 2), op, n=2) for w in range(x0, x1, pas)])


# ---------- Verrerie ----------
def dosette(vol_tex, op=0.95, h=1.5):
    corps = RoundedRectangle(corner_radius=0.18, width=h * 0.45, height=h, stroke_color=WHITE,
                             stroke_width=2.5, fill_color=MAGENTA, fill_opacity=op)
    col = Rectangle(width=h * 0.18, height=h * 0.18, stroke_color=WHITE, stroke_width=2.5,
                    fill_color=MAGENTA, fill_opacity=op).next_to(corps, UP, buff=0)
    bouchon = Rectangle(width=h * 0.26, height=h * 0.14, stroke_color=WHITE, stroke_width=2,
                        fill_color=SOFT, fill_opacity=1).next_to(col, UP, buff=0)
    lab = mx(vol_tex, VOL, 26).next_to(corps, DOWN, buff=0.15)
    return VGroup(VGroup(corps, col, bouchon), lab)


def fiole(vol_tex, op=0.5, r=0.55):
    """Fiole jaugée : [0] dessin, [1] volume."""
    ballon = Circle(radius=r, stroke_color=WHITE, stroke_width=2.5, fill_color=MAGENTA, fill_opacity=op)
    col = Rectangle(width=r * 0.38, height=r * 1.9, stroke_color=WHITE, stroke_width=2.5)
    col.next_to(ballon, UP, buff=-0.04)
    liquide = Rectangle(width=r * 0.38, height=r * 1.1, stroke_width=0, fill_color=MAGENTA,
                        fill_opacity=op).align_to(col, DOWN)
    trait = Line(LEFT * r * 0.3, RIGHT * r * 0.3, color="#FF5555", stroke_width=3).move_to(liquide.get_top())
    dessin = VGroup(liquide, ballon, col, trait)
    lab = mx(vol_tex, VOL, 26).next_to(ballon, DOWN, buff=0.15)
    return VGroup(dessin, lab)


def pipette(op=0.5, h=1.8):
    tube = Rectangle(width=0.13, height=h, stroke_color=WHITE, stroke_width=2)
    liq = Rectangle(width=0.13, height=h * 0.55, stroke_width=0, fill_color=MAGENTA, fill_opacity=op).align_to(tube, DOWN)
    pointe = Polygon(tube.get_corner(DL), tube.get_corner(DR), tube.get_bottom() + DOWN * 0.25,
                     stroke_color=WHITE, stroke_width=2, fill_color=MAGENTA, fill_opacity=op)
    return VGroup(liq, tube, pointe)


# ---------- Couleurs propres à cette vidéo ----------
PUIS_C = "#58C4DD"   # puissances de 10
EXP_P = "#FFD166"    # premier exposant (n)
EXP_Q = "#FF8C42"    # second exposant (p)
EXP_R = "#C77DFF"    # troisième exposant
EXP_N = "#FF7B9C"    # exposant négatif

def puiss(exp, fs=56, base_col=WHITE):
    """10 puissance (exposant) ; exp = liste de (texte LaTeX, couleur). [0] = « 10 », [1] = exposant (morceaux indexables)."""
    b = mx("10", base_col, fs)
    e = VGroup(*[mx(s, c, fs * 0.62) for s, c in exp]).arrange(RIGHT, buff=0.04)
    e.next_to(b, RIGHT, buff=0.05).align_to(b, UP).shift(UP * 0.2 * fs / 56)
    # cale invisible, symétrique de l'exposant : le CENTRE du groupe est celui du « 10 »,
    # donc dans une ligne (row) le 10 reste à la hauteur du signe =
    h = 2 * (e.get_top()[1] - b.get_center()[1])
    cale = Rectangle(width=0.001, height=h, stroke_opacity=0, fill_opacity=0).move_to(b.get_center())
    return VGroup(b, e, cale)


def chiffres(s, fs=72, col=WHITE):
    """Nombre écrit chiffre par chiffre (les espaces donnent un petit écart, la virgule est serrée)."""
    g = VGroup()
    x = 0.0
    for ch in s:
        if ch == " ":
            x += 0.18 * fs / 72
            continue
        m = mx("{,}" if ch == "," else ch, col, fs)
        if ch == ",":
            m.move_to([x + m.width / 2 + 0.02, -0.25 * fs / 72, 0])
            x += m.width + 0.06
        else:
            m.move_to([x + m.width / 2, 0, 0])
            x += m.width + 0.05 * fs / 72
        g.add(m)
    return g


# ---------- Minutage : début de chaque passage lu, d'après le SRT ----------
T = {
    "titre": 0.84, "ex1": 8.90, "photon": 17.20,
    "q1": 22.96, "q1_lit": 27.32, "q1_an1": 29.34, "q1_don": 34.78, "q1_an2": 36.92,
    "q1_res": 44.86, "q1_rep": 48.50,
    "q2": 49.60, "q2_rel": 57.44, "nu_rel": 69.36, "nu_lit": 78.12, "nu_an": 83.66,
    "nu_bar": 87.90, "nu_res": 89.98, "nu_rep": 91.00,
    "lam_lit": 105.88, "lam_box": 109.60, "lam_an": 114.88, "lam_bar": 117.60,
    "lam_res": 122.78, "lam_conv": 126.88, "lam_don": 131.00, "lam_rep": 133.00,
    "q3": 135.20, "q3_bande": 142.24, "q3_ir": 152.30, "q3_rad": 153.74, "q3_rep": 157.46,
    "ex2": 160.48, "q_ex2": 170.32, "q1b_bande": 181.82, "q1b_lit": 194.64, "q1b_rap": 197.74,
    "q1b_an": 208.68, "q1b_res": 214.16, "q1b_att": 217.04,
    "q1b_conv": 231.28, "q1b_an2": 234.26, "q1b_div": 237.46, "q1b_bar2": 239.10, "q1b_res2": 239.88,
    "q1b_rep": 242.66, "q1b_diag": 244.18, "q1b_arrow": 251.14, "q1b_rep2": 258.26,
    "q2b": 262.80, "q2b_note": 272.44, "q2b_diag": 280.66, "q2b_fl": 286.00, "q2b_lit": 290.46,
    "q2b_an": 294.72, "q2b_res": 298.32, "q2b_jlit": 302.32, "q2b_jan": 304.50, "q2b_jan2": 306.66,
    "q2b_jres": 308.60, "q2b_rep": 311.42,
    "q3b": 318.34, "q3b_lit": 342.70, "q3b_an": 349.60, "q3b_res": 351.80, "q3b_conv": 354.20,
    "q3b_rep": 368.42,
    "q4": 369.40, "q4_idee": 378.74, "q4_diag": 387.66, "q4_cond": 394.80, "q4_photon": 402.54,
    "q4_fl": 409.08, "q4_296": 410.50, "q4_reste": 419.16, "q4_calc": 426.76, "q4_lit": 437.28,
    "q4_an": 442.80, "q4_bar": 446.00, "q4_res": 446.50, "q4_conv": 448.00, "q4_conv_an": 450.20,
    "q4_conv_bar": 451.80, "q4_conv_res": 452.30,
    "q4_titre": 456.24, "q4_ecarts": 459.00, "q4_cmp": 469.66, "q4_rep": 478.34,
}

# ---------- Diagramme des niveaux du calcium (valeurs données à l'oral, E1 pris comme référence) ----------
EN = {1: 0.0, 2: 1.88, 3: 2.94, 4: 4.68}
EN_TEX = {1: r"E_1 = 0\ \mathrm{eV}", 2: r"E_2 = 1{,}88\ \mathrm{eV}",
          3: r"E_3 = 2{,}94\ \mathrm{eV}", 4: r"E_4 = 4{,}68\ \mathrm{eV}"}
X_DIAG = -3.0        # abscisse du diagramme (colonne de gauche)


def yE(E):
    return -2.1 + 0.85 * E


def niveaux(x0=X_DIAG):
    g = VGroup()
    for n in (1, 2, 3, 4):
        y = yE(EN[n])
        ligne = Line([x0 - 1.0, y, 0], [x0 + 1.0, y, 0], color=WHITE, stroke_width=3)
        nom = mx("n = %d" % n, SOFT, 28).next_to(ligne, LEFT, buff=0.25)
        valeur = mx(EN_TEX[n], WHITE, 28).next_to(ligne, RIGHT, buff=0.25)
        g.add(ligne, nom, valeur)
    return g


def fleche(ea, eb, c, x0=X_DIAG):
    """Transition entre le niveau ea et le niveau eb (flèche verticale)."""
    return Arrow(start=[x0 + 0.5, yE(EN[ea]), 0], end=[x0 + 0.5, yE(EN[eb]), 0],
                 buff=0, color=c, stroke_width=5)


# ---------- Bande spectrale : abscisse linéaire de 300 à 900 nm ----------
def xnm(nm):
    return -6.0 + (nm - 300) * 0.02


def bande_spectre():
    """Retourne (partie visible avec graduations, partie hors du visible)."""
    vis = VGroup()
    for w in range(400, 800, 4):
        vis.add(Rectangle(width=0.08, height=0.7, stroke_width=0, fill_color=wl_color(w + 2),
                          fill_opacity=1).move_to([xnm(w + 2), 0.2, 0]))
    vis.add(tx("400 nm", 20, WHITE).move_to([xnm(400), -0.5, 0]),
            tx("800 nm", 20, WHITE).move_to([xnm(800), -0.5, 0]),
            tx("Visible", 22, WHITE).move_to([0, 0.95, 0]))
    hors = VGroup(
        Rectangle(width=2.0, height=0.7, stroke_width=0, fill_color="#3A3F4B", fill_opacity=1).move_to([xnm(350), 0.2, 0]),
        Rectangle(width=2.0, height=0.7, stroke_width=0, fill_color="#3A3F4B", fill_opacity=1).move_to([xnm(850), 0.2, 0]),
        tx("Ultraviolets", 20, SOFT).move_to([-5.3, -1.25, 0]),
        tx("Infrarouges", 20, SOFT).move_to([5.3, -1.25, 0]))
    return vis, hors


def repere(nm, texte, c):
    """Repère (flèche + étiquette) au-dessus de la bande spectrale."""
    fl = Arrow(start=[xnm(nm), 1.6, 0], end=[xnm(nm), 0.6, 0], buff=0, color=c, stroke_width=4)
    return VGroup(fl, tx(texte, 22, c).move_to([xnm(nm), 1.9, 0]))


class Correction(Scene):
    # ---------------- Calage sur l'audio ----------------
    def p(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt, **kw)
        self.t += rt

    def at(self, t):
        """Attend jusqu'à l'instant t (en secondes) de l'audio."""
        if t > self.t + 0.02:
            self.wait(t - self.t)
            self.t = t

    # ---------------- Éléments récurrents ----------------
    def set_q(self, label):
        t = Text(label, font_size=20, color=BLACK, weight=BOLD)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.35, height=t.height + 0.2,
                             stroke_width=0, fill_color=ABSO, fill_opacity=1)
        chip = VGroup(r, t.move_to(r)).next_to(self.hdr_ex, RIGHT, buff=0.3)
        if self.hdr_q is None:
            self.p(FadeIn(chip, shift=LEFT * 0.2), rt=0.5)
        else:
            self.p(ReplacementTransform(self.hdr_q, chip), rt=0.5)
        self.hdr_q = chip

    def vider(self, rt=0.6, garder=()):
        """Fait disparaître tout l'écran sauf l'en-tête et les objets de « garder » (et leurs sous-objets)."""
        proteges = set()
        for g in (self.hdr_ex, self.hdr_q, getattr(self, "chrono", None), *garder):
            if g is not None:
                proteges.update(id(x) for x in g.get_family())
        mobs = [m for m in self.mobjects if id(m) not in proteges]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def question(self, s, rt=1.2):
        lignes = s if isinstance(s, (list, tuple)) else [s]
        q = VGroup(*[txm(l, 25, WHITE, w=12.8) if "$" in l else tx(l, 25, WHITE, w=12.8) for l in lignes])
        q.arrange(DOWN, aligned_edge=LEFT, buff=0.14).to_edge(UP, buff=0.78).to_edge(LEFT, buff=0.45)
        barre_g = Line(q.get_corner(UL) + LEFT * 0.15, q.get_corner(DL) + LEFT * 0.15, color=ABSO, stroke_width=4)
        g = VGroup(barre_g, q)
        self.p(FadeIn(g, shift=RIGHT * 0.2), rt=rt)
        self.cur_q = g
        return g

    def haut(self):
        """Ordonnée du haut de la zone de travail (sous l'énoncé de la question)."""
        if self.cur_q is not None and self.cur_q in self.mobjects:
            return self.cur_q.get_bottom()[1] - 0.3
        return 3.0

    def caser(self, g, top=None, bottom=ZONE_BAS, x=0.0, w=LARGEUR):
        """Place g dans la zone de travail : réduit si besoin, colle en haut, centre en x."""
        top = self.haut() if top is None else top
        ajuster(g, w, top - bottom)
        g.shift(UP * (top - g.get_top()[1]))
        g.set_x(x)
        return g

    def a_droite(self, m, ref, buff=0.5, marge=0.35):
        """Place m à droite de ref (alignés en haut) et le réduit s'il dépasse le bord droit."""
        m.next_to(ref, RIGHT, buff=buff).align_to(ref, UP)
        dispo = config.frame_width / 2 - marge - m.get_left()[0]
        if m.width > dispo:
            m.scale_to_fit_width(dispo)
            m.next_to(ref, RIGHT, buff=buff).align_to(ref, UP)
        return m

    def morph(self, pairs, *extra, rt=1.0):
        """Une copie de chaque source « vole » vers sa cible (la cible reste intacte)."""
        fantomes, anims = [], []
        for src, cible in pairs:
            g = cible.copy()
            fantomes.append((g, cible))
            anims.append(ReplacementTransform(src.copy(), g))
        self.p(*anims, *extra, rt=rt)
        for g, cible in fantomes:
            self.remove(g)
            self.add(cible)

    def barrer(self, *mobs, rt=0.6):
        """Barre les unités qui se simplifient."""
        traits = VGroup(*[barre(m) for m in mobs])
        self.p(LaggedStart(*[Create(l) for l in traits], lag_ratio=0.3), rt=rt)
        return traits

    def encadre(self, eq, rt=1.0):
        rect = SurroundingRectangle(eq, color=BOX, buff=0.2, corner_radius=0.08, stroke_width=4)
        lab = etiquette("Expression littérale", BOX).next_to(rect, UP, buff=0.06).align_to(rect, LEFT)
        self.p(Create(rect), FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return VGroup(rect, lab)

    def tag_an(self, m, rt=0.4):
        lab = etiquette("Application numérique", AN_C).next_to(m, UP, buff=0.08).align_to(m, LEFT)
        self.p(FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return lab

    def reponse(self, s, rt=1.8, fs=23):
        t = txm(s, fs, RES, w=12.0) if "$" in s else tx(s, fs, RES, w=12.0)
        box = SurroundingRectangle(t, color=RES, buff=0.2, corner_radius=0.12, stroke_width=3)
        box.set_fill(RES, opacity=0.08)
        g = VGroup(box, t).to_edge(DOWN, buff=0.28)
        lab = etiquette("Phrase réponse", RES).next_to(box, UP, buff=0.06).align_to(box, LEFT)
        self.p(Create(box), FadeIn(lab), FadeIn(t, shift=UP * 0.15), rt=rt)
        return VGroup(g, lab)

    # =================================================================
    #  Outils propres à cette vidéo
    # =================================================================
    def pause(self, d):
        if d > 0:
            self.wait(d)
            self.t += d

    def dire(self, s, c=WHITE, fs=26, rt=0.6, lire=None):
        """Sous-titre explicatif en bas de l'écran (remplace le précédent).
        s : texte, ou liste de morceaux ; un morceau commençant par « $ » est une formule LaTeX.
        lire : temps laissé pour lire (par défaut selon la longueur du texte)."""
        if isinstance(s, str) and "$" in s:
            t = txm(s, fs, c, w=12.6)
            s = s.replace("$", "")
        elif isinstance(s, str):
            t = tx(s, fs, c, w=12.6)
        else:
            parts = [mx(m.strip("$"), c, fs * 1.45) if m.startswith("$") else Text(m, font_size=fs, color=c) for m in s]
            t = VGroup(*parts).arrange(RIGHT, buff=0.12)
            ajuster(t, 12.6)
            s = "".join(m.lstrip("$") for m in s)
        fond = SurroundingRectangle(t, color=SOFT, buff=0.18, corner_radius=0.12, stroke_width=1.5)
        fond.set_fill("#1B1F27", opacity=0.92)
        g = VGroup(fond, t).to_edge(DOWN, buff=0.3)
        anims = [FadeIn(g, shift=UP * 0.12)]
        if self.sous_titre is not None:
            anims.append(FadeOut(self.sous_titre, shift=UP * 0.12))
        self.p(*anims, rt=rt)
        self.sous_titre = g
        if lire is None:
            lire = max(1.6, 0.06 * len(s))
        else:
            lire = max(lire, 0.032 * len(s))      # laisser le temps de lire avant l'animation suivante
        self.pause(lire)
        return g

    def effacer_sous_titre(self, rt=0.4):
        if self.sous_titre is not None:
            self.p(FadeOut(self.sous_titre), rt=rt)
            self.sous_titre = None

    def vider_tout(self, rt=0.6, garder=()):
        self.vider(rt=rt, garder=garder)
        if self.sous_titre is not None and self.sous_titre not in self.mobjects:
            self.sous_titre = None

    # =================================================================
    #  EXERCICES 1 ET 2 – modèle ondulatoire et particulaire de la lumière
    #  Correction muette, calée sur le SRT (chapitre 1.2, Première)
    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.cur_q = None
        self.sous_titre = None
        self.hdr_ex = tx("Chapitre 1.2 · Lumière : ondes et particules", 22, SOFT).to_corner(UL, buff=0.3)
        self.add(self.hdr_ex)

        # ---------- Titre ----------
        self.at(T["titre"])
        titre = VGroup(tx("Correction des exercices 1 et 2", 46, WHITE, bold=True),
                       tx("Énergie, fréquence et longueur d'onde des photons", 26, SOFT))
        titre.arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.p(FadeIn(titre, shift=UP * 0.2), rt=1.0)
        self.at(T["ex1"] - 0.6)
        self.p(FadeOut(titre), rt=0.5)

        # ---------- Exercice 1 : introduction ----------
        self.at(T["ex1"])
        intro = tx("Exercice 1 : les relations classiques du photon", 34, WHITE)
        self.p(FadeIn(intro, shift=UP * 0.2), rt=0.8)
        self.at(T["photon"] - 0.8)
        self.p(FadeOut(intro), rt=0.6)
        self.at(T["photon"])
        carte_e = row(mx("E", WHITE, 72), mx("=", WHITE, 72), val("3{,}40", r"\mathrm{eV}", RES, 72),
                      buff=0.3).move_to(ORIGIN)
        self.p(Write(carte_e), rt=1.2)
        self.at(T["q1"] - 0.6)
        self.p(FadeOut(carte_e), rt=0.5)

        # ---------- Exercice 1, question 1 : conversion en joules ----------
        # Principe : écrire la valeur × 1 eV, puis remplacer 1 eV par sa valeur en joules.
        self.at(T["q1"])
        self.set_q("Ex. 1 · Q1")
        self.question([r"Convertir en joules l'énergie du photon, $E = 3{,}40\ \mathrm{eV}$."])
        LIT = row(mx(r"\Delta E", WHITE, 54), mx("=", WHITE, 54), mx("E", WHITE, 54), mx(r"\times", WHITE, 54),
                  mx(r"1\ \mathrm{eV}", WHITE, 54))
        AN1 = row(mx(r"\Delta E", WHITE, 48), mx("=", WHITE, 48), mx(r"3{,}40", WHITE, 48), mx(r"\times", WHITE, 48),
                  mx(r"1\ \mathrm{eV}", WHITE, 48))
        DON = row(tx("Donnée :", 24, SOFT), mx(r"1\ \mathrm{eV} = 1{,}60\times10^{-19}\ \mathrm{J}", WHITE, 40))
        AN2 = row(mx(r"\Delta E", WHITE, 48), mx("=", WHITE, 48), mx(r"3{,}40", WHITE, 48), mx(r"\times", WHITE, 48),
                  mx(r"1{,}60\times10^{-19}\ \mathrm{J}", WHITE, 48))
        RR = row(mx(r"\Delta E", WHITE, 54), mx("=", WHITE, 54), val(r"5{,}44\times10^{-19}", r"\mathrm{J}", RES, 54))
        pg = VGroup(LIT, AN1, DON).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q1_lit"])
        self.p(Write(LIT), rt=1.0)
        self.encadre(LIT)
        self.at(T["q1_an1"])
        self.p(Write(AN1), rt=1.2)
        self.tag_an(AN1)
        self.at(T["q1_don"])
        self.p(FadeIn(DON, shift=UP * 0.1), rt=0.8)
        self.at(T["q1_an2"] - 0.5)
        self.vider(rt=0.4, garder=(self.cur_q,))
        pg = VGroup(AN2, RR).arrange(DOWN, aligned_edge=LEFT, buff=1.0)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q1_an2"])
        self.p(Write(AN2), rt=1.2)
        self.tag_an(AN2)
        self.at(T["q1_res"])
        self.p(Write(RR), rt=1.0)
        self.at(T["q1_rep"])
        self.reponse(r"L'énergie du photon vaut $5{,}44\times10^{-19}\ \mathrm{J}$.", rt=0.8)
        self.at(T["q2"] - 0.3)
        self.vider(rt=0.3)

        # ---------- Exercice 1, question 2 : fréquence et longueur d'onde ----------
        self.at(T["q2"])
        self.set_q("Ex. 1 · Q2")
        self.question([r"Exprimer puis calculer la fréquence $\nu$ et la longueur d'onde $\lambda$ du rayonnement."])
        TXT_REL = tx("Relation à utiliser : énergie d'un photon et fréquence", 26, SOFT).move_to([0, 1.6, 0])
        self.at(T["q2_rel"])
        self.p(FadeIn(TXT_REL), rt=0.8)
        NU_BIG = row(mx(r"\Delta E", WHITE, 68), mx("=", WHITE, 68), mx("h", WHITE, 68), mx(r"\nu", WHITE, 68))
        NU_BIG.move_to([0, 0.2, 0])
        self.at(T["nu_rel"])
        self.p(FadeOut(TXT_REL), Write(NU_BIG), rt=0.9)
        # Relation à utiliser, puis la même relation avec la grandeur isolée dessous
        NU_REL2 = row(mx(r"\Delta E", WHITE, 56), mx("=", WHITE, 56), mx("h", WHITE, 56), mx(r"\nu", WHITE, 56))
        NU_LIT = row(mx(r"\nu", WHITE, 56), mx("=", WHITE, 56),
                     frac(mx(r"\Delta E", WHITE, 56), mx("h", WHITE, 56)))
        pg = VGroup(NU_REL2, NU_LIT).arrange(DOWN, buff=0.9)
        self.at(T["nu_lit"] - 0.5)
        self.vider(rt=0.4, garder=(self.cur_q,))
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["nu_lit"])
        self.p(Write(NU_REL2), rt=0.8)
        self.p(Write(NU_LIT), rt=1.0)
        self.encadre(NU_LIT)
        NU_AN = row(mx(r"\nu", WHITE, 48), mx("=", WHITE, 48),
                    frac(val(r"5{,}44\times10^{-19}", r"\mathrm{J}", WHITE, 48),
                         val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 48)))
        NU_RES = row(mx(r"\nu", WHITE, 52), mx("=", WHITE, 52), val(r"8{,}21\times10^{14}", r"\mathrm{Hz}", RES, 52))
        self.at(T["nu_an"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))
        pg = VGroup(NU_AN, NU_RES).arrange(DOWN, aligned_edge=LEFT, buff=1.0)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["nu_an"])
        self.p(Write(NU_AN), rt=1.2)
        self.tag_an(NU_AN)
        self.at(T["nu_bar"])
        self.barrer(NU_AN[2][0][1], NU_AN[2][2][1][0])
        self.at(T["nu_res"])
        self.p(Write(NU_RES), rt=1.0)
        self.at(T["nu_rep"])
        self.reponse(r"La fréquence du rayonnement vaut $\nu = 8{,}21\times10^{14}\ \mathrm{Hz}$.", rt=0.8)

        # ---------- Longueur d'onde (même question) ----------
        self.at(T["lam_lit"] - 2.4)
        self.vider(rt=0.5, garder=(self.cur_q,))
        RAP = row(mx(r"\nu", WHITE, 44), mx("=", WHITE, 44), val(r"8{,}21\times10^{14}", r"\mathrm{Hz}", RES, 44))
        LIT_L = row(mx(r"\lambda", WHITE, 54), mx("=", WHITE, 54), frac(mx("c", WHITE, 54), mx(r"\nu", WHITE, 54)))
        cvL = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 44)
        dvL = val(r"8{,}21\times10^{14}", r"\mathrm{Hz}", WHITE, 44)
        AN_L = row(mx(r"\lambda", WHITE, 48), mx("=", WHITE, 48), frac(cvL, dvL))
        TETE_L = VGroup(LIT_L, RAP).arrange(RIGHT, buff=0.8)   # donnée ν à droite de l'expression encadrée
        pg = VGroup(TETE_L, AN_L).arrange(DOWN, aligned_edge=LEFT, buff=1.0)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["lam_lit"])
        self.p(FadeIn(RAP), rt=0.6)
        self.p(Write(LIT_L), rt=1.0)
        self.at(T["lam_box"])
        self.encadre(LIT_L)
        self.at(T["lam_an"])
        self.p(Write(AN_L), rt=1.2)
        self.tag_an(AN_L)
        self.at(T["lam_bar"])
        self.barrer(cvL[1][1], dvL[1][0])

        self.at(T["lam_res"] - 1.0)
        self.vider(rt=0.5, garder=(self.cur_q,))
        RES_L = row(mx(r"\lambda", WHITE, 48), mx("=", WHITE, 48), val(r"3{,}65\times10^{-7}", r"\mathrm{m}", RES, 48))
        CONV = row(mx(r"\lambda", WHITE, 48), mx("=", WHITE, 48), val("365", r"\mathrm{nm}", RES, 48))
        DON_NM = row(tx("Donnée :", 24, SOFT), mx(r"1\ \mathrm{nm}", WHITE, 36), mx("=", WHITE, 36),
                     mx(r"10^{-9}\ \mathrm{m}", WHITE, 36))
        pg = VGroup(RES_L, CONV, DON_NM).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["lam_res"])
        self.p(Write(RES_L), rt=1.0)
        self.at(T["lam_conv"])
        self.p(Write(CONV), rt=1.0)
        self.at(T["lam_don"])
        self.p(FadeIn(DON_NM), rt=0.8)
        self.at(T["lam_rep"])
        self.reponse(r"La longueur d'onde vaut $\lambda = 365\ \mathrm{nm}$.", rt=0.8)
        self.at(T["q3"] - 0.6)
        self.vider(rt=0.5)

        # ---------- Exercice 1, question 3 : domaine spectral ----------
        self.at(T["q3"])
        self.set_q("Ex. 1 · Q3")
        self.question(["Dans quel domaine des ondes électromagnétiques se trouve ce rayonnement ?"])
        VIS, HORS = bande_spectre()
        REP365 = repere(365, "365 nm", RES)
        self.at(T["q3_bande"])
        self.p(FadeIn(VIS), rt=1.2)
        self.at(T["q3_ir"])
        self.p(FadeIn(HORS), rt=0.8)
        self.at(T["q3_rad"])
        self.p(FadeIn(REP365), rt=0.6)
        self.at(T["q3_rep"])
        self.reponse("Le rayonnement de 365 nm se situe dans le domaine des ultraviolets.", rt=0.8)
        self.at(T["ex2"] - 0.7)
        self.vider(rt=0.4)

        # ---------- Exercice 2 : données (spectre et diagramme) ----------
        self.at(T["ex2"])
        self.set_q("Ex. 2 · Données")
        CAP2 = tx("Spectre d'émission et diagramme des niveaux d'énergie du calcium", 26, SOFT).move_to([0, 2.7, 0])
        D0 = niveaux()
        self.p(FadeIn(CAP2), FadeIn(D0), rt=1.2)
        self.at(T["q_ex2"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 2, question 1 : transition à 423 nm ----------
        self.at(T["q_ex2"])
        self.set_q("Ex. 2 · Q1")
        self.question(["1. Identifier la transition à l'origine de la raie de longueur d'onde 423 nm,",
                       "puis la représenter par une flèche sur le diagramme."])
        self.at(T["q1b_bande"])
        VIS2, _ = bande_spectre()
        REP423 = repere(423, "423 nm", WHITE)
        self.p(FadeIn(VIS2), FadeIn(REP423), rt=1.2)
        self.at(T["q1b_lit"] - 2.0)
        self.vider(rt=0.5, garder=(self.cur_q,))

        # Calcul de l'énergie : ΔE = h c / λ
        LIT_E = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), frac(mx(r"h\,c", WHITE, 40), mx(r"\lambda", WHITE, 40)))
        RAP_E = txm(r"Rappel : $\Delta E = h\,\nu$ et $\nu = c / \lambda$", 22, SOFT, w=5.6)
        TETE = VGroup(LIT_E, RAP_E).arrange(RIGHT, buff=0.6)
        hv = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 36)
        cv = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 36)
        dv = val(r"423\times10^{-9}", r"\mathrm{m}", WHITE, 36)
        AN_E = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), frac(row(hv, mx(r"\times", WHITE, 36), cv), dv))
        RES_E = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), val(r"4{,}70\times10^{-19}", r"\mathrm{J}", RES, 40))
        ATT = tx("Attention : le diagramme est gradué en électronvolts, pas en joules.", 22, ABSO)
        page = VGroup(TETE, AN_E, RES_E, ATT).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(page, top=self.haut() - 0.6)
        self.at(T["q1b_lit"])
        self.p(Write(LIT_E), rt=1.0)
        self.encadre(LIT_E)
        self.at(T["q1b_rap"])
        self.p(FadeIn(RAP_E), rt=0.8)
        self.at(T["q1b_an"])
        self.p(Write(AN_E), rt=1.2)
        self.tag_an(AN_E)
        self.at(T["q1b_an"] + 3.0)
        self.barrer(hv[1][1], cv[1][1], cv[1][0], dv[1][0])
        self.at(T["q1b_res"])
        self.p(Write(RES_E), rt=1.0)
        self.at(T["q1b_att"])
        self.p(FadeIn(ATT), rt=0.6)
        self.at(T["q1b_conv"] - 0.7)
        self.vider(rt=0.5, garder=(self.cur_q,))

        # Conversion en électronvolts : ΔE_eV = ΔE_J / (1 eV), puis 1 eV remplacé par sa valeur en joules
        LIT_C = row(mx(r"\Delta E_{\mathrm{eV}}", WHITE, 48), mx("=", WHITE, 48),
                    frac(mx(r"\Delta E_{\mathrm{J}}", WHITE, 48), mx(r"1\ \mathrm{eV}", WHITE, 48)))
        AN_C1 = row(mx(r"\Delta E_{\mathrm{eV}}", WHITE, 44), mx("=", WHITE, 44),
                    frac(val(r"4{,}70\times10^{-19}", r"\mathrm{J}", WHITE, 44), mx(r"1\ \mathrm{eV}", WHITE, 44)))
        cJ = val(r"4{,}70\times10^{-19}", r"\mathrm{J}", WHITE, 44)
        cD = val(r"1{,}60\times10^{-19}", r"\mathrm{J}", WHITE, 44)
        AN_C2 = row(mx(r"\Delta E_{\mathrm{eV}}", WHITE, 44), mx("=", WHITE, 44), frac(cJ, cD))
        RES_C = row(mx(r"\Delta E_{\mathrm{eV}}", WHITE, 52), mx("=", WHITE, 52), val(r"2{,}94", r"\mathrm{eV}", RES, 52))
        pg = VGroup(LIT_C, AN_C1).arrange(DOWN, aligned_edge=LEFT, buff=1.0)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q1b_conv"])
        self.p(Write(LIT_C), rt=1.0)
        self.encadre(LIT_C)
        self.at(T["q1b_an2"])
        self.p(Write(AN_C1), rt=1.2)
        self.tag_an(AN_C1)
        self.at(T["q1b_div"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))
        pg = VGroup(AN_C2, RES_C).arrange(DOWN, aligned_edge=LEFT, buff=1.0)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q1b_div"])
        self.p(Write(AN_C2), rt=1.2)
        self.tag_an(AN_C2)
        self.at(T["q1b_bar2"])
        self.barrer(cJ[1], cD[1])
        self.at(T["q1b_res2"])
        self.p(Write(RES_C), rt=1.0)
        self.at(T["q1b_rep"])
        REP_C = self.reponse(r"Le rayonnement de 423 nm a une énergie de $2{,}94\ \mathrm{eV}$.", rt=0.8)
        self.at(T["q1b_diag"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q, REP_C))

        # Retour sur le diagramme : transition du niveau 3 vers le niveau 1
        self.at(T["q1b_diag"])
        D1 = niveaux()
        self.p(FadeIn(D1), rt=0.8)
        self.at(T["q1b_arrow"])
        FL1 = fleche(3, 1, MAGENTA)
        self.p(Create(FL1), rt=0.8)
        self.at(T["q1b_rep2"])
        self.p(FadeOut(REP_C), rt=0.4)
        self.reponse("Raie à 423 nm : transition du niveau 3 vers le niveau 1.", rt=0.8)
        self.at(T["q2b"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 2, question 2 : énergie absorbée de E2 à E3 ----------
        self.at(T["q2b"])
        self.set_q("Ex. 2 · Q2")
        self.question([r"2. Calculer l'énergie du photon absorbé pour passer de $E_2$ à $E_3$, en eV puis en J."])
        NOTE = VGroup(txm(r"1er état excité : niveau 2, noté $E_2$", 24, SOFT, w=10),
                      txm(r"2e état excité : niveau 3, noté $E_3$", 24, SOFT, w=10),
                      txm(r"État de base : niveau 1, noté $E_1$", 24, SOFT, w=10)).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        self.caser(NOTE, top=self.haut() - 0.6, w=10)
        self.at(T["q2b_note"])
        self.p(FadeIn(NOTE), rt=0.8)
        self.at(T["q2b_diag"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))

        D2 = niveaux()
        FL2 = fleche(2, 3, ABSO)
        self.at(T["q2b_diag"])
        self.p(FadeIn(D2), rt=0.8)
        self.at(T["q2b_fl"])
        self.p(Create(FL2), rt=0.8)
        LIT_2 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), mx(r"E_3 - E_2", WHITE, 36))
        AN_2 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), val("2{,}94", r"\mathrm{eV}", WHITE, 36),
                   mx("-", WHITE, 36), val("1{,}88", r"\mathrm{eV}", WHITE, 36))
        RES_2 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), val("1{,}06", r"\mathrm{eV}", RES, 36))
        droite = VGroup(LIT_2, AN_2, RES_2).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(droite, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q2b_lit"])
        self.p(Write(LIT_2), rt=1.0)
        self.encadre(LIT_2)
        self.at(T["q2b_an"])
        self.p(Write(AN_2), rt=1.2)
        self.tag_an(AN_2)
        self.at(T["q2b_res"])
        self.p(Write(RES_2), rt=1.0)
        self.at(T["q2b_jlit"] - 0.7)
        self.vider(rt=0.4, garder=(self.cur_q, D2, FL2))

        # Conversion en joules : ΔE_J = ΔE_eV × 1 eV, puis 1 eV remplacé par sa valeur
        LIT_J = row(mx(r"\Delta E_{\mathrm{J}}", WHITE, 40), mx("=", WHITE, 40), mx(r"\Delta E_{\mathrm{eV}}", WHITE, 40),
                    mx(r"\times", WHITE, 40), mx(r"1\ \mathrm{eV}", WHITE, 40))
        AN_J1 = row(mx(r"\Delta E_{\mathrm{J}}", WHITE, 36), mx("=", WHITE, 36), mx("1{,}06", WHITE, 36),
                    mx(r"\times", WHITE, 36), mx(r"1\ \mathrm{eV}", WHITE, 36))
        AN_J2 = row(mx(r"\Delta E_{\mathrm{J}}", WHITE, 36), mx("=", WHITE, 36), mx("1{,}06", WHITE, 36),
                    mx(r"\times", WHITE, 36), mx(r"1{,}60\times10^{-19}\ \mathrm{J}", WHITE, 36))
        RES_J = row(mx(r"\Delta E_{\mathrm{J}}", WHITE, 40), mx("=", WHITE, 40), val(r"1{,}70\times10^{-19}", r"\mathrm{J}", RES, 40))
        droite2 = VGroup(LIT_J, AN_J1).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        self.caser(droite2, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q2b_jlit"])
        self.p(Write(LIT_J), rt=1.0)
        self.encadre(LIT_J)
        self.at(T["q2b_jan"])
        self.p(Write(AN_J1), rt=1.2)
        self.tag_an(AN_J1)
        self.at(T["q2b_jan2"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q, D2, FL2))
        droite3 = VGroup(AN_J2, RES_J).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        self.caser(droite3, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q2b_jan2"])
        self.p(Write(AN_J2), rt=1.2)
        self.tag_an(AN_J2)
        self.at(T["q2b_jres"])
        self.p(Write(RES_J), rt=1.0)
        self.at(T["q2b_rep"])
        self.reponse(r"Le photon a une énergie de $1{,}06\ \mathrm{eV}$, soit $1{,}70\times10^{-19}\ \mathrm{J}$.", rt=0.8)
        self.at(T["q3b"] - 0.7)
        self.vider(rt=0.4)

        # ---------- Exercice 2, question 3 : longueur d'onde E2 -> E3 ----------
        self.at(T["q3b"])
        self.set_q("Ex. 2 · Q3")
        self.question([r"3. Calculer la longueur d'onde correspondant à la transition de $E_2$ à $E_3$.",
                       "Préciser le domaine spectral de ce rayonnement."])
        LIT_3 = row(mx(r"\lambda", WHITE, 44), mx("=", WHITE, 44), frac(mx(r"h\,c", WHITE, 44), mx(r"\Delta E", WHITE, 44)))
        hv3 = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 36)
        cv3 = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 36)
        dv3 = val(r"1{,}70\times10^{-19}", r"\mathrm{J}", WHITE, 36)
        AN_3 = row(mx(r"\lambda", WHITE, 44), mx("=", WHITE, 44), frac(row(hv3, mx(r"\times", WHITE, 36), cv3), dv3))
        RES_3 = row(mx(r"\lambda", WHITE, 44), mx("=", WHITE, 44), val(r"1{,}17\times10^{-6}", r"\mathrm{m}", RES, 44))
        CONV_3 = row(mx(r"\lambda", WHITE, 44), mx("=", WHITE, 44), val(r"1\,170", r"\mathrm{nm}", RES, 44))
        pg = VGroup(LIT_3).arrange(DOWN)
        self.caser(LIT_3, top=self.haut() - 0.6)
        self.at(T["q3b_lit"])
        self.p(Write(LIT_3), rt=1.0)
        self.encadre(LIT_3)
        self.at(T["q3b_an"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))
        pg = VGroup(AN_3, RES_3, CONV_3).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q3b_an"])
        self.p(Write(AN_3), rt=1.2)
        self.tag_an(AN_3)
        self.at(T["q3b_res"] - 0.6)
        self.barrer(hv3[1][0], dv3[1][0], hv3[1][1], cv3[1][1])
        self.at(T["q3b_res"])
        self.p(Write(RES_3), rt=1.0)
        self.at(T["q3b_conv"])
        self.p(Write(CONV_3), rt=1.0)
        self.at(T["q3b_rep"])
        self.reponse(r"Ce rayonnement appartient au domaine des infrarouges, car $\lambda > 800\ \mathrm{nm}$.", rt=0.5)
        self.at(T["q4"] - 0.5)
        self.vider(rt=0.2)

        # ---------- Exercice 2, question 4 : photon de 520 nm ----------
        self.at(T["q4"])
        self.set_q("Ex. 2 · Q4")
        self.question(["4. Un photon de longueur d'onde 520 nm peut-il être absorbé par un atome de calcium ?"])
        TXT4 = tx("On calcule d'abord l'énergie de ce photon", 28, WHITE)
        self.at(T["q4_idee"])
        self.p(FadeIn(TXT4), rt=0.8)
        self.at(T["q4_diag"])
        self.vider(rt=0.4, garder=(self.cur_q,))
        D4 = niveaux()
        self.p(FadeIn(D4), rt=0.8)
        RC = txm(r"Condition : énergie du photon = écart entre niveaux", 24, WHITE, w=6.4)
        R1 = txm(r"Photon de $2{,}94\ \mathrm{eV}$ : passage de $E_1$ à $E_3$", 24, WHITE, w=6.4)
        R2 = txm(r"Photon de $2{,}96\ \mathrm{eV}$ : aucun niveau correspondant", 24, WHITE, w=6.4)
        R3 = txm(r"L'atome reste au niveau 1 : pas d'absorption", 24, WHITE, w=6.4)
        droite4 = VGroup(RC, R1, R2, R3).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        self.caser(droite4, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q4_cond"])
        self.p(FadeIn(RC), rt=0.8)
        self.at(T["q4_photon"])
        self.p(FadeIn(R1), rt=0.8)
        self.at(T["q4_fl"])
        FL4 = fleche(1, 3, RES)
        self.p(Create(FL4), rt=0.8)
        self.at(T["q4_296"])
        self.p(FadeIn(R2), rt=0.8)
        self.at(T["q4_reste"])
        self.p(FadeIn(R3), rt=0.8)
        self.at(T["q4_calc"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))

        # Calcul de l'énergie du photon de 520 nm : E = h c / λ
        TXT_CALC = tx("La longueur d'onde est connue : on calcule l'énergie.", 26, SOFT)
        self.at(T["q4_calc"])
        self.p(FadeIn(TXT_CALC), rt=0.6)
        LIT_4 = row(mx("E", WHITE, 48), mx("=", WHITE, 48), frac(mx(r"h\,c", WHITE, 48), mx(r"\lambda", WHITE, 48)))
        hv4 = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 40)
        cv4 = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 40)
        dv4 = val(r"520\times10^{-9}", r"\mathrm{m}", WHITE, 40)
        AN_4 = row(mx("E", WHITE, 44), mx("=", WHITE, 44), frac(row(hv4, mx(r"\times", WHITE, 40), cv4), dv4))
        RES_4 = row(mx("E", WHITE, 48), mx("=", WHITE, 48), val(r"3{,}83\times10^{-19}", r"\mathrm{J}", RES, 48))
        self.caser(LIT_4, top=self.haut() - 0.6)
        self.at(T["q4_lit"] - 0.6)
        self.p(FadeOut(TXT_CALC), rt=0.4)
        self.at(T["q4_lit"])
        self.p(Write(LIT_4), rt=1.0)
        self.encadre(LIT_4, rt=0.6)
        self.at(T["q4_an"] - 0.6)
        self.vider(rt=0.4, garder=(self.cur_q,))
        pg = VGroup(AN_4, RES_4).arrange(DOWN, aligned_edge=LEFT, buff=0.9)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q4_an"])
        self.p(Write(AN_4), rt=1.2)
        self.tag_an(AN_4)
        self.at(T["q4_bar"])
        self.barrer(hv4[1][1], cv4[1][1], cv4[1][0], dv4[1][0], rt=0.4)
        self.at(T["q4_res"])
        self.p(Write(RES_4), rt=0.8)
        self.at(T["q4_conv"] - 0.4)
        self.vider(rt=0.3, garder=(self.cur_q,))

        # Conversion de E en électronvolts : E_eV = E_J / (1 eV), puis 1 eV remplacé par sa valeur
        LIT_4C = row(mx(r"E_{\mathrm{eV}}", WHITE, 48), mx("=", WHITE, 48),
                     frac(mx(r"E_{\mathrm{J}}", WHITE, 48), mx(r"1\ \mathrm{eV}", WHITE, 48)))
        AN_4C = row(mx(r"E_{\mathrm{eV}}", WHITE, 44), mx("=", WHITE, 44),
                    frac(val(r"3{,}83\times10^{-19}", r"\mathrm{J}", WHITE, 44), mx(r"1{,}60\times10^{-19}\ \mathrm{J}", WHITE, 44)))
        cEJ = val(r"3{,}83\times10^{-19}", r"\mathrm{J}", WHITE, 44)
        cEc = val(r"1{,}60\times10^{-19}", r"\mathrm{J}", WHITE, 44)
        RES_4C = row(mx(r"E_{\mathrm{eV}}", WHITE, 52), mx("=", WHITE, 52), val("2{,}39", r"\mathrm{eV}", RES, 52))
        pg = VGroup(LIT_4C, AN_4C, RES_4C).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q4_conv"])
        self.p(Write(LIT_4C), rt=1.0)
        self.encadre(LIT_4C, rt=0.6)
        self.at(T["q4_conv_an"])
        self.p(Write(AN_4C), rt=1.2)
        self.tag_an(AN_4C)
        self.at(T["q4_conv_bar"])
        self.barrer(cEJ[1], rt=0.4)
        self.at(T["q4_conv_res"])
        self.p(Write(RES_4C), rt=0.8)
        self.at(T["q4_titre"] - 0.4)
        self.vider(rt=0.4)

        # Écarts entre niveaux, représentés sur le diagramme
        GAPS = [(2, 3, "1{,}06"), (3, 4, "1{,}74"), (1, 2, "1{,}88"), (2, 4, "2{,}80"), (1, 3, "2{,}94"), (1, 4, "4{,}68")]
        self.at(T["q4_titre"])
        DG = niveaux(-4.8)
        TIT_G = tx("Écarts d'énergie entre les niveaux", 28, SOFT).move_to([1.5, 2.9, 0])
        self.p(FadeIn(DG), FadeIn(TIT_G), rt=0.8)
        ECARTS = VGroup()
        ETIQ = VGroup()
        for i, (a, b, v) in enumerate(GAPS):
            xc = -0.6 + 1.0 * i
            ya, yb = yE(EN[a]), yE(EN[b])
            ECARTS.add(DoubleArrow(start=[xc, ya, 0], end=[xc, yb, 0], buff=0, color=CONC,
                                   stroke_width=4, tip_length=0.18))
            ETIQ.add(mx(v + r"\ \mathrm{eV}", WHITE, 26).move_to([xc + 0.45, (ya + yb) / 2, 0]))
        self.at(T["q4_ecarts"])
        self.p(LaggedStart(*[Create(a) for a in ECARTS], lag_ratio=0.4), FadeIn(ETIQ), rt=4.0)
        CMP = txm(r"Aucun écart ne vaut $2{,}39\ \mathrm{eV}$", 28, ABSO, w=10)
        CMP.move_to([0, 2.3, 0])
        self.at(T["q4_cmp"])
        self.p(FadeIn(CMP), rt=0.8)
        self.at(T["q4_rep"])
        self.reponse("Le photon de 520 nm n'est pas absorbé par l'atome de calcium.", rt=0.8)
        # Fin : l'audio dure 8 min (480 s) ; marge de 10 s sur la dernière image, à couper au montage
        self.at(480.0)
        self.pause(10.0)
