from manim import *
import math

# =====================================================================
#  Vidéo de cours – LA TEMPÉRATURE DE CURIE (niveau agrégation), ≈ 4 min.
#  Pour Manim Community (rendu sur GitHub). Vidéo autonome sous-titrée.
#  Prérequis : physique statistique de base (facteur de Boltzmann).
#  Plan : expérience du clou chauffé · ordre/désordre des spins · paramagnétisme
#  (Boltzmann → tanh → loi de Curie) · champ moléculaire de Weiss · résolution
#  graphique et m0(T) · β = 1/2 · Curie-Weiss · Landau et brisure de symétrie ·
#  limites du champ moyen · origine (échange) et ordres de grandeur.
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
BCOL = "#58C4DD"     # champ magnétique
LAMB = "#C77DFF"     # champ moléculaire / couplage

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
        self.phase = ValueTracker(0.0)
        self.titre()
        self.experience()
        self.ordre_desordre()
        self.paramagnetisme()
        self.champ_moleculaire()
        self.resolution_graphique()
        self.curie_weiss()
        self.landau()
        self.limites()
        self.origine()
        self.retenir()

    # =================================================================
    #  Outils
    # =================================================================
    @staticmethod
    def m0(t):
        """Aimantation réduite spontanée du champ moyen : solution > 0 de m = tanh(m / t)."""
        if t >= 1:
            return 0.0
        a, b = 1e-9, 1.0
        for _ in range(60):
            c = (a + b) / 2
            if c - math.tanh(c / t) < 0:
                a = c
            else:
                b = c
        return (a + b) / 2

    def grille_spins(self, nx, ny, pas, centre, ordre, agit, L=0.42, sw=4):
        """Réseau de spins : ordre ∈ [0,1] (1 = tous alignés vers le haut), agit = amplitude d'agitation."""
        rng = np.random.default_rng(11)
        base = rng.uniform(-PI, PI, nx * ny)
        phi = rng.uniform(0, TAU, nx * ny)
        sgn = rng.choice([-1, 1], nx * ny)

        def dessiner():
            o = ordre.get_value() if hasattr(ordre, "get_value") else ordre
            a = agit.get_value() if hasattr(agit, "get_value") else agit
            ph = self.phase.get_value()
            g = VGroup()
            for k in range(nx * ny):
                i, j = k % nx, k // nx
                c = np.array(centre) + np.array([(i - (nx - 1) / 2) * pas, (j - (ny - 1) / 2) * pas, 0])
                ang = PI / 2 + base[k] * (1 - o) + a * math.sin(ph * sgn[k] + phi[k])
                d = np.array([math.cos(ang), math.sin(ang), 0]) * L / 2
                col = interpolate_color(ManimColor(SPIN_D), ManimColor(SPIN), max(0.0, math.sin(ang)))
                g.add(Arrow(c - d, c + d, buff=0, stroke_width=sw, color=col, max_tip_length_to_length_ratio=0.38,
                            max_stroke_width_to_length_ratio=12))
            return g
        return always_redraw(dessiner)

    def tic(self, d, **anims):
        pass

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        t = tx("La température de Curie", 64, WHITE, bold=True)
        s = tx("de l'ordre ferromagnétique au désordre paramagnétique", 28, SOFT).next_to(t, DOWN, buff=0.35)
        fl = VGroup(*[Arrow(DOWN * 0.35, UP * 0.35, buff=0, color=SPIN, stroke_width=5) for _ in range(5)]).arrange(RIGHT, buff=0.35)
        fl2 = VGroup(*[Arrow(DOWN * 0.35, UP * 0.35, buff=0, color=SPIN_D, stroke_width=5).rotate(a)
                       for a in (2.1, -0.7, 3.0, 1.2, -2.4)]).arrange(RIGHT, buff=0.35)
        g = VGroup(fl, MathTex(r"\longrightarrow", color=TCOL, font_size=50), fl2).arrange(RIGHT, buff=0.5).next_to(s, DOWN, buff=0.6)
        self.p(Write(t), rt=1.3)
        self.p(FadeIn(s, shift=UP * 0.2), LaggedStart(*[GrowArrow(a) for a in fl], lag_ratio=0.1), rt=1.2)
        self.p(FadeIn(g[1]), LaggedStart(*[GrowArrow(a) for a in fl2], lag_ratio=0.1), rt=1.0)
        self.pause(1.2)
        self.hdr_ex = tx("La température de Curie", 22, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(t, self.hdr_ex), FadeOut(s), FadeOut(g), rt=0.8)

    # =================================================================
    #  EXPÉRIENCE INTRODUCTIVE : le clou chauffé
    # =================================================================
    def experience(self):
        self.set_q("Une expérience")
        pivot = np.array([0.6, 2.7, 0])
        fil = Line(pivot, pivot + DOWN * 3.2, color=SOFT, stroke_width=2)
        tete = Rectangle(width=0.32, height=0.07, stroke_width=0, fill_color="#9AA3AD", fill_opacity=1)
        tige = Rectangle(width=0.1, height=0.9, stroke_width=0, fill_color="#9AA3AD", fill_opacity=1).next_to(tete, DOWN, buff=0)
        pointe = Polygon(tige.get_corner(DL), tige.get_corner(DR), tige.get_bottom() + DOWN * 0.16, stroke_width=0,
                         fill_color="#9AA3AD", fill_opacity=1)
        clou = VGroup(tete, tige, pointe).next_to(fil.get_end(), DOWN, buff=0)
        pendule = VGroup(fil, clou)
        support = Line(pivot + LEFT * 0.6, pivot + RIGHT * 0.6, color=WHITE, stroke_width=4)
        # aimant en U
        a_n = Rectangle(width=0.5, height=1.1, stroke_width=0, fill_color="#E53935", fill_opacity=1)
        a_s = Rectangle(width=0.5, height=1.1, stroke_width=0, fill_color="#1E88E5", fill_opacity=1).next_to(a_n, DOWN, buff=0.5)
        dos = Rectangle(width=0.6, height=a_n.height * 2 + 0.5, stroke_width=0, fill_color="#B0B0B0", fill_opacity=1).next_to(VGroup(a_n, a_s), RIGHT, buff=0)
        nl = Text("N", font_size=24, color=WHITE, weight=BOLD).move_to(a_n)
        sl = Text("S", font_size=24, color=WHITE, weight=BOLD).move_to(a_s)
        aimant = VGroup(a_n, a_s, dos, nl, sl).move_to([3.4, -1.05, 0])
        lab_a = tx("aimant", 20, SOFT).next_to(aimant, DOWN, buff=0.15)
        lab_c = tx("clou en fer", 20, "#9AA3AD").next_to(clou, LEFT, buff=0.3)
        self.p(Create(support), Create(fil), FadeIn(clou), FadeIn(aimant), FadeIn(lab_a), FadeIn(lab_c), rt=1.2)
        angle = 0.42
        self.p(Rotate(pendule, angle, about_point=pivot), FadeOut(lab_c), rt=1.0, rate_func=rush_into)
        self.dire("Un clou en fer suspendu est attiré par un aimant.", lire=1.4)
        # chauffage
        flamme = VGroup(Ellipse(width=0.45, height=0.9, stroke_width=0, fill_color="#FF8F00", fill_opacity=0.95),
                        Ellipse(width=0.22, height=0.45, stroke_width=0, fill_color="#FFF59D", fill_opacity=1).shift(DOWN * 0.15))
        bec = Rectangle(width=0.3, height=0.8, stroke_width=0, fill_color="#555555", fill_opacity=1)
        bunsen = VGroup(bec, flamme.next_to(bec, UP, buff=0)).move_to(clou.get_center() + DOWN * 1.2)
        self.p(FadeIn(bunsen, shift=UP * 0.3), rt=0.7)
        self.dire("On le chauffe : il devient rouge…", lire=0.2)
        self.p(clou.animate.set_fill("#FF6A00", opacity=1), rt=2.2)
        self.p(Rotate(pendule, -angle, about_point=pivot), FadeOut(bunsen, shift=DOWN * 0.3), rt=1.1, rate_func=smooth)
        self.p(Rotate(pendule, -0.08, about_point=pivot), rt=0.4, rate_func=there_and_back)
        self.dire(["… et vers", r"$770\ ^\circ\mathrm{C}", "il n'est plus attiré : le fer a perdu son ferromagnétisme."], c=TCOL, lire=2.0)
        self.dire("En refroidissant, il est de nouveau attiré : le phénomène est réversible.", lire=0.2)
        self.p(clou.animate.set_fill("#9AA3AD", opacity=1), rt=1.8)
        self.p(Rotate(pendule, angle, about_point=pivot), rt=0.8, rate_func=rush_into)
        self.pause(0.8)
        tc = row(tx("Cette température critique est la", 26), tx("température de Curie", 26, TCOL, bold=True),
                 mx(r"T_C", TCOL, 40), buff=0.15)
        self.dire("Cette température critique est la température de Curie.", c=TCOL, lire=1.6)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  ORDRE / DÉSORDRE (réseau de spins)
    # =================================================================
    def ordre_desordre(self):
        self.set_q("Ordre et désordre")
        tt = ValueTracker(0.15)              # T / T_C
        ordre = ValueTracker(self.m0(0.15))
        agit = ValueTracker(0.12)
        reseau = self.grille_spins(9, 6, 0.62, [-2.4, 0.15, 0], ordre, agit)
        cadre = SurroundingRectangle(reseau, color=SOFT, buff=0.15, corner_radius=0.1, stroke_width=1.5)
        # jauge de température et d'aimantation
        def jauges():
            t = tt.get_value()
            barT = Rectangle(width=0.35, height=max(0.02, 3.2 * min(t, 1.6) / 1.6), stroke_width=0, fill_color=TCOL, fill_opacity=0.9)
            barT.move_to([3.0, -1.5, 0], aligned_edge=DOWN)
            m = self.m0(t)
            barM = Rectangle(width=0.35, height=max(0.02, 3.2 * m), stroke_width=0, fill_color=MCOL, fill_opacity=0.9)
            barM.move_to([4.6, -1.5, 0], aligned_edge=DOWN)
            ligneTc = DashedLine([2.6, -1.5 + 3.2 / 1.6, 0], [3.4, -1.5 + 3.2 / 1.6, 0], color=WHITE, stroke_width=2)
            return VGroup(barT, barM, ligneTc)
        cadres_j = VGroup(Rectangle(width=0.45, height=3.25).move_to([3.0, 0.1, 0]),
                          Rectangle(width=0.45, height=3.25).move_to([4.6, 0.1, 0])).set_stroke(SOFT, 1.5)
        lj = VGroup(mx("T", TCOL, 40).next_to(cadres_j[0], DOWN, buff=0.15), mx("M", MCOL, 40).next_to(cadres_j[1], DOWN, buff=0.15),
                    mx("T_C", WHITE, 30).next_to([2.6, -1.5 + 2.0, 0], LEFT, buff=0.1))
        J = always_redraw(jauges)
        self.p(Create(cadre), FadeIn(reseau), Create(cadres_j), FadeIn(lj), FadeIn(J), rt=1.0)
        self.dire("Microscopiquement : chaque atome de fer porte un moment magnétique (un « spin »).", lire=2.0)
        self.dire(["À basse température, ils s'alignent tous : aimantation spontanée", r"$\vec M \neq \vec 0", "sans champ appliqué."],
                  c=MCOL, lire=0.2)
        self.p(self.phase.animate.set_value(6), rt=2.4, rate_func=linear)
        # on chauffe
        self.dire("Quand T augmente, l'agitation thermique désordonne les spins…", c=TCOL, lire=0.2)
        self.p(tt.animate.set_value(0.95), ordre.animate.set_value(self.m0(0.95)), agit.animate.set_value(0.6),
               self.phase.animate.set_value(16), rt=4.0, rate_func=linear)
        self.p(tt.animate.set_value(1.0), ordre.animate.set_value(0.0), agit.animate.set_value(0.9),
               self.phase.animate.set_value(19), rt=1.2, rate_func=linear)
        self.dire(["… et au-delà de", r"$T_C$", ", l'ordre a disparu :", r"$\vec M = \vec 0$", ". Le fer est devenu paramagnétique."],
                  c=TCOL, lire=0.2)
        self.p(tt.animate.set_value(1.5), agit.animate.set_value(1.2), self.phase.animate.set_value(26), rt=3.0, rate_func=linear)
        self.dire("Questions : pourquoi un ordre spontané ? Pourquoi disparaît-il brutalement à une température précise ?", c=ABSO, lire=0.2)
        self.p(self.phase.animate.set_value(32), rt=3.2, rate_func=linear)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  1. PARAMAGNÉTISME : des spins indépendants
    # =================================================================
    def paramagnetisme(self):
        self.set_q("1. Spins indépendants")
        # deux niveaux d'énergie
        x = ValueTracker(0.4)                     # x = μB / (k_B T)
        haut_n = Line(LEFT * 1.3, RIGHT * 1.3, color=WHITE, stroke_width=3).move_to([-4.2, 1.2, 0])
        bas_n = Line(LEFT * 1.3, RIGHT * 1.3, color=WHITE, stroke_width=3).move_to([-4.2, -0.6, 0])
        e_h = mx(r"+\mu B", WHITE, 34).next_to(haut_n, LEFT, buff=0.2)
        e_b = mx(r"-\mu B", WHITE, 34).next_to(bas_n, LEFT, buff=0.2)
        s_h = Arrow(DOWN * 0.25, UP * 0.25, buff=0, color=SPIN_D, stroke_width=5).rotate(PI).next_to(haut_n, RIGHT, buff=0.25)
        s_b = Arrow(DOWN * 0.25, UP * 0.25, buff=0, color=SPIN, stroke_width=5).next_to(bas_n, RIGHT, buff=0.25)
        champ = VGroup(Arrow(DOWN * 0.6, UP * 0.6, buff=0, color=BCOL, stroke_width=6), mx(r"\vec B", BCOL, 36))
        champ[1].next_to(champ[0], RIGHT, buff=0.1)
        champ.move_to([-1.6, 0.3, 0])
        def populations():
            v = x.get_value()
            pb = math.exp(v) / (2 * math.cosh(v))
            n = 20
            nb = int(round(n * pb)); nh = n - nb
            g = VGroup()
            for k in range(nb):
                g.add(Dot(bas_n.get_left() + RIGHT * (0.15 + 0.125 * k) + UP * 0.14, radius=0.05, color=SPIN))
            for k in range(nh):
                g.add(Dot(haut_n.get_left() + RIGHT * (0.15 + 0.125 * k) + UP * 0.14, radius=0.05, color=SPIN_D))
            return g
        pops = always_redraw(populations)
        self.p(Create(haut_n), Create(bas_n), FadeIn(e_h), FadeIn(e_b), GrowArrow(s_h), GrowArrow(s_b), FadeIn(champ), rt=1.2)
        self.dire(r"Spin 1/2 de moment $\mu$ dans un champ $B$ : deux niveaux d'énergie $\mp \mu B$.", lire=1.8)
        self.add(pops)
        boltz = mx(r"p_\pm = \frac{e^{\pm \mu B / k_B T}}{2\cosh(\mu B / k_B T)}", WHITE, 40).move_to([2.6, 1.6, 0])
        self.p(Write(boltz), rt=1.2)
        self.dire("Populations données par le facteur de Boltzmann (statistique à l'équilibre).", lire=1.4)
        self.dire("Champ fort ou T faible : le niveau bas l'emporte…", c=SPIN, lire=0.2)
        self.p(x.animate.set_value(2.5), rt=1.8)
        self.dire("… T élevée : les deux niveaux s'équilibrent.", c=TCOL, lire=0.2)
        self.p(x.animate.set_value(0.05), rt=1.8)
        moy = mx(r"\langle \mu_z \rangle = \mu\,p_+ - \mu\,p_- = \mu \tanh\!\left(\frac{\mu B}{k_B T}\right)", WHITE, 38)
        mag = mx(r"M = N\mu \tanh\!\left(\frac{\mu B}{k_B T}\right)", MCOL, 46)
        VGroup(moy, mag).arrange(DOWN, buff=0.45).next_to(boltz, DOWN, buff=0.5)
        self.p(Write(moy), rt=1.4)
        self.p(TransformMatchingShapes(moy.copy(), mag), rt=1.2)
        cad = SurroundingRectangle(mag, color=BOX, buff=0.15, corner_radius=0.08)
        self.p(Create(cad), rt=0.5)
        self.dire(r"$N$ moments par unité de volume : aimantation $M$.", c=MCOL, lire=1.2)
        self.vider(garder=[cad, mag])
        # courbe tanh et loi de Curie
        self.p(VGroup(mag, cad).animate.scale(0.8).to_edge(UP, buff=1.0).set_x(-3.3), rt=0.7)
        ax = Axes(x_range=[0, 4, 1], y_range=[0, 1.15, 0.5], x_length=6.0, y_length=3.2, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([-2.6, -1.1, 0])
        lx = mx(r"\frac{\mu B}{k_B T}", SOFT, 30).next_to(ax.c2p(4, 0), RIGHT, buff=0.15)
        ly = mx(r"\frac{M}{N\mu}", MCOL, 30).next_to(ax.c2p(0, 1.15), UP, buff=0.1)
        un = mx("1", SOFT, 26).next_to(ax.c2p(0, 1), LEFT, buff=0.12)
        sat = DashedLine(ax.c2p(0, 1), ax.c2p(4, 1), color=SOFT, stroke_width=1.5)
        courbe = ax.plot(lambda u: math.tanh(u), x_range=[0, 4], color=MCOL, stroke_width=4)
        lin = ax.plot(lambda u: u, x_range=[0, 1.1], color=TCOL, stroke_width=3)
        self.p(Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(un), Create(sat), rt=1.0)
        self.p(Create(courbe), rt=1.4)
        self.dire("Saturation à basse température, régime linéaire à haute température.", lire=1.4)
        self.p(Create(lin), rt=0.8)
        curie = VGroup(mx(r"\frac{\mu B}{k_B T} \ll 1 \;\Rightarrow\; M \simeq \frac{N\mu^2}{k_B T}\,B", WHITE, 38),
                       row(tx("loi de Curie :", 24, TCOL), mx(r"\chi = \frac{C}{T}", TCOL, 46), buff=0.2)).arrange(DOWN, buff=0.4)
        curie.move_to([3.6, -0.6, 0])
        self.p(Write(curie[0]), rt=1.4)
        self.p(Write(curie[1]), rt=1.0)
        self.p(Create(SurroundingRectangle(curie[1], color=BOX, buff=0.15, corner_radius=0.08)), rt=0.5)
        self.dire(["(avec", r"$B = \mu_0 H$", "et", r"$M = \chi H$", ", la constante de Curie vaut", r"$C = \mu_0 N \mu^2 / k_B$", ")"],
                  c=SOFT, lire=2.0)
        self.dire(["Mais sans champ :", r"$M = 0$", "à toute température. Des spins indépendants ne s'ordonnent jamais seuls !"],
                  c=ABSO, lire=2.6)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  2. CHAMP MOLÉCULAIRE DE WEISS
    # =================================================================
    def champ_moleculaire(self):
        self.set_q("2. Champ moléculaire")
        # un spin et ses voisins -> remplacés par un champ moyen
        pas = 0.75
        c0 = np.array([-3.9, 0.35, 0])
        voisins = VGroup()
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1), (-1, 1), (1, -1)):
            ang = PI / 2 + 0.35 * math.sin(3 * dx + 5 * dy)
            d = np.array([math.cos(ang), math.sin(ang), 0]) * 0.22
            p = c0 + np.array([dx * pas, dy * pas, 0])
            voisins.add(Arrow(p - d, p + d, buff=0, color=SPIN_D, stroke_width=4, max_tip_length_to_length_ratio=0.38))
        central = Arrow(c0 + DOWN * 0.24, c0 + UP * 0.24, buff=0, color=SPIN, stroke_width=6, max_tip_length_to_length_ratio=0.38)
        halo = Circle(radius=0.36, color=ABSO, stroke_width=2).move_to(c0)
        self.p(FadeIn(voisins), GrowArrow(central), Create(halo), rt=1.0)
        self.dire("Pierre Weiss (1907) : chaque spin interagit avec ses voisins, qui tendent à l'aligner sur eux.", lire=2.0)
        moyen = VGroup(Arrow(c0 + LEFT * 0.75 + DOWN * 0.7, c0 + LEFT * 0.75 + UP * 0.7, buff=0, color=LAMB, stroke_width=7),
                       mx(r"\vec B_m = \lambda \vec M", LAMB, 36))
        moyen[1].next_to(moyen[0], LEFT, buff=0.15)
        self.p(FadeOut(voisins), FadeIn(moyen, shift=RIGHT * 0.2), rt=1.2)
        self.dire(r"Champ moyen : on remplace les voisins par un champ effectif proportionnel à $M$.", c=LAMB, lire=2.2)
        eq1 = mx(r"B \;\longrightarrow\; B + \lambda M", WHITE, 46)
        eq2 = mx(r"M = N\mu \tanh\!\left(\frac{\mu\,(B + \lambda M)}{k_B T}\right)", MCOL, 46)
        eq3 = mx(r"m = \tanh\!\left(\frac{T_C}{T}\, m\right)", MCOL, 54)
        def_m = row(tx("sans champ, avec", 22, SOFT), mx(r"m = \frac{M}{N\mu}", WHITE, 38), tx("et", 22, SOFT),
                    mx(r"T_C = \frac{\lambda N \mu^2}{k_B}", TCOL, 40), buff=0.2)
        col = VGroup(eq1, eq2, def_m, eq3).arrange(DOWN, buff=0.5).move_to([2.2, 0.0, 0])
        ajuster(col, 8.0)
        col.move_to([2.4, -0.1, 0])
        self.p(Write(eq1), rt=1.0)
        self.p(Write(eq2), rt=1.4)
        self.dire(r"$M$ apparaît des deux côtés : c'est une équation d'auto-cohérence.", c=ABSO, lire=1.6)
        self.p(FadeIn(def_m, shift=UP * 0.15), rt=1.0)
        self.p(TransformMatchingShapes(eq2.copy(), eq3), rt=1.4)
        cad = SurroundingRectangle(eq3, color=BOX, buff=0.2, corner_radius=0.1)
        self.p(Create(cad), Flash(eq3, color=BOX, flash_radius=1.6), rt=0.8)
        self.dire(r"Une seule échelle de température émerge : $T_C$, fixée par la force du couplage $\lambda$.", c=TCOL, lire=2.0)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  RÉSOLUTION GRAPHIQUE  +  m0(T) tracée en direct
    # =================================================================
    def resolution_graphique(self):
        self.set_q("Résolution graphique")
        eq = mx(r"m = \tanh\!\left(\frac{T_C}{T}\, m\right)", MCOL, 40).to_edge(UP, buff=0.85).set_x(-3.2)
        self.add(eq)
        ax = Axes(x_range=[-1.6, 1.6, 0.5], y_range=[-1.3, 1.3, 0.5], x_length=6.0, y_length=4.2, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([-3.3, -0.45, 0])
        nm = mx("m", SOFT, 32).next_to(ax.c2p(1.6, 0), DOWN, buff=0.12)
        un = VGroup(mx("1", SOFT, 24).next_to(ax.c2p(1, 0), DOWN, buff=0.1), mx("-1", SOFT, 24).next_to(ax.c2p(-1, 0), DOWN, buff=0.1))
        bis = ax.plot(lambda u: u, x_range=[-1.25, 1.25], color=WHITE, stroke_width=3)
        bis_l = mx("y = m", WHITE, 28).move_to(ax.c2p(-0.9, 1.05))
        tt = ValueTracker(1.6)
        th = always_redraw(lambda: ax.plot(lambda u: math.tanh(u / tt.get_value()), x_range=[-1.55, 1.55], color=MCOL, stroke_width=4))
        th_l = mx(r"y = \tanh\!\left(\tfrac{T_C}{T} m\right)", MCOL, 28).move_to(ax.c2p(-0.85, 0.6))
        def sols():
            t = tt.get_value()
            m = self.m0(t)
            g = VGroup(Dot(ax.c2p(0, 0), radius=0.08, color=WHITE if m > 0.01 else ABSO))
            if m > 0.01:
                g.add(Dot(ax.c2p(m, m), radius=0.09, color=ABSO), Dot(ax.c2p(-m, -m), radius=0.09, color=ABSO))
            return g
        S = always_redraw(sols)
        # m0(T) à droite
        ax2 = Axes(x_range=[0, 1.6, 0.5], y_range=[0, 1.15, 0.5], x_length=4.6, y_length=2.5, tips=True,
                   axis_config={"color": SOFT, "stroke_width": 2}).move_to([3.9, 0.55, 0])
        l2 = VGroup(mx(r"T/T_C", TCOL, 28).next_to(ax2.c2p(1.6, 0), DOWN, buff=0.12),
                    mx(r"m_0", MCOL, 32).next_to(ax2.c2p(0, 1.15), LEFT, buff=0.12),
                    mx("1", SOFT, 24).next_to(ax2.c2p(1, 0), DOWN, buff=0.1),
                    mx("1", SOFT, 24).next_to(ax2.c2p(0, 1), LEFT, buff=0.1))
        trace = always_redraw(lambda: VMobject(stroke_color=MCOL, stroke_width=4).set_points_as_corners(
            [ax2.c2p(t, self.m0(t)) for t in np.linspace(1.6, max(tt.get_value(), 0.05), 80)] if tt.get_value() < 1.599
            else [ax2.c2p(1.6, 0), ax2.c2p(1.599, 0)]))
        pt = always_redraw(lambda: Dot(ax2.c2p(tt.get_value(), self.m0(tt.get_value())), radius=0.08, color=ABSO))
        t_lab = always_redraw(lambda: mx(r"T = %s\,T_C" % ("%.2f" % (round(tt.get_value() * 20) / 20)).replace(".", "{,}"), TCOL, 34)
                              .move_to([3.9, 2.3, 0]))
        self.p(Create(ax), FadeIn(nm), FadeIn(un), Create(bis), FadeIn(bis_l), FadeIn(th_l), rt=1.0)
        self.add(th)
        self.p(FadeIn(S), Create(ax2), FadeIn(l2), FadeIn(t_lab), rt=1.0)
        self.add(trace, pt)
        self.dire(r"Les solutions sont les intersections de la droite $y = m$ et de la courbe $y = \tanh(T_C\, m / T)$.", lire=2.4)
        self.dire(r"$T > T_C$ : pente à l'origine $T_C/T < 1$, seule solution $m = 0$ : paramagnétique.", c=TCOL, lire=0.4)
        self.p(tt.animate.set_value(1.05), rt=2.6, rate_func=linear)
        self.dire(r"$T = T_C$ : la pente à l'origine vaut 1… deux nouvelles solutions $\pm m_0$ naissent.", c=ABSO, lire=0.3)
        self.p(tt.animate.set_value(0.98), rt=1.6, rate_func=linear)
        self.p(tt.animate.set_value(0.6), rt=3.4, rate_func=linear)
        self.dire(r"La solution $m = 0$ devient instable : le système choisit $+m_0$ ou $-m_0$.", c=MCOL, lire=0.4)
        self.p(tt.animate.set_value(0.08), rt=3.2, rate_func=linear)
        self.dire(r"À $T \to 0$, $m_0 \to 1$ : tous les spins sont alignés. C'est l'allure observée expérimentalement.", lire=2.4)
        # voisinage de T_C
        self.p(tt.animate.set_value(0.9), rt=1.2)
        dvt = VGroup(mx(r"\tanh u \simeq u - \frac{u^3}{3}", WHITE, 32),
                     mx(r"m_0 \simeq \sqrt{3}\left(1 - \frac{T}{T_C}\right)^{1/2}", MCOL, 36),
                     row(tx("exposant critique", 20, SOFT), mx(r"\beta = \tfrac{1}{2}", ABSO, 38), buff=0.2)).arrange(DOWN, buff=0.18)
        haut_d = ax2.get_bottom()[1] - 0.55
        ajuster(dvt, 6.0, haut_d - (-2.6))
        dvt.next_to([3.9, haut_d, 0], DOWN, buff=0)
        zone = Circle(radius=0.35, color=ABSO, stroke_width=3).move_to(ax2.c2p(1, 0.15))
        self.p(Create(zone), rt=0.5)
        self.dire(r"Près de $T_C$, $m_0$ est petit : on développe la tangente hyperbolique.", lire=0.3)
        self.p(Write(dvt[0]), rt=1.0)
        self.p(Write(dvt[1]), rt=1.2)
        self.p(FadeIn(dvt[2], scale=1.2), rt=0.8)
        self.dire("L'aimantation s'annule continûment, avec une tangente verticale : transition du second ordre.", c=ABSO, lire=2.4)
        for m in (th, S, trace, pt, t_lab):
            m.clear_updaters()
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  AU-DESSUS DE T_C : CURIE-WEISS
    # =================================================================
    def curie_weiss(self):
        self.set_q("Curie-Weiss")
        etapes = VGroup(
            txm(r"$T > T_C$, petit champ $B$ : $m$ petit, on linéarise", 22, SOFT),
            mx(r"m \simeq \frac{\mu B}{k_B T} + \frac{T_C}{T}\, m", WHITE, 42),
            mx(r"M = \frac{N\mu^2}{k_B\,(T - T_C)}\, B", MCOL, 42),
            row(tx("loi de Curie-Weiss :", 24, TCOL), mx(r"\chi = \frac{C}{T - T_C}", TCOL, 52), buff=0.2),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT)
        etapes.move_to([-3.3, 0.0, 0])
        ajuster(etapes, 6.3)
        etapes.move_to([-3.4, -0.1, 0])
        self.p(FadeIn(etapes[0]), rt=0.6)
        self.p(Write(etapes[1]), rt=1.2)
        self.p(TransformMatchingShapes(etapes[1].copy(), etapes[2]), rt=1.3)
        self.p(Write(etapes[3]), rt=1.0)
        cad = SurroundingRectangle(etapes[3], color=BOX, buff=0.15, corner_radius=0.08)
        self.p(Create(cad), rt=0.5)
        self.dire(r"La susceptibilité diverge à l'approche de $T_C$ : les spins répondent collectivement.", c=TCOL, lire=2.0)
        ax = Axes(x_range=[0, 2.2, 0.5], y_range=[0, 2.2, 0.5], x_length=4.6, y_length=3.8, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([3.6, -0.4, 0])
        l = VGroup(mx("T", SOFT, 30).next_to(ax.c2p(2.2, 0), DOWN, buff=0.12),
                   mx(r"1/\chi", TCOL, 30).next_to(ax.c2p(0, 2.2), LEFT, buff=0.12),
                   mx("T_C", TCOL, 28).next_to(ax.c2p(1, 0), DOWN, buff=0.12))
        cw = Line(ax.c2p(1, 0), ax.c2p(2.15, 2.15 - 1.0), color=TCOL, stroke_width=4)
        cu = DashedLine(ax.c2p(0, 0), ax.c2p(2.15, 2.15), color=SOFT, stroke_width=2.5)
        lcw = tx("Curie-Weiss", 20, TCOL).move_to(ax.c2p(1.7, 0.22))
        lcu = tx("Curie (spins libres)", 18, SOFT)
        lcu.move_to(ax.c2p(0.05, 2.0)).align_to(ax.c2p(0.08, 0), LEFT)
        self.p(Create(ax), FadeIn(l), rt=0.9)
        self.p(Create(cu), FadeIn(lcu), rt=0.8)
        self.p(Create(cw), FadeIn(lcw), rt=1.0)
        self.p(Flash(ax.c2p(1, 0), color=TCOL, flash_radius=0.3), rt=0.6)
        self.dire(r"Expérimentalement, $1/\chi$ est une droite au-dessus de $T_C$ : on mesure ainsi $T_C$ ($\gamma = 1$ en champ moyen).",
                  lire=2.8)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  3. LECTURE DE LANDAU : brisure de symétrie
    # =================================================================
    def landau(self):
        self.set_q("3. Landau")
        F = mx(r"F(m) = F_0 + a\,(T - T_C)\, m^2 + b\, m^4", WHITE, 44).to_edge(UP, buff=0.85).set_x(-1.5)
        ab = tx("(a > 0, b > 0)", 20, SOFT).next_to(F, RIGHT, buff=0.3)
        self.p(Write(F), FadeIn(ab), rt=1.4)
        self.dire(r"Près de $T_C$, $m$ est petit : on développe l'énergie libre en puissances paires de $m$ (symétrie $m \to -m$).", lire=2.6)
        ax = Axes(x_range=[-1.3, 1.3, 0.5], y_range=[-0.35, 0.6, 0.25], x_length=6.5, y_length=3.6, tips=True,
                  axis_config={"color": SOFT, "stroke_width": 2}).move_to([-2.2, -0.75, 0])
        lab = VGroup(mx("m", SOFT, 30).next_to(ax.c2p(1.3, 0), DOWN, buff=0.12),
                     mx("F - F_0", SOFT, 28).next_to(ax.c2p(0, 0.6), LEFT, buff=0.12))
        r = ValueTracker(0.6)                       # (T - T_C) en unités réduites
        fonc = lambda u, rr: 0.5 * rr * u ** 2 + 0.5 * u ** 4
        def umax(rr):
            x2 = -0.5 * rr + math.sqrt(0.25 * rr * rr + 1.16)     # f(u) = 0,58 (haut de l'axe)
            return min(math.sqrt(x2), 1.25)
        courbe = always_redraw(lambda: ax.plot(lambda u: fonc(u, r.get_value()),
                                               x_range=[-umax(r.get_value()), umax(r.get_value())], color=LAMB, stroke_width=4))
        def mmin():
            rr = r.get_value()
            return math.sqrt(-rr / 2) if rr < 0 else 0.0
        cote = ValueTracker(1.0)
        bille = always_redraw(lambda: Dot(ax.c2p(cote.get_value() * mmin(), fonc(cote.get_value() * mmin(), r.get_value())) + UP * 0.12,
                                          radius=0.11, color=ABSO))
        t_l = always_redraw(lambda: mx(r"T > T_C" if r.get_value() > 0.01 else (r"T = T_C" if r.get_value() > -0.01 else r"T < T_C"),
                                       TCOL, 44).move_to([3.6, 1.4, 0]))
        self.p(Create(ax), FadeIn(lab), rt=0.8)
        self.add(courbe, bille, t_l)
        self.dire(r"$T > T_C$ : un seul minimum, en $m = 0$ (phase désordonnée).", c=TCOL, lire=1.6)
        self.p(r.animate.set_value(0.0), rt=2.0)
        self.dire(r"$T = T_C$ : le fond du puits s'aplatit (fluctuations « gratuites »).", c=TCOL, lire=1.2)
        self.p(r.animate.set_value(-1.1), rt=2.4)
        self.dire(r"$T < T_C$ : double puits ! Le système tombe dans l'un des minima $\pm m_0$ : brisure spontanée de symétrie.",
                  c=MCOL, lire=1.4)
        res = VGroup(mx(r"\frac{\partial F}{\partial m} = 0 \;\Rightarrow\; m_0^2 = \frac{a\,(T_C - T)}{2b}", WHITE, 36),
                     row(tx("on retrouve", 20, SOFT), mx(r"\beta = \tfrac12", ABSO, 36), buff=0.15)).arrange(DOWN, buff=0.3)
        res.move_to([3.7, -0.4, 0])
        ajuster(res, 6.2)
        res.move_to([3.7, -0.4, 0])
        self.p(Write(res[0]), rt=1.4)
        self.p(FadeIn(res[1]), rt=0.6)
        self.dire("Les deux minima sont équivalents : le choix dépend d'un champ infime ou des conditions locales (domaines de Weiss).",
                  lire=2.6)
        self.p(cote.animate.set_value(-1.0), rt=1.4)
        for m in (courbe, bille, t_l):
            m.clear_updaters()
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  LIMITES DU CHAMP MOYEN
    # =================================================================
    def limites(self):
        self.set_q("Limites du champ moyen")
        tab = tableau([[r"\text{exposant}", r"\text{champ moyen}", r"\text{mesures (3D)}"],
                       [r"\beta\ :\ m_0 \propto (T_C - T)^{\beta}", r"1/2", r"\approx 0{,}33 - 0{,}37"],
                       [r"\gamma\ :\ \chi \propto (T - T_C)^{-\gamma}", r"1", r"\approx 1{,}24 - 1{,}39"]], fs=32)
        for c in tab[0][:3]:
            c.set_color(SOFT)
        tab[0][4].set_color(MCOL); tab[0][7].set_color(MCOL)
        tab[0][5].set_color(RES); tab[0][8].set_color(RES)
        tab.move_to(UP * 0.6)
        ajuster(tab, 12.0)
        self.p(Create(tab[1]), LaggedStart(*[FadeIn(c) for c in tab[0]], lag_ratio=0.08), rt=1.8)
        self.dire(r"Le champ moyen prévoit bien l'existence de $T_C$, mais pas le comportement exact près de $T_C$.", lire=2.0)
        self.p(Circumscribe(VGroup(tab[0][4], tab[0][5]), color=ABSO), rt=1.0)
        self.p(Circumscribe(VGroup(tab[0][7], tab[0][8]), color=ABSO), rt=1.0)
        expl = VGroup(tx("Il remplace les voisins par leur moyenne : il néglige les FLUCTUATIONS,", 24, WHITE),
                      txm(r"qui deviennent dominantes près de $T_C$ (corrélations à longue portée).", 24, WHITE),
                      tx("Traitement exact : modèle d'Ising 2D (Onsager), groupe de renormalisation.", 22, SOFT)
                      ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.6)
        ajuster(expl, 12.6)
        self.p(FadeIn(expl[0:2], shift=UP * 0.15), rt=1.0)
        self.pause(2.4)
        self.p(FadeIn(expl[2]), rt=0.8)
        self.dire("Les exposants critiques sont universels : ils ne dépendent que de la dimension et de la symétrie du paramètre d'ordre.",
                  c=ABSO, lire=2.6)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  4. ORIGINE DU CHAMP MOLÉCULAIRE
    # =================================================================
    def origine(self):
        self.set_q("4. Origine de λ")
        q = tx("Quelle interaction peut aligner les spins jusqu'à 1043 K dans le fer ?", 28, ABSO)
        q.to_edge(UP, buff=0.85)
        self.p(FadeIn(q, shift=DOWN * 0.15), rt=1.0)
        oms = VGroup(
            row(tx("Champ moléculaire équivalent :", 22, LAMB),
                mx(r"B_m \sim \frac{k_B T_C}{\mu_B} \approx 1{,}5\times10^{3}\ \mathrm{T}", LAMB, 40), buff=0.2),
            tx("(les plus forts champs continus de laboratoire : quelques dizaines de teslas)", 18, SOFT),
            row(tx("Interaction dipolaire entre moments voisins :", 22, BCOL),
                mx(r"k_B T \sim \frac{\mu_0 \mu_B^2}{4\pi a^3} \;\Rightarrow\; T \sim 0{,}05\ \mathrm{K}", BCOL, 38), buff=0.2),
            tx("beaucoup trop faible : l'origine n'est pas magnétique !", 22, "#FF7777", bold=True),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        oms.next_to(q, DOWN, buff=0.5)
        ajuster(oms, 12.8)
        oms.next_to(q, DOWN, buff=0.5)
        self.p(FadeIn(oms[0], shift=UP * 0.15), rt=1.2)
        self.p(FadeIn(oms[1]), rt=0.6)
        self.pause(1.6)
        self.p(FadeIn(oms[2], shift=UP * 0.15), rt=1.2)
        self.pause(1.2)
        self.p(FadeIn(oms[3], scale=1.1), rt=0.8)
        self.dire("(a ≈ 0,25 nm : distance entre atomes voisins)", c=SOFT, lire=1.2)
        ech = VGroup(row(tx("Interaction d'échange (Heisenberg) : Coulomb + principe de Pauli", 24, RES), buff=0.1),
                     row(mx(r"\mathcal{H} = -J \sum_{\langle i,j \rangle} \vec S_i \cdot \vec S_j", RES, 46),
                         mx(r"\qquad k_B T_C \sim J", RES, 40), buff=0.3)).arrange(DOWN, buff=0.3)
        ech.next_to(oms, DOWN, buff=0.45)
        ajuster(ech, 12.8)
        ech.next_to(oms, DOWN, buff=0.45)
        self.p(FadeIn(ech[0], shift=UP * 0.15), rt=1.0)
        self.p(Write(ech[1]), rt=1.4)
        self.dire("Effet purement quantique : l'énergie électrostatique dépend de l'orientation relative des spins.", c=RES, lire=2.4)
        self.vider()
        tab = tableau([[r"\text{matériau}", r"\mathrm{Fe}", r"\mathrm{Co}", r"\mathrm{Ni}", r"\mathrm{Gd}"],
                       [r"T_C\ (\mathrm{K})", "1043", "1388", "627", "292"]], fs=36)
        for c in tab[0][:5]:
            c.set_color(SOFT)
        tab[0][5].set_color(TCOL)
        tab_t = tx("Quelques températures de Curie", 24, TCOL).next_to(tab, UP, buff=0.3)
        g = VGroup(tab_t, tab).move_to(UP * 0.5)
        self.p(FadeIn(tab_t), Create(tab[1]), LaggedStart(*[FadeIn(c) for c in tab[0]], lag_ratio=0.08), rt=1.6)
        gd = SurroundingRectangle(VGroup(tab[0][4], tab[0][9]), color=RES, buff=0.1, corner_radius=0.06)
        self.p(Create(gd), rt=0.6)
        self.dire("Le gadolinium perd son ferromagnétisme vers 19 °C : ferromagnétique en hiver, paramagnétique en été !", c=RES, lire=2.6)
        self.dire("Le fer : 1043 K ≈ 770 °C, le clou chauffé de l'expérience.", c=TCOL, lire=1.8)
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
            row(etiquette("1", MCOL).scale(1.4), txm(r"$T < T_C$ : aimantation spontanée (ferro) ; $T > T_C$ : $M = 0$ sans champ (para)", 22), buff=0.3),
            row(etiquette("2", LAMB).scale(1.4), tx("Weiss : champ moléculaire λM", 22),
                mx(r"\Rightarrow\ m = \tanh\!\left(\tfrac{T_C}{T} m\right),\ T_C = \tfrac{\lambda N\mu^2}{k_B}", LAMB, 34), buff=0.25),
            row(etiquette("3", TCOL).scale(1.4), txm(r"au-dessus de $T_C$ : loi de Curie-Weiss", 22), mx(r"\chi = \frac{C}{T - T_C}", TCOL, 36), buff=0.25),
            row(etiquette("4", ABSO).scale(1.4), txm(r"transition du 2nd ordre, brisure de symétrie ; champ moyen : $\beta = 1/2$, $\gamma = 1$", 22), buff=0.3),
            row(etiquette("5", RES).scale(1.4), tx("origine : interaction d'échange (quantique), pas dipolaire", 22), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        g = VGroup(t, items).arrange(DOWN, buff=0.5)
        ajuster(g, 13.0, 6.9)
        g.move_to(DOWN * 0.2)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=2.2)
        self.pause(5.0)
