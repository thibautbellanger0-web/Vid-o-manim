from manim import *
import math

# =====================================================================
#  Correction en vidéo – Feuille 2.1 « Identification des espèces chimiques »
#  Exercices 1 à 3 – pour Manim Community (rendu sur GitHub).
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



# ---------- Dessins ----------
HUILE = "#E8C547"
EAU = "#4FA3E0"
PASTILLE = "#F2F2F2"
UVC = "#9B5DE5"
TACHE = "#B8B8B8"


def bouteille(liq=HUILE, h=2.4, etiquette_dechiree=True):
    """Bouteille avec liquide et étiquette (déchirée ou non)."""
    corps = RoundedRectangle(corner_radius=0.25, width=h * 0.42, height=h * 0.7, stroke_color=WHITE, stroke_width=3)
    epaule = Polygon(corps.get_corner(UL) + RIGHT * 0.05, corps.get_corner(UR) + LEFT * 0.05,
                     corps.get_top() + UP * h * 0.12 + RIGHT * h * 0.07, corps.get_top() + UP * h * 0.12 + LEFT * h * 0.07,
                     stroke_color=WHITE, stroke_width=3)
    goulot = Rectangle(width=h * 0.14, height=h * 0.1, stroke_color=WHITE, stroke_width=3).next_to(epaule, UP, buff=0)
    bouchon = Rectangle(width=h * 0.18, height=h * 0.07, stroke_width=0, fill_color=SOFT, fill_opacity=1).next_to(goulot, UP, buff=0)
    liquide = RoundedRectangle(corner_radius=0.22, width=h * 0.42 - 0.08, height=h * 0.6, stroke_width=0,
                               fill_color=liq, fill_opacity=0.75).align_to(corps, DOWN).shift(UP * 0.04)
    g = VGroup(liquide, corps, epaule, goulot, bouchon)
    if etiquette_dechiree:
        c = corps.get_center()
        w = h * 0.42
        pts = [c + LEFT * w / 2 + UP * 0.25, c + RIGHT * w / 2 + UP * 0.25, c + RIGHT * w / 2 + DOWN * 0.05,
               c + RIGHT * w * 0.25 + DOWN * 0.2, c + RIGHT * w * 0.05 + DOWN * 0.02, c + LEFT * w * 0.15 + DOWN * 0.25,
               c + LEFT * w * 0.35 + DOWN * 0.05, c + LEFT * w / 2 + DOWN * 0.18]
        g.add(Polygon(*pts, stroke_color=WHITE, stroke_width=1.5, fill_color="#F5F0E1", fill_opacity=1))
        g.add(Text("?", font_size=28, color=BLACK, weight=BOLD).move_to(c + UP * 0.08))
    return g


def balance(affichage, w=2.4, bol=True):
    """Balance électronique avec un bol et un affichage."""
    base = RoundedRectangle(corner_radius=0.12, width=w, height=w * 0.32, stroke_color=WHITE, stroke_width=2.5,
                            fill_color="#2A2F3A", fill_opacity=1)
    ecran = RoundedRectangle(corner_radius=0.06, width=w * 0.55, height=w * 0.15, stroke_width=0,
                             fill_color="#0B3D2E", fill_opacity=1).move_to(base).shift(DOWN * w * 0.03)
    txt = Text(affichage, font_size=22, color=RES, weight=BOLD).move_to(ecran)
    plateau = Rectangle(width=w * 0.8, height=0.08, stroke_width=0, fill_color=SOFT, fill_opacity=1).next_to(base, UP, buff=0.05)
    g = VGroup(base, ecran, txt, plateau)
    if bol:
        g.add(ArcBetweenPoints(plateau.get_top() + LEFT * w * 0.3 + UP * 0.6, plateau.get_top() + RIGHT * w * 0.3 + UP * 0.6,
                               angle=PI * 0.6, stroke_color=WHITE, stroke_width=3))
    return g


def bougie(h=1.6, w=0.9):
    corps = Rectangle(width=w, height=h, stroke_color=SOFT, stroke_width=2, fill_color="#F4F4F4", fill_opacity=1)
    dessus = Ellipse(width=w, height=w * 0.25, stroke_color=SOFT, stroke_width=2, fill_color="#FFFFFF",
                     fill_opacity=1).move_to(corps.get_top())
    meche = Line(dessus.get_center(), dessus.get_center() + UP * 0.18, color="#333333", stroke_width=3)
    flamme = VGroup(Ellipse(width=0.22, height=0.42, stroke_width=0, fill_color="#FFB703", fill_opacity=1),
                    Ellipse(width=0.1, height=0.22, stroke_width=0, fill_color="#FFF3B0", fill_opacity=1).shift(DOWN * 0.06))
    flamme.next_to(meche, UP, buff=-0.05)
    return VGroup(corps, dessus, meche, flamme)


def pastille(r=0.45):
    disque = Circle(radius=r, stroke_color=SOFT, stroke_width=2, fill_color=PASTILLE, fill_opacity=1)
    reflet = Arc(radius=r * 0.7, start_angle=PI * 0.6, angle=PI * 0.5, color=WHITE, stroke_width=3).move_arc_center_to(disque.get_center())
    return VGroup(disque, reflet)


# Chromatogramme : hauteurs relatives (0 = ligne de dépôt, 1 = front de l'éluant), lues sur le document
DEPOTS = ["S", "C", "M", "E", "L"]
HAUTEURS = {
    "S": [0.164, 0.388, 0.552, 0.705, 0.762],
    "C": [0.448],
    "M": [0.388],
    "E": [0.554],
    "L": [0.856],
}


def plaque_ccm(h=5.0, w=3.4, centre=ORIGIN):
    """Plaque de CCM. Renvoie un dict : plaque, ligne, front, lettres, taches, pos (fonction)."""
    plaque = Rectangle(width=w, height=h, stroke_color=WHITE, stroke_width=2.5, fill_color="#F7F7F2", fill_opacity=0.12)
    y0 = plaque.get_bottom()[1] + 0.55
    y1 = plaque.get_top()[1] - 0.55
    x_min, x_max = plaque.get_left()[0] + 0.45, plaque.get_right()[0] - 0.45
    xs = {d: x_min + (x_max - x_min) * i / 4 for i, d in enumerate(DEPOTS)}
    ligne = Line([plaque.get_left()[0], y0, 0], [plaque.get_right()[0], y0, 0], color=SOFT, stroke_width=2)
    front = DashedLine([plaque.get_left()[0], y1, 0], [plaque.get_right()[0], y1, 0], color=EAU, stroke_width=2)
    lettres = VGroup(*[Text(d, font_size=24, color=WHITE, weight=BOLD).move_to([xs[d], y0 - 0.3, 0]) for d in DEPOTS])
    marques = VGroup(*[Line([xs[d], y0 - 0.07, 0], [xs[d], y0 + 0.07, 0], color=WHITE, stroke_width=2) for d in DEPOTS])

    centre = np.array(centre, dtype=float)

    def pos(d, hh, _xs=dict(xs), _y0=y0, _y1=y1, _c=centre):
        return np.array([_xs[d], _y0 + (_y1 - _y0) * hh, 0]) + _c

    for m in (plaque, ligne, front, lettres, marques):
        m.shift(centre)
    taches = {d: VGroup(*[Ellipse(width=0.3, height=0.22, stroke_width=0, fill_color=TACHE, fill_opacity=1).move_to(pos(d, hh))
                          for hh in HAUTEURS[d]]) for d in DEPOTS}
    y0, y1 = y0 + centre[1], y1 + centre[1]
    xs = {d: x + centre[0] for d, x in xs.items()}
    return {"plaque": plaque, "ligne": ligne, "front": front, "lettres": lettres, "marques": marques,
            "taches": taches, "pos": pos, "y0": y0, "y1": y1, "xs": xs}


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

    def poser(self, m, x_g, top):
        """Pose m dans la colonne de droite : bord gauche en x_g, haut en top, réduit si trop large."""
        ajuster(m, config.frame_width / 2 - 0.3 - x_g)
        m.shift(UP * (top - m.get_top()[1]) + RIGHT * (x_g - m.get_left()[0]))
        return m

    def sous(self, m, ref, x_g, buff=0.4):
        """Pose m sous ref, aligné à gauche sur x_g, réduit si trop large."""
        return self.poser(m, x_g, ref.get_bottom()[1] - buff)

    def set_ex(self, label):
        """Change l'exercice affiché dans l'en-tête (et retire la pastille « Question »)."""
        new = tx(label, 22, SOFT).to_corner(UL, buff=0.3)
        anims = [ReplacementTransform(self.hdr_ex, new)]
        if self.hdr_q is not None:
            anims.append(FadeOut(self.hdr_q))
            self.hdr_q = None
        self.p(*anims, rt=0.6)
        self.hdr_ex = new

    def titre_exercice(self, num, titre, sous=None):
        """Carton de titre d'exercice, centré."""
        a = tx(f"Exercice {num}", 30, ABSO, bold=True)
        b = tx(titre, 50, WHITE, bold=True)
        g = VGroup(a, b)
        if sous:
            g.add(tx(sous, 26, SOFT))
        g.arrange(DOWN, buff=0.25)
        return g

    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.cur_q = None
        self.intro()
        self.exercice1()
        self.exercice2()
        self.exercice3()
        self.conclusion()

    # =================================================================
    #  INTRODUCTION (0 s → 7 s)
    # =================================================================
    def intro(self):
        self.at(0.3)
        sur = tx("Seconde – Chapitre 2.1", 28, SOFT)
        titre = tx("Identification des espèces chimiques", 50, WHITE, bold=True)
        sous = tx("Correction des exercices 1 à 3", 32, ABSO)
        bloc = VGroup(sur, titre, sous).arrange(DOWN, buff=0.3)
        trait = Line(LEFT, RIGHT, color=ABSO, stroke_width=5).set_width(titre.width).next_to(titre, DOWN, buff=0.15)
        sous.next_to(trait, DOWN, buff=0.3)
        self.p(FadeIn(sur, shift=DOWN * 0.2), Write(titre), rt=1.8)
        self.p(GrowFromCenter(trait), FadeIn(sous, shift=UP * 0.2), rt=1.0)
        self.hdr_ex = tx("Identification des espèces chimiques", 22, SOFT).to_corner(UL, buff=0.3)
        self.at(5.2)
        self.p(ReplacementTransform(titre, self.hdr_ex), FadeOut(VGroup(sur, trait, sous)), rt=0.9)

    # =================================================================
    #  EXERCICE 1 : nature d'une huile (7 s → 84 s)
    # =================================================================
    def exercice1(self):
        self.at(7.0)
        self.set_ex("Exercice 1 – La nature d'une huile")
        carton = self.titre_exercice(1, "La nature d'une huile")
        self.p(FadeIn(carton, shift=UP * 0.2), rt=0.9)
        self.at(10.0)
        self.p(FadeOut(carton, shift=UP * 0.3), rt=0.5)

        # --- la situation : une bouteille, une balance
        b = bouteille(HUILE, h=2.8).move_to(LEFT * 4.2 + UP * 0.3)
        b_lab = tx("huile inconnue", 22, HUILE).next_to(b, DOWN, buff=0.2)
        self.p(FadeIn(b, shift=UP * 0.2), FadeIn(b_lab), rt=1.0)
        self.at(12.7)
        dV = row(mx("V", VOL, 46), mx("=", WHITE, 46), val(r"0{,}5", r"\mathrm{L}", VOL, 46), buff=0.18)
        dV.move_to(UP * 1.3 + RIGHT * 0.6)
        self.p(Write(dV), Indicate(b[0], color=HUILE), rt=1.2)
        self.at(17.2)
        conv = row(mx("=", WHITE, 46), val("500", r"\mathrm{mL}", VOL, 46), buff=0.18).next_to(dV, RIGHT, buff=0.2)
        rap = tx("rappel : 1 L = 1000 mL", 20, SOFT).next_to(VGroup(dV, conv), UP, buff=0.2)
        self.p(FadeIn(conv, shift=LEFT * 0.2), FadeIn(rap), rt=1.0)
        self.at(19.8)
        bal = balance("460 g", w=2.6).move_to(RIGHT * 4.3 + DOWN * 1.8)
        dm = row(mx("m", MASSE, 46), mx("=", WHITE, 46), val("460", r"\mathrm{g}", MASSE, 46), buff=0.18)
        dm.next_to(dV, DOWN, buff=0.5).align_to(dV, LEFT)
        self.p(FadeIn(bal, shift=UP * 0.2), rt=0.8)
        self.p(Write(dm), Flash(bal[2], color=RES), rt=1.0)

        # --- la question et le tableau
        self.at(22.4)
        don = VGroup(etiquette("Données", SOFT),
                     row(mx("V", VOL, 40), mx("=", WHITE, 40), val(r"0{,}5", r"\mathrm{L}", VOL, 40), buff=0.15),
                     row(mx("m", MASSE, 40), mx("=", WHITE, 40), val("460", r"\mathrm{g}", MASSE, 40), buff=0.15)
                     ).arrange(RIGHT, buff=0.5)
        tab = tableau([[r"\text{Huile de}", r"\rho\ (\mathrm{g\cdot L^{-1}})"],
                       [r"\text{Tournesol}", "920"], [r"\text{Palme}", "895"], [r"\text{Coco}", "915"]], fs=30)
        tab[0][0].set_color(SOFT)
        tab[0][1].set_color(RHO)
        carte_t = carte("Masses volumiques de référence", tab, RHO)
        lit = row(mx(r"\rho", RHO, 54), mx("=", WHITE, 54), frac(mx("m", MASSE, 54), mx("V", VOL, 54)), buff=0.22)
        n1 = val("460", r"\mathrm{g}", MASSE, 46)
        d1 = val(r"0{,}5", r"\mathrm{L}", VOL, 46)
        res = val("920", r"\mathrm{g\cdot L^{-1}}", RES, 50)
        an = row(mx(r"\rho", RHO, 46), mx("=", WHITE, 46), frac(n1, d1), mx("=", WHITE, 46), res, buff=0.2)
        unite = row(mx(r"\frac{\mathrm{g}}{\mathrm{L}}", UNIT, 38), mx("=", WHITE, 38), mx(r"\mathrm{g/L}", UNIT, 38),
                    mx("=", WHITE, 38), mx(r"\mathrm{g\cdot L^{-1}}", RES, 38), buff=0.2)
        u_lab = tx("unité :", 20, SOFT)
        unite_g = row(u_lab, unite, buff=0.2)
        gauche = VGroup(don, lit, an, unite_g).arrange(DOWN, buff=0.65, aligned_edge=LEFT)
        for m in (lit, an, unite_g):
            m.shift(RIGHT * 0.4)
        page = VGroup(gauche, carte_t).arrange(RIGHT, buff=1.0, aligned_edge=UP)

        self.p(FadeOut(VGroup(b, b_lab, bal, rap)), rt=0.5)
        self.set_q("Question 1")
        self.question("1) Déterminer la nature de l'huile inconnue.", rt=1.0)
        self.caser(page, top=self.haut() - 0.25)
        self.p(ReplacementTransform(VGroup(dV, conv), don[1]), ReplacementTransform(dm, don[2]), FadeIn(don[0]), rt=1.0)

        self.at(25.5)
        self.p(FadeIn(carte_t[0]), Create(carte_t[1]), Create(tab[1]), rt=1.0)
        self.p(LaggedStart(*[FadeIn(c, shift=LEFT * 0.15) for c in tab[0]], lag_ratio=0.12), rt=1.6)
        self.at(31.0)
        self.p(Indicate(tab[0][1], color=RHO), rt=1.0)

        # --- la stratégie
        self.at(39.5)
        def puce(s, c):
            t = tx(s, 22, c)
            r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.4, height=t.height + 0.3, stroke_color=c,
                                 stroke_width=2, fill_color=c, fill_opacity=0.08)
            return VGroup(r, t.move_to(r))
        strat = VGroup(puce("m et V connus", WHITE), puce("calculer ρ = m / V", RHO), puce("comparer au tableau", ABSO))
        strat.arrange(DOWN, buff=0.45)
        fls = VGroup(*[Arrow(strat[i].get_bottom(), strat[i + 1].get_top(), buff=0.06, color=SOFT, stroke_width=3,
                             max_tip_length_to_length_ratio=0.3) for i in range(2)])
        bloc_s = VGroup(strat, fls)
        ajuster(bloc_s, gauche.width, VGroup(lit, an).height + 0.4)
        bloc_s.move_to(VGroup(lit, an))
        self.p(FadeIn(strat[0], shift=DOWN * 0.15), rt=0.7)
        self.at(43.3)
        self.p(GrowArrow(fls[0]), FadeIn(strat[1], shift=DOWN * 0.15), rt=0.9)
        self.at(46.7)
        self.p(GrowArrow(fls[1]), FadeIn(strat[2], shift=DOWN * 0.15), rt=0.9)
        self.p(Indicate(carte_t, color=ABSO, scale_factor=1.03), rt=1.0)

        # --- expression littérale
        self.at(52.4)
        self.p(FadeOut(bloc_s), rt=0.5)
        self.at(54.5)
        self.p(Write(lit), rt=1.5)
        self.at(60.8)
        self.encadre(lit)

        # --- application numérique
        self.at(62.6)
        self.tag_an(an)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1]), rt=0.4)
        self.at(63.8)
        self.morph([(don[2][2], n1)], rt=1.2)
        self.at(66.0)
        self.morph([(don[1][2], d1)], rt=1.1)
        self.at(68.3)
        self.p(Write(an[3]), Write(res), rt=1.2)
        self.p(Circumscribe(res, color=RES), rt=0.9)
        self.at(70.4)
        self.p(FadeIn(u_lab), Write(unite[0:3]), rt=1.2)
        self.at(72.1)
        self.p(Write(unite[3:]), Indicate(res[1], color=RES), rt=1.2)

        # --- comparaison au tableau
        self.at(75.6)
        sel = SurroundingRectangle(VGroup(tab[0][2], tab[0][3]), color=RES, buff=0.12, corner_radius=0.08, stroke_width=4)
        lien = CurvedArrow(res.get_right() + RIGHT * 0.1, sel.get_left() + LEFT * 0.05, color=RES, angle=-TAU / 8)
        self.p(Indicate(res, color=RES), rt=1.0)
        self.at(77.5)
        self.p(Create(lien), rt=1.0)
        self.at(79.5)
        self.p(Create(sel), Indicate(tab[0][3], color=RES, scale_factor=1.4), rt=1.2)
        self.at(81.3)
        self.reponse("La masse volumique de l'huile est ρ = 920 g·L⁻¹ : d'après le tableau, c'est de l'huile de tournesol.", rt=1.6)

    # =================================================================
    #  EXERCICE 2 : la paraffine (84 s → 226 s)
    # =================================================================
    def exercice2(self):
        self.at(84.2)
        self.vider()
        self.cur_q = None
        self.set_ex("Exercice 2 – La paraffine")
        bg = bougie(h=2.4, w=1.3)
        doc_t = VGroup(tx("Caractéristiques de la paraffine", 26, ABSO),
                       row(tx("– température de fusion : autour de", 24), mx(r"50\ ^\circ\mathrm{C}", "#FF8C42", 36), buff=0.15),
                       row(tx("– masse volumique :", 24), mx(r"0{,}9\ \mathrm{g\cdot mL^{-1}}", RHO, 36), buff=0.15)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        doc = VGroup(bg, doc_t).arrange(RIGHT, buff=1.0)
        doc_c = carte("Document", doc, SOFT)
        self.caser(doc_c, top=2.6)
        self.p(FadeIn(doc_c[0]), Create(doc_c[1]), FadeIn(bg, shift=UP * 0.2), rt=1.2)
        self.p(FadeIn(doc_t[0]), rt=0.6)
        self.at(87.5)
        cle = tx("Caractéristiques physiques d'une espèce : température de changement d'état, masse volumique…", 22, SOFT)
        cle.next_to(doc_c, DOWN, buff=0.6)
        self.p(FadeIn(doc_t[1], shift=LEFT * 0.2), rt=1.0)
        self.p(FadeIn(doc_t[2], shift=LEFT * 0.2), rt=1.0)
        self.at(91.0)
        self.p(FadeIn(cle), Indicate(doc_t[1][1], color="#FF8C42"), rt=1.4)

        # ---------------- Question 1 ----------------
        self.at(95.9)
        self.vider()
        self.set_q("Question 1")
        self.question("1) Préciser l'état physique de la paraffine à une température de 25 °C.", rt=1.0)
        top = self.haut() - 0.2
        H = top - ZONE_BAS - 0.3
        th_min, th_max = 0, 80
        x_axe = -4.6
        Y = lambda th: ZONE_BAS + 0.3 + H * (th - th_min) / (th_max - th_min)
        solide = Rectangle(width=0.7, height=Y(50) - Y(0), stroke_width=0, fill_color=EAU, fill_opacity=0.45)
        solide.move_to([x_axe, (Y(0) + Y(50)) / 2, 0])
        liquide = Rectangle(width=0.7, height=Y(80) - Y(50), stroke_width=0, fill_color="#FF8C42", fill_opacity=0.45)
        liquide.move_to([x_axe, (Y(50) + Y(80)) / 2, 0])
        axe = Arrow([x_axe - 0.35, Y(0), 0], [x_axe - 0.35, Y(80) + 0.3, 0], buff=0, color=SOFT, stroke_width=3,
                    max_tip_length_to_length_ratio=0.04)
        graduations = VGroup()
        for th in (0, 25, 50, 75):
            graduations.add(VGroup(Line([x_axe - 0.45, Y(th), 0], [x_axe - 0.25, Y(th), 0], color=SOFT),
                                   mx(f"{th}", SOFT, 26).next_to([x_axe - 0.45, Y(th), 0], LEFT, buff=0.1)))
        unite = mx(r"\theta\ (^\circ\mathrm{C})", SOFT, 26).next_to(axe, UP, buff=0.1)
        l_sol = tx("SOLIDE", 24, EAU, bold=True).next_to(solide, RIGHT, buff=0.3)
        l_liq = tx("LIQUIDE", 24, "#FF8C42", bold=True).next_to(liquide, RIGHT, buff=0.3)
        self.at(101.0)
        self.p(GrowArrow(axe), FadeIn(graduations), FadeIn(unite), rt=1.0)
        self.at(103.4)
        fus = DashedLine([x_axe - 0.4, Y(50), 0], [x_axe + 2.6, Y(50), 0], color="#FF8C42", stroke_width=3)
        fus_l = row(mx(r"\theta_{\mathrm{fus}} \approx 50\ ^\circ\mathrm{C}", "#FF8C42", 34), buff=0.1).next_to(fus, RIGHT, buff=0.15)
        self.p(Create(fus), Write(fus_l), rt=1.4)
        self.at(108.3)
        self.p(FadeIn(solide), FadeIn(liquide), FadeIn(l_sol), FadeIn(l_liq), rt=1.0)
        defn = VGroup(tx("Fusion :", 24, "#FF8C42", bold=True), tx("passage de l'état solide à l'état liquide", 24))
        defn.arrange(RIGHT, buff=0.15)
        fl_f = Arrow([x_axe + 0.55, Y(38), 0], [x_axe + 0.55, Y(62), 0], color="#FF8C42", buff=0, stroke_width=4)
        defn.next_to(fus_l, DOWN, buff=0.5).align_to(fus_l, LEFT)
        self.p(GrowArrow(fl_f), FadeIn(defn, shift=LEFT * 0.2), rt=1.2)

        self.at(113.3)
        th25 = Dot([x_axe, Y(25), 0], radius=0.12, color=WHITE)
        l25 = mx(r"25\ ^\circ\mathrm{C}", WHITE, 36).next_to(l_sol, DOWN, buff=0.25).align_to(l_sol, LEFT)
        self.p(GrowFromCenter(th25), Flash(th25, color=WHITE), Write(l25), rt=1.0)
        self.at(114.8)
        comp = row(mx(r"25\ ^\circ\mathrm{C}", WHITE, 40), mx("<", ABSO, 46), mx(r"\theta_{\mathrm{fus}} = 50\ ^\circ\mathrm{C}", "#FF8C42", 40), buff=0.25)
        comp.next_to(defn, DOWN, buff=0.6).align_to(defn, LEFT)
        self.p(Write(comp), rt=1.2)
        self.p(Indicate(solide, color=EAU), Indicate(l_sol, color=EAU), rt=1.0)
        self.at(118.3)
        bg2 = bougie(h=1.3, w=0.7).to_edge(RIGHT, buff=1.4).set_y(comp.get_y() + 0.3)
        bg_l = tx("bougie : solide à 25 °C", 18, SOFT).next_to(bg2, DOWN, buff=0.15)
        self.p(FadeIn(bg2, shift=UP * 0.2), FadeIn(bg_l), rt=1.0)
        self.at(119.8)
        self.reponse("À 25 °C, la température est inférieure à la température de fusion (≈ 50 °C) :\n"
                     "la paraffine est à l'état solide.", rt=1.8)

        # ---------------- Question 2 ----------------
        self.at(128.4)
        self.vider()
        self.set_q("Question 2")
        self.question("2) Comparer la masse volumique de la paraffine à celle de l'eau.", rt=1.0)
        # colonne gauche : bouteille d'eau sur balance
        b_eau = bouteille(EAU, h=2.2, etiquette_dechiree=False)
        b_eau_l = mx(r"1\ \mathrm{L}", VOL, 34).move_to(b_eau[1])
        bal = balance("1 kg", w=2.4, bol=False)
        b_eau_g = VGroup(b_eau, b_eau_l).next_to(bal[3], UP, buff=0.02)
        illus = VGroup(bal, b_eau_g)
        # colonne droite : calcul
        q_eau = row(mx(r"\rho_{eau} = \ ?", EAU, 44), buff=0.1)
        lit = row(mx(r"\rho_{eau}", EAU, 46), mx("=", WHITE, 46), frac(mx("m", MASSE, 46), mx("V", VOL, 46)), buff=0.2)
        n1 = val("1", r"\mathrm{kg}", MASSE, 42)
        d1 = val("1", r"\mathrm{L}", VOL, 42)
        r1 = val("1", r"\mathrm{kg\cdot L^{-1}}", RES, 44)
        an = row(mx(r"\rho_{eau}", EAU, 42), mx("=", WHITE, 42), frac(n1, d1), mx("=", WHITE, 42), r1, buff=0.18)
        n2 = val("1000", r"\mathrm{g}", MASSE, 42)
        d2 = val("1000", r"\mathrm{mL}", VOL, 42)
        r2 = val("1", r"\mathrm{g\cdot mL^{-1}}", RES, 44)
        an2 = row(mx(r"\rho_{eau}", EAU, 42), mx("=", WHITE, 42), frac(n2, d2), mx("=", WHITE, 42), r2, buff=0.18)
        conv = tx("1 kg = 1000 g  et  1 L = 1000 mL", 20, SOFT)
        droite_c = VGroup(VGroup(q_eau, lit).arrange(RIGHT, buff=1.0), an, VGroup(an2, conv).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
        droite_c.arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        page = VGroup(illus, droite_c).arrange(RIGHT, buff=1.0)
        self.caser(page, top=self.haut() - 0.2)
        self.at(130.6)
        self.p(Write(q_eau), rt=1.0)
        self.p(Indicate(q_eau, color=EAU), rt=0.8)
        self.at(140.2)
        self.p(FadeIn(bal, shift=UP * 0.2), FadeIn(b_eau_g, shift=DOWN * 0.3), rt=1.3)
        self.at(144.6)
        self.p(Flash(bal[2], color=RES), Indicate(b_eau_l, color=VOL), rt=1.0)
        self.at(147.3)
        self.p(Write(lit), rt=1.0)
        self.encadre(lit, rt=0.7)
        self.tag_an(an, rt=0.3)
        self.p(FadeIn(an[0:2]), FadeIn(an[2][1]), rt=0.3)
        self.morph([(bal[2], n1), (b_eau_l, d1)], rt=1.1)
        self.p(Write(an[3]), Write(r1), rt=0.9)
        self.at(152.5)
        self.p(FadeIn(an2[0:2]), FadeIn(an2[2][1]), FadeIn(conv), rt=0.6)
        self.morph([(n1, n2), (d1, d2)], rt=1.3)
        self.at(155.5)
        self.p(Write(an2[3]), Write(r2), rt=1.0)
        self.p(Circumscribe(r2, color=RES), rt=0.9)

        # comparaison
        self.at(160.3)
        self.vider(garder=[self.cur_q], rt=0.6)
        comp = row(mx(r"\rho_{paraffine}", RHO, 46), mx("=", WHITE, 46), val(r"0{,}9", r"\mathrm{g\cdot mL^{-1}}", RHO, 46),
                   mx("<", ABSO, 56),
                   mx(r"\rho_{eau}", EAU, 46), mx("=", WHITE, 46), val(r"1{,}0", r"\mathrm{g\cdot mL^{-1}}", EAU, 46), buff=0.2)
        meme = tx("même unité (g·mL⁻¹) : on peut comparer directement les valeurs", 20, SOFT)
        # illustration : la bougie flotte
        cuve = VGroup(Line(LEFT * 2.2 + UP * 0.9, LEFT * 2.2 + DOWN * 0.9, color=WHITE, stroke_width=3),
                      Line(LEFT * 2.2 + DOWN * 0.9, RIGHT * 2.2 + DOWN * 0.9, color=WHITE, stroke_width=3),
                      Line(RIGHT * 2.2 + DOWN * 0.9, RIGHT * 2.2 + UP * 0.9, color=WHITE, stroke_width=3))
        eau = Rectangle(width=4.4, height=1.2, stroke_width=0, fill_color=EAU, fill_opacity=0.45).align_to(cuve, DOWN)
        bougie_f = bougie(h=0.9, w=0.6)
        flotte = VGroup(cuve, eau)
        bas = VGroup(comp, meme, flotte).arrange(DOWN, buff=0.5)
        self.caser(bas, top=self.haut() - 0.2)
        bougie_f.move_to(eau.get_top() + UP * 1.6)
        self.p(Write(comp[0:3]), rt=1.2)
        self.at(165.0)
        self.p(Write(comp[4:]), rt=1.2)
        self.at(168.6)
        self.p(GrowFromCenter(comp[3]), Flash(comp[3], color=ABSO), rt=0.9)
        self.p(FadeIn(meme), rt=0.7)
        self.at(173.2)
        self.p(Create(cuve), FadeIn(eau), FadeIn(bougie_f, shift=DOWN * 0.3), rt=1.0)
        cible = eau.get_top() + UP * (bougie_f.height / 2 - 0.25)
        self.p(bougie_f.animate.move_to(cible), rt=0.8, )
        self.p(bougie_f.animate.shift(UP * 0.06), rt=0.4)
        self.p(bougie_f.animate.shift(DOWN * 0.06), rt=0.4)
        self.at(175.6)
        self.reponse("ρ(paraffine) = 0,9 g·mL⁻¹ < ρ(eau) = 1,0 g·mL⁻¹ : la paraffine est moins dense que l'eau,\n"
                     "une bougie posée sur l'eau flotte.", rt=1.8)

        # ---------------- Question 3 ----------------
        self.at(179.9)
        self.vider()
        self.set_q("Question 3")
        self.question("3) Proposer une manière de vérifier la valeur de la température de fusion de la paraffine.", rt=1.0)
        # montage : bain-marie, tube, thermomètre, chauffage
        becher = VGroup(Line(LEFT * 1.1 + UP * 0.9, LEFT * 1.1 + DOWN * 0.9, color=WHITE, stroke_width=3),
                        Line(LEFT * 1.1 + DOWN * 0.9, RIGHT * 1.1 + DOWN * 0.9, color=WHITE, stroke_width=3),
                        Line(RIGHT * 1.1 + DOWN * 0.9, RIGHT * 1.1 + UP * 0.9, color=WHITE, stroke_width=3))
        eau_b = Rectangle(width=2.2, height=1.3, stroke_width=0, fill_color=EAU, fill_opacity=0.35).align_to(becher, DOWN)
        tube = RoundedRectangle(corner_radius=0.15, width=0.45, height=2.3, stroke_color=WHITE, stroke_width=2.5).move_to(UP * 0.35)
        paraf = RoundedRectangle(corner_radius=0.15, width=0.45, height=0.8, stroke_width=0, fill_color="#F4F4F4",
                                 fill_opacity=0.95).align_to(tube, DOWN)
        thermo = VGroup(RoundedRectangle(corner_radius=0.05, width=0.1, height=2.6, stroke_color="#FF5555", stroke_width=2),
                        Circle(radius=0.09, stroke_width=0, fill_color="#FF5555", fill_opacity=1))
        thermo[0].move_to(tube.get_center() + UP * 0.45)
        thermo[1].move_to(thermo[0].get_bottom())
        colonne = Rectangle(width=0.06, height=0.5, stroke_width=0, fill_color="#FF5555", fill_opacity=1).align_to(thermo[0], DOWN)
        plaque_c = Rectangle(width=2.6, height=0.25, stroke_color=WHITE, stroke_width=2, fill_color="#555555",
                             fill_opacity=1).next_to(becher, DOWN, buff=0.02)
        flammes = VGroup(*[Triangle(stroke_width=0, fill_color="#FF8C42", fill_opacity=1).scale(0.15).next_to(plaque_c, DOWN, buff=0.03).shift(RIGHT * dx)
                           for dx in (-0.6, -0.2, 0.2, 0.6)])
        montage = VGroup(becher, eau_b, tube, paraf, thermo, colonne, plaque_c, flammes)
        lab_m = VGroup(tx("thermomètre", 18, "#FF5555").next_to(thermo[0], RIGHT, buff=0.15).shift(UP * 0.9),
                       tx("paraffine", 18, WHITE).next_to(paraf, LEFT, buff=0.95),
                       tx("bain-marie", 18, EAU).next_to(becher, RIGHT, buff=0.15).shift(DOWN * 0.4),
                       tx("chauffage", 18, "#FF8C42").next_to(flammes, DOWN, buff=0.12))
        gauche = VGroup(montage, lab_m)
        # courbe de chauffage
        ax = Axes(x_range=[0, 14, 2], y_range=[0, 80, 25], x_length=6.0, y_length=3.8, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2})
        ax_l = VGroup(mx(r"t\ (\mathrm{min})", SOFT, 24).next_to(ax.c2p(14, 0), DOWN, buff=0.15),
                      mx(r"\theta\ (^\circ\mathrm{C})", SOFT, 24).next_to(ax.c2p(0, 80), LEFT, buff=0.1),
                      mx("50", "#FF8C42", 24).next_to(ax.c2p(0, 50), LEFT, buff=0.1),
                      mx("20", SOFT, 22).next_to(ax.c2p(0, 20), LEFT, buff=0.1))
        pal_l = tx("palier : la température reste constante pendant la fusion", 20, "#FF8C42")
        droite_g = VGroup(VGroup(ax, ax_l), pal_l).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        page = VGroup(gauche, droite_g).arrange(RIGHT, buff=1.2)
        self.caser(page, top=self.haut() - 0.3)
        seg1 = Line(ax.c2p(0, 20), ax.c2p(4, 50), color=WHITE, stroke_width=4)
        seg2 = Line(ax.c2p(4, 50), ax.c2p(9, 50), color="#FF8C42", stroke_width=6)
        seg3 = Line(ax.c2p(9, 50), ax.c2p(12.5, 72), color=WHITE, stroke_width=4)
        e1 = tx("solide", 18, EAU).next_to(seg1.get_center(), RIGHT, buff=0.15)
        e2 = tx("solide + liquide", 18, "#FF8C42").next_to(seg2, UP, buff=0.15)
        e3 = tx("liquide", 18, "#FF8C42").next_to(seg3.get_center(), RIGHT, buff=0.15)

        self.at(187.0)
        self.p(Create(becher), FadeIn(eau_b), FadeIn(plaque_c), rt=1.0)
        self.p(FadeIn(tube), FadeIn(paraf), FadeIn(lab_m[1]), FadeIn(lab_m[2]), rt=1.0)
        self.at(191.0)
        self.p(LaggedStart(*[GrowFromEdge(f, DOWN) for f in flammes], lag_ratio=0.15), FadeIn(lab_m[3]), rt=1.0)
        self.at(198.4)
        self.p(FadeIn(thermo, shift=DOWN * 0.5), FadeIn(colonne), FadeIn(lab_m[0]), rt=1.2)
        self.at(203.9)
        self.p(colonne.animate.stretch_to_fit_height(1.2, about_edge=DOWN), rt=2.0)
        self.at(207.2)
        self.p(Create(ax), FadeIn(ax_l), rt=1.0)
        self.at(209.3)
        self.p(Create(seg1), FadeIn(e1), colonne.animate.stretch_to_fit_height(1.6, about_edge=DOWN), rt=2.0)
        self.at(212.0)
        self.p(Create(seg2), FadeIn(e2), paraf.animate.set_fill("#FFE8A3", opacity=0.9), rt=3.0)
        self.p(Create(seg3), FadeIn(e3), colonne.animate.stretch_to_fit_height(2.1, about_edge=DOWN), rt=1.6)
        self.at(219.0)
        palier = SurroundingRectangle(seg2, color="#FF8C42", buff=0.15, corner_radius=0.08)
        tir = DashedLine(ax.c2p(4, 50), ax.c2p(0, 50), color="#FF8C42", stroke_width=3)
        self.p(Create(palier), Create(tir), FadeIn(pal_l), Indicate(ax_l[2], color="#FF8C42"), rt=1.5)
        self.at(221.6)
        self.reponse("On chauffe la paraffine (bain-marie) en relevant sa température avec un thermomètre.\n"
                     "Pour un corps pur, un palier apparaît pendant la fusion : sa valeur est la température de fusion.", rt=1.8, fs=22)

    # =================================================================
    #  EXERCICE 3 : pastille à la menthe (226 s → fin)
    # =================================================================
    def exercice3(self):
        self.at(226.4)
        self.vider()
        self.cur_q = None
        self.set_ex("Exercice 3 – Pastille à la menthe")
        carton = self.titre_exercice(3, "Pastille à la menthe", "chromatographie sur couche mince (CCM)")
        self.p(FadeIn(carton, shift=UP * 0.2), rt=1.0)
        self.at(236.0)
        self.p(FadeOut(carton, shift=UP * 0.3), rt=0.6)

        # --- corps pur / mélange
        self.at(237.5)
        pst = pastille(0.75).move_to(LEFT * 4.3 + UP * 0.6)
        pst_l = tx("pastille à la menthe", 22, WHITE).next_to(pst, DOWN, buff=0.25)
        q_pst = tx("plusieurs espèces chimiques ?", 22, SOFT).next_to(pst_l, DOWN, buff=0.15)
        self.p(FadeIn(pst, scale=0.6), FadeIn(pst_l), rt=1.0)
        self.p(FadeIn(q_pst), rt=0.7)
        self.at(244.6)
        cp_ic = Circle(radius=0.4, stroke_width=0, fill_color=CONC, fill_opacity=0.9)
        cols = ["#58C4DD", "#FF862F", "#83C167", "#C77DFF"]
        mel_ic = VGroup(*[Circle(radius=0.22, stroke_width=0, fill_color=c, fill_opacity=0.9) for c in cols]).arrange_in_grid(2, 2, buff=0.08)
        cp = VGroup(cp_ic, tx("corps pur", 26, WHITE, bold=True), tx("une seule espèce chimique", 20, SOFT)).arrange(DOWN, buff=0.2)
        mel = VGroup(mel_ic, tx("mélange", 26, WHITE, bold=True), tx("plusieurs espèces chimiques", 20, SOFT)).arrange(DOWN, buff=0.2)
        defs = VGroup(cp, mel).arrange(RIGHT, buff=1.4).move_to(RIGHT * 2.2 + UP * 0.6)
        self.p(FadeIn(cp, shift=UP * 0.2), rt=1.0)
        self.at(248.5)
        self.p(FadeIn(mel, shift=UP * 0.2), rt=1.0)

        # --- protocole : broyage, solvant, solution S
        self.at(254.1)
        self.p(FadeOut(defs), FadeOut(q_pst), rt=0.5)
        morceaux = VGroup(*[Polygon(*[np.array([math.cos(a), math.sin(a), 0]) * r for a, r in
                                      zip(np.linspace(0, TAU, 6, endpoint=False), (0.22, 0.17, 0.25, 0.19, 0.23, 0.2))],
                                    stroke_color=SOFT, stroke_width=1.5, fill_color=PASTILLE, fill_opacity=1)
                            .move_to(pst.get_center() + np.array([dx, dy, 0]))
                            for dx, dy in ((-0.35, 0.2), (0.3, 0.3), (0.0, -0.3), (-0.4, -0.25), (0.4, -0.2))])
        self.p(ReplacementTransform(pst, morceaux), FadeOut(pst_l), rt=0.8)
        br = tx("broyage", 22, SOFT).next_to(morceaux, DOWN, buff=0.3)
        self.p(FadeIn(br), rt=0.4)
        tube = RoundedRectangle(corner_radius=0.2, width=0.7, height=2.0, stroke_color=WHITE, stroke_width=2.5).move_to(UP * 0.3)
        sol = RoundedRectangle(corner_radius=0.2, width=0.7, height=1.0, stroke_width=0, fill_color="#DDE7F0",
                               fill_opacity=0.5).align_to(tube, DOWN)
        fl1 = Arrow(morceaux.get_right(), tube.get_left(), color=SOFT, buff=0.3)
        solv = tx("+ solvant (cyclohexane)", 22, EAU).next_to(fl1, UP, buff=0.15)
        s_l = tx("solution S", 26, WHITE, bold=True).next_to(tube, DOWN, buff=0.25)
        self.at(256.0)
        self.p(GrowArrow(fl1), FadeIn(solv), Create(tube), rt=0.9)
        self.p(morceaux.animate.scale(0.3).move_to(sol), FadeIn(sol), rt=0.9)
        self.p(FadeOut(morceaux), FadeIn(s_l), rt=0.5)

        # --- la CCM (plaque à gauche, conservée pendant tout l'exercice)
        self.at(259.1)
        self.vider(rt=0.5)
        P = plaque_ccm(h=4.4, w=3.3, centre=[-4.4, -0.25, 0])
        cuve = VGroup(Line([-6.4, 2.4, 0], [-6.4, -3.1, 0], color=WHITE, stroke_width=3),
                      Line([-6.4, -3.1, 0], [-2.4, -3.1, 0], color=WHITE, stroke_width=3),
                      Line([-2.4, -3.1, 0], [-2.4, 2.4, 0], color=WHITE, stroke_width=3),
                      Line([-6.6, 2.4, 0], [-2.2, 2.4, 0], color=SOFT, stroke_width=3))
        eluant = Rectangle(width=3.95, height=0.9, stroke_width=0, fill_color=EAU, fill_opacity=0.35)
        eluant.move_to([-4.4, -3.1 + 0.45, 0])
        cuve_l = tx("cuve à CCM", 20, SOFT).next_to(cuve, UP, buff=0.1)
        self.p(FadeIn(P["plaque"]), Create(P["ligne"]), FadeIn(P["marques"]), FadeIn(P["lettres"]),
               Create(cuve), FadeIn(eluant), FadeIn(cuve_l), rt=1.0)
        depots = VGroup(*[Dot(P["pos"](d, 0), radius=0.08, color=TACHE) for d in DEPOTS])
        self.p(LaggedStart(*[GrowFromCenter(dd) for dd in depots], lag_ratio=0.2), rt=1.0)
        ref = VGroup(
            row(Text("S", font_size=22, color=WHITE, weight=BOLD), tx(": solution S (pastille)", 20)),
            row(Text("C", font_size=22, color=WHITE, weight=BOLD), tx(": citral (citron)", 20)),
            row(Text("M", font_size=22, color=WHITE, weight=BOLD), tx(": menthol (menthe)", 20)),
            row(Text("E", font_size=22, color=WHITE, weight=BOLD), tx(": eucalyptol (eucalyptus)", 20)),
            row(Text("L", font_size=22, color=WHITE, weight=BOLD), tx(": limonène (orange)", 20)),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(RIGHT * 2.6 + UP * 0.3)
        self.p(FadeIn(ref, shift=LEFT * 0.2), rt=0.8)
        self.at(262.2)
        # élution : le front monte, les espèces (incolores) migrent
        y_bas = P["y0"]
        front_zone = Rectangle(width=P["plaque"].width - 0.05, height=0.05, stroke_width=0, fill_color=EAU, fill_opacity=0.18)
        front_zone.move_to([-4.4, y_bas, 0])
        fantomes = VGroup()
        for d in DEPOTS:
            for hh in HAUTEURS[d]:
                e = Ellipse(width=0.3, height=0.22, stroke_color=TACHE, stroke_width=1.5, fill_opacity=0).move_to(P["pos"](d, 0))
                e.cible = P["pos"](d, hh)
                fantomes.add(e)
        el_l = tx("élution : l'éluant monte par capillarité", 20, EAU).next_to(ref, DOWN, buff=0.5).align_to(ref, LEFT)
        self.p(FadeIn(el_l), FadeOut(depots), FadeIn(fantomes), rt=0.6)
        self.p(front_zone.animate.stretch_to_fit_height(P["y1"] - y_bas, about_edge=DOWN),
               *[e.animate.move_to(e.cible) for e in fantomes], rt=2.6)
        self.p(Create(P["front"]), rt=0.6)
        inc = tx("les espèces sont incolores : on ne les voit pas encore", 20, SOFT).next_to(el_l, DOWN, buff=0.2).align_to(el_l, LEFT)
        self.p(FadeIn(inc), rt=0.6)
        self.at(267.0)
        taches = VGroup(*[P["taches"][d] for d in DEPOTS])
        self.p(FadeOut(VGroup(cuve, eluant, cuve_l)), FadeIn(taches), FadeOut(fantomes), rt=0.9)
        chro = tx("→ chromatogramme (après révélation)", 20, WHITE).next_to(inc, DOWN, buff=0.2).align_to(inc, LEFT)
        self.p(FadeIn(chro), rt=0.5)
        plaque_g = VGroup(P["plaque"], front_zone, P["ligne"], P["front"], P["marques"], P["lettres"], taches)

        # ---------------- Question 1 ----------------
        self.at(270.2)
        self.vider(garder=[plaque_g])
        self.set_q("Question 1")
        self.question("1) Rappeler le principe d'une CCM.", rt=0.9)
        x_g = P["plaque"].get_right()[0] + 0.7
        pts1 = VGroup(
            tx("La CCM permet de SÉPARER et d'IDENTIFIER", 24, ABSO, bold=True),
            tx("les espèces chimiques d'un mélange.", 24, ABSO, bold=True),
            row(tx("• phase fixe :", 22, WHITE, bold=True), tx("la plaque", 22, SOFT), buff=0.15),
            row(tx("• phase mobile :", 22, EAU, bold=True), tx("l'éluant, qui monte par capillarité", 22, SOFT), buff=0.15),
            tx("• chaque espèce est entraînée plus ou moins haut", 22, WHITE),
            row(tx("• deux taches à la même hauteur", 22, WHITE), tx("= même espèce chimique", 22, RES, bold=True), buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        self.poser(pts1, x_g, self.haut() - 0.2)
        self.at(273.6)
        self.p(FadeIn(pts1[0:2], shift=LEFT * 0.2), rt=1.2)
        self.at(277.5)
        self.p(FadeIn(pts1[2]), Indicate(P["plaque"], color=WHITE, scale_factor=1.02), rt=1.0)
        self.p(FadeIn(pts1[3]), Indicate(front_zone, color=EAU, scale_factor=1.02), rt=1.0)
        self.at(281.0)
        self.p(FadeIn(pts1[4]), rt=0.8)
        self.at(283.0)
        m_t = P["taches"]["M"][0]
        s_t = P["taches"]["S"][1]
        lien = DashedLine(s_t.get_center(), m_t.get_center(), color=RES, stroke_width=3)
        self.p(FadeIn(pts1[5]), Create(lien), rt=1.0)
        self.at(285.6)
        self.reponse("La CCM sépare les espèces d'un mélange (l'éluant les entraîne plus ou moins haut sur la plaque)\n"
                     "et permet de les identifier : deux taches à la même hauteur correspondent à la même espèce.", rt=1.8, fs=21)

        # ---------------- Question 2 ----------------
        self.at(291.7)
        self.vider(garder=[plaque_g])
        self.set_q("Question 2")
        self.question("2) Les espèces sont incolores. Décrire une technique pour les révéler sur le chromatogramme.", rt=0.9)
        self.p(taches.animate.set_fill(opacity=0.0).set_stroke(TACHE, width=1.5, opacity=0.6), rt=0.8)
        inv = tx("espèces incolores : invisibles à l'œil nu", 22, SOFT)
        self.poser(inv, x_g, self.haut() - 0.2)
        self.p(FadeIn(inv), rt=0.7)
        self.at(300.4)
        lampe = VGroup(RoundedRectangle(corner_radius=0.1, width=2.6, height=0.45, stroke_color=WHITE, stroke_width=2,
                                        fill_color="#2A2F3A", fill_opacity=1),
                       Rectangle(width=2.2, height=0.12, stroke_width=0, fill_color=UVC, fill_opacity=1))
        lampe[1].align_to(lampe[0], DOWN).shift(UP * 0.05)
        lampe.next_to(P["plaque"], UP, buff=0.15)
        ajuster(lampe, P["plaque"].width)
        lampe.next_to(P["plaque"], UP, buff=0.12)
        rayons = VGroup(*[Line(lampe.get_bottom() + RIGHT * dx, P["plaque"].get_bottom() + RIGHT * dx * 1.2 + UP * 0.3,
                               color=UVC, stroke_width=2, stroke_opacity=0.5) for dx in (-1.2, -0.6, 0, 0.6, 1.2)])
        uv_t = VGroup(row(tx("Lampe UV", 26, UVC, bold=True), tx(": on éclaire la plaque", 22, WHITE), buff=0.15),
                      tx("les taches apparaissent sombres sur la plaque fluorescente", 22, WHITE),
                      tx("→ on les entoure au crayon", 22, RES)).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.sous(uv_t, inv, x_g, 0.5)
        self.p(FadeIn(lampe, shift=DOWN * 0.2), rt=0.8)
        self.p(LaggedStart(*[Create(r) for r in rayons], lag_ratio=0.1), P["plaque"].animate.set_fill(UVC, opacity=0.18), rt=1.0)
        self.p(FadeIn(uv_t[0]), rt=0.6)
        self.at(303.2)
        self.p(taches.animate.set_fill("#3A3A3A", opacity=1).set_stroke(WHITE, width=1.5, opacity=1), FadeIn(uv_t[1]), rt=1.2)
        self.p(FadeIn(uv_t[2]), rt=0.6)
        self.at(305.8)
        autre = self.sous(tx("(il existe aussi des révélateurs chimiques, comme le diiode)", 20, SOFT), uv_t, x_g, 0.35)
        self.p(FadeIn(autre), rt=0.8)
        self.at(308.4)
        self.reponse("On place le chromatogramme sous une lampe UV : les taches des espèces incolores deviennent\n"
                     "visibles (sombres) et on les entoure au crayon.", rt=1.6)
        self.at(312.8)
        self.p(FadeOut(VGroup(lampe, rayons)), P["plaque"].animate.set_fill("#F7F7F2", opacity=0.12),
               taches.animate.set_fill(TACHE, opacity=1).set_stroke(width=0), rt=0.8)

        # ---------------- Question 3 ----------------
        self.at(314.1)
        self.vider(garder=[plaque_g])
        self.set_q("Question 3")
        self.question("3) Préciser si la pastille est un corps pur ou un mélange. Justifier.", rt=0.9)
        self.at(320.8)
        col_S = SurroundingRectangle(VGroup(P["lettres"][0], P["taches"]["S"]), color=CONC, buff=0.12, corner_radius=0.08)
        lS = tx("S : espèces de la pastille", 22, CONC)
        self.poser(lS, x_g, self.haut() - 0.2)
        self.p(Create(col_S), FadeIn(lS), rt=1.2)
        self.at(332.4)
        col_R = SurroundingRectangle(VGroup(*[P["lettres"][i] for i in range(1, 5)], *[P["taches"][d] for d in "CMEL"]),
                                     color=SOFT, buff=0.12, corner_radius=0.08)
        lR = self.sous(tx("C, M, E, L : espèces de référence (corps purs)", 22, SOFT), lS, x_g, 0.2)
        self.p(Create(col_R), FadeIn(lR), rt=1.2)

        self.at(340.8)
        fl_v = Arrow(P["pos"]("S", -0.02) + LEFT * 0.35, P["pos"]("S", 0.95) + LEFT * 0.35, color=CONC, buff=0, stroke_width=5)
        fl_h = Arrow(P["pos"]("S", 0.388) + LEFT * 0.1, P["pos"]("L", 0.388) + RIGHT * 0.3, color=RES, buff=0, stroke_width=5)
        lect = VGroup(
            row(tx("lecture verticale ↑", 22, CONC, bold=True), tx(": combien d'espèces dans un dépôt ?", 20), buff=0.15),
            row(tx("lecture horizontale →", 22, RES, bold=True), tx(": même hauteur = même espèce", 20), buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        self.sous(lect, lR, x_g, 0.5)
        self.p(FadeOut(col_R), GrowArrow(fl_v), FadeIn(lect[0]), rt=1.3)
        self.at(347.0)
        self.p(GrowArrow(fl_h), FadeIn(lect[1]), rt=1.3)
        self.at(352.0)
        self.p(FadeOut(fl_h), Indicate(lect[0], color=CONC), rt=1.0)

        self.at(361.3)
        regle = VGroup(row(tx("corps pur :", 22, WHITE, bold=True), tx("une seule tache au-dessus du dépôt", 22), buff=0.15),
                       row(tx("mélange :", 22, WHITE, bold=True), tx("plusieurs taches au-dessus du dépôt", 22), buff=0.15)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        self.sous(regle, lect, x_g, 0.45)
        self.p(FadeIn(regle[0], shift=LEFT * 0.2), rt=1.0)
        self.at(365.4)
        self.p(FadeIn(regle[1], shift=LEFT * 0.2), rt=1.0)
        self.at(367.7)
        nums = VGroup(*[Text(str(i + 1), font_size=20, color=CONC, weight=BOLD).next_to(t, RIGHT, buff=0.12)
                        for i, t in enumerate(P["taches"]["S"])])
        self.p(LaggedStart(*[AnimationGroup(Indicate(t, color=CONC, scale_factor=1.6), FadeIn(n))
                             for t, n in zip(P["taches"]["S"], nums)], lag_ratio=0.5), rt=2.6)
        cinq = self.sous(tx("5 taches au-dessus de S", 24, CONC, bold=True), regle, x_g, 0.35)
        self.p(FadeIn(cinq, scale=1.2), Indicate(regle[1], color=RES), rt=1.0)
        self.at(372.7)
        self.reponse("Au-dessus du dépôt S, il y a plusieurs taches (5) : la pastille contient plusieurs espèces chimiques,\n"
                     "c'est un mélange.", rt=1.6)

        # ---------------- Question 4 ----------------
        self.at(378.4)
        self.vider(garder=[plaque_g, fl_v, nums])
        self.set_q("Question 4")
        self.question("4) Nommer les espèces identifiables dans la pastille.", rt=0.9)
        self.at(380.6)
        self.p(Indicate(fl_v, color=CONC), rt=0.8)
        self.at(384.4)
        self.p(FadeOut(fl_v), rt=0.5)
        lh = tx("lecture horizontale : on compare la hauteur de chaque tache de S aux références", 22, RES)
        self.poser(lh, x_g, self.haut() - 0.2)
        self.p(FadeIn(lh), rt=0.9)

        x_fin = P["plaque"].get_right()[0] - 0.05
        def ligne_h(i, c):
            n = nums[i]
            y = P["taches"]["S"][i].get_center()[1]
            return DashedLine([n.get_right()[0] + 0.06, y, 0], [x_fin, y, 0], color=c, stroke_width=3)

        resultats = VGroup()
        def resultat(i, txt, c):
            r = row(Text(str(i + 1), font_size=22, color=CONC, weight=BOLD), tx(txt, 22, c), buff=0.25)
            return r

        res_lines = [resultat(0, "✗ aucune référence à cette hauteur", "#FF7777"),
                     resultat(1, "✓ même hauteur que M : MENTHOL", RES),
                     resultat(2, "✓ même hauteur que E : EUCALYPTOL", RES),
                     resultat(3, "✗ aucune référence", "#FF7777"),
                     resultat(4, "✗ aucune référence", "#FF7777")]
        resultats = VGroup(*res_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.sous(resultats, lh, x_g, 0.45)

        # tache 1
        self.at(396.0)
        l1 = ligne_h(0, "#FF7777")
        self.p(Indicate(P["taches"]["S"][0], color=CONC, scale_factor=1.6), rt=0.8)
        self.p(Create(l1), rt=1.2)
        self.at(401.7)
        self.p(FadeIn(resultats[0], shift=LEFT * 0.2), rt=0.8)
        ni = tx("ni citral, ni menthol, ni eucalyptol, ni limonène", 18, SOFT).next_to(resultats[0], DOWN, buff=0.05).align_to(resultats[0][1], LEFT)
        self.p(FadeIn(ni), rt=0.8)
        self.p(FadeOut(ni), rt=0.4)
        # tache 2 : menthol
        self.at(407.8)
        l2 = ligne_h(1, RES)
        self.p(Create(l2), rt=1.2)
        self.at(409.3)
        self.p(Indicate(P["taches"]["M"][0], color=RES, scale_factor=1.8), Flash(P["taches"]["M"][0], color=RES),
               Indicate(P["lettres"][2], color=RES, scale_factor=1.5), rt=1.2)
        self.p(FadeIn(resultats[1], shift=LEFT * 0.2), rt=0.8)
        # tache 3 : eucalyptol
        self.at(414.2)
        l3 = ligne_h(2, RES)
        self.p(Create(l3), rt=1.2)
        self.at(416.5)
        self.p(Indicate(P["taches"]["E"][0], color=RES, scale_factor=1.8), Flash(P["taches"]["E"][0], color=RES),
               Indicate(P["lettres"][3], color=RES, scale_factor=1.5), rt=1.2)
        self.p(FadeIn(resultats[2], shift=LEFT * 0.2), rt=0.8)
        # taches 4 et 5
        self.at(420.7)
        l4 = ligne_h(3, "#FF7777")
        self.p(Create(l4), FadeIn(resultats[3], shift=LEFT * 0.2), rt=1.2)
        self.at(422.6)
        l5 = ligne_h(4, "#FF7777")
        self.p(Create(l5), FadeIn(resultats[4], shift=LEFT * 0.2), rt=1.2)
        self.at(423.8)
        nb = tx("Taches 1, 4, 5 : espèces présentes dans la pastille, mais différentes des références déposées.", 19, SOFT)
        self.sous(nb, resultats, x_g, 0.35)
        self.p(FadeIn(nb), rt=1.0)
        self.at(427.5)
        self.p(Indicate(VGroup(P["taches"]["C"], P["lettres"][1]), color="#FF7777"),
               Indicate(VGroup(P["taches"]["L"], P["lettres"][4]), color="#FF7777"), rt=1.2)
        self.at(430.8)
        self.reponse("Deux taches de S sont à la même hauteur que M et E : la pastille contient du menthol et de l'eucalyptol.\n"
                     "Elle ne contient ni citral, ni limonène.", rt=1.6, fs=21)

    # =================================================================
    #  CONCLUSION
    # =================================================================
    def conclusion(self):
        self.at(435.2)
        self.vider(rt=0.8)
        self.cur_q = None
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 40, WHITE, bold=True)
        items = VGroup(
            row(etiquette("ρ", RHO).scale(1.4), tx("ρ = m / V : on calcule, puis on compare à une valeur de référence", 24), buff=0.3),
            row(etiquette("θ", "#FF8C42").scale(1.4), tx("un corps pur change d'état à température constante (palier)", 24), buff=0.3),
            row(etiquette("CCM", RES).scale(1.4), tx("vertical : nombre d'espèces · horizontal : identification", 24), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        g = VGroup(t, items).arrange(DOWN, buff=0.6)
        ajuster(g, 13.0)
        self.p(Write(t), rt=0.9)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=1.5)
        self.wait(2.5)
        self.t += 2.5
