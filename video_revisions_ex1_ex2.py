from manim import *
import math

# =====================================================================
#  Seconde – Révisions du collège : correction des exercices 1 et 2 (puissances de 10)
#  Vidéo muette calée sur le SRT de l'enregistrement (≈ 3 min 20). Pas de 3D.
#  Manim Community, rendu sur GitHub.
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
ZONE_BAS = -2.55     # bas de la zone de travail (en dessous : phrase réponse)
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
    u = VGroup(*[mx(p, UNIT, fs) for p in parts]).arrange(RIGHT, buff=0.04)
    return VGroup(mx(num, c, fs), u).arrange(RIGHT, buff=0.12)


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

# ---------- Minutage : d'après le SRT (TurboScribe) ----------
T = {
    "titre": 0.65, "ex1": 4.81, "idee": 7.55, "zeros_apres": 11.35, "zeros_avant": 16.01,
    "positif": 20.95, "autant": 28.15, "ex_10_4": 31.53, "dix_mille": 37.29,
    "negatif": 39.31, "meme_chose": 49.01, "methode": 55.57, "prendre_exp": 59.47, "isoler": 62.63,
    "trois_zeros": 69.79, "ex_10_m3": 72.33, "en_comptant": 78.19,
    "liste": 82.31, "un_centieme": 85.19, "pas_tous": 87.71,
    "ex2": 90.71, "regle_prod": 100.07, "additionne": 107.71, "regle_div": 113.51, "dessus": 118.0, "dessous": 122.45,
    "regle_pp": 124.85, "n_fois_p": 133.19,
    "A": 135.71, "A_somme": 141.79, "A_res": 143.3,
    "B": 145.37, "B_somme": 153.01, "B_res": 155.73,
    "C": 159.16, "C_dessus": 164.48, "C_diff": 167.0, "C_res": 170.0,
    "F": 172.12, "F_num": 178.6, "F_trois": 181.32, "F_div": 185.28, "F_res": 188.0,
}


def puiss(exp, fs=56, base_col=WHITE):
    """10 puissance (exposant) ; exp = liste de (texte LaTeX, couleur). [0] = « 10 », [1] = exposant (morceaux indexables)."""
    b = mx("10", base_col, fs)
    e = VGroup(*[mx(s, c, fs * 0.62) for s, c in exp]).arrange(RIGHT, buff=0.04)
    e.next_to(b, RIGHT, buff=0.05).align_to(b, UP).shift(UP * 0.2 * fs / 56)
    return VGroup(b, e)


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


# =====================================================================
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
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.cur_q = None
        self.sous_titre = None
        self.titre()
        self.ex1_methode()
        self.ex1_positif()
        self.ex1_negatif()
        self.ex1_reponses()
        self.ex2_regles()
        self.ex2_calculs()
        self.ex2_bilan()

    # ---------- outils propres à cette vidéo ----------
    def changer_titre(self, s):
        nv = tx(s, 22, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(self.hdr_ex, nv), rt=0.5)
        self.hdr_ex = nv
        if self.hdr_q is not None:
            self.hdr_q.next_to(nv, RIGHT, buff=0.3)

    def carte_regle(self, lignes, col, titre=None, w=12.0):
        g = VGroup(*lignes).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        ajuster(g, w)
        cad = SurroundingRectangle(g, color=col, buff=0.25, corner_radius=0.12, stroke_width=2.5).set_fill("#1B1F27", 0.9)
        out = VGroup(cad, g)
        if titre:
            out.add(tx(titre, 20, col, bold=True).next_to(cad, UP, buff=0.08).align_to(cad, LEFT))
        return out

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        self.at(T["titre"])
        t1 = tx("Révisions du collège", 54, WHITE, bold=True)
        t2 = tx("Correction · Exercices 1 et 2 : les puissances de 10", 30, PUIS_C)
        dec = VGroup(*[puiss([(s, c)], 44) for s, c in (("3", EXP_P), ("-2", EXP_N), ("6", EXP_P), ("0", SOFT))]).arrange(RIGHT, buff=1.0)
        bloc = VGroup(t1, t2, dec).arrange(DOWN, buff=0.5)
        self.p(Write(t1), rt=1.0)
        self.p(FadeIn(t2, shift=UP * 0.2), LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in dec], lag_ratio=0.2), rt=1.4)
        self.hdr_ex = tx("Exercice 1 : les puissances de 10", 22, SOFT).to_corner(UL, buff=0.3)
        self.at(T["ex1"] - 0.6)
        self.p(ReplacementTransform(t1, self.hdr_ex), FadeOut(VGroup(t2, dec)), rt=0.6)

    # =================================================================
    #  EXERCICE 1 – la méthode des zéros
    # =================================================================
    def ex1_methode(self):
        self.at(T["ex1"])
        self.question("Compléter les égalités : écrire chaque puissance de 10 en nombre décimal, ou l'inverse.")
        idee = tx("L'idée : compter le bon nombre de zéros.", 30, PUIS_C, bold=True).move_to(UP * 1.4)
        self.at(T["idee"])
        self.p(Write(idee), rt=1.0)
        l1 = row(puiss([("n", EXP_P)], 52), tx(": un 1 suivi de n zéros", 28, WHITE), buff=0.4)
        l2 = row(puiss([("-n", EXP_N)], 52), tx(": n zéros en tout, puis le 1", 28, WHITE), buff=0.4)
        VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.55).next_to(idee, DOWN, buff=0.7)
        self.at(T["zeros_apres"])
        self.p(FadeIn(l1, shift=RIGHT * 0.2), rt=0.8)
        self.at(T["zeros_avant"])
        self.p(FadeIn(l2, shift=RIGHT * 0.2), rt=0.8)
        self.pause(1.0)
        self.vider(garder=(self.cur_q,))

    def ex1_positif(self):
        self.at(T["positif"])
        self.set_q("Exposant positif")
        r = self.carte_regle([txm(r"Exposant positif : le nombre est supérieur à 1.", 28, WHITE),
                              txm(r"Il y a autant de zéros que l'exposant.", 28, EXP_P)], EXP_P, "à retenir")
        r.move_to(UP * 1.2)
        self.p(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1][0], shift=UP * 0.1), rt=0.8)
        self.at(T["autant"])
        self.p(FadeIn(r[1][1], shift=UP * 0.1), rt=0.6)
        # 10^4 = 10 000 : les zéros sortent un par un de l'exposant
        self.at(T["ex_10_4"])
        p4 = puiss([("4", EXP_P)], 72).move_to([-3.6, -1.4, 0])
        eg = mx("=", WHITE, 72).next_to(p4, RIGHT, buff=0.4)
        chif = chiffres("10 000", 72, WHITE).next_to(eg, RIGHT, buff=0.4)
        self.p(Write(p4), FadeIn(eg), rt=0.8)
        self.p(Indicate(p4[1], color=EXP_P, scale_factor=1.5), rt=0.8)
        self.p(FadeIn(chif[0], shift=UP * 0.2), rt=0.4)
        cpt = VGroup()
        for i, z in enumerate(chif[1:]):
            n = mx(str(i + 1), EXP_P, 30).next_to(z, DOWN, buff=0.2)
            cpt.add(n)
            self.p(TransformFromCopy(p4[1], z, path_arc=-0.8), FadeIn(n, shift=UP * 0.1), rt=0.45)
        self.at(T["dix_mille"])
        self.p(Circumscribe(chif, color=RES), rt=0.8)
        self.vider(garder=(self.cur_q,))

    def ex1_negatif(self):
        self.at(T["negatif"])
        self.set_q("Exposant négatif")
        r = self.carte_regle([txm(r"Exposant négatif : le nombre est inférieur à 1, il s'écrit 0,…", 28, WHITE),
                              txm(r"On écrit 0, puis des zéros, puis un 1.", 28, EXP_N)], EXP_N, "à retenir")
        r.move_to(UP * 1.2)
        self.p(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1][0], shift=UP * 0.1), rt=0.8)
        self.at(T["meme_chose"])
        self.p(FadeIn(r[1][1], shift=UP * 0.1), rt=0.6)
        # méthode avec 10^-3
        self.at(T["methode"])
        p3 = puiss([("-", EXP_N), ("3", EXP_N)], 72).move_to([-3.8, -1.3, 0])
        self.p(Write(p3), rt=0.8)
        self.at(T["prendre_exp"])
        self.p(Indicate(p3[1], color=EXP_N, scale_factor=1.5), rt=0.8)
        self.at(T["isoler"])
        moins = p3[1][0]
        n_l = tx("négatif → inférieur à 1", 20, EXP_N).next_to(p3, DOWN, buff=0.45)
        self.p(moins.animate.set_color(SOFT).set_opacity(0.4), FadeIn(n_l, shift=UP * 0.1), rt=0.8)
        self.p(Indicate(p3[1][1], color=EXP_N, scale_factor=1.6), rt=0.8)
        self.at(T["trois_zeros"])
        cible = tx("il faut 3 zéros en tout", 24, EXP_N).next_to(n_l, DOWN, buff=0.2)
        self.p(FadeIn(cible), rt=0.6)
        # 10^-3 = 0,001
        self.at(T["ex_10_m3"])
        eg = mx("=", WHITE, 72).next_to(p3, RIGHT, buff=0.4)
        ch = chiffres("0,001", 72, WHITE).next_to(eg, RIGHT, buff=0.4)
        self.p(FadeIn(eg), rt=0.3)
        zeros = [ch[0], ch[2], ch[3]]
        cpt = VGroup()
        for i, z in enumerate(zeros):
            n = mx(str(i + 1), EXP_N, 30).next_to(z, DOWN, buff=0.2)
            cpt.add(n)
            anims = [TransformFromCopy(p3[1][1], z, path_arc=-0.8), FadeIn(n, shift=UP * 0.1)]
            if i == 1:
                anims.append(FadeIn(ch[1]))
            self.p(*anims, rt=0.45)
        self.p(FadeIn(ch[4], shift=UP * 0.2), rt=0.4)
        self.at(T["en_comptant"])
        self.p(Indicate(ch[0], color=EXP_N, scale_factor=1.4), Indicate(cpt[0], color=EXP_N), rt=1.0)
        n_av = tx("le zéro avant la virgule compte !", 22, EXP_N).next_to(ch, UP, buff=0.45)
        self.p(FadeIn(n_av, shift=UP * 0.1), rt=0.6)
        self.p(Circumscribe(ch, color=RES), rt=0.8)
        self.vider(garder=(self.cur_q,))

    def ex1_reponses(self):
        self.at(T["liste"])
        self.set_q("Les réponses")
        fs = 46
        def eg(gauche, droite, num):
            return row(tx("%d)" % num, 26, SOFT), gauche, mx("=", WHITE, fs), droite, buff=0.3)
        L = [eg(puiss([("4", EXP_P)], fs), mx(r"10\,000", RES, fs), 1),
             eg(puiss([("-3", EXP_N)], fs), mx(r"0{,}001", RES, fs), 2),
             eg(mx(r"1\,000\,000", WHITE, fs), puiss([("6", RES)], fs, RES), 3),
             eg(mx(r"0{,}01", WHITE, fs), puiss([("-2", RES)], fs, RES), 4),
             eg(mx(r"0{,}000\,1", WHITE, fs), puiss([("-4", RES)], fs, RES), 5),
             eg(mx("1", WHITE, fs), puiss([("0", RES)], fs, RES), 6)]
        col1 = VGroup(*L[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        col2 = VGroup(*L[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        page = row(col1, col2, buff=1.6)
        self.caser(page, top=self.haut() - 0.4, x=0.0, w=12.0)
        self.p(FadeIn(L[0]), FadeIn(L[1]), rt=0.6)
        self.p(FadeIn(L[2], shift=RIGHT * 0.2), rt=0.6)
        c6 = tx("6 zéros", 20, EXP_P).next_to(L[2], DOWN, buff=0.12).align_to(L[2][1], LEFT)
        self.p(FadeIn(c6), rt=0.4)
        self.at(T["un_centieme"])
        self.p(FadeIn(L[3], shift=RIGHT * 0.2), rt=0.6)
        c2 = tx("2 zéros en tout", 20, EXP_N).next_to(L[3], DOWN, buff=0.12).align_to(L[3][1], LEFT)
        self.p(FadeIn(c2), rt=0.4)
        self.at(T["pas_tous"])
        self.p(LaggedStart(FadeIn(L[4], shift=RIGHT * 0.2), FadeIn(L[5], shift=RIGHT * 0.2), lag_ratio=0.5), rt=1.2)
        note = txm(r"$10^{0} = 1$ : aucun zéro.", 20, SOFT).next_to(page, DOWN, buff=0.4)
        self.p(FadeIn(note), rt=0.4)
        self.vider_tout()
        self.cur_q = None

    # =================================================================
    #  EXERCICE 2 – les règles de calcul
    # =================================================================
    def ex2_regles(self):
        self.at(T["ex2"])
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        self.changer_titre("Exercice 2 : calculer avec les puissances de 10")
        self.question("Sans calculatrice, écrire chaque expression sous la forme d'une seule puissance de 10.")
        fs = 50
        r1 = row(puiss([("n", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("p", EXP_Q)], fs), mx("=", WHITE, fs),
                 puiss([("n", EXP_P), ("+", WHITE), ("p", EXP_Q)], fs), buff=0.18)
        r2 = row(frac(puiss([("n", EXP_P)], fs), puiss([("p", EXP_Q)], fs)), mx("=", WHITE, fs),
                 puiss([("n", EXP_P), ("-", WHITE), ("p", EXP_Q)], fs), buff=0.18)
        r3 = row(mx("(", WHITE, fs), puiss([("n", EXP_P)], fs), mx(")", WHITE, fs), buff=0.05)
        exp_p = mx("p", EXP_Q, fs * 0.62).next_to(r3, RIGHT, buff=0.04).align_to(r3, UP).shift(UP * 0.12)
        r3 = row(VGroup(r3, exp_p), mx("=", WHITE, fs), puiss([("n", EXP_P), (r"\times", WHITE), ("p", EXP_Q)], fs), buff=0.18)
        c1 = tx("on multiplie → on additionne les exposants", 22, WHITE)
        c2 = tx("on divise → exposant du dessus moins exposant du dessous", 22, WHITE)
        c3 = tx("puissance d'une puissance → on multiplie les exposants", 22, WHITE)
        lignes = VGroup(*[VGroup(r, c).arrange(RIGHT, buff=0.7) for r, c in ((r1, c1), (r2, c2), (r3, c3))])
        lignes.arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        x_c = max(l[0].get_right()[0] for l in lignes) + 0.7
        for l in lignes:
            l[1].move_to([x_c, l[0].get_y(), 0], aligned_edge=LEFT)
        self.caser(lignes, top=self.haut() - 0.3, x=0.0, w=12.6)
        self.at(T["regle_prod"])
        self.p(Write(lignes[0][0]), rt=1.6)
        self.at(T["additionne"])
        self.p(FadeIn(lignes[0][1], shift=LEFT * 0.2), Indicate(lignes[0][0][4][1], color=RES, scale_factor=1.3), rt=1.0)
        self.at(T["regle_div"])
        self.p(Write(lignes[1][0]), rt=1.6)
        self.at(T["dessus"])
        self.p(Indicate(lignes[1][0][0][0][1], color=EXP_P, scale_factor=1.5), rt=0.8)
        self.at(T["dessous"])
        self.p(Indicate(lignes[1][0][0][2][1], color=EXP_Q, scale_factor=1.5), FadeIn(lignes[1][1], shift=LEFT * 0.2), rt=1.0)
        self.at(T["regle_pp"])
        self.p(Write(lignes[2][0]), rt=1.6)
        self.at(T["n_fois_p"])
        self.p(FadeIn(lignes[2][1], shift=LEFT * 0.2), Indicate(lignes[2][0][2][1], color=RES, scale_factor=1.3), rt=1.0)
        self.lignes_regles = lignes

    def ex2_calculs(self):
        self.at(T["A"] - 0.8)
        # les règles se rangent en petit en haut à droite
        mini = VGroup(*[l[0].copy() for l in self.lignes_regles]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.5)
        cad = SurroundingRectangle(mini, color=SOFT, buff=0.15, corner_radius=0.1, stroke_width=1.5)
        aide = VGroup(cad, mini).to_corner(UR, buff=0.3).shift(DOWN * 0.5)
        self.p(FadeOut(self.cur_q), FadeOut(VGroup(*[l[1] for l in self.lignes_regles])),
               ReplacementTransform(VGroup(*[l[0] for l in self.lignes_regles]), mini), FadeIn(cad), rt=0.8)
        self.cur_q = None
        fs = 56
        x_g = -6.3

        def ligne(nom, *morceaux, y):
            g = row(mx(nom, WHITE, fs), mx("=", WHITE, fs), *morceaux, buff=0.2)
            g.move_to([x_g, y, 0], aligned_edge=LEFT)
            return g
        # A
        self.set_q("A")
        a0 = ligne("A", puiss([("2", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("5", EXP_Q)], fs), y=2.0)
        self.p(Write(a0), rt=1.0)
        a1 = puiss([("2", EXP_P), ("+", WHITE), ("5", EXP_Q)], fs)
        a2 = puiss([("7", RES)], fs, RES)
        eg1, eg2 = mx("=", WHITE, fs), mx("=", WHITE, fs)
        suite = row(eg1, a1, eg2, a2, buff=0.2).next_to(a0, RIGHT, buff=0.2)
        self.at(T["A_somme"])
        self.p(FadeIn(eg1), FadeIn(a1[0]), TransformFromCopy(a0[2][1], a1[1][0], path_arc=-0.6),
               TransformFromCopy(a0[4][1], a1[1][2], path_arc=-0.6), FadeIn(a1[1][1]), rt=1.2)
        self.at(T["A_res"])
        self.p(FadeIn(eg2), TransformFromCopy(a1, a2), rt=0.9)
        self.p(Circumscribe(a2, color=RES), rt=0.7)
        # B
        self.at(T["B"])
        self.set_q("B")
        b0 = ligne("B", puiss([("-2", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("-4", EXP_Q)], fs), y=0.55)
        self.p(Write(b0), rt=1.0)
        b1 = puiss([("-2", EXP_P), ("+", WHITE), ("(-4)", EXP_Q)], fs)
        b2 = puiss([("-6", RES)], fs, RES)
        e1, e2 = mx("=", WHITE, fs), mx("=", WHITE, fs)
        row(e1, b1, e2, b2, buff=0.3).next_to(b0, RIGHT, buff=0.2)
        self.at(T["B_somme"])
        self.p(FadeIn(e1), FadeIn(b1[0]), TransformFromCopy(b0[2][1], b1[1][0], path_arc=-0.6),
               TransformFromCopy(b0[4][1], b1[1][2], path_arc=-0.6), FadeIn(b1[1][1]), rt=1.2)
        rap = txm(r"$-2 + (-4) = -2 - 4 = -6$", 24, SOFT).next_to(b1, DOWN, buff=0.25)
        self.at(T["B_res"])
        self.p(FadeIn(rap, shift=UP * 0.1), rt=0.6)
        self.p(FadeIn(e2), TransformFromCopy(b1, b2), rt=0.9)
        self.p(Circumscribe(b2, color=RES), rt=0.7)
        # C
        self.at(T["C"])
        self.set_q("C")
        c0 = row(mx("C", WHITE, fs), mx("=", WHITE, fs), frac(puiss([("8", EXP_P)], fs), puiss([("3", EXP_Q)], fs)), buff=0.2)
        c0.move_to([x_g, -1.55, 0], aligned_edge=LEFT)
        self.p(FadeOut(rap), Write(c0), rt=1.0)
        c1 = puiss([("8", EXP_P), ("-", WHITE), ("3", EXP_Q)], fs)
        c2 = puiss([("5", RES)], fs, RES)
        f1, f2 = mx("=", WHITE, fs), mx("=", WHITE, fs)
        row(f1, c1, f2, c2, buff=0.2).next_to(c0, RIGHT, buff=0.2)
        self.at(T["C_dessus"])
        self.p(Indicate(c0[2][0][1], color=EXP_P, scale_factor=1.5), rt=0.6)
        self.p(Indicate(c0[2][2][1], color=EXP_Q, scale_factor=1.5), rt=0.6)
        self.at(T["C_diff"])
        self.p(FadeIn(f1), FadeIn(c1[0]), TransformFromCopy(c0[2][0][1], c1[1][0], path_arc=-0.6),
               TransformFromCopy(c0[2][2][1], c1[1][2], path_arc=0.6), FadeIn(c1[1][1]), rt=1.2)
        self.at(T["C_res"])
        self.p(FadeIn(f2), TransformFromCopy(c1, c2), rt=0.8)
        self.p(Circumscribe(c2, color=RES), rt=0.6)
        self.vider(garder=(aide,))
        # F : le cas qui rassemble tout
        self.at(T["F"])
        self.set_q("F")
        num = row(puiss([("5", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("-2", EXP_Q)], fs), buff=0.15)
        F0 = row(mx("F", WHITE, fs), mx("=", WHITE, fs), frac(num, puiss([("4", EXP_R)], fs)), buff=0.2)
        F0.move_to([x_g, 0.9, 0], aligned_edge=LEFT)
        self.p(Write(F0), rt=1.4)
        tout = tx("on applique les règles une par une", 22, SOFT).next_to(F0, DOWN, buff=0.3).align_to(F0, LEFT)
        self.p(FadeIn(tout), rt=0.5)
        # étape 1 : le numérateur
        self.at(T["F_num"])
        n1 = puiss([("5", EXP_P), ("+", WHITE), ("(-2)", EXP_Q)], fs)
        F1 = row(mx("=", WHITE, fs), frac(n1, puiss([("4", EXP_R)], fs)), buff=0.2).next_to(F0, RIGHT, buff=0.25)
        self.p(Indicate(num, color=EXP_P, scale_factor=1.05), rt=0.6)
        self.p(FadeIn(F1[0]), FadeIn(F1[1][0][0]), TransformFromCopy(num[0][1], n1[1][0], path_arc=-0.6),
               TransformFromCopy(num[2][1], n1[1][2], path_arc=-0.6), FadeIn(n1[1][1]), FadeIn(F1[1][1]),
               TransformFromCopy(F0[2][2], F1[1][2]), rt=1.2)
        self.at(T["F_trois"])
        F2 = row(mx("=", WHITE, fs), frac(puiss([("3", EXP_P)], fs), puiss([("4", EXP_R)], fs)), buff=0.2)
        F2.move_to([x_g + 1.2, -1.6, 0], aligned_edge=LEFT)
        self.p(FadeOut(tout), FadeIn(F2[0]), TransformFromCopy(F1[1], F2[1]), rt=1.0)
        # étape 2 : la division
        self.at(T["F_div"])
        F3 = row(mx("=", WHITE, fs), puiss([("3", EXP_P), ("-", WHITE), ("4", EXP_R)], fs), mx("=", WHITE, fs),
                 puiss([("-1", RES)], fs, RES), buff=0.2).next_to(F2, RIGHT, buff=0.25)
        self.p(FadeIn(F3[0]), FadeIn(F3[1][0]), TransformFromCopy(F2[1][0][1], F3[1][1][0], path_arc=-0.6),
               TransformFromCopy(F2[1][2][1], F3[1][1][2], path_arc=0.6), FadeIn(F3[1][1][1]), rt=1.2)
        self.at(T["F_res"])
        self.p(FadeIn(F3[2]), TransformFromCopy(F3[1], F3[3]), rt=0.8)
        self.p(Circumscribe(F3[3], color=RES), rt=0.7)
        self.pause(1.2)
        self.vider()

    def ex2_bilan(self):
        self.set_q("Toutes les réponses")
        fs = 44
        lig = [("A", [puiss([("2", EXP_P), ("+", WHITE), ("5", EXP_Q)], fs)], puiss([("7", RES)], fs, RES)),
               ("B", [puiss([("-2", EXP_P), ("+", WHITE), ("(-4)", EXP_Q)], fs)], puiss([("-6", RES)], fs, RES)),
               ("C", [puiss([("8", EXP_P), ("-", WHITE), ("3", EXP_Q)], fs)], puiss([("5", RES)], fs, RES)),
               ("D", [puiss([("3", EXP_P), ("-", WHITE), ("(-2)", EXP_Q)], fs)], puiss([("5", RES)], fs, RES)),
               ("E", [puiss([("-3", EXP_P), (r"\times", WHITE), ("2", EXP_Q)], fs)], puiss([("-6", RES)], fs, RES)),
               ("F", [puiss([("3", EXP_P), ("-", WHITE), ("4", EXP_R)], fs)], puiss([("-1", RES)], fs, RES))]
        rows = []
        for nom, mid, res in lig:
            rows.append(row(mx(nom, WHITE, fs), mx("=", WHITE, fs), *mid, mx("=", WHITE, fs), res, buff=0.25))
        col1 = VGroup(*rows[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        col2 = VGroup(*rows[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        page = row(col1, col2, buff=1.6)
        self.caser(page, top=2.3, x=0.0, w=12.4)
        self.p(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25), rt=2.2)
        note = tx("D et E : à refaire seuls, puis vérifier ici.", 22, SOFT).next_to(page, DOWN, buff=0.5)
        self.p(FadeIn(note), Indicate(rows[3], color=EXP_Q, scale_factor=1.04), Indicate(rows[4], color=EXP_Q, scale_factor=1.04), rt=1.2)
        self.pause(4.0)
