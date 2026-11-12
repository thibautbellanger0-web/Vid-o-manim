from manim import *
import math

# =====================================================================
#  Correction en vidéo – Feuille 2.1 « Identification des espèces chimiques »
#  Exercices 4 et 5 – pour Manim Community (rendu sur GitHub).
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
TEAL = "#5CD0B3"


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
    def p(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt, **kw)
        self.t += rt

    def pause(self, d):
        if d > 0:
            self.wait(d)
            self.t += d

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
        self.hdr_ex = tx("Identification des espèces chimiques", 22, SOFT).to_corner(UL, buff=0.3)
        self.add(self.hdr_ex)
        self.exercice4()
        self.exercice5()
        self.conclusion()

    # =================================================================
    #  Dessins propres à ces exercices
    # =================================================================
    def tube_essai(self, h=2.4, w=0.55):
        """Tube à essai : [0] contour, [1] forme intérieure (invisible, pour remplir)."""
        corps = Rectangle(width=w, height=h - w / 2).shift(UP * w / 4)
        fond = Circle(radius=w / 2).move_to(corps.get_bottom())
        contour = Union(corps, fond, stroke_color=WHITE, stroke_width=2.5, fill_opacity=0)
        inte = Union(Rectangle(width=w - 0.07, height=h - w / 2).shift(UP * w / 4),
                     Circle(radius=w / 2 - 0.035).move_to(corps.get_bottom()))
        inte.set_opacity(0)
        return VGroup(contour, inte)

    def remplir(self, tube, y_bas, y_haut, couleur, op):
        if y_haut - y_bas < 0.012:
            return VMobject()
        inte = tube[1]
        boite = Rectangle(width=inte.width + 0.3, height=y_haut - y_bas).move_to([inte.get_x(), (y_bas + y_haut) / 2, 0])
        return Intersection(inte.copy().set_opacity(1), boite, stroke_width=0, fill_color=couleur, fill_opacity=op)

    def thermometre(self, h=2.2):
        tige = RoundedRectangle(corner_radius=0.05, width=0.12, height=h, stroke_color="#FF5555", stroke_width=2)
        bulbe = Circle(radius=0.1, stroke_width=0, fill_color="#FF5555", fill_opacity=1).move_to(tige.get_bottom())
        return VGroup(tige, bulbe)

    def molecule_o2(self, r=0.13):
        a = Circle(radius=r, stroke_color=WHITE, stroke_width=1, fill_color="#FF4D4D", fill_opacity=1)
        b = a.copy().shift(RIGHT * r * 1.5)
        return VGroup(a, b).center()

    def molecule_co2(self, r=0.12):
        c = Circle(radius=r * 1.1, stroke_color=WHITE, stroke_width=1, fill_color="#3A3A3A", fill_opacity=1)
        o1 = Circle(radius=r, stroke_color=WHITE, stroke_width=1, fill_color="#FF4D4D", fill_opacity=1).shift(LEFT * r * 1.75)
        o2 = o1.copy().shift(RIGHT * r * 3.5)
        return VGroup(o1, o2, c)

    def plante(self, s=1.0):
        pot = Polygon([-0.45, 0, 0], [0.45, 0, 0], [0.35, -0.6, 0], [-0.35, -0.6, 0], stroke_color="#8B5A2B", stroke_width=2,
                      fill_color="#A0522D", fill_opacity=1)
        tige = Line([0, 0, 0], [0, 1.4, 0], color="#4CAF50", stroke_width=6)
        feuilles = VGroup(
            Ellipse(width=0.9, height=0.38, stroke_width=0, fill_color="#66BB6A", fill_opacity=1).rotate(0.5).move_to([0.42, 0.75, 0]),
            Ellipse(width=0.9, height=0.38, stroke_width=0, fill_color="#43A047", fill_opacity=1).rotate(-0.5).move_to([-0.42, 1.05, 0]),
            Ellipse(width=0.7, height=0.32, stroke_width=0, fill_color="#81C784", fill_opacity=1).rotate(0.3).move_to([0.3, 1.45, 0]))
        return VGroup(pot, tige, feuilles).scale(s)

    def soleil(self, r=0.4):
        disque = Circle(radius=r, stroke_width=0, fill_color="#FFC107", fill_opacity=1)
        rayons = VGroup(*[Line(ORIGIN, RIGHT * r * 0.5, color="#FFC107", stroke_width=3).shift(RIGHT * r * 1.25).rotate(a, about_point=ORIGIN)
                          for a in np.linspace(0, TAU, 10, endpoint=False)])
        return VGroup(disque, rayons)

    def lune(self, r=0.38):
        return Difference(Circle(radius=r), Circle(radius=r).shift(RIGHT * r * 0.6 + UP * r * 0.25),
                          stroke_width=0, fill_color="#E8E8C8", fill_opacity=1)

    def buchette(self):
        bois = Rectangle(width=1.5, height=0.08, stroke_width=0, fill_color="#C8A26B", fill_opacity=1)
        braise = Dot(bois.get_right(), radius=0.07, color="#FF6D00")
        return VGroup(bois, braise)

    def flamme(self):
        return VGroup(Ellipse(width=0.26, height=0.5, stroke_width=0, fill_color="#FFB703", fill_opacity=1),
                      Ellipse(width=0.12, height=0.26, stroke_width=0, fill_color="#FFF3B0", fill_opacity=1).shift(DOWN * 0.07))

    # =================================================================
    #  EXERCICE 4 : identifier un liquide (0 s → 149 s)
    # =================================================================
    def exercice4(self):
        self.at(0.5)
        self.set_ex("Exercice 4 – Identifier un liquide")
        carton = self.titre_exercice(4, "Identifier un liquide", "par sa température de changement d'état")
        self.p(FadeIn(carton, shift=UP * 0.2), rt=1.0)
        self.at(9.0)
        self.p(Indicate(carton[2], color=ABSO), rt=1.2)
        self.at(12.6)
        self.p(FadeOut(carton, shift=UP * 0.3), rt=0.6)

        # --- le montage : tube dans un cristallisoir (eau + glace + sel)
        self.at(13.3)
        cris = VGroup(Line([-2.4, 0.7, 0], [-2.4, -0.7, 0]), Line([-2.4, -0.7, 0], [2.4, -0.7, 0]), Line([2.4, -0.7, 0], [2.4, 0.7, 0]))
        cris.set_stroke(WHITE, 3)
        bain = Rectangle(width=4.75, height=1.15, stroke_width=0, fill_color="#B3E5FC", fill_opacity=0.35).align_to(cris, DOWN).shift(UP * 0.03)
        rng = np.random.default_rng(3)
        glacons = VGroup(*[RoundedRectangle(corner_radius=0.05, width=0.32, height=0.28, stroke_color=WHITE, stroke_width=1.5,
                                            fill_color="#E1F5FE", fill_opacity=0.85).rotate(rng.uniform(-0.6, 0.6))
                           .move_to([x, rng.uniform(-0.45, 0.25), 0]) for x in (-2.0, -1.5, -1.0, 0.95, 1.45, 1.95)])
        sel = VGroup(*[Dot([rng.uniform(-2.3, 2.3), rng.uniform(-0.65, -0.45), 0], radius=0.025, color=WHITE) for _ in range(30)])
        tube = self.tube_essai(h=2.6, w=0.55)
        tube.align_to(cris, DOWN).shift(UP * 0.14)          # le tube repose dans le cristallisoir
        y_b = tube[1].get_bottom()[1]
        y_l = y_b + 1.3
        niveau_s = ValueTracker(0.0)            # fraction solidifiée (0 → 1)
        liq = always_redraw(lambda: self.remplir(tube, y_b + 1.3 * niveau_s.get_value(), y_l, "#9CC9F5", 0.45))
        sol = always_redraw(lambda: self.remplir(tube, y_b, y_b + 1.3 * niveau_s.get_value(), "#F0F8FF", 0.95))
        th = self.thermometre(2.4)
        th.move_to([0.0, y_b + 1.3, 0]).shift(UP * 0.0)
        th.align_to(tube[1], DOWN).shift(UP * 0.15)
        montage = VGroup(cris, bain, glacons, sel, tube, th)
        montage.shift(LEFT * 2.6 + DOWN * 0.6)
        y_b = tube[1].get_bottom()[1]
        y_l = y_b + 1.3
        lab = VGroup(
            tx("liquide inconnu", 20, "#9CC9F5").next_to(tube, RIGHT, buff=0.15).shift(UP * 0.75),
            tx("thermomètre", 20, "#FF5555").next_to(th, UP, buff=0.1),
            tx("cristallisoir", 20, WHITE).next_to(cris, DOWN, buff=0.15),
            tx("mélange réfrigérant : eau + glace + sel", 20, "#B3E5FC").next_to(cris, DOWN, buff=0.5),
        )
        self.p(Create(cris), FadeIn(bain), rt=0.8)
        self.add(liq, sol)
        self.p(FadeIn(tube[0]), FadeIn(lab[0]), FadeIn(lab[2]), rt=0.8)
        self.bring_to_front(tube[0])
        self.at(16.5)
        self.p(LaggedStart(*[FadeIn(g, shift=DOWN * 0.3) for g in glacons], lag_ratio=0.15), FadeIn(sel), FadeIn(lab[3]), rt=1.5)
        self.at(19.5)
        froid = tx("❄ abaisse la température", 24, "#B3E5FC").move_to([3.3, 1.6, 0])
        self.p(FadeIn(th), FadeIn(lab[1]), FadeIn(froid, shift=DOWN * 0.2), rt=1.0)

        # --- l'idée : refroidir et observer la solidification
        self.at(24.5)
        temp = ValueTracker(20.0)
        def affichage():
            v = temp.get_value()
            s = ("%.1f" % v).replace(".", ",").replace("-", "−") + " °C"
            t = Text(s, font_size=34, color=WHITE, weight=BOLD)
            r = RoundedRectangle(corner_radius=0.1, width=2.2, height=0.7, stroke_color="#FF5555", stroke_width=2,
                                 fill_color="#1B1F27", fill_opacity=1)
            return VGroup(r, t.move_to(r)).move_to([3.3, 0.5, 0])
        ecran = always_redraw(affichage)
        colonne = always_redraw(lambda: Rectangle(width=0.06, height=max(0.05, 0.3 + 0.07 * (temp.get_value() + 5)), stroke_width=0,
                                                  fill_color="#FF5555", fill_opacity=1).align_to(th[0], DOWN).set_x(th.get_x()))
        self.p(FadeIn(ecran), FadeIn(colonne), rt=0.6)
        idee = VGroup(row(tx("liquide", 24, "#9CC9F5", bold=True), Arrow(LEFT * 0.4, RIGHT * 0.4, buff=0, color=WHITE),
                          tx("solide", 24, "#F0F8FF", bold=True), buff=0.2),
                      tx("on observe le passage", 20, SOFT)).arrange(DOWN, buff=0.15).move_to([3.3, -0.7, 0])
        self.p(temp.animate.set_value(12.0), rt=3.0, rate_func=linear)
        self.at(30.5)
        self.p(FadeIn(idee, shift=UP * 0.2), rt=0.8)
        self.at(36.2)
        solid = tx("→ température de solidification", 22, ABSO).next_to(idee, DOWN, buff=0.3)
        self.p(FadeIn(solid), rt=0.8)
        self.at(38.6)
        self.vider(rt=0.6)

        # ---------------- Question 1 ----------------
        self.at(39.5)
        self.set_q("Question 1")
        self.question("1) Préciser pourquoi il est possible d'affirmer que le liquide inconnu est un corps pur.", rt=1.0)
        T = [20, 18, 16, 14, 12, 10, 8, 6.5, 6.5, 6.5, 6.5, 5, 4, 3, 2, 1, 0, -1, -2, -3, -4]
        def theta(t):
            t = min(max(t, 0), 20)
            i = min(int(t), 19)
            return T[i] + (T[i + 1] - T[i]) * (t - i)
        def frac_sol(t):
            return min(max((t - 7) / 3, 0), 1)
        ax = Axes(x_range=[0, 21, 5], y_range=[-5, 21, 5], x_length=6.6, y_length=4.3, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2})
        g_lab = VGroup()
        for v in (5, 10, 15, 20):
            g_lab.add(mx(str(v), SOFT, 22).next_to(ax.c2p(v, 0), DOWN, buff=0.12))
        for v in (-5, 0, 5, 10, 15, 20):
            g_lab.add(mx(str(v).replace("-", "-"), SOFT, 22).next_to(ax.c2p(0, v), LEFT, buff=0.12))
        n_x = tx("t (min)", 20, SOFT).next_to(ax.c2p(21, 0), UP, buff=0.12).shift(LEFT * 0.3)
        n_y = tx("θ (°C)", 20, SOFT).next_to(ax.c2p(0, 21), UP, buff=0.08).shift(RIGHT * 0.45)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(20.5, 0), color=SOFT, stroke_width=1.2, stroke_opacity=0.5)
        graph = VGroup(ax, g_lab, n_x, n_y, zero)
        # tube à droite, synchronisé avec le point mobile
        tube2 = self.tube_essai(h=2.4, w=0.6)
        th2 = self.thermometre(2.2)
        th2.align_to(tube2[1], DOWN).shift(UP * 0.15).set_x(tube2.get_x())
        reserve = Rectangle(width=2.4, height=1.0, stroke_width=0, fill_opacity=0).next_to(tube2, DOWN, buff=0.1)
        droite = VGroup(tube2, th2, reserve)
        page = VGroup(graph, droite).arrange(RIGHT, buff=1.6)
        self.caser(page, top=self.haut() - 0.75, bottom=-2.5)
        th2.align_to(tube2[1], DOWN).shift(UP * 0.15).set_x(tube2.get_x())
        yb2 = tube2[1].get_bottom()[1]
        H2 = 1.3
        tt = ValueTracker(0.0)
        liq2 = always_redraw(lambda: self.remplir(tube2, yb2 + H2 * frac_sol(tt.get_value()), yb2 + H2, "#9CC9F5", 0.45))
        sol2 = always_redraw(lambda: self.remplir(tube2, yb2, yb2 + H2 * frac_sol(tt.get_value()), "#F0F8FF", 0.95))
        def etat():
            f = frac_sol(tt.get_value())
            s, c = ("liquide", "#9CC9F5") if f <= 0 else (("solide", "#F0F8FF") if f >= 1 else ("liquide + solide", ABSO))
            return tx(s, 22, c, bold=True).next_to(tube2, DOWN, buff=0.2)
        lab_etat = always_redraw(etat)
        def lecture():
            v = theta(tt.get_value())
            s = ("%.1f" % v).replace(".", ",").replace("-", "−") + " °C"
            return Text(s, font_size=26, color=WHITE, weight=BOLD).next_to(tube2, DOWN, buff=0.62)
        lab_temp = always_redraw(lecture)
        courbe = always_redraw(lambda: VMobject(stroke_color=TEAL, stroke_width=4).set_points_as_corners(
            [ax.c2p(x, theta(x)) for x in np.linspace(0, max(tt.get_value(), 0.02), 60)]))
        croix = always_redraw(lambda: VGroup(*[Cross(stroke_color=WHITE, stroke_width=2).scale(0.07).move_to(ax.c2p(i, T[i]))
                                               for i in range(21) if i <= tt.get_value() + 1e-6]))
        point = always_redraw(lambda: Dot(ax.c2p(tt.get_value(), theta(tt.get_value())), radius=0.09, color=ABSO))

        self.at(43.6)
        self.p(Create(ax), FadeIn(g_lab), FadeIn(n_x), FadeIn(n_y), FadeIn(zero), rt=1.4)
        self.add(liq2, sol2)
        self.p(FadeIn(tube2[0]), FadeIn(th2), rt=0.6)
        self.bring_to_front(tube2[0])
        self.add(courbe, croix, point, lab_etat, lab_temp)
        self.at(47.3)
        self.p(Flash(ax.c2p(0, 20), color=ABSO, flash_radius=0.3), rt=0.8)
        self.at(50.3)
        apercu = DashedLine(ax.c2p(0, 20), ax.c2p(20, -4), color=SOFT, stroke_width=1.5, stroke_opacity=0.5)
        fin = Dot(ax.c2p(20, -4), radius=0.07, color=SOFT)
        self.p(Create(apercu), FadeIn(fin), rt=1.2)
        self.p(Flash(fin, color=SOFT, flash_radius=0.3), rt=0.8)
        self.p(FadeOut(apercu), FadeOut(fin), rt=0.4)
        self.at(55.4)
        baisse = tx("la température baisse régulièrement", 20, TEAL).next_to(ax.c2p(3.5, 15), RIGHT, buff=0.3)
        self.p(FadeIn(baisse), rt=0.5)
        self.p(tt.animate.set_value(7.0), rt=7.6, rate_func=linear)
        self.at(64.1)
        self.p(tt.animate.set_value(10.0), rt=5.4, rate_func=linear)
        pal = SurroundingRectangle(VGroup(Dot(ax.c2p(7, 6.5)), Dot(ax.c2p(10, 6.5))), color=ABSO, buff=0.15, corner_radius=0.08)
        pal_l = tx("PALIER", 22, ABSO, bold=True).next_to(pal, UP, buff=0.1)
        self.p(Create(pal), FadeIn(pal_l), FadeOut(baisse), rt=0.8)
        self.at(70.9)
        expl = VGroup(tx("pendant le palier :", 20, SOFT),
                      tx("le liquide se solidifie", 22, ABSO, bold=True)).arrange(DOWN, buff=0.1)
        expl.next_to(pal, RIGHT, buff=0.3).shift(UP * 0.9)
        self.p(FadeIn(expl, shift=UP * 0.15), Indicate(tube2[0], color=ABSO), rt=1.2)
        self.at(76.5)
        regle = tx("Corps pur : la température reste constante pendant le changement d'état", 22, RES)
        regle.next_to(self.cur_q, DOWN, buff=0.18).align_to(self.cur_q, LEFT)
        ajuster(regle, 12.8)
        self.p(FadeIn(regle, shift=DOWN * 0.1), rt=1.0)
        self.at(83.8)
        self.p(Indicate(pal_l, color=ABSO), Wiggle(tube2[0]), rt=1.4)
        self.at(87.3)
        self.p(tt.animate.set_value(20.0), rt=2.8, rate_func=linear)
        self.at(90.5)
        self.reponse("La courbe θ = f(t) présente un palier de température pendant le changement d'état (solidification) :\n"
                     "le liquide inconnu est donc un corps pur.", rt=1.6, fs=22)

        # ---------------- Question 2 ----------------
        self.at(101.9)
        courbe.clear_updaters(); croix.clear_updaters(); point.clear_updaters()
        lab_etat.clear_updaters(); lab_temp.clear_updaters(); liq2.clear_updaters(); sol2.clear_updaters()
        garde = [graph, courbe, croix, pal, pal_l]
        self.vider(garder=garde)
        self.set_q("Question 2")
        self.question("2) Déterminer la température de fusion de ce corps.", rt=1.0)
        x_d = graph.get_right()[0] + 0.7
        fs_ = VGroup(
            row(tx("SOLIDE", 24, "#F0F8FF", bold=True), Arrow(LEFT * 0.9, RIGHT * 0.9, buff=0, color="#FF8C42"),
                tx("LIQUIDE", 24, "#9CC9F5", bold=True), buff=0.2),
            tx("fusion", 20, "#FF8C42"),
            row(tx("SOLIDE", 24, "#F0F8FF", bold=True), Arrow(RIGHT * 0.9, LEFT * 0.9, buff=0, color=TEAL),
                tx("LIQUIDE", 24, "#9CC9F5", bold=True), buff=0.2),
            tx("solidification", 20, TEAL),
            tx("même température pour un corps pur", 20, RES, bold=True))
        fs_[1].next_to(fs_[0][1], UP, buff=0.05)
        bloc = VGroup(VGroup(fs_[0], fs_[1]), VGroup(fs_[2], fs_[3]), fs_[4]).arrange(DOWN, buff=0.3)
        fs_[3].next_to(fs_[2][1], DOWN, buff=0.12)
        self.poser(bloc, x_d, self.haut() - 0.3)
        self.at(106.2)
        self.p(FadeIn(VGroup(fs_[0], fs_[1]), shift=LEFT * 0.2), rt=0.9)
        self.at(110.0)
        self.p(FadeIn(VGroup(fs_[2], fs_[3]), shift=LEFT * 0.2), rt=0.9)
        self.at(113.5)
        self.p(FadeIn(fs_[4]), rt=0.8)
        self.at(118.2)
        lect = DashedLine(ax.c2p(7, 6.5), ax.c2p(0, 6.5), color=ABSO, stroke_width=3)
        self.p(Create(lect), Indicate(pal, color=ABSO), rt=1.4)
        self.at(123.8)
        val65 = mx(r"6{,}5", ABSO, 28).next_to(ax.c2p(0, 6.5), LEFT, buff=0.12)
        self.p(FadeOut(g_lab[6]), FadeIn(val65, scale=1.4), Flash(ax.c2p(0, 6.5), color=ABSO), rt=1.0)
        res = row(mx(r"\theta_{\mathrm{fus}} \approx 6{,}5\ ^\circ\mathrm{C}", RES, 40), buff=0.1)
        self.sous(res, bloc, x_d, 0.5)
        self.p(Write(res), rt=1.0)
        self.at(126.0)
        self.reponse("La température du palier est 6,5 °C : la température de fusion de ce corps pur est θfus = 6,5 °C.", rt=1.4)

        # ---------------- Question 3 ----------------
        self.at(128.2)
        self.vider(garder=[graph, courbe, croix, pal, pal_l, lect, val65])
        self.set_q("Question 3")
        self.question("3) En utilisant les données, en déduire le nom de ce corps pur.", rt=1.0)
        donnees = [("eau", "0"), ("éthanol", "-114"), ("cyclohexane", "6{,}5"), ("éther", "-116"),
                   ("pentan-3-ol", "-8"), ("benzène", "5{,}5"), ("méthanamide", "2{,}5")]
        lignes = VGroup()
        for nom, v in donnees:
            lignes.add(row(tx(nom, 22, WHITE), mx(v + r"\ ^\circ\mathrm{C}", ABSO, 30), buff=0.3))
        for l in lignes:
            l[1].set_x(0)
        tab = VGroup(*lignes).arrange(DOWN, buff=0.17, aligned_edge=LEFT)
        for l in lignes:
            l[1].align_to(lignes[0], LEFT).shift(RIGHT * 2.4)
        cadre_t = SurroundingRectangle(tab, color="#C0392B", buff=0.25, corner_radius=0.1, stroke_width=2.5)
        tete = tx("Données : températures de fusion", 20, "#FF7777", bold=True).next_to(cadre_t, UP, buff=0.1).align_to(cadre_t, LEFT)
        bloc3 = VGroup(tete, cadre_t, tab)
        self.poser(bloc3, x_d, self.haut() - 0.3)
        self.at(133.2)
        self.p(FadeIn(tete), Create(cadre_t), LaggedStart(*[FadeIn(l, shift=LEFT * 0.15) for l in lignes], lag_ratio=0.12), rt=2.0)
        self.at(136.0)
        self.p(Circumscribe(val65, color=ABSO), rt=1.0)
        self.at(139.0)
        sel = SurroundingRectangle(lignes[2], color=RES, buff=0.08, corner_radius=0.06, stroke_width=3)
        self.p(Create(sel), Indicate(lignes[2][1], color=RES, scale_factor=1.4), rt=1.2)
        presque = tx("≠ 6,5", 18, "#FF7777").next_to(lignes[5], RIGHT, buff=0.25)
        self.p(Indicate(lignes[5], color="#FF7777"), FadeIn(presque), rt=1.0)
        self.at(142.4)
        self.p(Indicate(val65, color=RES, scale_factor=1.5), Indicate(lignes[2], color=RES, scale_factor=1.15), rt=1.0)
        self.at(143.6)
        self.reponse("Sa température de fusion (6,5 °C) est celle du cyclohexane : le corps pur inconnu est le cyclohexane.", rt=1.5)

    # =================================================================
    #  EXERCICE 5 : la photosynthèse (149 s → fin)
    # =================================================================
    def exercice5(self):
        self.at(148.6)
        self.vider()
        self.cur_q = None
        self.set_ex("Exercice 5 – La photosynthèse")
        carton = self.titre_exercice(5, "La photosynthèse", "identifier des gaz par des tests caractéristiques")
        self.p(FadeIn(carton, shift=UP * 0.2), rt=1.0)
        self.at(154.6)
        self.p(FadeOut(carton, shift=UP * 0.3), rt=0.6)

        # --- respiration (nous) / photosynthèse (plante)
        self.at(155.5)
        tete = Circle(radius=0.35, stroke_color=WHITE, stroke_width=3)
        corps = RoundedRectangle(corner_radius=0.3, width=1.1, height=1.2, stroke_color=WHITE, stroke_width=3).next_to(tete, DOWN, buff=0.08)
        humain = VGroup(tete, corps)
        pl = self.plante(1.0)
        sol_ = self.soleil(0.32)
        panneauG = VGroup(tx("Respiration (nous)", 26, WHITE, bold=True), humain).arrange(DOWN, buff=0.4)
        panneauD = VGroup(tx("Photosynthèse (plante, à la lumière)", 26, "#66BB6A", bold=True), pl).arrange(DOWN, buff=0.4)
        panneaux = VGroup(panneauG, panneauD).arrange(RIGHT, buff=2.6)
        self.caser(panneaux, top=2.9, bottom=-1.2)
        sol_.next_to(pl, RIGHT, buff=0.25).align_to(pl, UP)
        sep = DashedLine([0, 2.9, 0], [0, -2.4, 0], color=SOFT, stroke_width=1.5).set_x((panneauG.get_right()[0] + panneauD.get_left()[0]) / 2)
        self.p(FadeIn(panneauG[0]), Create(humain), Create(sep), rt=1.0)
        self.p(FadeIn(panneauD[0]), FadeIn(pl, shift=UP * 0.2), FadeIn(sol_), rt=1.0)

        def flux(mol, a, b, n=3):
            ms = VGroup(*[mol().move_to(a) for _ in range(n)])
            return ms, [m.animate.move_to(b + UP * 0.25 * (k - 1)) for k, m in enumerate(ms)]
        self.at(160.1)
        a_in = humain.get_left() + LEFT * 0.85 + UP * 0.3
        a_out = humain.get_right() + RIGHT * 1.4 + UP * 0.3
        o2_in, anim1 = flux(self.molecule_o2, a_in, tete.get_center())
        l_o2 = VGroup(row(mx(r"\mathrm{O_2}", "#FF4D4D", 34), tx("inspiré", 18, SOFT), buff=0.1)).next_to(a_in, DOWN, buff=0.45)
        self.p(FadeIn(o2_in), FadeIn(l_o2), rt=0.5)
        self.p(*anim1, rt=1.2)
        co2_out = VGroup(*[self.molecule_co2().move_to(tete.get_center()) for _ in range(3)])
        l_co2 = row(mx(r"\mathrm{CO_2}", "#BBBBBB", 34), tx("rejeté", 18, SOFT), buff=0.1).next_to(a_out, DOWN, buff=0.45)
        self.p(FadeOut(o2_in), FadeIn(co2_out), rt=0.4)
        self.p(*[m.animate.move_to(a_out + UP * 0.3 * (k - 1)) for k, m in enumerate(co2_out)], FadeIn(l_co2), rt=1.2)

        self.at(164.2)
        f = pl[2]
        b_in = pl.get_left() + LEFT * 1.1 + UP * 0.6
        b_out = pl.get_right() + RIGHT * 1.1 + UP * 0.9
        co2_in = VGroup(*[self.molecule_co2().move_to(b_in + UP * 0.3 * (k - 1)) for k in range(3)])
        l2 = row(mx(r"\mathrm{CO_2}", "#BBBBBB", 34), tx("absorbé", 18, SOFT), buff=0.1).next_to(co2_in, DOWN, buff=0.3)
        self.p(FadeIn(co2_in), FadeIn(l2), rt=0.5)
        self.p(*[m.animate.move_to(f.get_center()) for m in co2_in], rt=1.3)
        o2_out = VGroup(*[self.molecule_o2().move_to(f.get_center()) for _ in range(3)])
        self.p(FadeOut(co2_in), FadeIn(o2_out), Flash(f.get_center(), color="#FFC107", flash_radius=0.5), rt=0.5)
        l3 = row(mx(r"\mathrm{O_2}", "#FF4D4D", 34), tx("rejeté", 18, SOFT), buff=0.1)
        self.p(*[m.animate.move_to(b_out + UP * 0.3 * (k - 1)) for k, m in enumerate(o2_out)], rt=1.3)
        l3.next_to(o2_out, DOWN, buff=0.3)
        self.p(FadeIn(l3), rt=0.4)
        inverse = tx("La photosynthèse fonctionne « à l'inverse » de la respiration.", 22, ABSO).to_edge(DOWN, buff=0.45)
        self.p(FadeIn(inverse, shift=UP * 0.15), rt=0.8)

        # --- les tests du jour et de la nuit
        self.at(173.4)
        self.vider()
        self.set_q("Question 1")
        self.question("1) Identifier les deux gaz produits par la plante le jour et la nuit, et conclure.", rt=1.0)
        top = self.haut() - 0.15
        W, Hp = 6.3, 2.2
        jour_bg = RoundedRectangle(corner_radius=0.15, width=W, height=Hp, stroke_width=0, fill_color="#5DADE2", fill_opacity=0.28)
        nuit_bg = RoundedRectangle(corner_radius=0.15, width=W, height=Hp, stroke_width=0, fill_color="#0B1640", fill_opacity=0.95)
        fonds = VGroup(jour_bg, nuit_bg).arrange(RIGHT, buff=0.35)
        fonds.shift(UP * (top - 0.4 - fonds.get_top()[1]))
        def scene_plante(bg, astre, titre, c_titre):
            p_ = self.plante(0.62).move_to(bg.get_center() + LEFT * 1.6 + DOWN * 0.15)
            cloche = VGroup(ArcBetweenPoints(p_.get_corner(DL) + LEFT * 0.25 + UP * 1.25, p_.get_corner(DR) + RIGHT * 0.25 + UP * 1.25,
                                             angle=-PI * 0.9, color=WHITE, stroke_width=2),
                            Line(p_.get_corner(DL) + LEFT * 0.25 + UP * 1.25, p_.get_corner(DL) + LEFT * 0.25, color=WHITE, stroke_width=2),
                            Line(p_.get_corner(DR) + RIGHT * 0.25 + UP * 1.25, p_.get_corner(DR) + RIGHT * 0.25, color=WHITE, stroke_width=2))
            astre.move_to(bg.get_top() + DOWN * 0.55 + LEFT * 0.2)
            t = tx(titre, 24, c_titre, bold=True).next_to(bg, UP, buff=0.08)
            return VGroup(p_, cloche, astre, t)
        sj = scene_plante(jour_bg, self.soleil(0.3), "LE JOUR", "#FFE082")
        sn = scene_plante(nuit_bg, self.lune(0.32), "LA NUIT", "#C5CAE9")
        self.p(FadeIn(jour_bg), FadeIn(sj), rt=0.9)
        self.p(FadeIn(nuit_bg), FadeIn(sn), rt=0.9)

        # tests sous chaque panneau
        def test_flamme(x, y):
            b = self.buchette().move_to([x, y, 0])
            return b
        def tube_chaux(x, y):
            tb = self.tube_essai(h=1.2, w=0.38).move_to([x, y, 0])
            liq = self.remplir(tb, tb[1].get_bottom()[1], tb[1].get_bottom()[1] + 0.6, "#DDEEFF", 0.35)
            return VGroup(liq, tb[0])
        yT = fonds.get_bottom()[1] - 1.05
        bj = test_flamme(jour_bg.get_x() - 1.7, yT + 0.1)
        bn = test_flamme(nuit_bg.get_x() - 1.7, yT + 0.1)
        cj = tube_chaux(jour_bg.get_x() + 2.1, yT)
        cn = tube_chaux(nuit_bg.get_x() + 2.1, yT)
        lab_tests = VGroup(tx("bûchette incandescente", 16, SOFT).next_to(bj, DOWN, buff=0.35),
                           tx("eau de chaux", 16, SOFT).next_to(cj, DOWN, buff=0.12),
                           tx("bûchette incandescente", 16, SOFT).next_to(bn, DOWN, buff=0.35),
                           tx("eau de chaux", 16, SOFT).next_to(cn, DOWN, buff=0.12))

        # jour : la flamme se rallume, l'eau de chaux reste limpide
        self.at(179.9)
        gaz_j = VGroup(*[self.molecule_o2(0.08).move_to(sj[1].get_center() + np.array([dx, dy, 0]))
                         for dx, dy in ((-0.3, 0.3), (0.25, 0.45), (0.0, 0.0), (0.35, -0.1))])
        self.p(FadeIn(gaz_j, lag_ratio=0.2), rt=0.8)
        self.p(FadeIn(bj), FadeIn(lab_tests[0]), rt=0.6)
        fl_j = self.flamme().next_to(bj[1], UP, buff=-0.05)
        self.at(183.5)
        self.p(FadeIn(fl_j, scale=0.3), Flash(bj[1], color="#FFB703", flash_radius=0.35), rt=0.8)
        ok1 = tx("se rallume !", 18, "#FFB703", bold=True).next_to(fl_j, RIGHT, buff=0.15)
        self.p(FadeIn(ok1), rt=0.4)
        self.at(186.5)
        self.p(FadeIn(cj), FadeIn(lab_tests[1]), rt=0.6)
        lim = tx("reste limpide", 18, SOFT).next_to(cj, LEFT, buff=0.15)
        self.p(FadeIn(lim), rt=0.5)

        # nuit : rien pour la flamme, l'eau de chaux se trouble
        self.at(190.6)
        gaz_n = VGroup(*[self.molecule_co2(0.065).move_to(sn[1].get_center() + np.array([dx, dy, 0]))
                         for dx, dy in ((-0.3, 0.3), (0.25, 0.45), (0.0, 0.0), (0.35, -0.1))])
        self.p(FadeIn(gaz_n, lag_ratio=0.2), rt=0.8)
        self.p(FadeIn(bn), FadeIn(lab_tests[2]), rt=0.6)
        ko = tx("ne se rallume pas", 18, SOFT).next_to(bn[1], UP, buff=0.15)
        self.p(FadeIn(ko), bn[1].animate.set_color("#5A3A20"), rt=0.7)
        self.at(194.4)
        self.p(FadeIn(cn), FadeIn(lab_tests[3]), rt=0.6)
        trouble = self.remplir(self.tube_essai(h=1.2, w=0.38).move_to(cn[1].get_center()),
                               cn[1].get_bottom()[1] + 0.03, cn[1].get_bottom()[1] + 0.6, "#FFFFFF", 0.85)
        self.p(Transform(cn[0], trouble), rt=1.4)
        prec = tx("précipité blanc !", 18, WHITE, bold=True).next_to(cn, LEFT, buff=0.15)
        self.p(FadeIn(prec), rt=0.5)

        # tests caractéristiques
        self.at(199.0)
        ref = VGroup(
            row(mx(r"\mathrm{O_2}", "#FF4D4D", 34), tx(": rallume une bûchette incandescente", 20), buff=0.15),
            row(mx(r"\mathrm{CO_2}", "#BBBBBB", 34), tx(": trouble l'eau de chaux (précipité blanc)", 20), buff=0.15),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        ref_c = SurroundingRectangle(ref, color=ABSO, buff=0.18, corner_radius=0.1, stroke_width=2)
        ref_t = tx("Tests caractéristiques (cours)", 18, ABSO, bold=True).next_to(ref_c, UP, buff=0.06).align_to(ref_c, LEFT)
        bloc_ref = VGroup(ref_t, ref_c, ref)
        bloc_ref.next_to(VGroup(lab_tests), DOWN, buff=0.3).set_x(0)
        if bloc_ref.get_bottom()[1] < -3.75:
            bloc_ref.shift(UP * (-3.75 - bloc_ref.get_bottom()[1]))
        self.p(FadeIn(ref_t), Create(ref_c), FadeIn(ref, shift=UP * 0.1), rt=1.2)

        # jour = O2
        self.at(204.5)
        self.p(Indicate(ref[0], color="#FF4D4D"), Indicate(fl_j, color="#FFB703"), rt=1.2)
        id_j = VGroup(tx("gaz du jour :", 20, "#FFE082"),
                      row(mx(r"\mathrm{O_2}", "#FF4D4D", 40), tx("dioxygène", 22, "#FF4D4D", bold=True), buff=0.15)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        id_j.move_to(jour_bg.get_center() + UP * 0.55)
        id_j.shift(RIGHT * (jour_bg.get_x() + 0.35 - id_j.get_left()[0]))
        self.at(208.0)
        self.p(FadeIn(id_j, scale=1.2), rt=0.8)
        self.at(221.3)
        self.p(Indicate(ref[1], color=WHITE), Indicate(lim, color=WHITE), rt=1.2)
        self.at(224.6)
        pas = tx("pas de CO₂ : c'est bien O₂", 16, SOFT, w=W / 2 - 0.6).next_to(id_j, DOWN, buff=0.12).align_to(id_j, LEFT)
        self.p(FadeIn(pas), rt=0.6)
        self.at(227.6)
        photo = tx("→ photosynthèse", 20, "#66BB6A", bold=True).next_to(pas, DOWN, buff=0.1).align_to(id_j, LEFT)
        self.p(FadeIn(photo, shift=UP * 0.1), Flash(sj[2], color="#FFC107", flash_radius=0.5), rt=1.0)

        # nuit = CO2 ; la démonstration de la paille
        self.at(235.3)
        self.p(Indicate(prec, color=WHITE), Indicate(ref[1], color=WHITE), rt=1.2)
        self.at(240.1)
        demo_bg = RoundedRectangle(corner_radius=0.12, width=3.8, height=2.6, stroke_color=SOFT, stroke_width=1.5,
                                   fill_color="#1B1F27", fill_opacity=0.97)
        demo_bg.move_to(nuit_bg.get_center() + RIGHT * 0.4 + DOWN * 0.15)
        bec = VGroup(Line(LEFT * 0.6 + UP * 0.5, LEFT * 0.6 + DOWN * 0.6), Line(LEFT * 0.6 + DOWN * 0.6, RIGHT * 0.6 + DOWN * 0.6),
                     Line(RIGHT * 0.6 + DOWN * 0.6, RIGHT * 0.6 + UP * 0.5)).set_stroke(WHITE, 2.5)
        eau_c = Rectangle(width=1.15, height=0.7, stroke_width=0, fill_color="#DDEEFF", fill_opacity=0.35).align_to(bec, DOWN).shift(UP * 0.03)
        paille = Line(UP * 1.0 + RIGHT * 0.25, DOWN * 0.45, color="#FF8A80", stroke_width=6)
        demo = VGroup(eau_c, bec, paille).move_to(demo_bg.get_center() + DOWN * 0.15)
        demo_t = tx("en classe : souffler dans l'eau de chaux", 15, SOFT, w=3.5).next_to(demo_bg.get_top(), DOWN, buff=0.12)
        self.p(FadeIn(demo_bg), FadeIn(demo), FadeIn(demo_t), rt=0.8)
        self.at(244.0)
        bulles = VGroup(*[Circle(radius=0.04 + 0.02 * (k % 3), stroke_color=WHITE, stroke_width=1.5)
                          .move_to(paille.get_end() + RIGHT * 0.05 * ((k % 3) - 1)) for k in range(9)])
        self.p(LaggedStart(*[b.animate.shift(UP * 0.55 + RIGHT * 0.12 * ((k % 3) - 1)).set_opacity(0)
                             for k, b in enumerate(bulles)], lag_ratio=0.2), rt=2.4)
        self.p(eau_c.animate.set_fill("#FFFFFF", opacity=0.85), rt=1.6)
        exp_t = tx("l'air expiré contient du CO₂", 15, WHITE, w=3.5).next_to(demo_bg.get_bottom(), UP, buff=0.12)
        self.at(249.4)
        self.p(FadeIn(exp_t), rt=0.6)
        self.at(253.9)
        self.p(FadeOut(VGroup(demo_bg, demo, demo_t, exp_t, bulles)), rt=0.6)
        id_n = VGroup(tx("gaz de la nuit :", 20, "#C5CAE9"),
                      row(mx(r"\mathrm{CO_2}", "#BBBBBB", 40), tx("dioxyde de carbone", 20, WHITE, bold=True), buff=0.15)
                      ).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        ajuster(id_n, W / 2 - 0.7)
        id_n.move_to(nuit_bg.get_center() + UP * 0.55)
        id_n.shift(RIGHT * (nuit_bg.get_x() + 0.35 - id_n.get_left()[0]))
        resp = tx("→ respiration", 20, "#C5CAE9", bold=True).next_to(id_n, DOWN, buff=0.15).align_to(id_n, LEFT)
        self.p(FadeIn(id_n, scale=1.2), rt=0.8)
        self.p(FadeIn(resp, shift=UP * 0.1), rt=0.6)

        # conclusion
        self.at(258.1)
        self.p(FadeOut(VGroup(bloc_ref, bj, fl_j, ok1, cj, lim, bn, ko, cn, prec, lab_tests)), rt=0.4)
        self.reponse("Jour : le gaz rallume la bûchette → dioxygène O₂ : la plante réalise la photosynthèse.\n"
                     "Nuit : le gaz trouble l'eau de chaux → dioxyde de carbone CO₂ : la plante respire.\n"
                     "Une plante ne rejette donc pas toujours du dioxygène.", rt=1.8, fs=21)
        self.at(262.5)
        nb = tx("(la plante respire aussi le jour, mais la photosynthèse l'emporte)", 16, SOFT)
        nb.next_to(fonds, DOWN, buff=0.12).align_to(fonds, RIGHT)
        self.p(FadeIn(nb), rt=0.6)
        self.pause(1.5)

    # =================================================================
    def conclusion(self):
        self.at(265.6)
        self.vider(rt=0.8)
        self.cur_q = None
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 40, WHITE, bold=True)
        items = VGroup(
            row(etiquette("θ", "#FF8C42").scale(1.4), tx("corps pur : palier de température pendant le changement d'état", 24), buff=0.3),
            row(etiquette("θ", "#FF8C42").scale(1.4), tx("la température du palier identifie l'espèce (θfus = θsolidification)", 24), buff=0.3),
            row(etiquette("O₂", "#FF4D4D").scale(1.4), tx("le dioxygène rallume une bûchette incandescente", 24), buff=0.3),
            row(etiquette("CO₂", "#BBBBBB").scale(1.4), tx("le dioxyde de carbone trouble l'eau de chaux", 24), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        g = VGroup(t, items).arrange(DOWN, buff=0.55)
        ajuster(g, 13.0, 6.6)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=1.8)
        self.pause(3.0)
