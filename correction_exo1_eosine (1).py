from manim import *
import math

# =====================================================================
#  Correction en vidéo – Exercice 1 : L'éosine (spectrophotométrie)
#  Version 2 – pour Manim Community (rendu sur GitHub).
#
#  Vidéo MUETTE, calée sur l'audio du professeur (fichier SRT) :
#  au montage, placer la vidéo et l'audio tous les deux à 0 s.
#
#  Rédaction attendue à chaque calcul (comme en évaluation) :
#    1. expression littérale encadrée
#    2. application numérique avec les unités
#    3. résultat avec son unité
#    4. phrase réponse
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


# ---------- Données de l'énoncé ----------
C_ETALON = [0, 0.005, 0.007, 0.010, 0.012, 0.015, 0.017, 0.020]
A_ETALON = [0, 0.50, 0.65, 0.95, 1.14, 1.42, 1.63, 1.90]
C_TXT = ["0", "0{,}005", "0{,}007", "0{,}010", "0{,}012", "0{,}015", "0{,}017", "0{,}020"]
A_TXT = ["0", "0{,}50", "0{,}65", "0{,}95", "1{,}14", "1{,}42", "1{,}63", "1{,}90"]
A_S0 = ["1{,}571", "1{,}506", "1{,}540", "1{,}506", "1{,}571", "1{,}541", "1{,}571", "1{,}523", "1{,}517"]
A_S0_NUM = [1.571, 1.506, 1.540, 1.506, 1.571, 1.541, 1.571, 1.523, 1.517]
K = 95.0
A_MOY = 1.54
CM0 = A_MOY / K


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

    def graphe(self, x_len=7.0, y_len=4.2, fs=22):
        """Graphique A = f(Cm) : renvoie (axes, décor, points, droite)."""
        ax = Axes(x_range=[0, 0.0225, 0.005], y_range=[0, 2.15, 0.5], x_length=x_len, y_length=y_len,
                  tips=True, axis_config={"color": SOFT, "stroke_width": 2})
        grille = VGroup()
        for v in (0.005, 0.010, 0.015, 0.020):
            grille.add(Line(ax.c2p(v, 0), ax.c2p(v, 2.1), stroke_color=WHITE, stroke_width=1, stroke_opacity=0.12))
        for v in (0.5, 1.0, 1.5, 2.0):
            grille.add(Line(ax.c2p(0, v), ax.c2p(0.0215, v), stroke_color=WHITE, stroke_width=1, stroke_opacity=0.12))
        labs = VGroup()
        for v, s in [(0.005, "0{,}005"), (0.010, "0{,}010"), (0.015, "0{,}015"), (0.020, "0{,}020")]:
            labs.add(mx(s, SOFT, fs).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
        for v, s in [(0.5, "0{,}5"), (1.0, "1{,}0"), (1.5, "1{,}5"), (2.0, "2{,}0")]:
            labs.add(mx(s, SOFT, fs).next_to(ax.c2p(0, v), LEFT, buff=0.15))
        xl = mx(r"C_m\ (\mathrm{g\cdot L^{-1}})", CONC, fs + 4).next_to(ax.c2p(0.0225, 0), DOWN, buff=0.5).shift(LEFT * 0.7)
        yl = mx("A", ABSO, fs + 8).next_to(ax.c2p(0, 2.15), LEFT, buff=0.2)
        pts = VGroup(*[Dot(ax.c2p(c, a), radius=0.065, color=WHITE) for c, a in zip(C_ETALON, A_ETALON)])
        droite = Line(ax.c2p(0, 0), ax.c2p(0.0215, K * 0.0215), color=KCOL, stroke_width=4)
        return ax, VGroup(grille, labs, xl, yl), pts, droite

    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.cur_q = None
        self.intro()
        self.question1()
        self.question2()
        self.question3()
        self.question4()
        self.question5()
        self.question6()
        self.question9()
        self.question10()
        self.conclusion()

    # =================================================================
    #  INTRODUCTION  (0 s → 60,7 s)
    # =================================================================
    def intro(self):
        self.at(0.8)
        sur = tx("Spectrophotométrie – correction", 28, SOFT)
        titre = tx("Exercice 1 : l'éosine", 64, WHITE, bold=True)
        bloc = VGroup(sur, titre).arrange(DOWN, buff=0.3)
        trait = Line(LEFT, RIGHT, color=MAGENTA, stroke_width=5).set_width(titre.width).next_to(titre, DOWN, buff=0.25)
        self.p(FadeIn(sur, shift=DOWN * 0.2), Write(titre), rt=1.8)
        self.p(GrowFromCenter(trait), rt=0.7)
        self.hdr_ex = tx("Exercice 1 – L'éosine", 22, SOFT).to_corner(UL, buff=0.3)
        self.at(4.0)
        self.p(ReplacementTransform(titre, self.hdr_ex), FadeOut(sur), FadeOut(trait), rt=0.9)

        # --- l'éosine, antiseptique vendu en dosettes
        self.at(5.0)
        dos = dosette(r"\text{dosette}", 0.95, h=2.3)
        dos[1].set_color(SOFT)
        nom = Text("ÉOSINE", font_size=20, color=WHITE, weight=BOLD).rotate(PI / 2).move_to(dos[0][0])
        dos_g = VGroup(dos, nom).move_to(LEFT * 4.3 + UP * 0.6)
        l1 = tx("Antiseptique local", 38, WHITE, bold=True)
        l2 = tx("vendu en dosettes, en pharmacie", 30, SOFT)
        infos = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(dos_g, RIGHT, buff=1.2).shift(UP * 0.3)
        self.p(DrawBorderThenFill(dos[0]), FadeIn(nom), FadeIn(dos[1]), rt=1.6)
        self.p(FadeIn(l1, shift=LEFT * 0.3), rt=0.9)
        self.at(7.8)
        self.p(FadeIn(l2, shift=LEFT * 0.3), rt=0.9)

        self.at(12.0)
        ob_t = tx("Objectif", 24, ABSO, bold=True)
        ob_1 = row(tx("déterminer la concentration massique", 28), mx("C_m", CONC, 42), buff=0.2)
        ob_2 = tx("d'éosine dans la solution commerciale", 28)
        ob = VGroup(ob_t, ob_1, ob_2).arrange(DOWN, buff=0.18)
        ob_box = SurroundingRectangle(ob, color=ABSO, buff=0.3, corner_radius=0.15, stroke_width=2.5)
        ob_g = VGroup(ob_box, ob).move_to(DOWN * 2.35)
        self.p(Create(ob_box), FadeIn(ob, shift=UP * 0.2), rt=1.5)
        self.at(16.0)
        self.p(Indicate(ob_1[1], color=CONC, scale_factor=1.5), rt=1.2)
        self.at(19.7)
        self.p(Indicate(dos_g, color=MAGENTA, scale_factor=1.08), rt=1.0)

        # --- les documents
        self.at(21.4)
        self.vider()
        t1 = tableau([[r"C_m\ (\mathrm{g\cdot L^{-1}})"] + C_TXT, ["A"] + A_TXT], fs=24, couleurs_tetes=[CONC, ABSO])
        doc1 = carte("Document 1 : absorbance des solutions étalons", t1)
        ajuster(doc1, 12.5)
        ax_s = Axes(x_range=[300, 650, 50], y_range=[0, 1.3, 0.4], x_length=6.0, y_length=2.2,
                    tips=False, axis_config={"color": SOFT, "stroke_width": 2})
        lx_s = VGroup(*[mx(str(v), SOFT, 20).next_to(ax_s.c2p(v, 0), DOWN, buff=0.12) for v in (300, 400, 500, 600)])
        lab_s = VGroup(mx(r"\lambda\ (\mathrm{nm})", SOFT, 20).next_to(ax_s.c2p(650, 0), RIGHT, buff=0.15),
                       mx("A", ABSO, 24).next_to(ax_s.c2p(300, 1.3), LEFT, buff=0.1))
        fond_s = aire(ax_s, spectre, 300, 640, MAGENTA, 0.25, n=140)
        courbe_s = trace(ax_s, spectre, 300, 640, MAGENTA, 3)
        spec = VGroup(ax_s, lx_s, lab_s, fond_s, courbe_s)
        doc2 = carte("Document 2 : spectre d'absorption de l'éosine", spec)
        docs = VGroup(doc1, doc2).arrange(DOWN, buff=0.45)
        self.caser(docs, top=3.05, bottom=-3.75)
        self.p(FadeIn(doc1[0]), Create(doc1[1]), rt=0.8)
        self.p(Create(t1[1]), LaggedStart(*[FadeIn(c) for c in t1[0]], lag_ratio=0.05), rt=2.0)
        self.at(24.5)
        self.p(Circumscribe(t1, color=ABSO, buff=0.05), rt=1.5)
        self.at(27.4)
        self.p(FadeIn(doc2[0]), Create(doc2[1]), Create(ax_s), FadeIn(lx_s), FadeIn(lab_s), rt=1.0)
        self.p(Create(courbe_s), FadeIn(fond_s), rt=1.6)

        # --- le protocole : deux dilutions -> S0
        self.at(31.8)
        self.vider()
        d0 = dosette(r"2{,}00\ \mathrm{mL}", 0.95, h=1.3)
        f1 = fiole(r"1{,}00\ \mathrm{L}", 0.5, r=0.62)
        f2 = fiole(r"25{,}0\ \mathrm{mL}", 0.25, r=0.42)
        verre = VGroup(d0, f1, f2).arrange(RIGHT, buff=3.0, aligned_edge=DOWN)
        fl1 = Arrow(d0[0].get_right(), f1[0].get_left(), color=SOFT, buff=0.3, stroke_width=4)
        fl2 = Arrow(f1[0].get_right(), f2[0].get_left(), color=SOFT, buff=0.3, stroke_width=4)
        e1 = tx("dilution 1", 20, SOFT).next_to(fl1, UP, buff=0.12)
        pip = pipette(0.5, h=1.0)
        e2 = VGroup(tx("dilution 2", 20, SOFT), row(pip, mx(r"10{,}0\ \mathrm{mL}", VOL, 24), buff=0.12)).arrange(DOWN, buff=0.12)
        e2.next_to(fl2, UP, buff=0.12)
        s0 = mx("S_0", CONC, 44).next_to(f2[0], RIGHT, buff=0.3)
        proto = VGroup(verre, fl1, fl2, e1, e2, s0)
        self.caser(proto, top=2.9, bottom=-0.6)
        self.p(FadeIn(d0, shift=UP * 0.2), rt=0.8)
        self.p(Indicate(d0[0], color=MAGENTA), rt=1.0)
        self.at(36.2)
        self.p(GrowArrow(fl1), FadeIn(e1), FadeIn(f1, shift=LEFT * 0.2), rt=1.4)
        self.at(38.4)
        self.p(GrowArrow(fl2), FadeIn(e2), FadeIn(f2, shift=LEFT * 0.2), rt=1.4)
        self.at(41.0)
        self.p(Write(s0), Flash(s0, color=CONC, flash_radius=0.5), rt=1.2)

        self.at(43.5)
        t9 = tableau([[r"\text{Binôme}"] + [str(i + 1) for i in range(9)], ["A"] + A_S0], fs=24, couleurs_tetes=[SOFT, ABSO])
        for c in t9[0][10:]:
            c.set_color(ABSO)
        t9_t = row(tx("Absorbance de", 24), mx("S_0", CONC, 34), tx("mesurée par 9 binômes", 24), buff=0.15)
        bloc9 = VGroup(t9_t, t9).arrange(DOWN, buff=0.3)
        ajuster(bloc9, 12.8)
        bloc9.next_to(proto, DOWN, buff=0.55).set_x(0)
        self.p(FadeIn(t9_t), Create(t9[1]), rt=1.2)
        self.p(LaggedStart(*[FadeIn(c) for c in t9[0][:10]], lag_ratio=0.05), rt=1.0)
        self.at(49.1)
        self.p(LaggedStart(*[FadeIn(c, shift=DOWN * 0.15) for c in t9[0][10:]], lag_ratio=0.2), rt=2.5)

        # --- feuille de route
        self.at(55.5)
        self.vider()
        titre_r = tx("Comment s'y prendre ?", 40, WHITE, bold=True)
        etapes = ["1  Couleur", "2  Gamme", "3  Droite", "4  Beer-Lambert",
                  "5  Moyenne", "6  Concentration", "9  % massique", "10  Cohérence"]
        chips = VGroup()
        for s in etapes:
            t = tx(s, 22, WHITE)
            r = RoundedRectangle(corner_radius=0.15, width=2.9, height=0.65, stroke_color=ABSO, stroke_width=2,
                                 fill_color=ABSO, fill_opacity=0.08)
            chips.add(VGroup(r, t.move_to(r)))
        grille = VGroup(VGroup(*chips[:4]).arrange(RIGHT, buff=0.25), VGroup(*chips[4:]).arrange(RIGHT, buff=0.25)).arrange(DOWN, buff=0.3)
        VGroup(titre_r, grille).arrange(DOWN, buff=0.7)
        self.p(Write(titre_r), rt=1.0)
        self.p(LaggedStart(*[FadeIn(c, shift=UP * 0.2) for c in chips], lag_ratio=0.12), rt=2.0)
        self.at(59.4)
        self.vider(rt=0.6)

    # =================================================================
    #  QUESTION 1  (60,8 s → 105,9 s)
    # =================================================================
    def question1(self):
        self.at(60.8)
        self.set_q("Question 1")
        self.question("1) Déterminer la couleur d'une solution aqueuse d'éosine. Justifier avec son spectre.")

        self.at(68.1)
        ax = Axes(x_range=[300, 660, 50], y_range=[0, 1.3, 0.4], x_length=10.0, y_length=3.4,
                  tips=True, axis_config={"color": SOFT, "stroke_width": 2})
        lx = VGroup(*[mx(str(v), SOFT, 22).next_to(ax.c2p(v, 0), DOWN, buff=0.5) for v in (300, 400, 500, 600)])
        ly = VGroup(*[mx(s, SOFT, 22).next_to(ax.c2p(300, v), LEFT, buff=0.12)
                      for v, s in ((0.4, "0{,}4"), (0.8, "0{,}8"), (1.2, "1{,}2"))])
        nx = mx(r"\lambda\ (\mathrm{nm})", WHITE, 26).next_to(ax.c2p(660, 0), DOWN, buff=0.5)
        ny = mx("A", ABSO, 32).next_to(ax.c2p(300, 1.3), LEFT, buff=0.15)
        dx = ax.c2p(305, 0)[0] - ax.c2p(300, 0)[0]
        bande = VGroup(*[Rectangle(width=dx * 1.03, height=0.2, stroke_width=0, fill_color=wl_color(w), fill_opacity=1)
                         .move_to(ax.c2p(w + 2.5, 0) + DOWN * 0.2) for w in range(380, 655, 5)])
        vis = tx("lumière visible", 18, SOFT).next_to(bande, DOWN, buff=0.45)
        graph = VGroup(ax, lx, ly, nx, ny, bande, vis)
        self.caser(graph, top=self.haut() - 0.2, bottom=-2.7, x=0.2)
        courbe = trace(ax, spectre, 300, 645, WHITE, 4)
        couleurs = aire_couleurs(ax, spectre, 380, 645, 5, 0.85)
        self.p(Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(nx), FadeIn(ny), rt=1.0)
        self.p(Create(courbe), rt=1.2)

        self.at(70.4)
        self.p(LaggedStart(*[FadeIn(b) for b in bande], lag_ratio=0.02), FadeIn(vis), rt=1.8)
        self.p(LaggedStart(*[FadeIn(c) for c in couleurs], lag_ratio=0.03), rt=1.6)

        self.at(74.3)
        pic = DashedLine(ax.c2p(528, 0), ax.c2p(528, 1.13), color=GREEN, stroke_width=3)
        lmax = mx(r"\lambda_{max}\approx 530\ \mathrm{nm}", GREEN, 32).next_to(ax.c2p(560, 1.05), RIGHT, buff=0.2)
        self.p(Create(pic), Write(lmax), rt=1.2)
        self.at(76.3)
        zone = SurroundingRectangle(VGroup(*couleurs[23:37]), color=GREEN, buff=0.08, stroke_width=3)
        absv = tx("absorbe dans le VERT", 28, GREEN, bold=True).next_to(lmax, DOWN, buff=0.3).align_to(lmax, LEFT)
        self.p(Create(zone), Write(absv), rt=1.3)

        # --- synthèse additive : blanc = R + V + B
        self.at(78.6)
        self.p(*[FadeOut(m) for m in (graph, courbe, couleurs, pic, zone)],
               VGroup(lmax, absv).animate.scale(0.8).to_corner(UR, buff=0.4).shift(DOWN * 0.9), rt=0.9)
        cuve = Rectangle(width=1.3, height=2.1, stroke_color=WHITE, stroke_width=3,
                         fill_color=MAGENTA, fill_opacity=0.35).move_to(DOWN * 0.3)
        cuve_l = tx("solution d'éosine", 20, SOFT).next_to(cuve, DOWN, buff=0.15)
        depart = LEFT * 6.0 + DOWN * 0.3
        blanc = Arrow(depart, cuve.get_left(), color=WHITE, buff=0.05, stroke_width=10,
                      max_tip_length_to_length_ratio=0.06)
        bl_lab = tx("lumière blanche", 22, WHITE).next_to(blanc, UP, buff=0.15)
        self.p(FadeIn(cuve), FadeIn(cuve_l), rt=0.8)
        self.p(GrowArrow(blanc), FadeIn(bl_lab), rt=1.2)

        self.at(85.7)
        ys = [0.38, 0.0, -0.38]
        cols = [RED, GREEN, BLUE]
        rvb = VGroup(*[Arrow(depart + UP * y, cuve.get_left() + UP * y, color=c, buff=0.05, stroke_width=8,
                             max_tip_length_to_length_ratio=0.06) for y, c in zip(ys, cols)])
        eq_rvb = row(tx("blanc", 26), tx("=", 26), tx("rouge", 26, RED), tx("+", 26),
                     tx("vert", 26, GREEN), tx("+", 26), tx("bleu", 26, BLUE), buff=0.15)
        eq_rvb.next_to(self.cur_q, DOWN, buff=0.45).set_x(-2.5)
        self.p(ReplacementTransform(blanc, rvb), FadeOut(bl_lab), Write(eq_rvb), rt=1.6)

        self.at(90.2)
        vert = rvb[1]
        self.p(vert.animate.put_start_and_end_on(vert.get_start(), cuve.get_center()), rt=1.0)
        self.p(Flash(cuve.get_center(), color=GREEN, flash_radius=0.45), FadeOut(vert, scale=0.3),
               Indicate(eq_rvb[4], color=GREEN), rt=0.9)
        sortie = VGroup(
            Arrow(cuve.get_right() + UP * 0.38, RIGHT * 3.4 + UP * 0.08, color=RED, buff=0.05, stroke_width=8,
                  max_tip_length_to_length_ratio=0.1),
            Arrow(cuve.get_right() + DOWN * 0.38, RIGHT * 3.4 + DOWN * 0.68, color=BLUE, buff=0.05, stroke_width=8,
                  max_tip_length_to_length_ratio=0.1),
        )
        self.p(GrowArrow(sortie[0]), GrowArrow(sortie[1]), rt=1.0)
        trans = tx("transmis", 20, SOFT).next_to(sortie, DOWN, buff=0.2)
        self.p(FadeIn(trans), rt=0.5)

        self.at(94.4)
        c_r = Circle(radius=0.5, stroke_width=0, fill_color=RED, fill_opacity=0.9).move_to(RIGHT * 4.6 + UP * 0.1)
        c_b = Circle(radius=0.5, stroke_width=0, fill_color=BLUE, fill_opacity=0.9).move_to(RIGHT * 4.6 + DOWN * 0.8)
        c_m = Circle(radius=0.75, stroke_color=WHITE, stroke_width=2, fill_color=MAGENTA, fill_opacity=1).move_to(RIGHT * 4.8 + DOWN * 0.35)
        m_lab = tx("magenta", 28, MAGENTA, bold=True).next_to(c_m, DOWN, buff=0.2)
        self.p(FadeIn(c_r, scale=0.5), FadeIn(c_b, scale=0.5), rt=0.4)
        self.p(ReplacementTransform(VGroup(c_r, c_b), c_m), Write(m_lab), cuve.animate.set_fill(MAGENTA, opacity=0.85), rt=0.9)
        self.at(95.6)
        self.reponse("La solution absorbe dans le vert (λmax ≈ 530 nm) : le rouge et le bleu sont transmis.\n"
                     "Une solution d'éosine est donc MAGENTA, couleur complémentaire du vert.", rt=2.2)

    # =================================================================
    #  QUESTION 2  (105,9 s → 133,2 s)
    # =================================================================
    def question2(self):
        self.at(105.9)
        self.vider()
        self.set_q("Question 2")
        self.question("2) La gamme d'étalonnage permet-elle d'exploiter les résultats expérimentaux ?")

        self.at(111.8)
        x0, x1 = -5.6, 5.4
        f = lambda a: x0 + (x1 - x0) * a / 2.0
        axe = Arrow(RIGHT * (x0 - 0.2), RIGHT * (x1 + 0.5), color=SOFT, buff=0, stroke_width=3,
                    max_tip_length_to_length_ratio=0.02)
        ticks = VGroup()
        for a, s in [(0, "0"), (0.5, "0{,}50"), (1.0, "1{,}00"), (1.5, "1{,}50"), (2.0, "2{,}00")]:
            ticks.add(VGroup(Line(UP * 0.12, DOWN * 0.12, color=SOFT).move_to(RIGHT * f(a)),
                             mx(s, SOFT, 24).move_to(RIGHT * f(a) + DOWN * 0.45)))
        nom_axe = mx("A", ABSO, 34).next_to(axe, RIGHT, buff=0.15)
        etal = VGroup(*[Dot(RIGHT * f(a), radius=0.075, color=ABSO) for a in A_ETALON])
        ligne = VGroup(axe, ticks, nom_axe, etal)
        ligne.shift(DOWN * 0.2)
        self.p(GrowArrow(axe), FadeIn(ticks), FadeIn(nom_axe), rt=1.3)
        et_lab = tx("● solutions étalons", 20, ABSO).next_to(axe, UP, buff=0.35).align_to(axe, LEFT)
        self.p(LaggedStart(*[GrowFromCenter(d) for d in etal], lag_ratio=0.12), FadeIn(et_lab), rt=1.4)

        self.at(115.5)
        acc = Brace(VGroup(etal[1], etal[-1]), DOWN, color=ABSO, buff=0.75)
        acc_l = tx("gamme des étalons : de 0,50 à 1,90", 24, ABSO).next_to(acc, DOWN, buff=0.12)
        self.p(GrowFromCenter(acc), FadeIn(acc_l), rt=1.2)

        self.at(119.0)
        s0 = VGroup(*[Dot(RIGHT * f(a) + DOWN * 0.2 + UP * (0.22 + 0.12 * (i % 3)), radius=0.06, color=CONC)
                      for i, a in enumerate(A_S0_NUM)])
        s0_l = row(mx("S_0", CONC, 34), tx(": A ≈ 1,5", 24, CONC), buff=0.1).next_to(s0, UP, buff=1.05).shift(RIGHT * 1.2)
        fl = Arrow(s0_l.get_bottom(), s0.get_top(), color=CONC, buff=0.1, stroke_width=3)
        self.p(LaggedStart(*[FadeIn(d, shift=DOWN * 0.3) for d in s0], lag_ratio=0.1), rt=1.4)
        self.p(FadeIn(s0_l), GrowArrow(fl), rt=0.8)
        self.at(122.0)
        ok = tx("✓ dans la gamme", 26, RES, bold=True).next_to(s0_l, LEFT, buff=0.6)
        self.p(Circumscribe(s0, color=CONC, buff=0.1), FadeIn(ok, scale=1.2), rt=1.4)

        self.at(124.2)
        self.reponse("Oui : l'absorbance de S0 (A ≈ 1,5) est comprise entre 0,50 et 1,90, absorbances extrêmes\n"
                     "des solutions étalons. Les résultats expérimentaux sont donc exploitables.", rt=2.2)

    # =================================================================
    #  QUESTION 3  (133,2 s → 158,4 s)
    # =================================================================
    def question3(self):
        self.at(133.2)
        self.vider()
        self.set_q("Question 3")
        self.question("3) Tracer la droite d'étalonnage de l'absorbance en fonction de la concentration massique.")
        ax, deco, pts, droite = self.graphe(x_len=7.0, y_len=4.3)
        g = VGroup(ax, deco, pts, droite)
        self.caser(g, top=self.haut() - 0.1, bottom=-2.5, x=-2.9)
        self.p(Create(ax), FadeIn(deco), rt=1.6)

        self.at(138.9)
        anims = []
        for d in pts:
            anims.append(AnimationGroup(GrowFromCenter(d), Flash(d, color=WHITE, flash_radius=0.18, line_length=0.1)))
        self.p(LaggedStart(*anims, lag_ratio=0.35), rt=3.2)

        self.at(142.4)
        self.p(Create(droite), rt=1.8)
        orig = Circle(radius=0.22, color=RES, stroke_width=4).move_to(ax.c2p(0, 0))
        self.at(144.3)
        self.p(Create(orig), Flash(ax.c2p(0, 0), color=RES), rt=0.8)

        self.at(146.9)
        b1 = tx("Points alignés sur une droite", 24, KCOL, bold=True)
        b2 = tx("passant par l'origine", 24, KCOL, bold=True)
        b3 = tx("donc A est proportionnelle à Cm :", 22, WHITE)
        b4 = tx("loi de Beer-Lambert vérifiée", 22, RES)
        bl = VGroup(b1, b2, b3, b4).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        self.a_droite(bl, g)
        self.p(FadeIn(VGroup(b1, b2), shift=LEFT * 0.2), rt=1.0)
        self.p(FadeIn(VGroup(b3, b4), shift=LEFT * 0.2), rt=1.0)

        self.at(152.4)
        pente = row(mx("A", ABSO, 44), mx("=", WHITE, 44), mx("k", KCOL, 44), mx(r"\times", WHITE, 44),
                    mx("C_m", CONC, 44), buff=0.15)
        k_l = tx("k : coefficient directeur de la droite", 20, KCOL)
        bloc_p = VGroup(pente, k_l).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bloc_p.next_to(bl, DOWN, buff=0.45).align_to(bl, LEFT)
        ajuster(bloc_p, config.frame_width / 2 - 0.35 - bloc_p.get_left()[0])
        bloc_p.next_to(bl, DOWN, buff=0.45).align_to(bl, LEFT)
        p1, p2 = ax.c2p(0.010, K * 0.010), ax.c2p(0.020, K * 0.020)
        coin = ax.c2p(0.020, K * 0.010)
        tri = VGroup(DashedLine(p1, coin, color=KCOL, stroke_width=3), DashedLine(coin, p2, color=KCOL, stroke_width=3))
        self.p(Write(pente), Create(tri), rt=1.4)
        self.p(FadeIn(k_l), Indicate(droite, color=KCOL), rt=0.9)
        self.at(155.2)
        self.reponse("La droite d'étalonnage passe par l'origine : A = k × Cm.", rt=1.2)

    # =================================================================
    #  QUESTION 4  (158,4 s → 246,9 s)
    # =================================================================
    def question4(self):
        self.at(158.4)
        self.vider()
        self.set_q("Question 4")
        self.question("4) Énoncer la loi de Beer-Lambert, détailler grandeurs et unités, calculer le coefficient k.")

        self.at(167.1)
        bl_t = tx("Loi de Beer-Lambert", 34, KCOL, bold=True)
        bl_d = tx("Pour une solution diluée, l'absorbance est proportionnelle à la concentration de l'espèce colorée.", 22, WHITE)
        tete = VGroup(bl_t, bl_d).arrange(DOWN, buff=0.2)
        self.caser(tete, top=self.haut() - 0.1)
        self.p(Write(bl_t), rt=1.0)
        self.p(FadeIn(bl_d, shift=UP * 0.15), rt=1.0)

        self.at(177.9)
        fs = 56
        loi1 = row(mx("A", ABSO, fs), mx("=", WHITE, fs), mx(r"\varepsilon", KCOL, fs), mx(r"\times", WHITE, fs),
                   mx(r"\ell", VOL, fs), mx(r"\times", WHITE, fs), mx("C", CONC, fs), buff=0.22)
        ou = tx("ou", 24, SOFT)
        loi2 = row(mx("A", ABSO, fs), mx("=", WHITE, fs), mx("k", KCOL, fs), mx(r"\times", WHITE, fs),
                   mx("C_m", CONC, fs), buff=0.22)
        gauche = VGroup(loi1, ou, loi2).arrange(DOWN, buff=0.4)

        def leg(sym, nom, unite, c):
            return row(mx(sym, c, 34), tx(": " + nom, 20, c), tx("(" + unite + ")", 20, UNIT), buff=0.15)
        legs = VGroup(
            leg("A", "absorbance", "sans unité", ABSO),
            leg(r"\varepsilon", "coefficient d'absorption molaire", "L·mol⁻¹·cm⁻¹", KCOL),
            leg(r"\ell", "largeur de la cuve", "cm", VOL),
            leg("C", "concentration en quantité de matière", "mol·L⁻¹", CONC),
            leg("k", "coefficient de proportionnalité", "L·g⁻¹", KCOL),
            leg("C_m", "concentration massique", "g·L⁻¹", CONC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24)
        corps = VGroup(gauche, legs).arrange(RIGHT, buff=0.8)
        self.caser(corps, top=tete.get_bottom()[1] - 0.35)
        self.p(FadeOut(bl_d), Write(loi1), rt=1.4)
        for i, t in enumerate((179.5, 181.4, 183.1, 184.6)):
            self.at(t)
            self.p(FadeIn(legs[i], shift=LEFT * 0.2), Indicate(loi1[2 * i], color=legs[i][0].get_color()), rt=0.8)

        self.at(188.3)
        self.p(FadeIn(ou), Write(loi2), rt=1.3)
        self.at(193.0)
        self.p(FadeIn(legs[4], shift=LEFT * 0.2), Indicate(loi2[2], color=KCOL), rt=0.8)
        self.p(FadeIn(legs[5], shift=LEFT * 0.2), Indicate(loi2[4], color=CONC), rt=0.8)

        # --- calcul de k avec le dernier point
        self.at(198.0)
        ax, deco, pts, droite = self.graphe(x_len=4.6, y_len=3.1, fs=18)
        mini = VGroup(ax, deco, pts, droite)
        loi_k = row(mx("A", ABSO, 44), mx("=", WHITE, 44), mx("k", KCOL, 44), mx(r"\times", WHITE, 44),
                    mx("C_m", CONC, 44), buff=0.18)
        lit = row(mx("k", KCOL, 48), mx("=", WHITE, 48), frac(mx("A", ABSO, 48), mx("C_m", CONC, 48)), buff=0.2)
        n1 = mx(r"1{,}90", ABSO, 44)
        d1 = val(r"0{,}020", r"\mathrm{g\cdot L^{-1}}", CONC, 44)
        res = val("95", r"\mathrm{L\cdot g^{-1}}", RES, 46)
        an = row(mx("k", KCOL, 44), mx("=", WHITE, 44), frac(n1, d1), mx("=", WHITE, 44), res, buff=0.2)
        u1 = row(tx("A est sans unité, donc l'unité de k est", 20, SOFT),
                 mx(r"\frac{1}{\mathrm{g\cdot L^{-1}}} = \mathrm{L\cdot g^{-1}}", UNIT, 34), buff=0.2)
        droite_col = VGroup(loi_k, lit, an, u1).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        page = VGroup(mini, droite_col).arrange(RIGHT, buff=0.8, aligned_edge=UP)
        self.caser(page, top=self.haut() - 0.15)
        self.p(FadeOut(VGroup(bl_t, gauche[0], ou, legs)), ReplacementTransform(loi2, loi_k), rt=1.0)
        self.p(FadeIn(mini), rt=1.0)

        self.at(203.5)
        pt = pts[-1]
        pc = ax.c2p(0.020, 1.90)
        hl = VGroup(DashedLine(pc, ax.c2p(0, 1.90), color=ABSO, stroke_width=3),
                    DashedLine(pc, ax.c2p(0.020, 0), color=CONC, stroke_width=3))
        lab_c = deco[1][3]                      # graduation « 0,020 » déjà présente
        lab_a = mx(r"1{,}90", ABSO, 24).next_to(ax.c2p(0, 1.90), LEFT, buff=0.12)
        self.p(pt.animate.scale(1.8).set_color(RES), Flash(pt, color=RES), rt=0.8)
        self.p(Create(hl[1]), lab_c.animate.set_color(CONC).scale(1.3), rt=1.0)
        self.at(208.2)
        self.p(Create(hl[0]), FadeOut(deco[1][7]), FadeIn(lab_a), rt=1.0)

        self.at(210.2)
        note = tx("(on peut aussi calculer k pour chaque point puis faire la moyenne)", 18, SOFT)
        note.next_to(mini, DOWN, buff=0.25).align_to(mini, LEFT)
        ajuster(note, mini.width + 0.6)
        self.p(FadeIn(note), rt=0.8)

        self.at(216.4)
        self.p(TransformMatchingShapes(loi_k.copy(), lit), rt=1.8)
        self.at(219.8)
        self.encadre(lit)

        self.at(228.2)
        self.tag_an(an)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1]), rt=0.4)
        self.morph([(lab_a, n1), (lab_c, d1[0])], FadeIn(d1[1]), rt=1.4)
        self.at(232.3)
        self.p(Write(an[3]), Write(res), rt=1.0)
        self.p(Circumscribe(res, color=RES), rt=0.8)

        self.at(234.2)
        self.p(FadeIn(u1, shift=UP * 0.15), rt=1.0)
        self.at(238.5)
        self.p(Indicate(u1[1], color=KCOL), Indicate(res[1], color=KCOL), rt=1.2)

        self.at(244.6)
        self.reponse("Le coefficient de proportionnalité entre absorbance et concentration massique est k = 95 L·g⁻¹.", rt=1.6)

    # =================================================================
    #  QUESTION 5  (246,9 s → 271,4 s)
    # =================================================================
    def question5(self):
        self.at(246.9)
        self.vider(rt=0.4)
        self.set_q("Question 5")
        self.question("5) Calculer la valeur moyenne de l'absorbance de la solution S0.", rt=1.0)

        vals = VGroup(*[mx(A_S0[i], ABSO, 32) for i in range(9)]).arrange(RIGHT, buff=0.42)
        idx = VGroup(*[mx(f"A_{i + 1}", SOFT, 24).next_to(vals[i], UP, buff=0.15) for i in range(9)])
        haut_v = VGroup(idx, vals)
        lit = row(mx(r"A_{moy}", ABSO, 46), mx("=", WHITE, 46),
                  frac(mx(r"A_1 + A_2 + \dots + A_9", ABSO, 46), mx("9", WHITE, 46)), buff=0.2)
        somme = VGroup()
        for i in range(9):
            somme.add(mx(A_S0[i], ABSO, 30))
            if i < 8:
                somme.add(mx("+", WHITE, 30))
        somme.arrange(RIGHT, buff=0.08)
        an = row(mx(r"A_{moy}", ABSO, 32), mx("=", WHITE, 32), frac(somme, mx("9", WHITE, 32)), buff=0.15)
        page = VGroup(haut_v, lit, an).arrange(DOWN, buff=0.75)
        self.caser(page, top=self.haut() - 0.1)
        self.p(LaggedStart(*[FadeIn(VGroup(a, b), shift=DOWN * 0.15) for a, b in zip(idx, vals)], lag_ratio=0.1), rt=1.6)

        self.at(256.0)
        self.p(Write(lit), rt=1.4)
        self.encadre(lit)

        self.at(261.4)
        self.tag_an(an, rt=0.3)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1:]), rt=0.3)
        self.morph([(vals[i], somme[2 * i]) for i in range(9)], *[FadeIn(somme[2 * i + 1]) for i in range(8)], rt=1.5)

        self.at(263.6)
        fin = row(mx(r"A_{moy}", ABSO, 40), mx("=", WHITE, 40), frac(mx(r"13{,}846", ABSO, 40), mx("9", WHITE, 40)),
                  mx("=", WHITE, 40), mx(r"1{,}54", RES, 46), buff=0.2).move_to(an)
        self.p(ReplacementTransform(an[0], fin[0]), ReplacementTransform(an[1], fin[1]),
               ReplacementTransform(an[2], fin[2]), rt=1.1)
        self.p(Write(fin[3:]), Circumscribe(fin[4], color=RES), rt=1.0)

        self.at(266.0)
        self.reponse("La valeur moyenne de l'absorbance de la solution S0 est Amoy = 1,54.", rt=1.4)

    # =================================================================
    #  QUESTION 6  (271,4 s → 343,7 s)
    # =================================================================
    def question6(self):
        self.at(271.4)
        self.vider()
        self.set_q("Question 6")
        self.question("6) Déterminer la concentration massique Cm0 d'éosine dans S0 : par lecture graphique, puis par le calcul.")

        # --- méthode 1 : lecture graphique
        self.at(277.8)
        ax, deco, pts, droite = self.graphe(x_len=7.0, y_len=4.3)
        g = VGroup(ax, deco, pts, droite)
        self.caser(g, top=self.haut() - 0.1, bottom=-2.6, x=-2.9)
        m1 = etiquette("Méthode 1 : lecture graphique", ABSO).scale(1.5)
        self.a_droite(m1, g)
        self.p(FadeIn(m1, shift=DOWN * 0.15), rt=0.8)

        self.at(281.9)
        self.p(Create(ax), FadeIn(deco), FadeIn(pts), rt=1.3)
        self.p(Create(droite), rt=1.0)

        self.at(287.5)
        y_lab = mx(r"1{,}54", ABSO, 28).next_to(ax.c2p(0, A_MOY), LEFT, buff=0.12)
        marque = Dot(ax.c2p(0, A_MOY), radius=0.08, color=ABSO)
        self.p(FadeOut(deco[1][6]), FadeIn(y_lab), GrowFromCenter(marque), rt=0.8)
        self.at(290.0)
        h = DashedLine(ax.c2p(0, A_MOY), ax.c2p(CM0, A_MOY), color=ABSO, stroke_width=3)
        self.p(Create(h), rt=1.4)
        point = Dot(ax.c2p(CM0, A_MOY), radius=0.09, color=CONC)
        self.p(GrowFromCenter(point), Flash(point, color=CONC), rt=0.7)
        self.at(294.6)
        v = DashedLine(ax.c2p(CM0, A_MOY), ax.c2p(CM0, 0), color=CONC, stroke_width=3)
        self.p(Create(v), rt=1.3)
        self.p(Flash(ax.c2p(CM0, 0), color=CONC), rt=0.5)

        self.at(296.6)
        l1 = row(mx(r"C_{m0} \approx", CONC, 38), val(r"0{,}016", r"\mathrm{g\cdot L^{-1}}", CONC, 38), buff=0.15)
        l2 = row(mx(r"C_{m0} \approx", CONC, 38), val(r"1{,}6\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 38), buff=0.15)
        lect = VGroup(l1, l2).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(m1, DOWN, buff=0.6).align_to(m1, LEFT)
        ajuster(lect, config.frame_width / 2 - 0.35 - lect.get_left()[0])
        lect.next_to(m1, DOWN, buff=0.6).align_to(m1, LEFT)
        self.p(Write(l1), rt=1.2)
        self.at(298.3)
        self.p(FadeIn(l2, shift=DOWN * 0.15), rt=0.9)

        # --- méthode 2 : par le calcul
        self.at(301.8)
        rappel = VGroup(tx("Lecture graphique :", 18, SOFT), l2.copy().scale(0.65)).arrange(RIGHT, buff=0.15)
        self.vider(garder=[self.cur_q, l2])
        m2 = etiquette("Méthode 2 : relation de Beer-Lambert", KCOL).scale(1.5)
        loi = row(mx("A_{moy}", ABSO, 46), mx("=", WHITE, 46), mx("k", KCOL, 46), mx(r"\times", WHITE, 46),
                  mx(r"C_{m0}", CONC, 46), buff=0.18)
        lit = row(mx(r"C_{m0}", CONC, 48), mx("=", WHITE, 48), frac(mx(r"A_{moy}", ABSO, 48), mx("k", KCOL, 48)), buff=0.2)
        fl = Arrow(LEFT * 0.5, RIGHT * 0.5, color=SOFT, buff=0)
        ligne1 = VGroup(loi, fl, lit).arrange(RIGHT, buff=0.5)
        n6 = mx(r"1{,}54", ABSO, 44)
        d6 = val("95", r"\mathrm{L\cdot g^{-1}}", KCOL, 44)
        res6 = val(r"1{,}62\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", RES, 46)
        an = row(mx(r"C_{m0}", CONC, 44), mx("=", WHITE, 44), frac(n6, d6), mx("=", WHITE, 44), res6, buff=0.2)
        u6 = row(tx("unité :", 20, SOFT), mx(r"\frac{1}{\mathrm{L\cdot g^{-1}}} = \mathrm{g\cdot L^{-1}}", UNIT, 34), buff=0.2)
        bas = VGroup(an, u6).arrange(RIGHT, buff=0.8)
        page = VGroup(m2, ligne1, bas).arrange(DOWN, buff=0.6, aligned_edge=LEFT)
        self.caser(page, top=self.haut() - 0.1)
        rappel.to_edge(RIGHT, buff=0.4).align_to(m2, UP)
        self.p(FadeIn(m2, shift=DOWN * 0.15), ReplacementTransform(l2, rappel), rt=1.0)

        self.at(308.9)
        self.p(Write(loi), rt=1.3)
        self.at(311.6)
        self.p(GrowArrow(fl), TransformMatchingShapes(loi.copy(), lit), rt=1.6)
        self.encadre(lit, rt=0.9)

        self.at(322.2)
        self.tag_an(an, rt=0.3)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1]), rt=0.3)
        self.morph([(lit[2][0], n6), (lit[2][2], d6[0])], FadeIn(d6[1]), rt=1.3)
        self.at(325.1)
        self.p(Write(an[3]), Write(res6), rt=1.2)
        self.p(FadeIn(u6), rt=0.7)

        self.at(329.6)
        comp = tx("✓ très proche de la lecture graphique", 22, RES).next_to(rappel, DOWN, buff=0.2).align_to(rappel, RIGHT)
        self.p(FadeIn(comp, shift=LEFT * 0.2), Indicate(rappel, color=RES), rt=1.2)
        self.at(331.4)
        self.reponse("La concentration massique d'éosine dans la solution S0 est Cm0 = 1,62×10⁻² g·L⁻¹.", rt=1.5)
        self.at(337.0)
        deux = etiquette("À savoir faire : les DEUX méthodes", ABSO).scale(1.4)
        deux.to_edge(RIGHT, buff=0.4).align_to(rappel, UP)
        self.p(FadeOut(VGroup(rappel, comp)), FadeIn(deux, scale=1.2), rt=0.9)

    # =================================================================
    #  QUESTION 9  (343,7 s → 522,2 s)
    # =================================================================
    def question9(self):
        self.at(343.7)
        self.vider()
        self.set_q("Question 9")
        q = self.question("9) En déduire le pourcentage massique d'éosine dans la dosette commerciale. Détailler la démarche.")
        self.at(349.7)
        self.p(Indicate(q[1], color=ABSO, scale_factor=1.04), rt=1.2)

        # --- schéma des deux dilutions
        self.at(355.9)
        d0 = dosette(r"V_{dos} = 2{,}00\ \mathrm{mL}", 0.95, h=1.25)
        c_d = mx(r"C_{m,dos} = \ ?", CONC, 28).next_to(d0, DOWN, buff=0.12)
        f1 = fiole(r"V_{fiole} = 1{,}00\ \mathrm{L}", 0.5, r=0.55)
        c_1 = mx(r"C_{m1} = \ ?", CONC, 28).next_to(f1, DOWN, buff=0.12)
        f2 = fiole(r"V_0 = 25{,}0\ \mathrm{mL}", 0.25, r=0.4)
        c_0 = mx(r"C_{m0} = 1{,}62\times10^{-2}\ \mathrm{g\cdot L^{-1}}", CONC, 26).next_to(f2, DOWN, buff=0.12)
        n_s0 = mx("S_0", CONC, 36).next_to(f2[0], RIGHT, buff=0.2)
        A = VGroup(d0, c_d)
        B = VGroup(f1, c_1)
        C = VGroup(f2, c_0, n_s0)
        verre = VGroup(A, B, C).arrange(RIGHT, buff=2.2, aligned_edge=DOWN)
        a1 = Arrow(d0[0].get_right(), f1[0].get_left(), color=SOFT, buff=0.25, stroke_width=4)
        a2 = Arrow(f1[0].get_right(), f2[0].get_left(), color=SOFT, buff=0.25, stroke_width=4)
        a1l = tx("dilution 1", 18, SOFT).next_to(a1, UP, buff=0.1)
        a2l = VGroup(tx("dilution 2", 18, SOFT), mx(r"V = 10{,}0\ \mathrm{mL}", VOL, 24)).arrange(DOWN, buff=0.08).next_to(a2, UP, buff=0.1)
        schema = VGroup(verre, a1, a2, a1l, a2l)
        self.caser(schema, top=self.haut() - 1.25, bottom=-1.9)
        self.p(FadeIn(A, shift=UP * 0.2), rt=0.8)
        self.p(GrowArrow(a1), FadeIn(a1l), FadeIn(B, shift=LEFT * 0.2), rt=1.0)
        self.p(GrowArrow(a2), FadeIn(a2l), FadeIn(C, shift=LEFT * 0.2), rt=1.0)
        self.at(363.0)
        deux = tx("deux dilutions successives", 24, ABSO).next_to(schema, DOWN, buff=0.5)
        self.p(FadeIn(deux), Indicate(a1l), Indicate(a2l[0]), rt=1.3)

        self.at(370.1)
        r1 = CurvedArrow(f2[0].get_top() + UP * 0.25, f1[0].get_top() + UP * 0.25, color=ABSO, angle=TAU / 7)
        r2 = CurvedArrow(f1[0].get_top() + UP * 0.25, d0[0].get_top() + UP * 0.25, color=ABSO, angle=TAU / 7)
        e1 = tx("étape 1", 18, ABSO).next_to(r1, UP, buff=0.05)
        e2 = tx("étape 2", 18, ABSO).next_to(r2, UP, buff=0.05)
        rem = tx("on remonte petit à petit, de S0 jusqu'à la dosette", 24, ABSO).move_to(deux)
        self.p(Create(r1), FadeIn(e1), ReplacementTransform(deux, rem), rt=1.2)
        self.p(Create(r2), FadeIn(e2), rt=1.0)

        # ---------- étape 1 ----------
        self.at(373.9)
        self.p(FadeOut(VGroup(r1, r2, e1, e2, rem)), schema.animate.scale(0.55).next_to(self.cur_q, DOWN, buff=0.3).set_x(0), rt=1.0)
        top = schema.get_bottom()[1] - 0.25
        et1 = row(etiquette("Étape 1", ABSO).scale(1.3), tx("de S0 à la fiole de 1,00 L", 24, WHITE), buff=0.25)
        p1 = row(tx("dilution : la masse d'éosine se conserve", 22, SOFT),
                 mx(r"(\,m = C_m \times V\,)", SOFT, 30), buff=0.2)
        tete1 = VGroup(et1, p1).arrange(RIGHT, buff=0.6)
        sC1, sV, sC0, sV0 = mx("C_{m1}", CONC, 44), mx("V", VOL, 44), mx("C_{m0}", CONC, 44), mx("V_0", VOL, 44)
        cons = row(sC1, mx(r"\times", WHITE, 44), sV, mx("=", WHITE, 44), sC0, mx(r"\times", WHITE, 44), sV0, buff=0.16)
        lit = row(mx("C_{m1}", CONC, 44), mx("=", WHITE, 44),
                  frac(row(mx("C_{m0}", CONC, 44), mx(r"\times", WHITE, 44), mx("V_0", VOL, 44), buff=0.12),
                       mx("V", VOL, 44)), buff=0.2)
        ligne_a = VGroup(cons, Arrow(LEFT * 0.4, RIGHT * 0.4, color=SOFT, buff=0), lit).arrange(RIGHT, buff=0.45)
        nC0 = val(r"1{,}62\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 38)
        nV0 = val(r"25{,}0", r"\mathrm{mL}", VOL, 38)
        dV = val(r"10{,}0", r"\mathrm{mL}", VOL, 38)
        r1v = val(r"4{,}05\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", RES, 40)
        an1 = row(mx("C_{m1}", CONC, 38), mx("=", WHITE, 38),
                  frac(row(nC0, mx(r"\times", WHITE, 38), nV0, buff=0.12), dV), mx("=", WHITE, 38), r1v, buff=0.18)
        page1 = VGroup(tete1, ligne_a, an1).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        ligne_a.shift(RIGHT * 0.3)
        an1.shift(RIGHT * 0.3)
        self.caser(page1, top=top, x=0)
        self.p(FadeIn(et1, shift=RIGHT * 0.2), Circumscribe(VGroup(B, C), color=ABSO), rt=1.4)
        self.at(384.8)
        self.p(FadeIn(p1, shift=UP * 0.15), rt=1.0)

        self.at(395.9)
        self.p(Write(cons[0:3]), rt=1.2)
        self.at(402.0)
        self.p(Indicate(sV, color=VOL), Indicate(a2l[1], color=VOL), rt=1.0)
        self.at(406.0)
        self.p(Write(cons[3:]), rt=1.4)
        self.at(414.0)
        self.p(Indicate(sV0, color=VOL), Indicate(f2[1], color=VOL), rt=1.0)
        self.at(419.3)
        self.p(GrowArrow(ligne_a[1]), TransformMatchingShapes(cons.copy(), lit), rt=1.5)
        self.encadre(lit, rt=0.9)

        self.at(422.8)
        self.tag_an(an1, rt=0.3)
        self.p(FadeIn(an1[0:2]), FadeIn(an1[2][1]), FadeIn(an1[2][0][1]), rt=0.3)
        self.morph([(c_0, nC0), (f2[1], nV0[0]), (a2l[1], dV[0])], FadeIn(nV0[1]), FadeIn(dV[1]), rt=1.3)
        tr1 = self.barrer(nV0[1], dV[1], rt=0.6)
        self.p(Write(an1[3]), Write(r1v), rt=1.0)

        self.at(427.8)
        att = row(tx("Attention :", 22, "#FF5555", bold=True),
                  tx("ce n'est pas encore la dosette ! La fiole de 1,00 L vient elle-même d'une dilution.", 22, "#FF5555"),
                  buff=0.15)
        ajuster(att, 12.8)
        att.to_edge(DOWN, buff=0.45)
        self.p(FadeIn(att, shift=UP * 0.2), Circumscribe(A, color="#FF5555"), rt=1.5)
        self.at(436.0)
        self.p(Indicate(a1, color="#FF5555"), Indicate(a1l, color="#FF5555"), rt=1.0)

        # ---------- étape 2 ----------
        self.at(442.6)
        rappel1 = row(tx("Étape 1 :", 18, SOFT), mx(r"C_{m1} = 4{,}05\times10^{-2}\ \mathrm{g\cdot L^{-1}}", CONC, 30), buff=0.15)
        self.vider(garder=[self.cur_q, schema], rt=0.6)
        et2 = row(etiquette("Étape 2", ABSO).scale(1.3), tx("de la fiole de 1,00 L à la dosette (même démarche)", 24, WHITE), buff=0.25)
        cons2 = row(mx(r"C_{m,dos}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{dos}", VOL, 42), mx("=", WHITE, 42),
                    mx("C_{m1}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{fiole}", VOL, 42), buff=0.15)
        lit2 = row(mx(r"C_{m,dos}", CONC, 42), mx("=", WHITE, 42),
                   frac(row(mx("C_{m1}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{fiole}", VOL, 42), buff=0.12),
                        mx(r"V_{dos}", VOL, 42)), buff=0.2)
        ligne_b = VGroup(cons2, Arrow(LEFT * 0.4, RIGHT * 0.4, color=SOFT, buff=0), lit2).arrange(RIGHT, buff=0.4)
        conv = row(tx("conversion :", 18, SOFT), mx(r"V_{fiole} = 1{,}00\ \mathrm{L} = 1000\ \mathrm{mL}", VOL, 32), buff=0.15)
        nC1 = val(r"4{,}05\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 38)
        nVf = val(r"1000", r"\mathrm{mL}", VOL, 38)
        dVd = val(r"2{,}00", r"\mathrm{mL}", VOL, 38)
        r2v = val(r"20{,}2", r"\mathrm{g\cdot L^{-1}}", RES, 40)
        an2 = row(mx(r"C_{m,dos}", CONC, 38), mx("=", WHITE, 38),
                  frac(row(nC1, mx(r"\times", WHITE, 38), nVf, buff=0.12), dVd), mx("=", WHITE, 38), r2v, buff=0.18)
        page2 = VGroup(VGroup(et2, rappel1).arrange(RIGHT, buff=0.6), ligne_b, conv, an2).arrange(DOWN, buff=0.38, aligned_edge=LEFT)
        for m in (ligne_b, conv, an2):
            m.shift(RIGHT * 0.3)
        self.caser(page2, top=top, x=0)
        self.p(FadeIn(et2, shift=RIGHT * 0.2), FadeIn(rappel1), Circumscribe(VGroup(A, B), color=ABSO), rt=1.4)
        self.p(Write(cons2), rt=1.6)
        self.at(447.0)
        self.p(GrowArrow(ligne_b[1]), TransformMatchingShapes(cons2.copy(), lit2), rt=1.2)
        self.encadre(lit2, rt=0.7)
        self.at(448.9)
        self.p(FadeIn(conv), rt=0.6)
        self.tag_an(an2, rt=0.3)
        self.p(FadeIn(an2[0:2]), FadeIn(an2[2][1]), FadeIn(an2[2][0][1]), rt=0.3)
        self.morph([(rappel1[1], nC1), (conv[1], nVf[0]), (d0[1], dVd[0])], FadeIn(nVf[1]), FadeIn(dVd[1]), rt=1.2)
        self.at(451.6)
        self.barrer(nVf[1], dVd[1], rt=0.5)
        self.p(Write(an2[3]), Write(r2v), rt=0.9)
        self.p(Circumscribe(r2v, color=RES), rt=0.9)
        self.at(455.0)
        c_d2 = mx(r"C_{m,dos} = 20{,}2\ \mathrm{g\cdot L^{-1}}", RES, 28).match_height(c_d).move_to(c_d)
        self.p(ReplacementTransform(c_d, c_d2), rt=0.9)

        # ---------- étape 3 : pourcentage massique ----------
        self.at(459.1)
        self.vider(garder=[self.cur_q])
        et3 = row(etiquette("Étape 3", ABSO).scale(1.3), tx("pourcentage massique", 24, WHITE), buff=0.25)
        defP = row(mx("P", WHITE, 46), mx("=", WHITE, 46),
                   frac(mx(r"m_{\text{éosine}}", MASSE, 46), mx(r"m_{\text{solution}}", MASSE, 46)),
                   mx(r"\times 100", WHITE, 46), buff=0.2)
        dans = row(tx("Dans", 22), mx(r"V = 1{,}00\ \mathrm{L}", VOL, 32), tx("de solution pharmaceutique :", 22), buff=0.15)
        rappel2 = row(tx("Étape 2 :", 18, SOFT), mx(r"C_{m,dos} = 20{,}2\ \mathrm{g\cdot L^{-1}}", CONC, 30), buff=0.15)
        # masse d'éosine
        lme = row(mx(r"m_{\text{éosine}}", MASSE, 38), mx("=", WHITE, 38), mx(r"C_{m,dos}", CONC, 38),
                  mx(r"\times", WHITE, 38), mx("V", VOL, 38), buff=0.14)
        u_me = val(r"20{,}2", (r"\mathrm{g}", r"\cdot\mathrm{L^{-1}}"), CONC, 38)
        u_V = val(r"1{,}00", r"\mathrm{L}", VOL, 38)
        r_me = val(r"20{,}2", r"\mathrm{g}", RES, 40)
        ame = row(mx("=", WHITE, 38), u_me, mx(r"\times", WHITE, 38), u_V, mx("=", WHITE, 38), r_me, buff=0.14)
        ligne_me = VGroup(lme, ame).arrange(RIGHT, buff=0.7)
        # masse de solution
        lms = row(mx(r"m_{\text{solution}}", MASSE, 38), mx("=", WHITE, 38), mx(r"\rho", RHO, 38),
                  mx(r"\times", WHITE, 38), mx("V", VOL, 38), buff=0.14)
        u_r = val(r"1{,}02", (r"\mathrm{g}", r"\cdot\mathrm{mL^{-1}}"), RHO, 38)
        u_V2 = val(r"1000", r"\mathrm{mL}", VOL, 38)
        r_ms = val(r"1020", r"\mathrm{g}", RES, 40)
        ams = row(mx("=", WHITE, 38), u_r, mx(r"\times", WHITE, 38), u_V2, mx("=", WHITE, 38), r_ms, buff=0.14)
        ligne_ms = VGroup(lms, ams).arrange(RIGHT, buff=0.7)
        ams.align_to(ame, LEFT)
        # pourcentage
        pn = val(r"20{,}2", r"\mathrm{g}", MASSE, 40)
        pd = val(r"1020", r"\mathrm{g}", MASSE, 40)
        rP = mx(r"1{,}98\ \%", RES, 46)
        aP = row(mx("P", WHITE, 40), mx("=", WHITE, 40), frac(pn, pd), mx(r"\times 100", WHITE, 40),
                 mx("=", WHITE, 40), rP, buff=0.18)
        tete3 = VGroup(VGroup(et3, rappel2).arrange(DOWN, aligned_edge=LEFT, buff=0.3), defP).arrange(RIGHT, buff=0.9)
        page3 = VGroup(tete3, dans, ligne_me, ligne_ms, aP).arrange(DOWN, buff=0.42, aligned_edge=LEFT)
        for m in (ligne_me, ligne_ms, aP):
            m.shift(RIGHT * 0.3)
        self.caser(page3, top=self.haut() - 0.15)
        self.p(FadeIn(et3, shift=RIGHT * 0.2), FadeIn(rappel2), rt=0.7)
        self.p(Write(defP), rt=1.6)
        self.at(466.0)
        self.p(Indicate(defP[2][0], color=MASSE), rt=0.8)
        self.at(469.0)
        self.p(Indicate(defP[2][2], color=MASSE), rt=0.8)

        self.at(472.1)
        self.p(FadeIn(dans, shift=UP * 0.15), rt=0.8)
        self.at(474.5)
        self.p(Write(lme), rt=1.0)
        self.encadre(lme, rt=0.6)
        self.at(478.0)
        self.p(FadeIn(ame[0]), FadeIn(ame[2]), FadeIn(ame[4]), FadeIn(u_V), rt=0.4)
        self.morph([(rappel2[1], u_me)], rt=1.0)
        tr_me = self.barrer(u_me[1][1], u_V[1], rt=0.5)
        self.p(Write(r_me), rt=0.7)

        self.at(486.3)
        self.p(Write(lms), rt=1.0)
        self.encadre(lms, rt=0.6)
        self.at(489.0)
        self.p(FadeIn(ams), rt=1.0)
        tr_ms = self.barrer(u_r[1][1], u_V2[1], rt=0.5)
        rq = tx("(V = 1,00 L = 1000 mL)", 18, VOL).next_to(ams, DOWN, buff=0.08).align_to(ams, LEFT)
        self.p(FadeIn(rq), rt=0.4)

        self.at(493.9)
        self.encadre(defP, rt=0.9)
        self.at(500.0)
        cent = tx("× 100 → résultat en %  (sans × 100 : nombre entre 0 et 1, sans le signe %)", 18, SOFT)
        cent.next_to(defP, DOWN, buff=0.12).align_to(defP, LEFT)
        ajuster(cent, config.frame_width / 2 - 0.3 - cent.get_left()[0])
        cent.next_to(defP, DOWN, buff=0.12).align_to(defP, LEFT)
        self.p(FadeIn(cent), Indicate(defP[3], color=ABSO), rt=1.3)

        self.at(508.8)
        self.tag_an(aP, rt=0.3)
        self.p(FadeIn(aP[0:2]), FadeIn(aP[2][1]), FadeIn(aP[3]), rt=0.3)
        self.morph([(r_me, pn), (r_ms, pd)], rt=1.2)
        self.barrer(pn[1], pd[1], rt=0.5)
        self.p(Write(aP[4]), Write(rP), rt=0.9)
        self.p(Circumscribe(rP, color=RES), rt=0.8)
        self.at(514.2)
        self.reponse("Le pourcentage massique d'éosine dans la dosette commerciale est P = 1,98 % :\n"
                     "1,98 % de la masse de la solution est de l'éosine.", rt=1.8)

    # =================================================================
    #  QUESTION 10  (522,2 s → fin)
    # =================================================================
    def question10(self):
        self.at(522.2)
        self.vider()
        self.set_q("Question 10")
        self.question("10) Ce résultat est-il cohérent avec les informations de l'énoncé ?")

        donnees = VGroup(row(tx("expérience :", 20, SOFT), mx(r"P_{exp} = 1{,}98\ \%", RES, 38), buff=0.2),
                         row(tx("étiquette :", 20, SOFT), mx(r"P_{ref} = 2{,}0\ \%", ABSO, 38), buff=0.2)
                         ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        lit = row(mx("e", WHITE, 48), mx("=", WHITE, 48),
                  frac(mx(r"\left|\, P_{exp} - P_{ref} \,\right|", WHITE, 48), mx(r"P_{ref}", ABSO, 48)),
                  mx(r"\times 100", WHITE, 48), buff=0.2)
        haut_l = VGroup(donnees, lit).arrange(RIGHT, buff=1.4)
        an = row(mx("e", WHITE, 44), mx("=", WHITE, 44),
                 frac(mx(r"\left|\, 1{,}98 - 2{,}0 \,\right|", WHITE, 44), mx(r"2{,}0", ABSO, 44)),
                 mx(r"\times 100", WHITE, 44), mx("=", WHITE, 44), mx(r"1\ \%", RES, 50), buff=0.2)
        page = VGroup(haut_l, an).arrange(DOWN, buff=1.0)
        self.caser(page, top=self.haut() - 0.3)
        self.at(525.0)
        self.p(FadeIn(donnees, shift=RIGHT * 0.2), rt=1.0)
        self.at(528.8)
        self.p(Write(lit), rt=1.6)
        self.encadre(lit, rt=0.9)
        self.at(535.0)
        ecart = tx("écart à la valeur de référence", 20, SOFT).next_to(lit, DOWN, buff=0.35)
        self.p(FadeIn(ecart), rt=0.8)

        self.at(540.7)
        self.tag_an(an, rt=0.3)
        self.p(Write(an[:4]), rt=1.4)
        self.p(Write(an[4:]), rt=0.8)
        self.at(543.9)
        self.reponse("L'écart relatif n'est que de 1 % : le résultat est cohérent avec l'étiquette (2,0 % en masse).", rt=1.6)
        self.at(546.5)
        self.p(Circumscribe(an[5], color=RES), rt=1.2)

    # =================================================================
    #  CONCLUSION
    # =================================================================
    def conclusion(self):
        self.at(550.4)
        self.vider(rt=0.8)
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir : la rédaction d'un calcul", 34, WHITE, bold=True)
        items = VGroup(
            row(etiquette("1", BOX).scale(1.4), tx("Expression littérale encadrée", 26, BOX), buff=0.3),
            row(etiquette("2", AN_C).scale(1.4), tx("Application numérique avec les unités", 26, AN_C), buff=0.3),
            row(etiquette("3", RES).scale(1.4), tx("Résultat avec son unité", 26, RES), buff=0.3),
            row(etiquette("4", RES).scale(1.4), tx("Phrase réponse", 26, RES), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        VGroup(t, items).arrange(DOWN, buff=0.6)
        self.p(Write(t), rt=1.0)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=1.6)
        self.wait(2.0)
        self.t += 2.0
