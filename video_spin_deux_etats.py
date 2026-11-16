from manim import *
import math

# =====================================================================
#  Vidéo de cours – UN SPIN 1/2 DANS UN CHAMP (modèle à deux états), ≈ 5 min.
#  Niveau agrégation, prérequis : facteur de Boltzmann.
#  Pour Manim Community (rendu sur GitHub). Vidéo autonome sous-titrée.
#  Plan : le système · l'énergie dans un champ · Boltzmann · normalisation ·
#  trois vues liées (barres, population de spins, courbe) · moment moyen tanh x ·
#  loi de Curie (avec ordre de grandeur) · limite du modèle et idée de Weiss.
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
        for g in (self.hdr_ex, self.hdr_q, *garder):
            if g is not None:
                proteges.update(id(x) for x in g.get_family())
        mobs = [m for m in self.mobjects if id(m) not in proteges]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def question(self, s, rt=1.2):
        q = tx(s, 25, WHITE).to_edge(UP, buff=0.78).to_edge(LEFT, buff=0.45)
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
        t = tx(s, fs, RES, w=12.0)
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
        self.x = ValueTracker(0.0)          # x = μB / (k_B T)
        self.phase = ValueTracker(0.0)      # agitation thermique (scintillement des spins)
        rng = np.random.default_rng(5)
        self.u0 = rng.random(60)
        self.v0 = rng.uniform(0.6, 1.4, 60)
        self.titre()
        self.le_spin()
        self.energie()
        self.boltzmann()
        self.normalisation()
        self.trois_vues()
        self.moment_moyen()
        self.loi_de_curie()
        self.universel()
        self.limite()
        self.retenir()

    # =================================================================
    #  Petits objets
    # =================================================================
    def spin(self, haut=True, r=0.2, L=0.62, sw=4):
        """Un spin : petite sphère éclairée traversée par sa flèche de moment."""
        c = UPC if haut else DNC
        sphere = Circle(radius=r, stroke_color=WHITE, stroke_width=1, fill_color=c, fill_opacity=1)
        sphere.set_sheen(-0.45, DR)
        d = UP if haut else DOWN
        fl = Arrow(-d * L / 2, d * L / 2, buff=0, color=WHITE, stroke_width=sw, max_tip_length_to_length_ratio=0.3)
        return VGroup(sphere, fl)

    def p_haut(self, x):
        return math.exp(x) / (2 * math.cosh(x))

    def ensemble(self, centre, nx=12, ny=5, pas=0.42):
        """60 spins indépendants : chacun est « haut » avec la probabilité p↑(x), et scintille avec l'agitation."""
        def dessiner():
            p = self.p_haut(self.x.get_value())
            ph = self.phase.get_value()
            g = VGroup()
            for k in range(nx * ny):
                i, j = k % nx, k // nx
                c = np.array(centre) + np.array([(i - (nx - 1) / 2) * pas, ((ny - 1) / 2 - j) * pas, 0])
                u = (self.u0[k] + self.v0[k] * ph) % 1.0
                g.add(self.spin(u < p, r=0.1, L=0.3, sw=2).move_to(c))
            return g
        return always_redraw(dessiner)

    def compteur(self, ref, nx=12, ny=5):
        def dessiner():
            p = self.p_haut(self.x.get_value())
            ph = self.phase.get_value()
            n = sum(1 for k in range(nx * ny) if (self.u0[k] + self.v0[k] * ph) % 1.0 < p)
            return txm(r"$\uparrow$ : %d / %d" % (n, nx * ny), 22, UPC).next_to(ref, DOWN, buff=0.2)
        return always_redraw(dessiner)

    def barres(self, base, h=2.4, w=0.7):
        """Diagramme en barres de p↑ et p↓, piloté par x."""
        cadre = VGroup(Line(base + LEFT * 0.9, base + RIGHT * 0.9, color=SOFT, stroke_width=2))
        def dessiner():
            p = self.p_haut(self.x.get_value())
            g = VGroup()
            for k, (q, c, s) in enumerate(((p, UPC, r"p_\uparrow"), (1 - p, DNC, r"p_\downarrow"))):
                x0 = base + RIGHT * (-0.45 + 0.9 * k)
                b = Rectangle(width=w, height=max(0.01, h * q), stroke_width=0, fill_color=c, fill_opacity=0.85)
                b.set_sheen(0.25, UP)
                b.move_to(x0, aligned_edge=DOWN)
                g.add(b)
                g.add(mx(s, c, 30).next_to(x0, DOWN, buff=0.15))
                g.add(Text(("%d %%" % round(100 * q)), font_size=20, color=c).next_to(b, UP, buff=0.08))
            return g
        return cadre, always_redraw(dessiner)

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        t = tx("Un spin dans un champ magnétique", 56, WHITE, bold=True)
        s = tx("le modèle à deux états, brique de base du magnétisme", 28, SOFT).next_to(t, DOWN, buff=0.35)
        sp = VGroup(self.spin(True, 0.32, 1.0, 6), self.spin(False, 0.32, 1.0, 6)).arrange(RIGHT, buff=1.2).next_to(s, DOWN, buff=0.7)
        self.p(Write(t), rt=1.3)
        self.p(FadeIn(s, shift=UP * 0.2), rt=0.8)
        self.p(LaggedStart(*[GrowFromCenter(m) for m in sp], lag_ratio=0.3), rt=1.0)
        self.pause(1.0)
        self.hdr_ex = tx("Le spin 1/2 à deux états", 22, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(t, self.hdr_ex), FadeOut(s), FadeOut(sp), rt=0.8)

    # =================================================================
    #  1. LE SYSTÈME : un spin, deux états
    # =================================================================
    def le_spin(self):
        self.set_q("1. Le système")
        s = self.spin(True, 0.45, 1.6, 7).move_to(LEFT * 3.5)
        self.p(GrowFromCenter(s), rt=0.9)
        self.dire("Un électron (ou un atome) porte un petit moment magnétique : comme une minuscule aiguille aimantée.", lire=2.4)
        axe = DashedLine(LEFT * 3.5 + DOWN * 1.6, LEFT * 3.5 + UP * 1.6, color=SOFT, stroke_width=2)
        z = mx("z", SOFT, 34).next_to(axe, UP, buff=0.1)
        self.p(Create(axe), FadeIn(z), rt=0.7)
        haut = VGroup(self.spin(True, 0.38, 1.3, 6), txm(r"$\mu_z = +\mu$", 26, UPC), tx("« haut »", 22, UPC)).arrange(DOWN, buff=0.25)
        bas = VGroup(self.spin(False, 0.38, 1.3, 6), txm(r"$\mu_z = -\mu$", 26, DNC), tx("« bas »", 22, DNC)).arrange(DOWN, buff=0.25)
        deux = VGroup(haut, bas).arrange(RIGHT, buff=1.6).move_to(RIGHT * 2.6 + UP * 0.2)
        self.dire(r"Pour un spin 1/2, la mécanique quantique n'autorise que DEUX valeurs de la projection $\mu_z$ :", c=ABSO, lire=0.3)
        self.p(TransformFromCopy(s, haut[0], path_arc=-0.6), FadeIn(haut[1:], shift=UP * 0.15), rt=1.2)
        self.p(TransformFromCopy(s, bas[0], path_arc=0.6), FadeIn(bas[1:], shift=UP * 0.15), rt=1.2)
        self.pause(1.4)
        self.dire("Pas d'intermédiaire : le moment est soit « haut », soit « bas ». C'est tout le modèle.", lire=2.2)
        self.p(Circumscribe(deux, color=ABSO, buff=0.2), rt=1.2)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  2. L'ÉNERGIE DANS UN CHAMP
    # =================================================================
    def energie(self):
        self.set_q("2. L'énergie")
        B = ValueTracker(0.0)
        # lignes de champ en arrière-plan (de plus en plus visibles quand B augmente)
        def champ():
            g = VGroup()
            for i in range(6):
                for j in range(2):
                    p = np.array([-5.6 + 0.9 * i, 0.05 + 1.15 * j, 0])
                    g.add(Arrow(p + DOWN * 0.3, p + UP * 0.3, buff=0, stroke_width=2, color=BCOL,
                                max_tip_length_to_length_ratio=0.3).set_opacity(0.55 * B.get_value()))
            return g
        lignes = always_redraw(champ)
        cadre_B = RoundedRectangle(corner_radius=0.12, width=5.8, height=2.2, stroke_color=SOFT, stroke_width=1.2).move_to([-3.35, 0.62, 0])
        b_l = always_redraw(lambda: txm(r"champ $B$" + (" = 0" if B.get_value() < 0.02 else ""), 22, BCOL)
                            .next_to(cadre_B, UP, buff=0.08).align_to(cadre_B, LEFT))
        self.p(Create(cadre_B), rt=0.4)
        self.add(lignes)
        self.p(FadeIn(b_l), rt=0.4)
        # diagramme d'énergie
        ax_E = Arrow([0.7, -2.3, 0], [0.7, 2.3, 0], buff=0, color=SOFT, stroke_width=2, max_tip_length_to_length_ratio=0.04)
        e_l = mx("E", SOFT, 32).next_to(ax_E, UP, buff=0.08)
        zero = DashedLine([0.7, 0, 0], [5.6, 0, 0], color=SOFT, stroke_width=1.2, stroke_opacity=0.5)
        k = 1.5
        def niveaux():
            b = B.get_value()
            yh, yb = -k * b, k * b
            g = VGroup(Line([1.4, yh, 0], [3.6, yh, 0], color=UPC, stroke_width=5),
                       Line([1.4, yb, 0], [3.6, yb, 0], color=DNC, stroke_width=5))
            g.add(self.spin(True, 0.16, 0.5, 3).move_to([4.1, yh, 0]), self.spin(False, 0.16, 0.5, 3).move_to([4.1, yb, 0]))
            if b > 0.15:
                g.add(mx(r"-\mu B", UPC, 30).next_to([3.6, yh, 0], RIGHT, buff=0.75),
                      mx(r"+\mu B", DNC, 30).next_to([3.6, yb, 0], RIGHT, buff=0.75))
            return g
        niv = always_redraw(niveaux)
        self.p(GrowArrow(ax_E), FadeIn(e_l), Create(zero), FadeIn(niv), rt=1.0)
        self.dire("Sans champ, les deux états ont la même énergie : rien ne distingue « haut » de « bas ».", lire=2.0)
        eq = row(mx("E", WHITE, 46), mx("=", WHITE, 46), mx(r"-\mu_z", WHITE, 46), mx("B", BCOL, 46), buff=0.15).move_to([-3.35, -0.95, 0])
        self.dire(r"Un champ $B$ selon z : l'énergie d'un moment vaut $E = -\mu_z B$.", c=BCOL, lire=0.2)
        self.p(B.animate.set_value(1.0), Write(eq), rt=2.4)
        self.dire("Le signe « − » : l'énergie est minimale quand le moment est ALIGNÉ avec le champ (comme une boussole).", lire=2.4)
        ecart = always_redraw(lambda: VGroup(DoubleArrow([1.1, -k * B.get_value(), 0], [1.1, k * B.get_value(), 0], buff=0,
                                                        color=ABSO, stroke_width=3, tip_length=0.15),
                                             mx(r"2\mu B", ABSO, 30).next_to([0.7, 0, 0], LEFT, buff=0.15)))
        self.p(FadeIn(ecart), rt=0.6)
        self.dire(r"Les deux niveaux se séparent d'un écart $2\mu B$, proportionnel au champ.", c=ABSO, lire=0.2)
        self.p(B.animate.set_value(1.35), rt=1.2)
        self.p(B.animate.set_value(1.0), rt=1.0)
        self.pause(0.8)
        # la compétition
        duel = VGroup(
            VGroup(tx("le champ", 24, BCOL, bold=True), tx("veut aligner (état bas en énergie)", 20, SOFT)).arrange(DOWN, buff=0.08),
            mx(r"\longleftrightarrow", ABSO, 44),
            VGroup(tx("l'agitation thermique", 24, TCOL, bold=True), tx("mélange les deux états", 20, SOFT)).arrange(DOWN, buff=0.08),
        ).arrange(RIGHT, buff=0.4)
        ajuster(duel, 6.0)
        duel.move_to([-3.35, -2.0, 0])
        self.p(FadeIn(duel[0], shift=RIGHT * 0.2), rt=0.7)
        self.p(GrowFromCenter(duel[1]), FadeIn(duel[2], shift=LEFT * 0.2), rt=0.8)
        self.dire("À température T, qui gagne ? C'est la question de toute la vidéo.", c=ABSO, lire=2.0)
        self.effacer_sous_titre()
        lignes.clear_updaters(); niv.clear_updaters(); ecart.clear_updaters(); b_l.clear_updaters()
        self.vider()

    # =================================================================
    #  3. LE FACTEUR DE BOLTZMANN
    # =================================================================
    def boltzmann(self):
        self.set_q("3. Boltzmann")
        rappel = row(tx("Rappel :", 24, SOFT), mx(r"p(E) \propto e^{-E / k_B T}", WHITE, 50), buff=0.3).move_to([0, 2.15, 0])
        self.p(FadeIn(rappel[0]), Write(rappel[1]), rt=1.2)
        self.dire("Système à l'équilibre avec un thermostat à T : la probabilité d'un état décroît exponentiellement avec son énergie.", lire=2.6)
        kT = ValueTracker(1.0)
        ax = Axes(x_range=[-2.2, 2.2, 1], y_range=[0, 6.2, 2], x_length=7.0, y_length=3.4, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([-1.6, -0.75, 0])
        nE = mx("E", SOFT, 30).next_to(ax.c2p(2.2, 0), DOWN, buff=0.12)
        courbe = always_redraw(lambda: ax.plot(lambda e: math.exp(-e / kT.get_value()),
                                               x_range=[max(-2.0, -kT.get_value() * math.log(6.0)), 2.0], color=TCOL, stroke_width=4))
        def coupe(e, c):
            def f():
                y = math.exp(-e / kT.get_value())
                return VGroup(Line(ax.c2p(e, 0), ax.c2p(e, y), color=c, stroke_width=6),
                              Dot(ax.c2p(e, y), radius=0.08, color=c))
            return always_redraw(f)
        cH = coupe(-1.0, UPC)
        cB = coupe(1.0, DNC)
        eH = mx(r"-\mu B", UPC, 28).next_to(ax.c2p(-1, 0), DOWN, buff=0.15)
        eB = mx(r"+\mu B", DNC, 28).next_to(ax.c2p(1, 0), DOWN, buff=0.15)
        T_l = always_redraw(lambda: txm(r"$k_B T$ = %s $\mu B$" % ("%.1f" % kT.get_value()).replace(".", ","), 24, TCOL).move_to([4.4, 1.0, 0]))
        self.p(Create(ax), FadeIn(nE), rt=0.8)
        self.p(Create(courbe), rt=1.0)
        self.p(FadeIn(cH), FadeIn(cB), FadeIn(eH), FadeIn(eB), FadeIn(T_l), rt=0.8)
        self.dire("On lit sur la courbe le poids de chaque état : l'état « haut » (énergie basse) est plus probable.", lire=2.4)
        self.dire("Température basse : la courbe est raide, l'état d'énergie basse domine écrasant…", c=UPC, lire=0.2)
        self.p(kT.animate.set_value(0.6), rt=2.2)
        self.pause(1.0)
        self.dire("… température élevée : la courbe s'aplatit, les deux états deviennent presque équiprobables.", c=TCOL, lire=0.2)
        self.p(kT.animate.set_value(4.0), rt=2.6)
        self.pause(1.0)
        self.p(kT.animate.set_value(1.0), rt=1.2)
        rap = row(mx(r"\frac{p_\uparrow}{p_\downarrow} = e^{2\mu B / k_B T}", WHITE, 42), buff=0.1).move_to([4.2, -0.6, 0])
        self.p(Write(rap), rt=1.2)
        self.dire(r"Tout ne dépend que du RAPPORT entre l'énergie magnétique $\mu B$ et l'énergie thermique $k_B T$.", c=ABSO, lire=2.4)
        for m in (courbe, cH, cB, T_l):
            m.clear_updaters()
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  4. NORMALISATION : p↑ et p↓
    # =================================================================
    def normalisation(self):
        self.set_q("4. Les probabilités")
        fs = 44
        l1 = row(mx(r"p_\uparrow", UPC, fs), mx("=", WHITE, fs), mx("A", WHITE, fs), mx(r"e^{+\mu B / k_B T}", UPC, fs), buff=0.15)
        l2 = row(mx(r"p_\downarrow", DNC, fs), mx("=", WHITE, fs), mx("A", WHITE, fs), mx(r"e^{-\mu B / k_B T}", DNC, fs), buff=0.15)
        bloc = VGroup(l1, l2).arrange(DOWN, buff=0.4, aligned_edge=LEFT).move_to([-3.2, 1.2, 0])
        self.p(Write(l1), rt=1.0)
        self.p(Write(l2), rt=1.0)
        self.dire(r"On applique Boltzmann aux deux états, d'énergies $E = \mp \mu B$ ; $A$ est une constante encore inconnue.", lire=2.2)
        defx = row(tx("on pose", 24, SOFT), mx(r"x = \frac{\mu B}{k_B T}", XCOL, 48), buff=0.3).move_to([3.2, 1.2, 0])
        self.p(FadeIn(defx[0]), Write(defx[1]), rt=1.2)
        self.p(Circumscribe(defx[1], color=XCOL), rt=0.9)
        self.dire(r"$x$ compare l'énergie magnétique à l'énergie thermique : c'est le seul paramètre du problème.", c=XCOL, lire=2.2)
        l1b = row(mx(r"p_\uparrow", UPC, fs), mx("=", WHITE, fs), mx("A", WHITE, fs), mx(r"e^{x}", UPC, fs), buff=0.15).move_to(l1, LEFT)
        l2b = row(mx(r"p_\downarrow", DNC, fs), mx("=", WHITE, fs), mx("A", WHITE, fs), mx(r"e^{-x}", DNC, fs), buff=0.15).move_to(l2, LEFT)
        self.p(TransformMatchingShapes(l1, l1b), TransformMatchingShapes(l2, l2b), rt=1.2)
        somme = row(mx(r"p_\uparrow + p_\downarrow = 1", WHITE, fs), mx(r"\;\Rightarrow\;", SOFT, fs),
                    mx(r"A\,(e^{x} + e^{-x}) = 1", WHITE, fs), buff=0.2).move_to([0, -0.4, 0])
        self.dire("Le spin est forcément dans l'un des deux états : les probabilités doivent sommer à 1.", lire=1.4)
        self.p(Write(somme[0]), rt=1.0)
        self.p(FadeIn(somme[1]), TransformFromCopy(VGroup(l1b[2:], l2b[2:]), somme[2], path_arc=-0.4), rt=1.4)
        resA = row(mx("A", WHITE, fs), mx("=", WHITE, fs), frac(mx("1", WHITE, fs), mx(r"e^{x} + e^{-x}", WHITE, fs)),
                   mx("=", WHITE, fs), frac(mx("1", WHITE, fs), mx(r"2\cosh x", WHITE, fs)), buff=0.18).next_to(somme, DOWN, buff=0.55)
        self.p(Write(resA[:3]), rt=1.2)
        self.p(Write(resA[3:]), rt=1.0)
        self.dire(r"(par définition, $e^{x} + e^{-x} = 2\cosh x$)", c=SOFT, lire=1.4)
        fin = VGroup(
            row(mx(r"p_\uparrow", UPC, fs), mx("=", WHITE, fs), frac(mx(r"e^{x}", UPC, fs), mx(r"2\cosh x", WHITE, fs)), buff=0.18),
            row(mx(r"p_\downarrow", DNC, fs), mx("=", WHITE, fs), frac(mx(r"e^{-x}", DNC, fs), mx(r"2\cosh x", WHITE, fs)), buff=0.18),
        ).arrange(RIGHT, buff=1.4).move_to([0, 0.3, 0])
        self.p(FadeOut(VGroup(somme, resA, defx)), TransformMatchingShapes(l1b, fin[0]), TransformMatchingShapes(l2b, fin[1]), rt=1.5)
        cad = SurroundingRectangle(fin, color=BOX, buff=0.3, corner_radius=0.12)
        self.p(Create(cad), rt=0.6)
        self.dire("Les deux probabilités, entièrement déterminées par x.", c=BOX, lire=1.6)
        self.fin_p = VGroup(fin, cad)
        self.effacer_sous_titre()
        self.p(self.fin_p.animate.scale(0.62).to_corner(UR, buff=0.35).shift(DOWN * 0.5), rt=0.8)

    # =================================================================
    #  5. TROIS VUES D'UNE MÊME PHYSIQUE (barres, population, courbe)
    # =================================================================
    def trois_vues(self):
        self.set_q("5. Ce que ça donne")
        self.x.set_value(0.0)
        cadre_b, barres = self.barres(np.array([-5.0, -1.6, 0]), h=2.6)
        ens = self.ensemble([-0.6, 0.2, 0], nx=12, ny=5, pas=0.42)
        cnt = self.compteur(Rectangle(width=5, height=2.1).move_to([-0.6, 0.2, 0]))
        x_l = always_redraw(lambda: txm(r"$x$ = %s" % ("%.2f" % self.x.get_value()).replace(".", ","), 28, XCOL).move_to([-0.6, 1.95, 0]))
        t_ens = tx("60 spins indépendants", 20, SOFT).move_to([-0.6, -1.75, 0])
        self.p(Create(cadre_b), FadeIn(barres), FadeIn(ens), FadeIn(cnt), FadeIn(x_l), FadeIn(t_ens), rt=1.0)
        self.dire(r"$x = 0$ (pas de champ, ou $T$ très grande) : 50 % / 50 %. Les spins scintillent au gré de l'agitation.", lire=0.3)
        self.p(self.phase.animate.set_value(3.0), rt=3.0, rate_func=linear)
        self.dire(r"On augmente $x$ : le champ l'emporte peu à peu, les spins « haut » deviennent majoritaires.", c=UPC, lire=0.2)
        self.p(self.x.animate.set_value(0.8), self.phase.animate.set_value(7.0), rt=3.4, rate_func=linear)
        self.p(self.x.animate.set_value(2.5), self.phase.animate.set_value(10.0), rt=2.6, rate_func=linear)
        self.dire(r"$x$ grand : presque tous alignés. L'agitation ne parvient plus à les retourner.", c=UPC, lire=0.4)
        self.p(self.phase.animate.set_value(12.0), rt=1.8, rate_func=linear)
        self.dire(r"Retour vers $x$ petit : le désordre reprend.", c=TCOL, lire=0.2)
        self.p(self.x.animate.set_value(0.25), self.phase.animate.set_value(16.0), rt=3.0, rate_func=linear)
        self.dire("Chaque spin reste aléatoire ; c'est la MOYENNE sur la population qui est bien définie.", c=ABSO, lire=2.2)
        self.vues = VGroup(cadre_b, barres, ens, cnt, x_l, t_ens)

    # =================================================================
    #  6. MOMENT MOYEN : tanh x
    # =================================================================
    def moment_moyen(self):
        self.set_q("6. Le moment moyen")
        self.p(FadeOut(self.fin_p), rt=0.4)
        for m in (self.vues[2], self.vues[3]):
            m.clear_updaters()
        self.p(FadeOut(VGroup(self.vues[2], self.vues[3], self.vues[5])), self.vues[4].animate.move_to([-5.0, 1.9, 0]), rt=0.6)
        fs = 40
        m1 = row(mx(r"\langle \mu_z \rangle", WHITE, fs), mx("=", WHITE, fs), mx(r"(+\mu)", UPC, fs), mx(r"p_\uparrow", UPC, fs),
                 mx("+", WHITE, fs), mx(r"(-\mu)", DNC, fs), mx(r"p_\downarrow", DNC, fs), buff=0.12)
        m2 = row(mx(r"\langle \mu_z \rangle", WHITE, fs), mx("=", WHITE, fs), mx(r"\mu", WHITE, fs),
                 frac(mx(r"e^{x} - e^{-x}", WHITE, fs), mx(r"e^{x} + e^{-x}", WHITE, fs)), buff=0.15)
        m3 = row(mx(r"\langle \mu_z \rangle", WHITE, fs + 6), mx("=", WHITE, fs + 6), mx(r"\mu", WHITE, fs + 6),
                 mx(r"\tanh x", MCOL, fs + 6), buff=0.15)
        col = VGroup(m1, m2, m3).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0.9, 1.2, 0])
        ajuster(col, 7.0)
        col.move_to([0.9, 0.9, 0])
        self.dire("Moyenne des deux valeurs possibles, chacune pondérée par sa probabilité :", lire=0.2)
        self.p(Write(m1), rt=1.6)
        self.p(Indicate(m1[2:4], color=UPC), rt=0.8)
        self.p(Indicate(m1[5:7], color=DNC), rt=0.8)
        self.dire(r"On remplace $p_\uparrow$ et $p_\downarrow$ par leurs expressions : le facteur $1/(2\cosh x)$ se met en facteur.", lire=0.4)
        self.p(TransformMatchingShapes(m1.copy(), m2), rt=1.6)
        self.pause(1.4)
        self.dire("Et ce quotient, c'est la définition de la tangente hyperbolique :", c=MCOL, lire=0.2)
        self.p(TransformMatchingShapes(m2.copy(), m3), rt=1.4)
        cad = SurroundingRectangle(m3, color=BOX, buff=0.18, corner_radius=0.1)
        self.p(Create(cad), Flash(m3[3], color=MCOL, flash_radius=0.7), rt=0.8)
        self.pause(1.0)
        # courbe tanh reliée aux barres
        self.p(FadeOut(VGroup(m1, m2)), VGroup(m3, cad).animate.scale(0.75).move_to([-0.8, 2.2, 0]), rt=0.8)
        ax = Axes(x_range=[0, 3.2, 1], y_range=[0, 1.15, 0.5], x_length=5.6, y_length=3.0, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([2.9, -0.7, 0])
        lab = VGroup(mx("x", XCOL, 32).next_to(ax.c2p(3.2, 0), DOWN, buff=0.12),
                     mx(r"\langle \mu_z \rangle / \mu", MCOL, 30).next_to(ax.c2p(0, 1.15), UP, buff=0.08),
                     mx("1", SOFT, 24).next_to(ax.c2p(0, 1), LEFT, buff=0.1))
        sat = DashedLine(ax.c2p(0, 1), ax.c2p(3.2, 1), color=SOFT, stroke_width=1.5)
        th = ax.plot(lambda u: math.tanh(u), x_range=[0, 3.1], color=MCOL, stroke_width=4)
        pt = always_redraw(lambda: Dot(ax.c2p(self.x.get_value(), math.tanh(self.x.get_value())), radius=0.09, color=ABSO))
        self.p(Create(ax), FadeIn(lab), Create(sat), rt=0.9)
        self.p(Create(th), rt=1.4)
        self.add(pt)
        self.dire(r"Le point suit la valeur de $x$, en même temps que les barres de probabilités :", lire=0.2)
        self.p(self.x.animate.set_value(3.0), rt=3.0)
        self.p(self.x.animate.set_value(0.05), rt=2.4)
        # deux régimes
        lin = ax.plot(lambda u: u, x_range=[0, 1.05], color=XCOL, stroke_width=3)
        r1 = txm(r"$x \ll 1$ : $\tanh x \simeq x$", 22, XCOL).move_to(ax.c2p(1.75, 0.3))
        r2 = txm(r"$x \gg 1$ : $\tanh x \to 1$", 22, UPC).move_to(ax.c2p(2.3, 0.78))
        self.p(Create(lin), FadeIn(r1), rt=1.0)
        self.dire(r"$x \ll 1$ (agitation dominante) : réponse LINÉAIRE, le moment moyen est proportionnel à $x$.", c=XCOL, lire=2.2)
        self.p(FadeIn(r2), self.x.animate.set_value(2.8), rt=1.6)
        self.dire(r"$x \gg 1$ (champ dominant) : SATURATION, tous les spins sont alignés et $\langle \mu_z \rangle \to \mu$.", c=UPC, lire=2.2)
        pt.clear_updaters(); self.vues[1].clear_updaters()
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  7. DE N SPINS À LA LOI DE CURIE
    # =================================================================
    def loi_de_curie(self):
        self.set_q("7. La loi de Curie")
        fs = 42
        M1 = row(mx("M", MCOL, fs), mx("=", WHITE, fs), mx("N", WHITE, fs), mx(r"\langle \mu_z \rangle", WHITE, fs), mx("=", WHITE, fs),
                 mx(r"N\mu \tanh\!\left(\frac{\mu B}{k_B T}\right)", WHITE, fs), buff=0.15).move_to([0, 2.0, 0])
        self.dire("Avec N spins indépendants par unité de volume, l'aimantation est N fois le moment moyen.", lire=0.3)
        self.p(Write(M1), rt=1.6)
        self.pause(1.2)
        # ordre de grandeur
        odg = VGroup(tx("Ordre de grandeur, à température ambiante :", 24, ABSO),
                     mx(r"\mu \approx \mu_B = 9{,}3\times10^{-24}\ \mathrm{J\cdot T^{-1}},\quad B = 1\ \mathrm{T},\quad T = 300\ \mathrm{K}", WHITE, 34),
                     mx(r"x = \frac{\mu B}{k_B T} \approx \frac{9{,}3\times10^{-24}}{1{,}38\times10^{-23}\times 300} \approx 2\times10^{-3}", XCOL, 38)
                     ).arrange(DOWN, buff=0.3).move_to([0, 0.15, 0])
        ajuster(odg, 12.6)
        odg.move_to([0, 0.1, 0])
        self.p(FadeIn(odg[0]), rt=0.6)
        self.p(Write(odg[1]), rt=1.4)
        self.p(Write(odg[2]), rt=1.6)
        self.dire(r"$x \approx 0{,}002 \ll 1$ : on est dans le régime LINÉAIRE, même avec un champ d'un tesla !", c=XCOL, lire=2.4)
        self.p(FadeOut(odg), rt=0.5)
        M2 = row(mx("M", MCOL, fs), mx(r"\simeq", WHITE, fs), mx(r"N\mu \cdot \frac{\mu B}{k_B T}", WHITE, fs), mx("=", WHITE, fs),
                 mx(r"\frac{N \mu^2}{k_B}", WHITE, fs), mx(r"\cdot", WHITE, fs), mx(r"\frac{B}{T}", WHITE, fs), buff=0.15).move_to([0, 0.6, 0])
        self.p(TransformMatchingShapes(M1.copy(), M2), rt=1.6)
        self.dire("On remplace tanh x par x : l'aimantation est proportionnelle à B et inversement proportionnelle à T.", lire=2.4)
        curie = row(tx("loi de Curie :", 26, TCOL), mx(r"\chi = \frac{C}{T}", TCOL, 54), tx("avec", 22, SOFT),
                    mx(r"C = \frac{\mu_0 N \mu^2}{k_B}", TCOL, 42), buff=0.3).move_to([0, -1.0, 0])
        self.p(FadeIn(curie[0]), Write(curie[1]), rt=1.2)
        self.p(FadeIn(curie[2:]), rt=0.8)
        cad = SurroundingRectangle(curie[1], color=BOX, buff=0.15, corner_radius=0.08)
        self.p(Create(cad), rt=0.5)
        self.dire(r"(susceptibilité : $M = \chi H$ avec $B = \mu_0 H$). Deux fois plus chaud : deux fois moins aimanté.", c=SOFT, lire=2.6)
        self.dire("C'est la loi observée par Pierre Curie (1895) pour les corps paramagnétiques.", c=TCOL, lire=2.0)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  8. UNE SEULE COURBE POUR TOUTES LES TEMPÉRATURES
    # =================================================================
    def universel(self):
        self.set_q("8. Une courbe universelle")
        k_ = 0.672                                   # μ_B / k_B en K/T
        ax = Axes(x_range=[0, 5.2, 1], y_range=[0, 1.15, 0.5], x_length=7.0, y_length=3.6, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([-1.8, -0.4, 0])
        nx_ = always_redraw(lambda: mx(r"B\ (\mathrm{T})", SOFT, 30).next_to(ax.c2p(5.2, 0), DOWN, buff=0.12))
        ny_ = mx(r"M / N\mu", MCOL, 30).next_to(ax.c2p(0, 1.15), UP, buff=0.08)
        un = mx("1", SOFT, 24).next_to(ax.c2p(0, 1), LEFT, buff=0.1)
        Ts = [(0.5, "#4FC3F7"), (1.0, "#81C784"), (2.0, "#FF8A65")]
        courbes = VGroup(*[ax.plot(lambda b, T=T: math.tanh(k_ * b / T), x_range=[0, 5.1], color=c, stroke_width=4) for T, c in Ts])
        etiq = VGroup(*[txm(r"$T$ = %s K" % str(T).replace(".", ","), 20, c) for T, c in Ts]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        etiq.next_to(ax, RIGHT, buff=0.4).align_to(ax, UP)
        self.p(Create(ax), FadeIn(nx_), FadeIn(ny_), FadeIn(un), rt=0.9)
        self.dire("Expérience de pensée : on mesure M en fonction de B, à plusieurs températures très basses.", lire=0.3)
        self.p(LaggedStart(*[Create(c) for c in courbes], lag_ratio=0.4), FadeIn(etiq), rt=2.6)
        self.dire("Trois courbes différentes : plus il fait froid, plus vite on sature.", lire=1.8)
        self.dire(r"Mais $M$ ne dépend de $B$ et $T$ qu'à travers $x = \mu B / k_B T$ : traçons $M$ en fonction de $B/T$…", c=XCOL, lire=0.3)
        ax2 = Axes(x_range=[0, 5.2, 1], y_range=[0, 1.15, 0.5], x_length=7.0, y_length=3.6, tips=True,
                   axis_config={"color": SOFT, "stroke_width": 2}).move_to(ax)
        cibles = VGroup(*[ax2.plot(lambda u: math.tanh(k_ * u), x_range=[0, 5.1], color=c, stroke_width=4) for T, c in Ts])
        nx2 = mx(r"B/T\ (\mathrm{T\cdot K^{-1}})", XCOL, 30).next_to(ax2.c2p(5.2, 0), DOWN, buff=0.12)
        nx_.clear_updaters()
        self.p(*[Transform(a, b) for a, b in zip(courbes, cibles)], ReplacementTransform(nx_, nx2), rt=2.6)
        self.p(Flash(ax2.c2p(2, math.tanh(1.344)), color=XCOL, flash_radius=0.5), rt=0.6)
        self.dire("… toutes les mesures tombent sur UNE SEULE courbe : la signature d'un paramagnétique idéal.", c=XCOL, lire=2.4)
        sat = VGroup(tx("Pour voir la saturation (x ~ 1) :", 22, ABSO),
                     mx(r"B = 2\ \mathrm{T} \;\Rightarrow\; T \approx 1\ \mathrm{K}", ABSO, 34)).arrange(DOWN, buff=0.15)
        sat.next_to(etiq, DOWN, buff=0.6).align_to(etiq, LEFT)
        ajuster(sat, config.frame_width / 2 - 0.3 - sat.get_left()[0])
        sat.next_to(etiq, DOWN, buff=0.6).align_to(etiq, LEFT)
        self.p(FadeIn(sat, shift=UP * 0.15), rt=0.9)
        self.dire("C'est pourquoi la saturation des sels paramagnétiques ne s'observe qu'à quelques kelvins.", lire=2.2)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  9. LA LIMITE DU MODÈLE (et la suite)
    # =================================================================
    def limite(self):
        self.set_q("9. Et sans champ ?")
        self.x.set_value(0.0)
        ens = self.ensemble([-2.8, 0.3, 0], nx=12, ny=5, pas=0.42)
        cnt = self.compteur(Rectangle(width=5, height=2.1).move_to([-2.8, 0.3, 0]))
        eq = VGroup(txm(r"$B = 0$", 30, BCOL), mx(r"\Rightarrow\; x = 0 \;\Rightarrow\; p_\uparrow = p_\downarrow = \tfrac12", WHITE, 40),
                    mx(r"\Rightarrow\; M = 0", MCOL, 50)).arrange(DOWN, buff=0.35).move_to([3.6, 0.6, 0])
        self.p(FadeIn(ens), FadeIn(cnt), rt=0.8)
        self.p(Write(eq[0]), rt=0.6)
        self.p(Write(eq[1]), rt=1.2)
        self.p(self.phase.animate.set_value(22.0), Write(eq[2]), rt=2.4, rate_func=linear)
        self.dire("Sans champ, aucune aimantation, à TOUTE température : des spins indépendants ne s'ordonnent jamais seuls.", c=MCOL, lire=0.3)
        self.p(self.phase.animate.set_value(26.0), rt=2.4, rate_func=linear)
        self.dire("Or le fer est aimanté spontanément sous 770 °C ! Il manque quelque chose : les INTERACTIONS entre spins.", c=ABSO, lire=0.3)
        self.p(self.phase.animate.set_value(29.0), rt=2.6, rate_func=linear)
        ens.clear_updaters(); cnt.clear_updaters()
        self.p(FadeOut(VGroup(eq)), rt=0.5)
        suite = VGroup(tx("Idée de Weiss (prochaine vidéo) :", 26, LAMB, bold=True),
                       mx(r"B \;\longrightarrow\; B + \lambda M", LAMB, 50),
                       tx("chaque spin ressent un champ créé par ses voisins", 22, SOFT),
                       txm(r"→ ordre spontané sous une température critique $T_C$", 22, TCOL)).arrange(DOWN, buff=0.3).move_to([3.4, 0.4, 0])
        ajuster(suite, 6.4)
        suite.move_to([3.4, 0.4, 0])
        self.p(LaggedStart(*[FadeIn(s, shift=UP * 0.15) for s in suite], lag_ratio=0.3), rt=2.2)
        self.dire("Le même calcul, avec un champ qui dépend de M lui-même, fera apparaître la température de Curie.", c=LAMB, lire=2.6)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  À RETENIR
    # =================================================================
    def retenir(self):
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 42, WHITE, bold=True)
        items = VGroup(
            row(etiquette("1", UPC).scale(1.4), txm(r"Deux états, d'énergies $\mp \mu B$ : le champ favorise l'alignement", 24), buff=0.3),
            row(etiquette("2", TCOL).scale(1.4), txm(r"Boltzmann + normalisation : $p_{\uparrow,\downarrow} = e^{\pm x} / (2\cosh x)$, avec $x = \mu B / k_B T$", 24), buff=0.3),
            row(etiquette("3", MCOL).scale(1.4), txm(r"$\langle \mu_z \rangle = \mu \tanh x$ : linéaire si $x \ll 1$, saturé si $x \gg 1$", 24), buff=0.3),
            row(etiquette("4", BOX).scale(1.4), txm(r"Régime usuel $x \ll 1$ : loi de Curie $\chi = C / T$", 24), buff=0.3),
            row(etiquette("5", LAMB).scale(1.4), txm(r"Sans interactions, $M = 0$ en champ nul : pas d'ordre spontané", 24), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        g = VGroup(t, items).arrange(DOWN, buff=0.5)
        ajuster(g, 13.0, 6.9)
        g.move_to(DOWN * 0.2)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=2.4)
        self.pause(5.0)
