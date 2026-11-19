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


# ---------- Minutage : début de chaque passage lu, d'après le SRT (exercices 3 et 4) ----------
T = {
    "titre": 0.46, "ex3": 4.44, "li_diag": 7.76,
    "q1": 19.30, "q1_fl": 31.82, "q1_txt": 38.94, "q1_rep": 55.40,
    "q2": 59.04, "q2_lit": 72.30, "q2_an": 80.10, "q2_res": 83.04, "q2_att": 86.42, "q2_rep": 92.90,
    "q3": 97.36, "q3_diag": 99.10, "q3_fl": 102.30, "q3_rep": 105.00,
    "q4": 106.70, "q4_lit": 119.50, "q4_rap": 121.62, "q4_rep": 126.00,
    "q5": 128.52, "q5_lit": 140.34, "q5_don": 145.00, "q5_conv": 149.50, "q5_bar_cj": 150.90,
    "q5_res_cj": 151.50, "q5_an": 152.60, "q5_bar": 154.00, "q5_res": 154.42, "q5_nm": 155.40,
    "q5_rep": 157.46,
    "q6": 161.06, "q6_rel": 164.08, "q6_vid": 173.30, "q6_lit": 174.84, "q6_an": 177.00,
    "q6_bar": 178.60, "q6_res": 179.54, "q6_rep": 184.64,
    "ex4": 188.44, "ex4_diag": 193.88,
    "q1h": 198.08, "q1h_hl": 212.22, "q1h_marq": 214.52, "q1h_rep": 253.00,
    "q2h": 254.94, "q2h_fl": 265.40, "q2h_lit": 270.40, "q2h_an": 281.02, "q2h_res": 283.12,
    "q2h_rep": 285.18,
    "q3h": 291.82, "q3h_lit": 305.26, "q3h_an": 322.40, "q3h_res": 328.34, "q3h_rep": 330.26,
    "q4h": 340.06, "q4h_lit": 345.20, "q4h_an": 349.82, "q4h_bar": 351.90, "q4h_res": 354.62,
    "q4h_rep": 357.50,
    "q5h": 361.91, "q5h_diag": 363.70, "q5h_fl": 369.29, "q5h_rep": 380.00,
    "q6h": 382.73, "q6h_txt": 398.65, "q6h_rep": 401.00,
    "q7h": 404.35, "q7h_lit": 411.69, "q7h_att": 416.91, "q7h_an": 420.50, "q7h_bar": 422.10,
    "q7h_res": 423.00, "q7h_conv": 426.25, "q7h_rep": 429.00,
    "fin": 436.00,
}


# ---------- Diagrammes des niveaux d'énergie (exercices 3 et 4) ----------
# Valeurs dictées à l'oral : E1 et E3 (lithium), E1, E2, -0,37 eV (hydrogène).
# Les autres niveaux sont reconstruits (à vérifier sur la feuille).
X_LI = -4.2          # abscisse du diagramme du lithium (colonne de gauche)
X_H = -4.2           # abscisse du diagramme de l'hydrogène
EN_LI_TEX = {1: r"E_1 = -5{,}39\ \mathrm{eV}", 2: r"E_2 = -3{,}54\ \mathrm{eV}", 3: r"E_3 = -2{,}01\ \mathrm{eV}",
             4: r"E_4 = -1{,}85\ \mathrm{eV}", 5: r"E_5 = -1{,}51\ \mathrm{eV}", 6: r"E_6 = -1{,}05\ \mathrm{eV}"}
EN_H_TEX = {1: r"E_1 = -13{,}6\ \mathrm{eV}", 2: r"E_2 = -3{,}39\ \mathrm{eV}", 3: r"E_3 = -1{,}51\ \mathrm{eV}",
            4: r"E_4 = -0{,}85\ \mathrm{eV}", 5: r"E_5 = -0{,}54\ \mathrm{eV}", 6: r"E_6 = -0{,}37\ \mathrm{eV}"}


def y_li(k):
    return -2.0 + 0.62 * (k - 1)


def y_h(k):
    """Hydrogène : niveau 1 isolé en bas (cassure d'échelle), niveaux 2 à 6 espacés."""
    return -2.1 if k == 1 else -0.8 + 0.55 * (k - 2)


def niveau_ligne(x0, y):
    return Line([x0 - 1.0, y, 0], [x0 + 1.0, y, 0], color=WHITE, stroke_width=3)


def niveaux_li(x0=X_LI):
    g = VGroup()
    for k in range(1, 7):
        ligne = niveau_ligne(x0, y_li(k))
        nom = tx("État %d" % k, 22, SOFT).next_to(ligne, LEFT, buff=0.25)
        valeur = mx(EN_LI_TEX[k], WHITE, 26).next_to(ligne, RIGHT, buff=0.25)
        g.add(ligne, nom, valeur)
    g.add(tx("Échelle non linéaire", 18, SOFT).move_to([x0 + 0.2, 1.85, 0]))
    return g


def niveaux_h(x0=X_H):
    g = VGroup()
    for k in range(1, 7):
        ligne = niveau_ligne(x0, y_h(k))
        nom = mx("n = %d" % k, SOFT, 26).next_to(ligne, LEFT, buff=0.25)
        valeur = mx(EN_H_TEX[k], WHITE, 26).next_to(ligne, RIGHT, buff=0.25)
        g.add(ligne, nom, valeur)
    return g


def marque_h(x0=X_H):
    """Cassure de l'échelle entre les niveaux 1 et 2, et légende."""
    cassure = VGroup(*[Line([x0 - 1.4 + d - 0.12, -1.55, 0], [x0 - 1.4 + d + 0.12, -1.35, 0],
                            color=SOFT, stroke_width=3) for d in (-0.1, 0.1)])
    legende = tx("Échelle non linéaire", 18, SOFT).move_to([x0 + 0.2, 1.85, 0])
    return VGroup(cassure, legende)


def fleche_li(a, b, c, x0=X_LI):
    """Transition entre les états a et b du lithium (flèche verticale)."""
    return Arrow(start=[x0 + 0.5, y_li(a), 0], end=[x0 + 0.5, y_li(b), 0], buff=0, color=c, stroke_width=5)


def fleche_h(a, b, c, x0=X_H):
    """Transition entre les niveaux a et b de l'hydrogène (flèche verticale)."""
    return Arrow(start=[x0 + 0.5, y_h(a), 0], end=[x0 + 0.5, y_h(b), 0], buff=0, color=c, stroke_width=5)


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
    #  EXERCICES 3 ET 4 – spectres du lithium et de l'hydrogène
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
        titre = VGroup(tx("Correction des exercices 3 et 4", 46, WHITE, bold=True),
                       tx("Niveaux d'énergie, absorption et émission de photons", 26, SOFT))
        titre.arrange(DOWN, buff=0.35).move_to(ORIGIN)
        self.p(FadeIn(titre, shift=UP * 0.2), rt=1.0)
        self.at(T["ex3"] - 0.6)
        self.p(FadeOut(titre), rt=0.5)

        # ---------- Exercice 3 : introduction et diagramme du lithium ----------
        self.at(T["ex3"])
        intro = tx("Exercice 3 : spectre d'émission du lithium", 34, WHITE)
        self.p(FadeIn(intro, shift=UP * 0.2), rt=0.8)
        self.at(T["li_diag"] - 0.6)
        self.p(FadeOut(intro), rt=0.6)
        self.at(T["li_diag"])
        D_LI = niveaux_li()
        self.p(FadeIn(D_LI), rt=1.2)

        # ---------- Exercice 3, question 1 : absorption ou émission ----------
        self.at(T["q1"])
        self.set_q("Ex. 3 · Q1")
        self.question(["1. L'atome passe de l'état 1 à l'état 3.",
                       "Le photon mis en jeu est-il absorbé ou émis ?"])
        self.at(T["q1_fl"])
        self.p(Create(fleche_li(1, 3, ABSO)), rt=0.9)
        self.at(T["q1_txt"])
        EXPL = tx("Énergie croissante : l'atome gagne de l'énergie", 24, ABSO, w=6.0).move_to([3.2, 0.0, 0])
        self.p(FadeIn(EXPL, shift=LEFT * 0.2), rt=0.8)
        self.at(T["q1_rep"])
        self.reponse("Le photon est absorbé : l'atome passe de l'état 1 à l'état 3.", rt=0.8)
        self.at(T["q2"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 3, question 2 : énergie du photon en eV ----------
        self.at(T["q2"])
        self.set_q("Ex. 3 · Q2")
        self.question(["2. Calculer en électron-volts l'énergie du photon responsable de cette transition."])
        LIT_a = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), mx(r"E_3 - E_1", WHITE, 40))
        AN_a = mx(r"\Delta E = (-2{,}01\ \mathrm{eV}) - (-5{,}39\ \mathrm{eV})", WHITE, 40)
        RS_a = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), val("3{,}38", r"\mathrm{eV}", RES, 40))
        ATT_a = txm(r"Attention : $\Delta E = E_3 - E_1$, et non $E_1 - E_3$", 22, ABSO, w=12.0)
        pg = VGroup(LIT_a, AN_a, RS_a, ATT_a).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q2_lit"])
        self.p(Write(LIT_a), rt=1.0)
        self.encadre(LIT_a)
        self.at(T["q2_an"])
        self.p(Write(AN_a), rt=1.2)
        self.tag_an(AN_a)
        self.at(T["q2_res"])
        self.p(Write(RS_a), rt=1.0)
        self.at(T["q2_att"])
        self.p(FadeIn(ATT_a), rt=0.6)
        self.at(T["q2_rep"])
        self.reponse(r"Le photon a une énergie de $3{,}38\ \mathrm{eV}$.", rt=0.8)
        self.at(T["q3"] - 0.6)
        self.vider(rt=0.4)

        # ---------- Exercice 3, question 3 : flèche sur le diagramme ----------
        self.at(T["q3"])
        self.set_q("Ex. 3 · Q3")
        self.question(["3. Indiquer par une flèche sur le diagramme la transition correspondante."])
        D3 = niveaux_li()
        self.at(T["q3_diag"])
        self.p(FadeIn(D3), rt=1.0)
        self.at(T["q3_fl"])
        self.p(Create(fleche_li(1, 3, ABSO)), rt=0.9)
        self.at(T["q3_rep"])
        self.reponse("La flèche relie l'état 1 à l'état 3, vers le haut : c'est une absorption.", rt=0.8)
        self.at(T["q4"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 3, question 4 : E en fonction de λ ----------
        self.at(T["q4"])
        self.set_q("Ex. 3 · Q4")
        self.question([r"4. Exprimer l'énergie du photon en fonction de la longueur d'onde $\lambda$ de la radiation."])
        LIT_c = row(mx("E", WHITE, 44), mx("=", WHITE, 44), frac(mx(r"h\,c", WHITE, 44), mx(r"\lambda", WHITE, 44)))
        RAP_c = txm(r"Rappel : $E = h\,\nu$ et $\nu = c / \lambda$", 22, SOFT, w=10.0)
        pg = VGroup(LIT_c, RAP_c).arrange(DOWN, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q4_lit"])
        self.p(Write(LIT_c), rt=1.0)
        self.encadre(LIT_c)
        self.at(T["q4_rap"])
        self.p(FadeIn(RAP_c), rt=0.8)
        self.at(T["q4_rep"])
        self.reponse(r"L'énergie du photon s'écrit $E = \frac{h\,c}{\lambda}$.", rt=0.8)
        self.at(T["q5"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 3, question 5 : longueur d'onde ----------
        self.at(T["q5"])
        self.set_q("Ex. 3 · Q5")
        self.question([r"5. Calculer la longueur d'onde $\lambda$ de la radiation correspondante."])
        LIT_d = row(mx(r"\lambda", WHITE, 40), mx("=", WHITE, 40), frac(mx(r"h\,c", WHITE, 40), mx(r"\Delta E", WHITE, 40)))
        DON_d = row(tx("Donnée :", 24, SOFT), mx(r"1\ \mathrm{eV} = 1{,}60\times10^{-19}\ \mathrm{J}", WHITE, 36))
        pg = VGroup(LIT_d, DON_d).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q5_lit"])
        self.p(Write(LIT_d), rt=1.0)
        self.encadre(LIT_d)
        self.at(T["q5_don"])
        self.p(FadeIn(DON_d), rt=0.8)
        self.at(T["q5_conv"] - 0.5)
        self.vider(rt=0.4, garder=(self.cur_q,))

        # Conversion de ΔE en joules
        cE = val("3{,}38", r"\mathrm{eV}", WHITE, 36)
        cC = val(r"1{,}60\times10^{-19}", (r"\mathrm{J\cdot}", r"\mathrm{eV}^{-1}"), WHITE, 36)
        AN_cj = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), cE, mx(r"\times", WHITE, 36), cC)
        RS_cj = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), val(r"5{,}41\times10^{-19}", r"\mathrm{J}", RES, 40))
        pg = VGroup(AN_cj, RS_cj).arrange(DOWN, aligned_edge=LEFT, buff=0.9)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q5_conv"])
        self.p(Write(AN_cj), rt=1.0)
        self.tag_an(AN_cj)
        self.at(T["q5_bar_cj"])
        self.barrer(cE[1][0], cC[1][1], rt=0.6)
        self.at(T["q5_res_cj"])
        self.p(Write(RS_cj), rt=0.7)
        self.at(T["q5_an"] - 0.4)
        self.vider(rt=0.3, garder=(self.cur_q,))

        # Calcul de λ
        hv5 = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 36)
        cv5 = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 36)
        dv5 = val(r"5{,}41\times10^{-19}", r"\mathrm{J}", WHITE, 36)
        AN_l = row(mx(r"\lambda", WHITE, 40), mx("=", WHITE, 40), frac(row(hv5, mx(r"\times", WHITE, 36), cv5), dv5))
        RS_l = row(mx(r"\lambda", WHITE, 40), mx("=", WHITE, 40), val(r"3{,}68\times10^{-7}", r"\mathrm{m}", RES, 40))
        CV_l = row(mx(r"\lambda", WHITE, 40), mx("=", WHITE, 40), val("368", r"\mathrm{nm}", RES, 40))
        pg = VGroup(AN_l, RS_l, CV_l).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q5_an"])
        self.p(Write(AN_l), rt=1.0)
        self.tag_an(AN_l)
        self.at(T["q5_bar"])
        self.barrer(hv5[1][0], hv5[1][1], cv5[1][1], dv5[1][0], rt=0.4)
        self.at(T["q5_res"])
        self.p(Write(RS_l), rt=0.7)
        self.at(T["q5_nm"])
        self.p(Write(CV_l), rt=0.7)
        self.at(T["q5_rep"])
        self.reponse(r"La longueur d'onde vaut $\lambda = 368\ \mathrm{nm}$.", rt=0.8)
        self.at(T["q6"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 3, question 6 : fréquence du photon ----------
        self.at(T["q6"])
        self.set_q("Ex. 3 · Q6")
        self.question([r"6. Déterminer la fréquence $\nu$ de ce photon."])
        NU_REL = row(mx(r"\Delta E", WHITE, 40), mx("=", WHITE, 40), mx("h", WHITE, 40), mx(r"\nu", WHITE, 40))
        self.at(T["q6_rel"])
        self.p(Write(NU_REL), rt=0.9)
        self.at(T["q6_vid"])
        self.vider(rt=0.4, garder=(self.cur_q,))

        RAP6 = txm(r"Donnée : $\Delta E = 5{,}41\times10^{-19}\ \mathrm{J}$ (question 5)", 22, SOFT, w=12.0)
        NU_LIT = row(mx(r"\nu", WHITE, 40), mx("=", WHITE, 40), frac(mx(r"\Delta E", WHITE, 40), mx("h", WHITE, 40)))
        num6 = val(r"5{,}41\times10^{-19}", r"\mathrm{J}", WHITE, 36)
        den6 = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 36)
        NU_AN = row(mx(r"\nu", WHITE, 40), mx("=", WHITE, 40), frac(num6, den6))
        NU_RES = row(mx(r"\nu", WHITE, 40), mx("=", WHITE, 40), val(r"8{,}16\times10^{14}", r"\mathrm{Hz}", RES, 40))
        pg = VGroup(RAP6, NU_LIT, NU_AN, NU_RES).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q6_lit"])
        self.p(Write(NU_LIT), rt=1.0)
        self.encadre(NU_LIT)
        self.at(T["q6_an"])
        self.p(FadeIn(RAP6), Write(NU_AN), rt=1.2)
        self.tag_an(NU_AN)
        self.at(T["q6_bar"])
        self.barrer(num6[1][0], den6[1][0])
        self.at(T["q6_res"])
        self.p(Write(NU_RES), rt=1.0)
        self.at(T["q6_rep"])
        self.reponse(r"La fréquence du photon vaut $\nu = 8{,}16\times10^{14}\ \mathrm{Hz}$.", rt=0.8)
        self.at(T["ex4"] - 0.6)
        self.vider(rt=0.4)

        # ---------- Exercice 4 : introduction et diagramme de l'hydrogène ----------
        self.at(T["ex4"])
        intro4 = tx("Exercice 4 : spectre d'émission de l'hydrogène", 34, WHITE)
        self.p(FadeIn(intro4, shift=UP * 0.2), rt=0.8)
        self.at(T["ex4_diag"] - 0.6)
        self.p(FadeOut(intro4), rt=0.6)
        self.at(T["ex4_diag"])
        D_H = niveaux_h()
        self.p(FadeIn(D_H), rt=1.0)

        # ---------- Exercice 4, question 1 : énergie de l'état fondamental ----------
        self.at(T["q1h"])
        self.set_q("Ex. 4 · Q1")
        self.question(["1. Quelle est la valeur de l'énergie de l'état fondamental de l'atome d'hydrogène ?"])
        self.at(T["q1h_hl"])
        self.p(Indicate(D_H[2], color=RES, scale_factor=1.15), rt=1.0)
        MARQ = marque_h()
        self.at(T["q1h_marq"])
        self.p(FadeIn(MARQ), rt=0.8)
        self.at(T["q1h_rep"])
        self.reponse(r"L'état fondamental a pour énergie $E_1 = -13{,}6\ \mathrm{eV}$, le niveau le plus bas.", rt=0.8)
        self.at(T["q2h"] - 0.4)
        self.vider(rt=0.4, garder=(D_H, MARQ))

        # ---------- Exercice 4, question 2 : énergie d'excitation ----------
        self.at(T["q2h"])
        self.set_q("Ex. 4 · Q2")
        self.question(["2. Quelle est l'énergie minimale, en électron-volts, à fournir à l'atome pour l'exciter ?"])
        self.at(T["q2h_fl"])
        FL_h2 = fleche_h(1, 2, ABSO)
        self.p(Create(FL_h2), rt=0.8)
        LIT_h2 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), mx(r"E_2 - E_1", WHITE, 36))
        AN_h2 = mx(r"\Delta E = (-3{,}39\ \mathrm{eV}) - (-13{,}6\ \mathrm{eV})", WHITE, 34)
        RS_h2 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), val("10{,}2", r"\mathrm{eV}", RES, 36))
        pg = VGroup(LIT_h2, AN_h2, RS_h2).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q2h_lit"])
        self.p(Write(LIT_h2), rt=1.0)
        self.encadre(LIT_h2)
        self.at(T["q2h_an"])
        self.p(Write(AN_h2), rt=1.2)
        self.tag_an(AN_h2)
        self.at(T["q2h_res"])
        self.p(Write(RS_h2), rt=1.0)
        self.at(T["q2h_rep"])
        self.reponse(r"Il faut fournir $10{,}2\ \mathrm{eV}$ à l'atome d'hydrogène pour l'exciter.", rt=0.8)
        self.at(T["q3h"] - 0.6)
        self.vider(rt=0.4, garder=(D_H, MARQ))

        # ---------- Exercice 4, question 3 : variation d'énergie ----------
        self.at(T["q3h"])
        self.set_q("Ex. 4 · Q3")
        self.question([r"3. Calculer la variation d'énergie $\Delta E$ de l'atome lorsqu'il passe",
                       r"de l'état d'énergie $-0{,}37\ \mathrm{eV}$ à l'état d'énergie $-3{,}39\ \mathrm{eV}$."])
        LIT_h3 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), mx(r"E_{\mathrm{finale}} - E_{\mathrm{initiale}}", WHITE, 36))
        AN_h3 = mx(r"\Delta E = (-3{,}39\ \mathrm{eV}) - (-0{,}37\ \mathrm{eV})", WHITE, 34)
        RS_h3 = row(mx(r"\Delta E", WHITE, 36), mx("=", WHITE, 36), val("-3{,}02", r"\mathrm{eV}", RES, 36))
        pg = VGroup(LIT_h3, AN_h3, RS_h3).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q3h_lit"])
        self.p(Write(LIT_h3), rt=1.0)
        self.encadre(LIT_h3)
        self.at(T["q3h_an"])
        self.p(Write(AN_h3), rt=1.2)
        self.tag_an(AN_h3)
        self.at(T["q3h_res"])
        self.p(Write(RS_h3), rt=1.0)
        self.at(T["q3h_rep"])
        self.reponse(r"Au cours de cette transition, l'atome perd $3{,}02\ \mathrm{eV}$.", rt=0.8)
        self.at(T["q4h"] - 0.6)
        self.vider(rt=0.4)

        # ---------- Exercice 4, question 4 : conversion en joules ----------
        self.at(T["q4h"])
        self.set_q("Ex. 4 · Q4")
        self.question([r"4. Convertir en joules l'énergie perdue par l'atome à la question 3, soit $3{,}02\ \mathrm{eV}$."])
        LIT_h4 = row(mx(r"E_{\mathrm{J}}", WHITE, 36), mx("=", WHITE, 36), mx(r"E_{\mathrm{eV}}", WHITE, 36),
                     mx(r"\times", WHITE, 36), mx(r"1{,}60\times10^{-19}\ \mathrm{J\cdot eV^{-1}}", WHITE, 36))
        cE4 = val("3{,}02", r"\mathrm{eV}", WHITE, 36)
        cC4 = val(r"1{,}60\times10^{-19}", (r"\mathrm{J\cdot}", r"\mathrm{eV}^{-1}"), WHITE, 36)
        AN_h4 = row(mx(r"E_{\mathrm{J}}", WHITE, 36), mx("=", WHITE, 36), cE4, mx(r"\times", WHITE, 36), cC4)
        RS_h4 = row(mx(r"E_{\mathrm{J}}", WHITE, 40), mx("=", WHITE, 40), val(r"4{,}83\times10^{-19}", r"\mathrm{J}", RES, 40))
        pg = VGroup(LIT_h4, AN_h4, RS_h4).arrange(DOWN, aligned_edge=LEFT, buff=0.8)
        self.caser(pg, top=self.haut() - 0.6)
        self.at(T["q4h_lit"])
        self.p(Write(LIT_h4), rt=1.0)
        self.encadre(LIT_h4)
        self.at(T["q4h_an"])
        self.p(Write(AN_h4), rt=1.2)
        self.tag_an(AN_h4)
        self.at(T["q4h_bar"])
        self.barrer(cE4[1][0], cC4[1][1])
        self.at(T["q4h_res"])
        self.p(Write(RS_h4), rt=1.0)
        self.at(T["q4h_rep"])
        self.reponse(r"L'énergie perdue par l'atome vaut $4{,}83\times10^{-19}\ \mathrm{J}$.", rt=0.8)
        self.at(T["q5h"] - 0.5)
        self.vider(rt=0.4)

        # ---------- Exercice 4, question 5 : flèche de la transition ----------
        self.at(T["q5h"])
        self.set_q("Ex. 4 · Q5")
        self.question(["5. Représenter cette transition par une flèche sur le diagramme."])
        D5 = niveaux_h()
        MARQ5 = marque_h()
        self.at(T["q5h_diag"])
        self.p(FadeIn(D5), FadeIn(MARQ5), rt=1.0)
        self.at(T["q5h_fl"])
        FL5 = fleche_h(6, 2, MAGENTA)
        self.p(Create(FL5), rt=1.0)
        self.at(T["q5h_rep"])
        self.reponse(r"La flèche relie le niveau 6 au niveau 2, vers le bas : la transition est une émission.", rt=0.8)
        self.at(T["q6h"] - 0.4)
        self.vider(rt=0.3, garder=(D5, MARQ5, FL5))

        # ---------- Exercice 4, question 6 : photon libéré ou absorbé ----------
        self.at(T["q6h"])
        self.set_q("Ex. 4 · Q6")
        self.question(["6. Le photon mis en jeu est-il libéré ou absorbé par l'atome ?"])
        TXT6 = tx("Énergie qui diminue : l'atome émet un photon", 24, MAGENTA, w=6.0).move_to([3.2, 0.0, 0])
        self.at(T["q6h_txt"])
        self.p(FadeIn(TXT6, shift=LEFT * 0.2), rt=0.8)
        self.at(T["q6h_rep"])
        self.reponse(r"Le photon est libéré : l'atome émet un photon en passant du niveau 6 au niveau 2.", rt=0.8)
        self.at(T["q7h"] - 0.5)
        self.vider(rt=0.4, garder=(D5, MARQ5, FL5))

        # ---------- Exercice 4, question 7 : longueur d'onde du photon émis ----------
        self.at(T["q7h"])
        self.set_q("Ex. 4 · Q7")
        self.question([r"7. Calculer la longueur d'onde $\lambda$ du photon correspondant à cette transition."])
        LIT_7 = row(mx(r"\lambda", WHITE, 36), mx("=", WHITE, 36), frac(mx(r"h\,c", WHITE, 36), mx(r"\Delta E", WHITE, 36)))
        ATT_7 = txm(r"Attention : $\Delta E$ doit être en joules, et non en électron-volts", 22, ABSO, w=6.4)
        pg1 = VGroup(LIT_7, ATT_7).arrange(DOWN, aligned_edge=LEFT, buff=0.7)
        self.caser(pg1, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q7h_lit"])
        self.p(Write(LIT_7), rt=1.0)
        self.encadre(LIT_7)
        self.at(T["q7h_att"])
        self.p(FadeIn(ATT_7), rt=0.6)
        self.at(T["q7h_an"] - 0.9)
        self.vider(rt=0.4, garder=(self.cur_q, D5, MARQ5, FL5))

        hv7 = val(r"6{,}63\times10^{-34}", (r"\mathrm{J\cdot}", r"\mathrm{s}"), WHITE, 36)
        cv7 = val(r"3{,}00\times10^{8}", (r"\mathrm{m\cdot}", r"\mathrm{s^{-1}}"), WHITE, 36)
        dv7 = val(r"4{,}83\times10^{-19}", r"\mathrm{J}", WHITE, 36)
        AN_7 = row(mx(r"\lambda", WHITE, 36), mx("=", WHITE, 36), frac(row(hv7, mx(r"\times", WHITE, 36), cv7), dv7))
        RS_7 = row(mx(r"\lambda", WHITE, 36), mx("=", WHITE, 36), val(r"4{,}12\times10^{-7}", r"\mathrm{m}", RES, 36))
        CV_7 = row(mx(r"\lambda", WHITE, 36), mx("=", WHITE, 36), val("412", r"\mathrm{nm}", RES, 36))
        pg2 = VGroup(AN_7, RS_7, CV_7).arrange(DOWN, aligned_edge=LEFT, buff=0.6)
        self.caser(pg2, top=self.haut() - 0.6, x=3.6, w=6.4)
        self.at(T["q7h_an"])
        self.p(Write(AN_7), rt=1.2)
        self.tag_an(AN_7)
        self.at(T["q7h_bar"])
        self.barrer(hv7[1][0], hv7[1][1], cv7[1][1], dv7[1][0])
        self.at(T["q7h_res"])
        self.p(Write(RS_7), rt=1.0)
        self.at(T["q7h_conv"])
        self.p(Write(CV_7), rt=1.0)
        self.at(T["q7h_rep"])
        self.reponse(r"Le photon a une longueur d'onde de $412\ \mathrm{nm}$ : il est dans le domaine visible, de couleur violette.", rt=0.8)
        self.at(T["fin"])
        self.pause(2.0)
