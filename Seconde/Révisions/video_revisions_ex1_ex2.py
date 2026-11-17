from manim import *
import math

# =====================================================================
#  Seconde – Révisions du collège : correction des exercices 1 et 2 (puissances de 10)
#  Vidéo muette calée sur le SRT du 2e enregistrement (≈ 3 min 55 avec l'écran final). Pas de 3D.
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

# ---------- Minutage : d'après le SRT (TurboScribe, 2e enregistrement) ----------
T = {
    "titre": 0.52, "ex1": 6.08, "idee": 9.42, "deux_cas": 20.48,
    "positif": 21.34, "un_puis_zeros": 27.30, "ex_10_4": 32.80,
    "negatif": 40.42, "forme_0": 51.64, "entre_0_1": 57.46,
    "methode": 62.54, "isoler": 69.40, "ecrire": 74.70, "compter": 78.36,
    "q3": 84.48, "q4": 90.86, "q4_res": 99.28, "laisse": 103.66,
    "ex2": 106.52, "regle_prod": 117.38, "additionne": 122.18, "regle_div": 127.32, "dessus": 131.22, "dessous": 133.58,
    "regle_pp": 137.50, "n_fois_p": 142.92, "exemples": 147.52,
    "A": 150.20, "A_somme": 152.12,
    "C": 159.44, "C_diff": 162.98, "C_res": 170.20,
    "E": 173.42, "E_imag": 180.34, "E_prop1": 184.84, "E_res": 187.22, "E_prop3": 191.04,
    "F": 197.88, "F_num": 209.24, "F_trois": 212.92, "F_div": 214.44, "F_res": 219.86,
}


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
        self.ex2_A_C()
        self.ex2_E()
        self.ex2_F()
        self.bilan_final()

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

    def puiss_pp(self, inner, outer, fs=56):
        """(10^inner)^outer ; [0] = parenthèse+puissance, [1] = exposant extérieur."""
        dedans = row(mx("(", WHITE, fs), puiss(inner, fs), mx(")", WHITE, fs), buff=0.05)
        e = VGroup(*[mx(s, c, fs * 0.62) for s, c in outer]).arrange(RIGHT, buff=0.04)
        e.next_to(dedans, RIGHT, buff=0.04).align_to(dedans, UP).shift(UP * 0.1 * fs / 56)
        return VGroup(dedans, e)

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        self.at(T["titre"])
        t1 = tx("Révisions du collège", 54, WHITE, bold=True)
        t2 = tx("Correction · Exercices 1 et 2 : les puissances de 10", 30, PUIS_C)
        dec = VGroup(*[puiss([(s, c)], 44) for s, c in (("3", EXP_P), ("-2", EXP_N), ("6", EXP_P), ("0", SOFT))]).arrange(RIGHT, buff=1.0)
        VGroup(t1, t2, dec).arrange(DOWN, buff=0.5)
        self.p(Write(t1), rt=1.0)
        self.p(FadeIn(t2, shift=UP * 0.2), LaggedStart(*[FadeIn(d, shift=UP * 0.2) for d in dec], lag_ratio=0.2), rt=1.4)
        self.hdr_ex = tx("Exercice 1 : les puissances de 10", 22, SOFT).to_corner(UL, buff=0.3)
        self.at(T["ex1"] - 0.6)
        self.p(ReplacementTransform(t1, self.hdr_ex), FadeOut(VGroup(t2, dec)), rt=0.6)

    # =================================================================
    #  EXERCICE 1
    # =================================================================
    def ex1_methode(self):
        self.at(T["ex1"])
        self.question("Compléter les égalités : écrire chaque puissance de 10 en nombre décimal, ou l'inverse.")
        self.at(T["idee"])
        ex = row(puiss([("4", EXP_P)], 60), mx("=", WHITE, 60), mx(r"\,?", RES, 60), buff=0.3).move_to(UP * 0.8)
        idee = tx("L'idée : écrire la valeur « en entier » de la puissance de 10.", 28, PUIS_C, bold=True).next_to(ex, DOWN, buff=0.6)
        self.p(FadeIn(ex, shift=UP * 0.15), rt=0.8)
        self.p(Write(idee), rt=1.2)
        self.at(T["deux_cas"] - 2.9)
        cas = VGroup(tx("2 cas :", 26, WHITE, bold=True), tx("exposant positif", 26, EXP_P), tx("ou", 26, SOFT),
                     tx("exposant négatif", 26, EXP_N)).arrange(RIGHT, buff=0.3).next_to(idee, DOWN, buff=0.7)
        self.p(FadeIn(cas, shift=UP * 0.1), rt=0.8)
        self.at(T["positif"] - 0.45)
        self.vider(garder=(self.cur_q,), rt=0.4)

    def ex1_positif(self):
        self.at(T["positif"])
        self.set_q("Exposant positif")
        r = self.carte_regle([txm(r"Exposant positif : le nombre est supérieur à 1.", 28, WHITE),
                              txm(r"On écrit un 1, puis autant de zéros que l'exposant.", 28, EXP_P)], EXP_P, "à retenir")
        r.move_to(UP * 1.2)
        self.p(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1][0], shift=UP * 0.1), rt=0.8)
        self.at(T["un_puis_zeros"])
        self.p(FadeIn(r[1][1], shift=UP * 0.1), rt=0.6)
        self.at(T["ex_10_4"])
        p4 = puiss([("4", EXP_P)], 72).move_to([-3.6, -1.4, 0])
        eg = mx("=", WHITE, 72).next_to(p4, RIGHT, buff=0.4)
        chif = chiffres("10 000", 72, WHITE).next_to(eg, RIGHT, buff=0.4)
        self.p(Write(p4), FadeIn(eg), rt=0.8)
        self.p(Indicate(p4[1], color=EXP_P, scale_factor=1.5), rt=0.8)
        self.p(FadeIn(chif[0], shift=UP * 0.2), rt=0.4)
        for i, z in enumerate(chif[1:]):
            n = mx(str(i + 1), EXP_P, 30).next_to(z, DOWN, buff=0.2)
            self.p(TransformFromCopy(p4[1], z, path_arc=-0.8), FadeIn(n, shift=UP * 0.1), rt=0.45)
        leg = txm(r"un 1 suivi de 4 zéros", 24, EXP_P).next_to(chif, UP, buff=0.35)
        self.p(FadeIn(leg), Circumscribe(chif, color=RES), rt=0.8)
        self.at(T["negatif"] - 0.55)
        self.vider(garder=(self.cur_q,), rt=0.5)

    def ex1_negatif(self):
        self.at(T["negatif"])
        self.set_q("Exposant négatif")
        r = self.carte_regle([txm(r"Exposant négatif : le nombre est inférieur à 1.", 28, WHITE),
                              txm(r"Il s'écrit 0,… : il est compris entre 0 et 1.", 28, EXP_N)], EXP_N, "à retenir")
        r.move_to(UP * 1.3)
        self.p(FadeIn(r[0]), FadeIn(r[2]), FadeIn(r[1][0], shift=UP * 0.1), rt=0.8)
        self.at(T["forme_0"])
        self.p(FadeIn(r[1][1], shift=UP * 0.1), rt=0.6)
        # droite graduée de 0 à 1 (puis de 1 à 10 000, en compressé)
        self.at(T["entre_0_1"])
        y = -1.3
        d = Line([-5.5, y, 0], [5.5, y, 0], color=SOFT, stroke_width=2)
        g0 = VGroup(Line([-5.0, y - 0.1, 0], [-5.0, y + 0.1, 0], color=WHITE), mx("0", WHITE, 32).next_to([-5.0, y - 0.1, 0], DOWN, buff=0.1))
        g1 = VGroup(Line([0.0, y - 0.1, 0], [0.0, y + 0.1, 0], color=WHITE), mx("1", WHITE, 32).next_to([0.0, y - 0.1, 0], DOWN, buff=0.1))
        zone_n = Rectangle(width=5.0, height=0.36, stroke_width=0, fill_color=EXP_N, fill_opacity=0.3).move_to([-2.5, y, 0])
        zone_p = Rectangle(width=5.0, height=0.36, stroke_width=0, fill_color=EXP_P, fill_opacity=0.25).move_to([2.6, y, 0])
        l_n = txm(r"exposant négatif : $0{,}\dots$", 22, EXP_N).next_to(zone_n, UP, buff=0.15)
        l_p = txm(r"exposant positif : plus grand que 1", 22, EXP_P).next_to(zone_p, UP, buff=0.15)
        self.p(Create(d), FadeIn(g0), FadeIn(g1), rt=0.8)
        self.p(FadeIn(zone_n), FadeIn(l_n), rt=0.6)
        self.p(FadeIn(zone_p), FadeIn(l_p), rt=0.6)
        self.at(T["methode"] - 0.55)
        self.vider(garder=(self.cur_q, self.hdr_q), rt=0.5)
        # méthode avec 10^-3
        self.at(T["methode"])
        self.set_q("La méthode")
        p3 = puiss([("-", EXP_N), ("3", EXP_N)], 72).move_to([-3.8, 0.6, 0])
        self.p(Write(p3), rt=0.8)
        self.p(Indicate(p3[1], color=EXP_N, scale_factor=1.5), rt=0.8)
        n_l = tx("négatif → 0,…", 22, EXP_N).next_to(p3, DOWN, buff=0.45)
        self.p(p3[1][0].animate.set_color(SOFT).set_opacity(0.4), FadeIn(n_l, shift=UP * 0.1), rt=0.8)
        self.at(T["isoler"])
        self.p(Indicate(p3[1][1], color=EXP_N, scale_factor=1.6), rt=0.8)
        cible = tx("il faut 3 zéros en tout", 24, EXP_N).next_to(n_l, DOWN, buff=0.2)
        self.p(FadeIn(cible), rt=0.6)
        self.at(T["ecrire"])
        eg = mx("=", WHITE, 72).next_to(p3, RIGHT, buff=0.4)
        ch = chiffres("0,001", 72, WHITE).next_to(eg, RIGHT, buff=0.4)
        self.p(FadeIn(eg), FadeIn(ch[0]), FadeIn(ch[1]), rt=0.6)
        self.p(FadeIn(ch[2]), rt=0.4)
        self.p(FadeIn(ch[3]), rt=0.4)
        self.p(FadeIn(ch[4]), rt=0.4)
        self.at(T["compter"])
        cpt = VGroup()
        for i, z in enumerate([ch[0], ch[2], ch[3]]):
            n = mx(str(i + 1), EXP_N, 30).next_to(z, DOWN, buff=0.2)
            cpt.add(n)
            self.p(Indicate(z, color=EXP_N, scale_factor=1.3), FadeIn(n, shift=UP * 0.1), rt=0.6)
        n_av = tx("le zéro avant la virgule compte", 22, EXP_N).next_to(cpt, DOWN, buff=0.3).align_to(ch, LEFT)
        self.p(FadeIn(n_av, shift=UP * 0.1), Circumscribe(ch, color=RES), rt=0.9)
        self.at(T["q3"] - 2.15)
        self.vider(garder=(self.cur_q,), rt=0.5)

    def ex1_reponses(self):
        self.at(T["q3"] - 1.6)
        self.set_q("Les réponses")
        fs = 46

        def eg(gauche, droite, num):
            return row(tx("%d)" % num, 26, SOFT), gauche, mx("=", WHITE, fs), droite, buff=0.3)
        L = [eg(puiss([("4", EXP_P)], fs), mx(r"10\,000", RES, fs), 1),
             eg(puiss([("-3", EXP_N)], fs), mx(r"0{,}001", RES, fs), 2),
             eg(mx(r"1\,000\,000", WHITE, fs), puiss([("6", RES)], fs, RES), 3),
             eg(mx(r"0{,}01", WHITE, fs), puiss([("-2", RES)], fs, RES), 4),
             eg(mx(r"0{,}000\,1", WHITE, fs), mx(r"10^{\,?}", EXP_R, fs), 5),
             eg(mx("1", WHITE, fs), mx(r"10^{\,?}", EXP_R, fs), 6)]
        col1 = VGroup(*L[:3]).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        col2 = VGroup(*L[3:]).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        page = row(col1, col2, buff=1.6)
        self.caser(page, top=self.haut() - 0.4, x=0.0, w=12.0)
        self.p(FadeIn(L[0]), FadeIn(L[1]), rt=0.6)
        self.at(T["q3"])
        self.p(FadeIn(VGroup(L[2][0], L[2][1], L[2][2])), rt=0.5)
        c6 = tx("6 zéros", 20, EXP_P).next_to(L[2], DOWN, buff=0.12).align_to(L[2][1], LEFT)
        self.p(FadeIn(c6), Indicate(L[2][1], color=EXP_P, scale_factor=1.05), rt=0.8)
        self.p(FadeIn(L[2][3], shift=LEFT * 0.2), rt=0.6)
        self.at(T["q4"])
        self.p(FadeIn(VGroup(L[3][0], L[3][1], L[3][2])), rt=0.5)
        c2 = tx("2 zéros, nombre inférieur à 1", 20, EXP_N).next_to(L[3], DOWN, buff=0.12).align_to(L[3][1], LEFT)
        self.p(FadeIn(c2), Indicate(L[3][1], color=EXP_N, scale_factor=1.05), rt=0.8)
        self.at(T["q4_res"])
        self.p(FadeIn(L[3][3], shift=LEFT * 0.2), rt=0.6)
        self.at(T["laisse"])
        a_vous = tx("à vous !", 24, EXP_R, bold=True).next_to(L[5], DOWN, buff=0.35).align_to(L[5], LEFT)
        self.p(LaggedStart(FadeIn(L[4], shift=RIGHT * 0.2), FadeIn(L[5], shift=RIGHT * 0.2), lag_ratio=0.4), FadeIn(a_vous), rt=1.0)
        self.at(T["ex2"] - 0.55)
        self.vider_tout(rt=0.5)
        self.cur_q = None

    # =================================================================
    #  EXERCICE 2
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
        r3 = row(self.puiss_pp([("n", EXP_P)], [("p", EXP_Q)], fs), mx("=", WHITE, fs),
                 puiss([("n", EXP_P), (r"\times", WHITE), ("p", EXP_Q)], fs), buff=0.18)
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
        self.p(Write(lignes[1][0]), rt=1.4)
        self.at(T["dessus"])
        self.p(Indicate(lignes[1][0][0][0][1], color=EXP_P, scale_factor=1.5), rt=0.8)
        self.at(T["dessous"])
        self.p(Indicate(lignes[1][0][0][2][1], color=EXP_Q, scale_factor=1.5), FadeIn(lignes[1][1], shift=LEFT * 0.2), rt=1.0)
        self.at(T["regle_pp"])
        self.p(Write(lignes[2][0]), rt=1.6)
        self.at(T["n_fois_p"])
        self.p(FadeIn(lignes[2][1], shift=LEFT * 0.2), Indicate(lignes[2][0][2][1], color=RES, scale_factor=1.3), rt=1.0)
        # les règles se rangent en aide-mémoire
        self.at(T["exemples"])
        mini = VGroup(*[l[0].copy() for l in lignes]).arrange(DOWN, aligned_edge=LEFT, buff=0.25).scale(0.5)
        cad = SurroundingRectangle(mini, color=SOFT, buff=0.15, corner_radius=0.1, stroke_width=1.5)
        self.aide = VGroup(cad, mini).to_corner(UR, buff=0.3).shift(DOWN * 0.5)
        self.p(FadeOut(self.cur_q), FadeOut(VGroup(*[l[1] for l in lignes])),
               ReplacementTransform(VGroup(*[l[0] for l in lignes]), mini), FadeIn(cad), rt=0.8)
        self.cur_q = None

    def ligne(self, nom, *morceaux, y, fs=56):
        g = row(mx(nom, WHITE, fs), mx("=", WHITE, fs), *morceaux, buff=0.2)
        g.move_to([-6.3, y, 0], aligned_edge=LEFT)
        return g

    def ex2_A_C(self):
        fs = 56
        self.at(T["A"])
        self.set_q("A")
        a0 = self.ligne("A", puiss([("2", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("5", EXP_Q)], fs), y=1.6)
        self.p(Write(a0), rt=1.0)
        a1 = puiss([("2", EXP_P), ("+", WHITE), ("5", EXP_Q)], fs)
        a2 = puiss([("7", RES)], fs, RES)
        eg1, eg2 = mx("=", WHITE, fs), mx("=", WHITE, fs)
        row(eg1, a1, eg2, a2, buff=0.25).next_to(a0, RIGHT, buff=0.2)
        self.at(T["A_somme"])
        self.p(FadeIn(eg1), FadeIn(a1[0]), TransformFromCopy(a0[2][1], a1[1][0], path_arc=-0.6),
               TransformFromCopy(a0[4][1], a1[1][2], path_arc=-0.6), FadeIn(a1[1][1]), rt=1.2)
        mult = tx("multiplication → on additionne", 20, SOFT).next_to(a1, DOWN, buff=0.25)
        self.p(FadeIn(mult), rt=0.5)
        self.p(FadeIn(eg2), TransformFromCopy(a1, a2), rt=0.9)
        self.p(Circumscribe(a2, color=RES), rt=0.7)
        # C
        self.at(T["C"])
        self.set_q("C")
        c0 = row(mx("C", WHITE, fs), mx("=", WHITE, fs), frac(puiss([("8", EXP_P)], fs), puiss([("3", EXP_Q)], fs)), buff=0.2)
        c0.move_to([-6.3, -1.3, 0], aligned_edge=LEFT)
        self.p(Write(c0), rt=1.0)
        c1 = puiss([("8", EXP_P), ("-", WHITE), ("3", EXP_Q)], fs)
        c2 = puiss([("5", RES)], fs, RES)
        f1, f2 = mx("=", WHITE, fs), mx("=", WHITE, fs)
        row(f1, c1, f2, c2, buff=0.25).next_to(c0, RIGHT, buff=0.2)
        self.at(T["C_diff"])
        self.p(FadeIn(f1), FadeIn(c1[0]), TransformFromCopy(c0[2][0][1], c1[1][0], path_arc=-0.6),
               TransformFromCopy(c0[2][2][1], c1[1][2], path_arc=0.6), FadeIn(c1[1][1]), rt=1.2)
        self.p(Indicate(c1[1][0], color=EXP_P, scale_factor=1.4), rt=0.6)
        self.p(Indicate(c1[1][2], color=EXP_Q, scale_factor=1.4), rt=0.6)
        self.at(T["C_res"])
        self.p(FadeIn(f2), TransformFromCopy(c1, c2), rt=0.8)
        self.p(Circumscribe(c2, color=RES), rt=0.6)
        self.at(T["E"] - 0.55)
        self.vider(garder=(self.aide,), rt=0.5)

    def ex2_E(self):
        fs = 56
        self.at(T["E"])
        self.set_q("E")
        e0 = self.ligne("E", self.puiss_pp([("-3", EXP_P)], [("2", EXP_Q)], fs), y=1.6)
        self.p(Write(e0), rt=1.0)
        self.p(Indicate(e0[2][1], color=EXP_Q, scale_factor=1.6), rt=0.7)
        car = tx("« au carré » : 2 fois le même facteur", 20, SOFT).next_to(e0, DOWN, buff=0.25).align_to(e0[2], LEFT)
        self.p(FadeIn(car), rt=0.5)
        # méthode 1 : on revient à un produit
        self.at(T["E_imag"])
        m1 = row(mx("=", WHITE, fs), puiss([("-3", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("-3", EXP_P)], fs), buff=0.2)
        m1.next_to(e0, RIGHT, buff=0.25)
        self.p(FadeIn(m1[0]), TransformFromCopy(e0[2][0][1], m1[1]), TransformFromCopy(e0[2][0][1], m1[3]), FadeIn(m1[2]), rt=1.2)
        self.at(T["E_prop1"])
        m2 = row(mx("=", WHITE, fs), puiss([("-3", EXP_P), ("+", WHITE), ("(-3)", EXP_P)], fs), mx("=", WHITE, fs),
                 puiss([("-6", RES)], fs, RES), buff=0.25)
        m2.move_to([-4.6, 0.1, 0], aligned_edge=LEFT)
        l1 = tx("1re règle : on additionne", 20, SOFT).next_to(m2, DOWN, buff=0.2).align_to(m2, LEFT)
        self.p(FadeOut(car), FadeIn(m2[0]), FadeIn(m2[1][0]), TransformFromCopy(m1[1][1], m2[1][1][0], path_arc=-0.5),
               TransformFromCopy(m1[3][1], m2[1][1][2], path_arc=-0.5), FadeIn(m2[1][1][1]), FadeIn(l1), rt=1.2)
        self.at(T["E_res"])
        self.p(FadeIn(m2[2]), TransformFromCopy(m2[1], m2[3]), rt=0.8)
        self.p(Circumscribe(m2[3], color=RES), rt=0.6)
        # méthode 2 : la 3e règle directement
        self.at(T["E_prop3"])
        m3 = row(mx("E", WHITE, fs), mx("=", WHITE, fs), self.puiss_pp([("-3", EXP_P)], [("2", EXP_Q)], fs), mx("=", WHITE, fs),
                 puiss([("-3", EXP_P), (r"\times", WHITE), ("2", EXP_Q)], fs), mx("=", WHITE, fs), puiss([("-6", RES)], fs, RES), buff=0.22)
        m3.move_to([-6.3, -1.9, 0], aligned_edge=LEFT)
        l3 = tx("ou directement, avec la 3e règle :", 20, SOFT).next_to(m3, UP, buff=0.2).align_to(m3, LEFT)
        self.p(FadeIn(l3), FadeIn(m3[:3]), rt=0.6)
        self.p(FadeIn(m3[3]), FadeIn(m3[4][0]), TransformFromCopy(m3[2][0][1][1], m3[4][1][0], path_arc=-0.5),
               TransformFromCopy(m3[2][1], m3[4][1][2], path_arc=0.5), FadeIn(m3[4][1][1]), rt=1.2)
        self.p(FadeIn(m3[5]), TransformFromCopy(m3[4], m3[6]), rt=0.8)
        self.p(Circumscribe(m3[6], color=RES), rt=0.6)
        self.at(T["F"] - 0.55)
        self.vider(garder=(self.aide,), rt=0.5)

    def ex2_F(self):
        fs = 56
        self.at(T["F"])
        self.set_q("F")
        num = row(puiss([("5", EXP_P)], fs), mx(r"\times", WHITE, fs), puiss([("-2", EXP_Q)], fs), buff=0.15)
        F0 = row(mx("F", WHITE, fs), mx("=", WHITE, fs), frac(num, puiss([("4", EXP_R)], fs)), buff=0.2)
        F0.move_to([-6.3, 0.9, 0], aligned_edge=LEFT)
        self.p(Write(F0), rt=1.4)
        tout = tx("on applique les règles une par une", 22, SOFT).next_to(F0, DOWN, buff=0.3).align_to(F0, LEFT)
        self.p(FadeIn(tout), rt=0.5)
        self.at(T["F_num"])
        n1 = puiss([("5", EXP_P), ("+", WHITE), ("(-2)", EXP_Q)], fs)
        F1 = row(mx("=", WHITE, fs), frac(n1, puiss([("4", EXP_R)], fs)), buff=0.2).next_to(F0, RIGHT, buff=0.25)
        self.p(Indicate(num, color=EXP_P, scale_factor=1.05), rt=0.6)
        self.p(FadeIn(F1[0]), FadeIn(F1[1][0][0]), TransformFromCopy(num[0][1], n1[1][0], path_arc=-0.6),
               TransformFromCopy(num[2][1], n1[1][2], path_arc=-0.6), FadeIn(n1[1][1]), FadeIn(F1[1][1]),
               TransformFromCopy(F0[2][2], F1[1][2]), rt=1.2)
        self.at(T["F_trois"])
        F2 = row(mx("=", WHITE, fs), frac(puiss([("3", EXP_P)], fs), puiss([("4", EXP_R)], fs)), buff=0.2)
        F2.move_to([-5.1, -1.6, 0], aligned_edge=LEFT)
        self.p(FadeOut(tout), FadeIn(F2[0]), TransformFromCopy(F1[1], F2[1]), rt=0.9)
        self.at(T["F_div"])
        F3 = row(mx("=", WHITE, fs), puiss([("3", EXP_P), ("-", WHITE), ("4", EXP_R)], fs), mx("=", WHITE, fs),
                 puiss([("-1", RES)], fs, RES), buff=0.25).next_to(F2, RIGHT, buff=0.25)
        self.p(FadeIn(F3[0]), FadeIn(F3[1][0]), TransformFromCopy(F2[1][0][1], F3[1][1][0], path_arc=-0.6),
               TransformFromCopy(F2[1][2][1], F3[1][1][2], path_arc=0.6), FadeIn(F3[1][1][1]), rt=1.2)
        self.at(T["F_res"])
        self.p(FadeIn(F3[2]), TransformFromCopy(F3[1], F3[3]), rt=0.8)
        self.p(Circumscribe(F3[3], color=RES), rt=0.7)
        self.pause(1.0)
        self.vider(rt=0.5)

    # =================================================================
    #  ÉCRAN FINAL (muet) : toutes les réponses pour vérifier
    # =================================================================
    def bilan_final(self):
        self.set_q("Vérifiez vos réponses")
        fs = 40
        ex1 = VGroup(*[row(tx("%d)" % k, 22, SOFT), g, mx("=", WHITE, fs), d, buff=0.22) for k, g, d in (
            (1, puiss([("4", EXP_P)], fs), mx(r"10\,000", RES, fs)),
            (2, puiss([("-3", EXP_N)], fs), mx(r"0{,}001", RES, fs)),
            (3, mx(r"1\,000\,000", WHITE, fs), puiss([("6", RES)], fs, RES)),
            (4, mx(r"0{,}01", WHITE, fs), puiss([("-2", RES)], fs, RES)),
            (5, mx(r"0{,}000\,1", WHITE, fs), puiss([("-4", RES)], fs, RES)),
            (6, mx("1", WHITE, fs), puiss([("0", RES)], fs, RES)))]).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lig = [("A", puiss([("2", EXP_P), ("+", WHITE), ("5", EXP_Q)], fs), puiss([("7", RES)], fs, RES)),
               ("B", puiss([("-2", EXP_P), ("+", WHITE), ("(-4)", EXP_Q)], fs), puiss([("-6", RES)], fs, RES)),
               ("C", puiss([("8", EXP_P), ("-", WHITE), ("3", EXP_Q)], fs), puiss([("5", RES)], fs, RES)),
               ("D", puiss([("3", EXP_P), ("-", WHITE), ("(-2)", EXP_Q)], fs), puiss([("5", RES)], fs, RES)),
               ("E", puiss([("-3", EXP_P), (r"\times", WHITE), ("2", EXP_Q)], fs), puiss([("-6", RES)], fs, RES)),
               ("F", puiss([("3", EXP_P), ("-", WHITE), ("4", EXP_R)], fs), puiss([("-1", RES)], fs, RES))]
        ex2 = VGroup(*[row(mx(n, WHITE, fs), mx("=", WHITE, fs), m, mx("=", WHITE, fs), r, buff=0.22) for n, m, r in lig]
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        t1 = tx("Exercice 1", 24, PUIS_C, bold=True)
        t2 = tx("Exercice 2", 24, PUIS_C, bold=True)
        g1 = VGroup(t1, ex1).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        g2 = VGroup(t2, ex2).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        page = row(g1, g2, buff=1.6)
        self.caser(page, top=2.9, x=0.0, w=12.4)
        self.p(FadeIn(t1), FadeIn(t2), rt=0.5)
        self.p(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in list(ex1) + list(ex2)], lag_ratio=0.12), rt=2.4)
        self.p(*[Indicate(ex1[k], color=EXP_R, scale_factor=1.04) for k in (4, 5)],
               *[Indicate(ex2[k], color=EXP_R, scale_factor=1.04) for k in (1, 3)], rt=1.2)
        self.pause(5.0)
