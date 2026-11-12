from manim import *
import math

# =====================================================================
#  Vidéo de cours – LA DILUTION (≈ 2 min 15), pour Manim Community (rendu sur GitHub).
#  Vidéo autonome : les explications sont écrites à l'écran (sous-titres),
#  pas besoin d'audio.
#  Partie 1 : le principe sans chiffres (vision macroscopique puis microscopique).
#  Partie 2 : un exemple chiffré rédigé (expression littérale encadrée, application
#             numérique avec unités, phrase réponse), le protocole, et la vérification
#             « particules ».
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
    def p(self, *anims, rt=1.0):
        self.play(*anims, run_time=rt)
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
        lire : temps laissé pour lire (par défaut selon la longueur du texte)."""
        t = tx(s, fs, c, w=12.6)
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
        self.partie1_macro()
        self.partie1_micro()
        self.partie1_relation()
        self.partie2_calcul()
        self.partie2_protocole()
        self.retenir()

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        t = tx("La dilution", 72, WHITE, bold=True)
        s = tx("comprendre avant de calculer", 30, SOFT).next_to(t, DOWN, buff=0.35)
        gouttes = VGroup(*[Circle(radius=r, stroke_width=0, fill_color=SOLUTE, fill_opacity=o)
                           for r, o in ((0.22, 1.0), (0.22, 0.6), (0.22, 0.3), (0.22, 0.12))]).arrange(RIGHT, buff=0.35)
        gouttes.next_to(s, DOWN, buff=0.6)
        self.p(Write(t), rt=1.3)
        self.p(FadeIn(s, shift=UP * 0.2), LaggedStart(*[GrowFromCenter(g) for g in gouttes], lag_ratio=0.25), rt=1.2)
        self.pause(1.2)
        self.hdr_ex = tx("La dilution", 22, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(t, self.hdr_ex), FadeOut(s), FadeOut(gouttes), rt=0.8)

    # =================================================================
    #  PARTIE 1 – sans chiffres : ce qu'on voit
    # =================================================================
    def becher(self, w=1.8, h=2.4, niveau=0.45, op=0.9):
        verre = VGroup(Line(UP * h / 2 + LEFT * w / 2, DOWN * h / 2 + LEFT * w / 2),
                       Line(DOWN * h / 2 + LEFT * w / 2, DOWN * h / 2 + RIGHT * w / 2),
                       Line(DOWN * h / 2 + RIGHT * w / 2, UP * h / 2 + RIGHT * w / 2),
                       Line(UP * h / 2 + LEFT * w / 2, UP * h / 2 + LEFT * w / 2 + LEFT * 0.15 + UP * 0.1))
        verre.set_stroke(WHITE, 3)
        liq = Rectangle(width=w - 0.06, height=h * niveau, stroke_width=0, fill_color=SOLUTE, fill_opacity=op)
        liq.align_to(verre, DOWN).shift(UP * 0.03)
        return VGroup(liq, verre)

    def partie1_macro(self):
        self.set_q("Partie 1 : le principe")
        b = self.becher(w=2.0, h=3.0, niveau=0.3, op=0.9).move_to(LEFT * 3.2 + DOWN * 0.3)
        lab = tx("solution concentrée", 24, SOLUTE).next_to(b, DOWN, buff=0.25)
        self.p(Create(b[1]), rt=0.7)
        self.p(GrowFromEdge(b[0], DOWN), FadeIn(lab), rt=0.9)
        self.dire("Une solution contient un soluté (ici coloré) dissous dans un solvant, souvent l'eau.", lire=2.6)

        # on ajoute de l'eau
        robinet = VGroup(Rectangle(width=0.9, height=0.35, stroke_color=WHITE, stroke_width=2.5, fill_color="#2A2F3A", fill_opacity=1),
                         Rectangle(width=0.25, height=0.35, stroke_color=WHITE, stroke_width=2.5, fill_color="#2A2F3A", fill_opacity=1))
        robinet[1].next_to(robinet[0], DOWN, buff=0).align_to(robinet[0], RIGHT)
        robinet.next_to(b, UP, buff=0.9).shift(RIGHT * 0.1)
        eau_l = tx("eau (solvant)", 22, EAU).next_to(robinet, RIGHT, buff=0.25)
        filet = Line(robinet[1].get_bottom(), [robinet[1].get_x(), b[0].get_top()[1], 0], color=EAU, stroke_width=7)
        self.p(FadeIn(robinet, shift=DOWN * 0.2), FadeIn(eau_l), rt=0.6)
        self.dire("DILUER, c'est ajouter du solvant à une solution.", c=ABSO, lire=0.6)
        self.p(Create(filet), rt=0.4)
        self.p(b[0].animate.stretch_to_fit_height(3.0 * 0.85, about_edge=DOWN).set_fill(SOLUTE, opacity=0.3),
               filet.animate.put_start_and_end_on(robinet[1].get_bottom(), [robinet[1].get_x(), b[0].get_bottom()[1] + 3.0 * 0.85, 0]),
               rt=2.6)
        self.p(FadeOut(filet), rt=0.3)
        lab2 = tx("solution diluée", 24, SOLUTE).move_to(lab)
        self.p(ReplacementTransform(lab, lab2), rt=0.6)
        # comparaison avant / après
        avant = self.becher(w=1.3, h=1.9, niveau=0.3, op=0.9)
        apres = self.becher(w=1.3, h=1.9, niveau=0.85, op=0.3)
        comp = VGroup(VGroup(avant, tx("avant", 20, SOFT).next_to(avant, DOWN, buff=0.15)),
                      Arrow(LEFT * 0.5, RIGHT * 0.5, color=SOFT, buff=0),
                      VGroup(apres, tx("après", 20, SOFT).next_to(apres, DOWN, buff=0.15))).arrange(RIGHT, buff=0.4)
        comp.move_to(RIGHT * 3.0 + UP * 0.2)
        self.p(FadeIn(comp, shift=LEFT * 0.2), rt=0.8)
        pts = VGroup(row(tx("volume :", 22, VOL), tx("augmente ↑", 22, WHITE), buff=0.15),
                     row(tx("couleur :", 22, SOLUTE), tx("plus claire", 22, WHITE), buff=0.15)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        pts.next_to(comp, DOWN, buff=0.5)
        self.p(FadeIn(pts[0], shift=LEFT * 0.2), rt=0.5)
        self.p(FadeIn(pts[1], shift=LEFT * 0.2), rt=0.5)
        self.dire("La couleur s'éclaircit : la solution est MOINS CONCENTRÉE. Mais pourquoi ?", lire=2.4)
        self.macro = VGroup(b, lab2, robinet, eau_l)
        self.p(FadeOut(VGroup(comp, pts)), rt=0.5)

    # =================================================================
    #  PARTIE 1 – vision microscopique
    # =================================================================
    def partie1_micro(self):
        b = self.macro[0]
        # loupe sur le bécher
        loupe = Circle(radius=0.38, color=WHITE, stroke_width=3).move_to(b[0].get_center())
        cote = 1.4                        # côté d'une « unité de volume »
        box1 = Rectangle(width=2 * cote, height=2 * cote, stroke_color=WHITE, stroke_width=3)
        box1.move_to(RIGHT * 0.6 + UP * 0.35).align_to(RIGHT * 0.1, LEFT)
        rayons = VGroup(Line(loupe.get_top(), box1.get_corner(UL), color=SOFT, stroke_width=1.5),
                        Line(loupe.get_bottom(), box1.get_corner(DL), color=SOFT, stroke_width=1.5))
        self.p(FadeOut(VGroup(self.macro[2], self.macro[3])), rt=0.3)
        # on revient à l'état « avant » pour le zoom
        self.p(b[0].animate.stretch_to_fit_height(3.0 * 0.3, about_edge=DOWN).set_fill(SOLUTE, opacity=0.9),
               Transform(self.macro[1], tx("solution concentrée", 24, SOLUTE).move_to(self.macro[1])), rt=0.8)
        loupe.move_to(b[0].get_center())
        rayons = VGroup(Line(loupe.get_top(), box1.get_corner(UL), color=SOFT, stroke_width=1.5),
                        Line(loupe.get_bottom(), box1.get_corner(DL), color=SOFT, stroke_width=1.5))
        self.p(Create(loupe), rt=0.4)
        self.p(Create(rayons), Create(box1), rt=0.8)
        zoom_l = tx("zoom sur les particules", 20, SOFT).next_to(box1, UP, buff=0.15)
        self.p(FadeIn(zoom_l), rt=0.3)

        # particules : 4 par unité de volume au départ (2 x 2 unités)
        offs4 = [np.array(v) for v in ((-0.33, 0.3, 0), (0.32, 0.34, 0), (-0.3, -0.32, 0), (0.34, -0.28, 0))]
        offs2 = [np.array(v) for v in ((-0.3, 0.25, 0), (0.3, -0.25, 0))]
        def centre(box, i, j, cols, rows):
            return box.get_corner(UL) + np.array([cote * (i + 0.5), -cote * (j + 0.5), 0])
        solute = VGroup()
        for j in range(2):
            for i in range(2):
                c = centre(box1, i, j, 2, 2)
                for o in offs4:
                    solute.add(Dot(c + o, radius=0.11, color=SOLUTE))
        rng = np.random.default_rng(7)
        def eau_pts(box, n):
            w, h = box.width, box.height
            return [box.get_corner(DL) + np.array([0.12 + rng.random() * (w - 0.24), 0.12 + rng.random() * (h - 0.24), 0]) for _ in range(n)]
        eau1 = VGroup(*[Dot(pnt, radius=0.045, color=EAU, fill_opacity=0.75) for pnt in eau_pts(box1, 16)])
        leg = VGroup(row(Dot(radius=0.11, color=SOLUTE), tx("particule de soluté", 20, SOLUTE), buff=0.15),
                     row(Dot(radius=0.045, color=EAU), tx("molécule d'eau", 20, EAU), buff=0.15)).arrange(RIGHT, buff=0.6)
        leg.next_to(box1, DOWN, buff=0.3).align_to(box1, LEFT)
        self.p(LaggedStart(*[GrowFromCenter(d) for d in solute], lag_ratio=0.05), FadeIn(eau1), rt=1.2)
        self.p(FadeIn(leg), rt=0.4)
        cpt1 = row(tx("particules de soluté :", 22, SOLUTE), mx("16", SOLUTE, 40), buff=0.15).next_to(zoom_l, UP, buff=0.15).align_to(box1, LEFT)
        self.p(FadeIn(cpt1), rt=0.4)
        self.dire("Au départ : 16 particules de soluté dans un petit volume.", lire=1.6)

        # dilution : la boîte double de volume
        box2 = Rectangle(width=4 * cote, height=2 * cote, stroke_color=WHITE, stroke_width=3).align_to(box1, UL)
        cibles = []
        for j in range(2):
            for i in range(4):
                c = centre(box2, i, j, 4, 2)
                for o in offs2:
                    cibles.append(c + o)
        eau2_new = VGroup(*[Dot(pnt, radius=0.045, color=EAU, fill_opacity=0.75) for pnt in eau_pts(box2, 16)])
        eau1_cibles = eau_pts(box2, 16)
        self.dire("On ajoute de l'eau : le volume DOUBLE…", c=EAU, lire=0.3)
        self.p(Transform(box1, box2), FadeOut(zoom_l), leg.animate.next_to(box2, DOWN, buff=0.3).align_to(box2, LEFT),
               b[0].animate.stretch_to_fit_height(3.0 * 0.6, about_edge=DOWN).set_fill(SOLUTE, opacity=0.45),
               rt=1.0)
        self.p(FadeIn(eau2_new), rt=0.6)
        self.p(*[d.animate.move_to(c) for d, c in zip(solute, cibles)],
               *[d.animate.move_to(c) for d, c in zip(eau1, eau1_cibles)], rt=2.0)
        self.p(Transform(self.macro[1], tx("solution diluée", 24, SOLUTE).move_to(self.macro[1])), rt=0.5)

        # le nombre de particules ne change pas
        cpt2 = row(tx("particules de soluté :", 22, SOLUTE), mx("16", SOLUTE, 40), buff=0.15).move_to(cpt1)
        self.p(Indicate(cpt1[1], color=SOLUTE, scale_factor=1.6), rt=0.8)
        self.p(LaggedStart(*[Indicate(d, color=WHITE, scale_factor=1.6) for d in solute], lag_ratio=0.04), rt=1.4)
        cons = tx("toujours 16 : la QUANTITÉ DE MATIÈRE de soluté n se CONSERVE", 24, ABSO, bold=True)
        self.dire("Toujours 16 particules : la QUANTITÉ DE MATIÈRE de soluté n se CONSERVE.", c=ABSO, lire=2.4)

        # ... mais par unité de volume, il y en a moins
        grille = VGroup()
        for i in range(1, 4):
            grille.add(DashedLine(box2.get_corner(UL) + RIGHT * cote * i, box2.get_corner(DL) + RIGHT * cote * i, color=SOFT, stroke_width=2))
        grille.add(DashedLine(box2.get_left(), box2.get_right(), color=SOFT, stroke_width=2))
        nums = VGroup()
        for j in range(2):
            for i in range(4):
                nums.add(Text("2", font_size=22, color=ABSO, weight=BOLD).move_to(centre(box2, i, j, 4, 2) + np.array([0.5, 0.5, 0])))
        self.p(Create(grille), rt=0.8)
        self.p(LaggedStart(*[FadeIn(n, scale=1.5) for n in nums], lag_ratio=0.08), rt=1.0)
        self.dire("Mais elles occupent plus de place : 2 particules par unité de volume au lieu de 4.", lire=2.0)
        # rappel visuel de l'état initial (miniature)
        mini = VGroup(Rectangle(width=2 * cote, height=2 * cote, stroke_color=SOFT, stroke_width=2))
        for j in range(2):
            for i in range(2):
                c = centre(mini[0], i, j, 2, 2)
                for o in offs4:
                    mini.add(Dot(c + o, radius=0.11, color=SOLUTE))
        mini.add(DashedLine(mini[0].get_top(), mini[0].get_bottom(), color=SOFT, stroke_width=1.5),
                 DashedLine(mini[0].get_left(), mini[0].get_right(), color=SOFT, stroke_width=1.5))
        for j in range(2):
            for i in range(2):
                mini.add(Text("4", font_size=22, color=ABSO, weight=BOLD).move_to(centre(mini[0], i, j, 2, 2) + np.array([0.5, 0.5, 0])))
        mini.scale(0.5)
        mini_l = tx("avant", 18, SOFT)
        mini_g = VGroup(mini_l, mini).arrange(DOWN, buff=0.1)
        mini_g.move_to([b.get_x(), 2.15, 0])
        self.p(FadeIn(mini_g, shift=DOWN * 0.2), rt=0.6)
        self.dire("Moins de particules par unité de volume : la CONCENTRATION DIMINUE.", c=CONC, lire=2.2)
        self.vider_tout()

    # =================================================================
    #  PARTIE 1 – la relation
    # =================================================================
    def partie1_relation(self):
        mere = self.becher(w=1.5, h=2.0, niveau=0.55, op=0.9)
        fille = self.becher(w=2.1, h=2.6, niveau=0.8, op=0.3)
        lm = VGroup(tx("solution MÈRE", 24, WHITE, bold=True),
                    row(mx(r"C_{\text{mère}}", CONC, 34), mx(",", WHITE, 34), mx(r"V_{\text{mère}}", VOL, 34), buff=0.08),
                    tx("(volume prélevé)", 16, SOFT)).arrange(DOWN, buff=0.1)
        lf = VGroup(tx("solution FILLE", 24, WHITE, bold=True),
                    row(mx(r"C_{\text{fille}}", CONC, 34), mx(",", WHITE, 34), mx(r"V_{\text{fille}}", VOL, 34), buff=0.08),
                    tx("(volume final)", 16, SOFT)).arrange(DOWN, buff=0.1)
        gm = VGroup(mere, lm).arrange(DOWN, buff=0.25)
        gf = VGroup(fille, lf).arrange(DOWN, buff=0.25)
        fl = Arrow(LEFT, RIGHT, color=SOFT, buff=0)
        fl_l = tx("+ eau", 22, EAU).next_to(fl, UP, buff=0.1)
        schema = VGroup(gm, VGroup(fl, fl_l), gf).arrange(RIGHT, buff=0.7, aligned_edge=DOWN)
        self.caser(schema, top=3.0, bottom=-0.2)
        fl_l.next_to(fl, UP, buff=0.1)
        self.p(FadeIn(gm, shift=RIGHT * 0.2), rt=0.8)
        self.p(GrowArrow(fl), FadeIn(fl_l), FadeIn(gf, shift=RIGHT * 0.2), rt=0.9)
        self.dire("On parle de solution MÈRE (de départ) et de solution FILLE (obtenue).", lire=2.2)

        # conservation de n
        eq1 = row(mx(r"n_{\text{mère}}", SOLUTE, 50), mx("=", WHITE, 50), mx(r"n_{\text{fille}}", SOLUTE, 50), buff=0.25)
        eq1.next_to(schema, DOWN, buff=0.45)
        self.p(Write(eq1), rt=1.0)
        self.dire("Le soluté prélevé se retrouve en entier dans la fille : n se conserve.", c=SOLUTE, lire=1.8)
        rap = row(tx("et comme", 22, SOFT), mx(r"n = C \times V", WHITE, 40), buff=0.2).next_to(eq1, RIGHT, buff=0.8)
        self.p(FadeIn(rap, shift=LEFT * 0.2), rt=0.6)
        eq2 = row(mx(r"C_{\text{mère}}", CONC, 50), mx(r"\times", WHITE, 50), mx(r"V_{\text{mère}}", VOL, 50), mx("=", WHITE, 50),
                  mx(r"C_{\text{fille}}", CONC, 50), mx(r"\times", WHITE, 50), mx(r"V_{\text{fille}}", VOL, 50), buff=0.15)
        eq2.move_to(eq1).set_x(0)
        self.p(TransformMatchingShapes(eq1, eq2), FadeOut(rap), rt=1.4)
        cad = SurroundingRectangle(eq2, color=BOX, buff=0.2, corner_radius=0.1, stroke_width=4)
        self.p(Create(cad), Flash(eq2, color=BOX, flash_radius=1.2), rt=0.8)
        self.dire("La relation de la dilution : C_mère × V_mère = C_fille × V_fille", c=BOX, lire=2.2)
        # facteur de dilution
        F = row(mx("F", ABSO, 46), mx("=", WHITE, 46), frac(mx(r"C_{\text{mère}}", CONC, 46), mx(r"C_{\text{fille}}", CONC, 46)),
                mx("=", WHITE, 46), frac(mx(r"V_{\text{fille}}", VOL, 46), mx(r"V_{\text{mère}}", VOL, 46)), buff=0.2)
        F.next_to(cad, DOWN, buff=0.35)
        self.p(FadeOut(VGroup(gm, fl, fl_l, gf)), VGroup(eq2, cad).animate.shift(UP * 2.4), rt=0.8)
        F.next_to(cad, DOWN, buff=0.5)
        self.p(Write(F), rt=1.2)
        self.dire("Facteur de dilution F : la solution est F fois moins concentrée, dans un volume F fois plus grand.", c=ABSO, lire=2.8)
        self.effacer_sous_titre()
        self.vider_tout()

    # =================================================================
    #  PARTIE 2 – avec des chiffres
    # =================================================================
    def partie2_calcul(self):
        self.set_q("Partie 2 : un exemple chiffré")
        q = self.question("On veut préparer 100,0 mL de solution fille à 0,020 mol·L⁻¹ à partir d'une solution mère\n"
                          "à 0,10 mol·L⁻¹. Quel volume de solution mère faut-il prélever ?", rt=1.0)
        self.pause(3.2)
        don = VGroup(etiquette("Données", SOFT),
                     row(mx(r"C_{\text{mère}} =", CONC, 34), val(r"0{,}10", r"\mathrm{mol\cdot L^{-1}}", CONC, 34), buff=0.1),
                     row(mx(r"C_{\text{fille}} =", CONC, 34), val(r"0{,}020", r"\mathrm{mol\cdot L^{-1}}", CONC, 34), buff=0.1),
                     row(mx(r"V_{\text{fille}} =", VOL, 34), val(r"100{,}0", r"\mathrm{mL}", VOL, 34), buff=0.1),
                     row(mx(r"V_{\text{mère}} = \ ?", VOL, 34), buff=0.1)).arrange(RIGHT, buff=0.35)
        cons = row(mx(r"C_{\text{mère}}", CONC, 44), mx(r"\times", WHITE, 44), mx(r"V_{\text{mère}}", VOL, 44), mx("=", WHITE, 44),
                   mx(r"C_{\text{fille}}", CONC, 44), mx(r"\times", WHITE, 44), mx(r"V_{\text{fille}}", VOL, 44), buff=0.15)
        lit = row(mx(r"V_{\text{mère}}", VOL, 46), mx("=", WHITE, 46),
                  frac(row(mx(r"C_{\text{fille}}", CONC, 46), mx(r"\times", WHITE, 46), mx(r"V_{\text{fille}}", VOL, 46), buff=0.12),
                       mx(r"C_{\text{mère}}", CONC, 46)), buff=0.2)
        ligne = VGroup(cons, Arrow(LEFT * 0.4, RIGHT * 0.4, color=SOFT, buff=0), lit).arrange(RIGHT, buff=0.45)
        nCf = val(r"0{,}020", r"\mathrm{mol\cdot L^{-1}}", CONC, 40)
        nVf = val(r"100{,}0", r"\mathrm{mL}", VOL, 40)
        dCm = val(r"0{,}10", r"\mathrm{mol\cdot L^{-1}}", CONC, 40)
        res = val("20", r"\mathrm{mL}", RES, 46)
        an = row(mx(r"V_{\text{mère}}", VOL, 40), mx("=", WHITE, 40), frac(row(nCf, mx(r"\times", WHITE, 40), nVf, buff=0.12), dCm),
                 mx("=", WHITE, 40), res, buff=0.18)
        verif = row(tx("vérification :", 20, SOFT), mx(r"F = \frac{0{,}10}{0{,}020} = 5", ABSO, 36), tx("et", 20, SOFT),
                    mx(r"\frac{100{,}0\ \mathrm{mL}}{20\ \mathrm{mL}} = 5", ABSO, 36), mx(r"\checkmark", RES, 40), buff=0.2)
        page = VGroup(don, ligne, an, verif).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        self.caser(page, top=self.haut() - 0.15, bottom=-2.3)

        self.p(FadeIn(don[0]), rt=0.3)
        self.p(LaggedStart(*[FadeIn(d, shift=DOWN * 0.15) for d in don[1:]], lag_ratio=0.3), rt=1.6)
        self.p(Indicate(don[4], color=VOL), rt=0.7)
        self.dire("On part de la conservation de la quantité de matière de soluté.", lire=1.2)
        self.p(Write(cons), rt=1.3)
        self.dire("On isole l'inconnue V_mère AVANT de remplacer par les valeurs.", lire=0.4)
        self.p(GrowArrow(ligne[1]), TransformMatchingShapes(cons.copy(), lit), rt=1.5)
        self.encadre(lit, rt=0.8)
        self.pause(0.8)

        self.tag_an(an, rt=0.3)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1]), FadeIn(an[2][0][1]), rt=0.3)
        self.dire("On remplace chaque grandeur par sa valeur, AVEC son unité.", c=AN_C, lire=0.2)
        self.morph([(don[2][1], nCf), (don[3][1], nVf), (don[1][1], dCm)], rt=1.6)
        self.barrer(nCf[1], dCm[1], rt=0.8)
        self.dire("Les mol·L⁻¹ se simplifient : il reste des mL, c'est bien un volume.", c=UNIT, lire=1.4)
        self.p(Write(an[3]), Write(res), rt=0.9)
        self.p(Circumscribe(res, color=RES), rt=0.9)
        self.p(FadeIn(verif, shift=UP * 0.15), rt=0.9)
        self.pause(1.4)
        self.effacer_sous_titre(rt=0.3)
        self.reponse("Il faut prélever V_mère = 20 mL de solution mère (pipette jaugée de 20,0 mL),\n"
                     "puis compléter avec de l'eau jusqu'à 100,0 mL.", rt=1.4)
        self.pause(3.0)

    # =================================================================
    #  PARTIE 2 – le protocole, et ce qui se passe pour les particules
    # =================================================================
    def partie2_protocole(self):
        self.vider_tout(garder=[self.cur_q])
        # matériel
        mere = self.becher(w=1.6, h=2.0, niveau=0.6, op=0.9)
        m_l = tx("solution mère", 20, SOLUTE).next_to(mere, DOWN, buff=0.15)
        ballon = Circle(radius=0.85, stroke_color=WHITE, stroke_width=3, fill_color=SOLUTE, fill_opacity=0)
        col = Rectangle(width=0.36, height=2.0, stroke_color=WHITE, stroke_width=3).next_to(ballon, UP, buff=-0.05)
        col_liq = Rectangle(width=0.36, height=0.6, stroke_width=0, fill_color=SOLUTE, fill_opacity=0).align_to(col, DOWN)
        trait = Line(LEFT * 0.28, RIGHT * 0.28, color="#FF5555", stroke_width=3).move_to(col_liq.get_top())
        fiole = VGroup(col_liq, ballon, col, trait)
        f_l = tx("fiole jaugée 100,0 mL", 20, VOL).next_to(ballon, DOWN, buff=0.15)
        mat = VGroup(VGroup(mere, m_l), VGroup(fiole, f_l)).arrange(RIGHT, buff=4.2, aligned_edge=DOWN)
        self.caser(mat, top=self.haut() - 1.6, bottom=-2.4)
        tube = Rectangle(width=0.14, height=1.9, stroke_color=WHITE, stroke_width=2.5)
        pointe = Polygon(tube.get_corner(DL), tube.get_corner(DR), tube.get_bottom() + DOWN * 0.3, stroke_color=WHITE, stroke_width=2.5)
        liq_p = Rectangle(width=0.14, height=0.01, stroke_width=0, fill_color=SOLUTE, fill_opacity=0.9).align_to(tube, DOWN)
        tr_p = Line(LEFT * 0.12, RIGHT * 0.12, color="#FF5555", stroke_width=3).move_to(tube.get_top() + DOWN * 0.5)
        pip = VGroup(liq_p, tube, pointe, tr_p)
        pip_l = tx("pipette jaugée 20,0 mL", 20, VOL)
        pip.move_to(mere.get_top() + UP * 1.25)
        pip_l.next_to(pip, RIGHT, buff=0.2)
        self.p(FadeIn(mat), FadeIn(pip), FadeIn(pip_l), rt=0.8)

        etapes = ["① Prélever 20,0 mL de solution mère à la pipette jaugée.",
                  "② Les verser dans la fiole jaugée de 100,0 mL.",
                  "③ Compléter avec de l'eau distillée jusqu'au trait de jauge.",
                  "④ Boucher et agiter : la solution fille est prête."]
        # ①
        self.dire(etapes[0], lire=0.2)
        self.p(pip.animate.shift(DOWN * (pip.get_bottom()[1] - mere[0].get_bottom()[1] - 0.15)), pip_l.animate.shift(
            DOWN * (pip.get_bottom()[1] - mere[0].get_bottom()[1] - 0.15)), rt=0.8)
        self.p(liq_p.animate.stretch_to_fit_height(tr_p.get_y() - tube.get_bottom()[1], about_edge=DOWN),
               mere[0].animate.stretch_to_fit_height(mere[0].height * 0.8, about_edge=DOWN), rt=1.2)
        self.pause(0.5)
        # ②
        dessus = fiole[2].get_top() + DOWN * 0.45
        self.dire(etapes[1], lire=0.2)
        delta = dessus - pip.get_bottom()
        self.p(VGroup(pip, pip_l).animate.shift(UP * 1.2), rt=0.5)
        delta = dessus - pip.get_bottom()
        self.p(VGroup(pip, pip_l).animate.shift(delta), rt=1.0)
        self.p(liq_p.animate.stretch_to_fit_height(0.01, about_edge=DOWN), ballon.animate.set_fill(SOLUTE, opacity=0.9), rt=1.2)
        self.p(FadeOut(VGroup(pip, pip_l)), rt=0.4)
        # ③
        self.dire(etapes[2], c=EAU, lire=0.2)
        filet = Line(col.get_top() + UP * 0.8, col.get_top(), color=EAU, stroke_width=6)
        self.p(Create(filet), rt=0.3)
        self.p(ballon.animate.set_fill(SOLUTE, opacity=0.22), col_liq.animate.set_fill(SOLUTE, opacity=0.22), rt=2.0)
        self.p(FadeOut(filet), Flash(trait, color="#FF5555", flash_radius=0.3), rt=0.6)
        # ④
        self.dire(etapes[3], lire=0.2)
        self.p(Wiggle(VGroup(fiole, f_l), scale_value=1.05, rotation_angle=0.06 * TAU), rt=1.2)
        f_l2 = tx("solution fille : 5 fois moins concentrée", 20, SOLUTE).move_to(f_l)
        self.p(ReplacementTransform(f_l, f_l2), rt=0.6)
        self.pause(1.0)

        # vision microscopique : 5 particules par unité de volume -> 1
        self.vider_tout(garder=[self.cur_q])
        u = 0.9
        def boite(nx, ny, par, couleur_num):
            cadre = Rectangle(width=nx * u, height=ny * u, stroke_color=WHITE, stroke_width=2.5)
            g = VGroup(cadre)
            offs = {5: [(-0.25, 0.25), (0.25, 0.25), (0, 0), (-0.25, -0.25), (0.25, -0.25)], 1: [(0, 0)]}[par]
            for j in range(ny):
                for i in range(nx):
                    c = cadre.get_corner(UL) + np.array([u * (i + 0.5), -u * (j + 0.5), 0])
                    for ox, oy in offs:
                        g.add(Dot(c + np.array([ox, oy, 0]), radius=0.07, color=SOLUTE))
            lignes = VGroup(*[DashedLine(cadre.get_corner(UL) + RIGHT * u * i, cadre.get_corner(DL) + RIGHT * u * i,
                                         color=SOFT, stroke_width=1.2) for i in range(1, nx)])
            lignes.add(*[DashedLine(cadre.get_corner(UL) + DOWN * u * j, cadre.get_corner(UR) + DOWN * u * j,
                                    color=SOFT, stroke_width=1.2) for j in range(1, ny)])
            return VGroup(g, lignes)
        bm = boite(1, 2, 5, ABSO)          # 2 unités de volume, 10 particules
        bf = boite(5, 2, 1, ABSO)          # 10 unités de volume, 10 particules
        lm = VGroup(tx("mère : 20 mL", 22, WHITE), tx("5 particules / unité de volume", 18, ABSO)).arrange(DOWN, buff=0.08)
        lf = VGroup(tx("fille : 100 mL", 22, WHITE), tx("1 particule / unité de volume", 18, ABSO)).arrange(DOWN, buff=0.08)
        gm = VGroup(bm, lm).arrange(DOWN, buff=0.25)
        gf = VGroup(bf, lf).arrange(DOWN, buff=0.25)
        fl = Arrow(LEFT * 0.6, RIGHT * 0.6, color=SOFT, buff=0)
        fl_l = tx("× 5 en volume", 20, VOL).next_to(fl, UP, buff=0.1)
        vue = VGroup(gm, VGroup(fl, fl_l), gf).arrange(RIGHT, buff=0.6)
        self.caser(vue, top=self.haut() - 0.6, bottom=-2.3)
        self.p(FadeIn(gm, shift=RIGHT * 0.2), rt=0.8)
        self.p(GrowArrow(fl), FadeIn(fl_l), rt=0.5)
        copies = VGroup(*[d.copy() for d in bm[0][1:]])
        self.p(FadeIn(bf[0][0]), FadeIn(bf[1]), FadeIn(lf), rt=0.6)
        self.p(*[ReplacementTransform(c, d) for c, d in zip(copies, bf[0][1:])], rt=1.6)
        self.dire("Les mêmes 10 particules (n conservée) dans 5 fois plus de volume : 5 fois moins concentrée.", c=ABSO, lire=2.6)

    # =================================================================
    #  À RETENIR
    # =================================================================
    def retenir(self):
        self.effacer_sous_titre(rt=0.3)
        self.vider_tout(rt=0.6)
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 42, WHITE, bold=True)
        l1 = row(etiquette("1", SOLUTE).scale(1.4), tx("Diluer = ajouter du solvant : la quantité de matière de soluté se conserve.", 24), buff=0.3)
        l2 = row(etiquette("2", BOX).scale(1.4), mx(r"C_{\text{mère}} \times V_{\text{mère}} = C_{\text{fille}} \times V_{\text{fille}}", BOX, 42), buff=0.3)
        l3 = row(etiquette("3", ABSO).scale(1.4),
                 mx(r"F = \frac{C_{\text{mère}}}{C_{\text{fille}}} = \frac{V_{\text{fille}}}{V_{\text{mère}}}", ABSO, 40),
                 tx("(F > 1)", 22, SOFT), buff=0.3)
        items = VGroup(l1, l2, l3).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        g = VGroup(t, items).arrange(DOWN, buff=0.6)
        ajuster(g, 13.0, 6.8)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.35), rt=1.8)
        self.pause(4.0)
