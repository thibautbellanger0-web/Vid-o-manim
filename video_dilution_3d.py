from manim import *
import math

# =====================================================================
#  Vidéo de cours (Seconde, « Constitution de la matière ») – LA DILUTION, en 3D, ≈ 4 min.
#  Vidéo autonome sous-titrée. Fil conducteur : la CONSERVATION DE LA MASSE DE SOLUTÉ.
#  Plan : protocole en 3D (pipette jaugée, fiole jaugée, ajustement au trait, retournements)
#  → vision particulaire (même masse m, volume 10 fois plus grand) → relation
#  C_pipette × V_pipette = C_fiole × V_fiole établie pas à pas → exemple chiffré rédigé.
#  Manim Community, rendu sur GitHub. Caméra Manim fixe ; monde 3D projeté par une vue
#  animable (phi, theta, cible, zoom), comme frame.reorient chez 3B1B.
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
BLEU_M = "#1E5BD8"   # solution mère (concentrée)
BLEU_F = "#6FA8F0"   # solution fille (diluée)
BLEU_C = CONC        # concentrations (code couleur habituel)
EAU_L = "#CFE8FF"    # eau distillée ajoutée
VERRE = "#DDEEFF"    # verre


# =====================================================================
class Correction(ThreeDScene):
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
        self.O = np.zeros(3)
        self.phi = ValueTracker(75 * DEGREES)
        self.theta = ValueTracker(-90 * DEGREES)
        self.zv = ValueTracker(1.0)
        self.cx, self.cy, self.cz = ValueTracker(0.0), ValueTracker(0.0), ValueTracker(0.0)
        self.horloge = 0.0
        self.rotation_auto = 0.0
        self.balancement = None
        self.taches = []
        self.chrono = Dot(radius=0.001, fill_opacity=0, stroke_width=0)
        self.chrono.add_updater(lambda m, dt: self._tick(dt))
        self.add(self.chrono)
        self.preparer_verrerie()
        self.titre()
        self.protocole()
        self.microscopique()
        self.relation()
        self.exemple()
        self.retenir()

    # =================================================================
    #  Moteur 3D maison (inspiré de la caméra « frame.reorient » de 3B1B)
    # =================================================================
    def _tick(self, dt):
        if dt <= 0:
            return
        self.horloge += dt
        if self.rotation_auto:
            self.theta.increment_value(self.rotation_auto * dt)
        if self.balancement is not None:
            c, a, w, t0 = self.balancement
            self.theta.set_value(c + a * math.sin(w * (self.horloge - t0)))
        for f in self.taches:
            f(self.horloge, dt)

    def R(self):
        return rotation_matrix(-self.phi.get_value(), RIGHT) @ rotation_matrix(-self.theta.get_value() - PI / 2, OUT)

    def T(self):
        """Projection courante monde → écran (z de l'écran = profondeur, utilisée pour l'ombrage et le tri)."""
        R = self.R()
        z = self.zv.get_value()
        O = np.array(self.O, dtype=float)
        C0 = np.array([self.cx.get_value(), self.cy.get_value(), self.cz.get_value()])

        def f(p):
            return O + z * ((np.asarray(p, dtype=float) - C0) @ R.T)
        return f

    def vue(self, O, phi, theta, zoom=1.0):
        self.O = np.array(O, dtype=float)
        self.phi.set_value(phi * DEGREES)
        self.theta.set_value(theta * DEGREES)
        self.zv.set_value(zoom)

    def bouger_vue(self, *extra, rt=2.0, phi=None, theta=None, zoom=None, **kw):
        anims = list(extra)
        if phi is not None:
            anims.append(self.phi.animate.set_value(phi * DEGREES))
        if theta is not None:
            anims.append(self.theta.animate.set_value(theta * DEGREES))
        if zoom is not None:
            anims.append(self.zv.animate.set_value(zoom))
        self.p(*anims, rt=rt, **kw)

    def vers_spectateur(self):
        """Direction (dans le monde) qui pointe vers le spectateur."""
        return self.R().T @ OUT

    # ---------- briques 3D ----------
    def poly3(self, T, pts, col, op=1.0, sw=0.0, sc=None):
        m = Polygon(*T(np.array(pts, dtype=float)), fill_color=col, fill_opacity=op,
                    stroke_color=sc or col, stroke_width=sw)
        m.set_shade_in_3d(True)
        return m

    def boite(self, T, c, d, col, op=1.0, sans=(), couleurs=None, sw=0.6, sc=None):
        c = np.array(c, dtype=float)
        hx, hy, hz = np.array(d, dtype=float) / 2

        def P(sx, sy, sz):
            return c + np.array([sx * hx, sy * hy, sz * hz])
        F = {"+x": [P(1, -1, -1), P(1, 1, -1), P(1, 1, 1), P(1, -1, 1)],
             "-x": [P(-1, -1, -1), P(-1, -1, 1), P(-1, 1, 1), P(-1, 1, -1)],
             "+y": [P(-1, 1, -1), P(-1, 1, 1), P(1, 1, 1), P(1, 1, -1)],
             "-y": [P(-1, -1, -1), P(1, -1, -1), P(1, -1, 1), P(-1, -1, 1)],
             "+z": [P(-1, -1, 1), P(1, -1, 1), P(1, 1, 1), P(-1, 1, 1)],
             "-z": [P(-1, -1, -1), P(-1, 1, -1), P(1, 1, -1), P(1, -1, -1)]}
        g = VGroup()
        for k, f in F.items():
            if k in sans:
                continue
            cc = (couleurs or {}).get(k, col)
            g.add(self.poly3(T, f, cc, op, sw, sc or cc))
        return g

    def sphere3(self, T, c, r, col, res=(16, 8), op=1.0, demi=False, sw=0.3, sc=None, so=1.0):
        c = np.array(c, dtype=float)
        v0 = PI / 2 if demi else 0.0
        return Surface(lambda u, v: T(c + r * np.array([np.cos(u) * np.sin(v), np.sin(u) * np.sin(v), -np.cos(v)])),
                       u_range=[0, TAU], v_range=[v0, PI], resolution=res, checkerboard_colors=False,
                       fill_color=col, fill_opacity=op, stroke_color=sc or col, stroke_width=sw, stroke_opacity=so)

    def cylindre3(self, T, a, b, r, col, res=(16, 1), op=1.0, bouchons=True):
        a, b = np.array(a, dtype=float), np.array(b, dtype=float)
        ax_ = b - a
        e = normalize(ax_)
        e1 = normalize(np.cross(e, np.array([1.0, 0, 0]) if abs(e[0]) < 0.9 else np.array([0, 0, 1.0])))
        e2 = np.cross(e, e1)
        s = Surface(lambda u, v: T(a + v * ax_ + r * (np.cos(u) * e1 + np.sin(u) * e2)), u_range=[0, TAU], v_range=[0, 1],
                    resolution=res, checkerboard_colors=False, fill_color=col, fill_opacity=op, stroke_color=col, stroke_width=0.3)
        g = VGroup(s)
        if bouchons:
            for p in (a, b):
                g.add(self.poly3(T, [p + r * (np.cos(t) * e1 + np.sin(t) * e2) for t in np.linspace(0, TAU, 17)[:-1]], col, op))
        return g

    def arc3(self, T, c, r, e1, e2, a0, a1, col, op, sw, trier=False):
        pts = [np.array(c) + r * (np.cos(t) * np.array(e1) + np.sin(t) * np.array(e2)) for t in np.linspace(a0, a1, 28)]
        m = VMobject(stroke_color=col, stroke_width=sw, stroke_opacity=op)
        m.set_points_smoothly(T(np.array(pts)))
        if trier:
            m.set_shade_in_3d(True)
        return m

    def anneau3(self, T, c, r, e1, e2, col, op, sw):
        """Cercle complet : moitié avant dessinée par-dessus, moitié arrière triée en profondeur (cachée par les objets)."""
        d = self.vers_spectateur()
        a0 = math.atan2(np.dot(d, e2), np.dot(d, e1))
        return VGroup(self.arc3(T, c, r, e1, e2, a0 + PI / 2, a0 + 3 * PI / 2, col, op * 0.6, sw, trier=True),
                      self.arc3(T, c, r, e1, e2, a0 - PI / 2, a0 + PI / 2, col, op, sw))

    def vide(self):
        return Dot(radius=0.001, fill_opacity=0, stroke_width=0)

    def fronts(self, T, src, c, plans, v=1.2, rmin=0.3, rmax=4.0, col=None, gain=1.0, sw=3.0, complet=False):
        """Fronts d'onde émis par la source (fil de fer façon 3B1B), opacité décroissante avec la distance."""
        col = col or SONC
        g = VGroup(self.vide())
        for (tk, ak) in src.emis:
            r = rmin + v * (self.horloge - tk)
            if r >= rmax or r <= rmin:
                continue
            op = min(1.0, gain * ak) * (1 - (r - rmin) / (rmax - rmin)) ** 1.2
            if op < 0.03:
                continue
            w = sw * min(1.6, 0.5 + gain * ak)
            for (e1, e2, a0, a1) in plans:
                if complet:
                    g.add(self.anneau3(T, c, r, e1, e2, col, op, w))
                else:
                    g.add(self.arc3(T, c, r, e1, e2, a0, a1, col, op, w))
        return g

    def epingle(self, m, pw, decal=ORIGIN):
        """Étiquette plate qui suit un point du monde 3D."""
        m.set_stroke(BLACK, width=5, background=True)
        return always_redraw(lambda: m.copy().move_to(self.T()(pw) + np.array(decal)))

    def jauge(self, val_fn, c, h=2.6, w=0.42, col=None, titre="niveau sonore"):
        col = col or SONC
        cadre = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=SOFT, stroke_width=1.5).move_to(c)
        bar = always_redraw(lambda: Rectangle(width=w - 0.12, height=max(0.01, (h - 0.12) * min(1.0, val_fn())),
                                              stroke_width=0, fill_color=col, fill_opacity=0.9)
                            .move_to(cadre.get_bottom() + UP * 0.06, aligned_edge=DOWN))
        lab = tx(titre, 18, SOFT).next_to(cadre, UP, buff=0.15)
        return VGroup(cadre, bar, lab)

    def nouvelle_scene(self):
        self.taches = []
        self.rotation_auto = 0.0
        self.balancement = None

    # ---------- caméra : cible et zoom ----------
    def viser(self, cible, zoom=None, phi=None, theta=None, rt=2.0, *extra):
        anims = [self.cx.animate.set_value(cible[0]), self.cy.animate.set_value(cible[1]), self.cz.animate.set_value(cible[2])]
        if zoom is not None:
            anims.append(self.zv.animate.set_value(zoom))
        if phi is not None:
            anims.append(self.phi.animate.set_value(phi * DEGREES))
        if theta is not None:
            anims.append(self.theta.animate.set_value(theta * DEGREES))
        self.p(*anims, *extra, rt=rt)

    def placer_vue(self, O, cible, phi, theta, zoom):
        self.O = np.array(O, dtype=float)
        self.cx.set_value(cible[0]); self.cy.set_value(cible[1]); self.cz.set_value(cible[2])
        self.phi.set_value(phi * DEGREES)
        self.theta.set_value(theta * DEGREES)
        self.zv.set_value(zoom)

    # =================================================================
    #  Verrerie de révolution (verre translucide + silhouettes, liquide coloré)
    # =================================================================
    def preparer_verrerie(self):
        # fiole jaugée (unités locales, z vertical depuis le fond)
        def r_fiole(z):
            if z > 3.1:
                return 0.15
            e = 0.95 * math.sqrt(max(0.0, 1 - ((z - 0.75) / 0.85) ** 2))
            return e if z < 0.75 else max(0.12, e)
        def r_pip(z):
            if z < 0.35:
                return 0.018 + 0.03 * z / 0.35
            if 1.3 <= z <= 2.1:
                return 0.048 + 0.14 * math.sin(PI * (z - 1.3) / 0.8)
            return 0.048
        self.r_fiole, self.r_pip = r_fiole, r_pip
        self.Z_TRAIT_F, self.Z_HAUT_F = 2.55, 3.2
        self.Z_TRAIT_P, self.Z_HAUT_P = 3.0, 3.7
        # volumes intérieurs → niveau (pour un remplissage réaliste)
        zs = np.linspace(0, self.Z_TRAIT_F + 0.3, 600)
        aire = np.array([PI * max(0.0, r_fiole(z) - 0.03) ** 2 for z in zs])
        vol = np.concatenate([[0], np.cumsum((aire[1:] + aire[:-1]) / 2 * np.diff(zs))])
        self.zs_f, self.vol_f = zs, vol
        self.V_F = float(np.interp(self.Z_TRAIT_F, zs, vol))
        zp = np.linspace(0, self.Z_TRAIT_P + 0.2, 400)
        ap = np.array([PI * max(0.0, r_pip(z) - 0.015) ** 2 for z in zp])
        vp = np.concatenate([[0], np.cumsum((ap[1:] + ap[:-1]) / 2 * np.diff(zp))])
        self.zs_p, self.vol_p = zp, vp
        self.V_P = float(np.interp(self.Z_TRAIT_P, zp, vp))

    def niveau_fiole(self, frac):
        """Hauteur du liquide pour une fraction frac du volume jaugé de la fiole."""
        return float(np.interp(frac * self.V_F, self.vol_f, self.zs_f))

    def niveau_pip(self, frac):
        return float(np.interp(frac * self.V_P, self.vol_p, self.zs_p))

    def revol(self, T, base, M, prof, z0, z1, col, op, res=(14, 18), sw=0.3, sc=None, so=1.0):
        base = np.array(base, dtype=float)
        if z1 - z0 < 0.005:
            return self.vide()

        def f(u, v):
            r = prof(u)
            return T(base + M @ np.array([r * math.cos(v), r * math.sin(v), u]))
        return Surface(f, u_range=[z0, z1], v_range=[0, TAU], resolution=res, checkerboard_colors=False,
                       fill_color=col, fill_opacity=op, stroke_color=sc or col, stroke_width=sw, stroke_opacity=so)

    def disque3(self, T, base, M, r, z, col, op, n=20):
        base = np.array(base, dtype=float)
        pts = [base + M @ np.array([r * math.cos(t), r * math.sin(t), z]) for t in np.linspace(0, TAU, n + 1)[:-1]]
        return self.poly3(T, pts, col, op, 0.6, col)

    def silhouette(self, T, base, M, prof, z0, z1, sw=2.2, col=WHITE, op=0.85):
        """Les deux bords visibles du verre (comme sur un schéma) + le cercle du haut."""
        base = np.array(base, dtype=float)
        d = M.T @ self.vers_spectateur()
        a0 = math.atan2(d[1], d[0])
        g = VGroup()
        zz = np.linspace(z0, z1, 40)
        for a in (a0 + PI / 2, a0 - PI / 2):
            pts = [base + M @ np.array([prof(z) * math.cos(a), prof(z) * math.sin(a), z]) for z in zz]
            m = VMobject(stroke_color=col, stroke_width=sw, stroke_opacity=op)
            m.set_points_smoothly(T(np.array(pts)))
            g.add(m)
        e1, e2 = M @ RIGHT, M @ UP
        g.add(self.anneau3(T, base + M @ np.array([0, 0, z1]), prof(z1), e1, e2, col, op, sw * 0.8))
        return g

    def trait3(self, T, base, M, r, z, col="#FF5555"):
        e1, e2 = M @ RIGHT, M @ UP
        return self.anneau3(T, np.array(base, dtype=float) + M @ np.array([0, 0, z]), r + 0.004, e1, e2, col, 1.0, 3.0)

    def fiole3(self, T, base, M, niv=0.0, h1=0.0, c_bas=None, c_haut=None, op_bas=0.8, op_haut=0.3, bouchon=False):
        """Fiole jaugée ; liquide en deux couches (bas : solution prélevée, haut : eau ajoutée)."""
        verre = self.revol(T, base, M, self.r_fiole, 0.0, self.Z_HAUT_F, VERRE, 0.07, res=(18, 20), sw=0.25, sc=WHITE, so=0.12)
        rin = lambda z: max(0.0, self.r_fiole(z) - 0.03)
        g = VGroup(verre, self.disque3(T, base, M, self.r_fiole(0.0), 0.0, VERRE, 0.10))
        if niv > 0.01:
            hb = min(h1, niv)
            g.add(self.revol(T, base, M, rin, 0.02, max(0.03, hb), c_bas, op_bas, res=(10, 18)))
            if niv > hb + 0.01:
                g.add(self.revol(T, base, M, rin, hb, niv, c_haut, op_haut, res=(10, 18)))
            g.add(self.disque3(T, base, M, rin(niv), niv, c_haut if niv > hb + 0.01 else c_bas, 0.5))
        g.add(self.silhouette(T, base, M, self.r_fiole, 0.0, self.Z_HAUT_F))
        g.add(self.trait3(T, base, M, self.r_fiole(self.Z_TRAIT_F), self.Z_TRAIT_F))
        if bouchon:
            b = np.array(base, dtype=float)
            g.add(self.cylindre3(T, b + M @ np.array([0, 0, 3.12]), b + M @ np.array([0, 0, 3.42]), 0.17, "#E6EEF5", res=(14, 1)))
        return g

    def pipette3(self, T, tip, niv=0.0, col=None, op=0.8):
        M = np.eye(3)
        g = VGroup(self.revol(T, tip, M, self.r_pip, 0.0, self.Z_HAUT_P, VERRE, 0.08, res=(16, 10), sw=0.2, sc=WHITE, so=0.1))
        rin = lambda z: max(0.004, self.r_pip(z) - 0.015)
        if niv > 0.01:
            g.add(self.revol(T, tip, M, rin, 0.0, niv, col, op, res=(12, 10)))
        g.add(self.silhouette(T, tip, M, self.r_pip, 0.0, self.Z_HAUT_P, sw=1.8))
        g.add(self.trait3(T, tip, M, self.r_pip(self.Z_TRAIT_P), self.Z_TRAIT_P))
        return g

    def becher3(self, T, base, niv, col, op=0.85):
        M = np.eye(3)
        r = lambda z: 0.78
        g = VGroup(self.revol(T, base, M, r, 0.0, 1.35, VERRE, 0.07, res=(3, 22), sw=0.2, sc=WHITE, so=0.12),
                   self.disque3(T, base, M, 0.78, 0.0, VERRE, 0.10))
        rin = lambda z: 0.75
        g.add(self.revol(T, base, M, rin, 0.02, niv, col, op, res=(3, 22)))
        g.add(self.disque3(T, base, M, 0.75, niv, col, 0.55))
        g.add(self.silhouette(T, base, M, r, 0.0, 1.35))
        return g

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        self.nouvelle_scene()
        self.placer_vue([2.9, -0.6, 0], [0, 0, 1.5], 74, -80, 1.05)
        niv = self.niveau_fiole(1.0)
        fi = always_redraw(lambda: self.fiole3(self.T(), [0, 0, 0], np.eye(3), niv, niv, BLEU_F, BLEU_F, 0.55, 0.55, bouchon=True))
        t1 = tx("La dilution", 60, WHITE, bold=True)
        t2 = tx("ou comment conserver la masse de soluté", 28, BLEU_C)
        t3 = tx("Physique-chimie · Seconde · Solutions aqueuses", 20, SOFT)
        bloc = VGroup(t1, t2, t3).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-2.6, 0.4, 0])
        self.add(fi)
        self.rotation_auto = 0.18
        self.p(FadeIn(fi), rt=1.0)
        self.p(Write(t1), rt=1.2)
        self.p(FadeIn(t2, shift=UP * 0.2), FadeIn(t3), rt=1.0)
        self.pause(4.0)
        self.hdr_ex = tx("La dilution", 20, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(t1, self.hdr_ex), FadeOut(VGroup(t2, t3)), FadeOut(fi), rt=1.0)
        self.nouvelle_scene()

    # =================================================================
    #  1. LE PROTOCOLE EN 3D
    # =================================================================
    def protocole(self):
        self.set_q("1. Le protocole")
        self.nouvelle_scene()
        self.placer_vue([0.1, -0.15, 0], [-1.1, 0, 2.3], 78, -90, 0.68)
        B = np.array([-3.4, 0, 0])
        F = np.array([1.2, 0, 0])
        e = {"px": B[0], "pz": 2.0, "np": 0.0, "nf": 0.0, "h1": 0.0, "mix": 0.0, "ang": 0.0, "bouchon": False,
             "jet": 0.0, "gouttes": []}
        px, pz, n_p, n_f, mix, ang = (ValueTracker(B[0]), ValueTracker(2.0), ValueTracker(0.0), ValueTracker(0.0),
                                      ValueTracker(0.0), ValueTracker(0.0))
        jet = ValueTracker(0.0)
        visp = ValueTracker(1.0)
        f_pip = 0.1                                     # V_pipette = V_fiole / 10
        h1 = self.niveau_fiole(f_pip)
        pivot = F + np.array([0, 0, 1.3])

        def couleurs():
            m = mix.get_value()
            cb = interpolate_color(ManimColor(BLEU_M), ManimColor(BLEU_F), m)
            ch = interpolate_color(ManimColor(EAU_L), ManimColor(BLEU_F), m)
            return cb, ch, 0.85 + (0.55 - 0.85) * m, 0.25 + (0.55 - 0.25) * m

        def fiole():
            T = self.T()
            a = ang.get_value()
            Rm = rotation_matrix(a, RIGHT)
            base = pivot + Rm @ (F - pivot)
            cb, ch, ob, oh = couleurs()
            niv = n_f.get_value()
            return self.fiole3(T, base, Rm, niv, min(h1, niv), cb, ch, ob, oh, bouchon=e["bouchon"])

        def becher():
            return self.becher3(self.T(), B, 0.95, BLEU_M)

        def pipette():
            if visp.get_value() < 0.5:
                return self.vide()
            return self.pipette3(self.T(), np.array([px.get_value(), 0, pz.get_value()]), n_p.get_value(), BLEU_M)

        def eau():
            T = self.T()
            g = VGroup(self.vide())
            j = jet.get_value()
            if j > 0.01:
                z_bas = n_f.get_value()
                g.add(self.cylindre3(T, F + np.array([0, 0, 4.4]), F + np.array([0, 0, max(z_bas, 0.1)]), 0.035 * j, EAU_L,
                                     res=(8, 1), op=0.7, bouchons=False))
            for zg in e["gouttes"]:
                g.add(self.sphere3(T, F + np.array([0, 0, zg]), 0.06, EAU_L, res=(8, 4), op=0.9))
            return g
        fi, be, pi_, ea = always_redraw(fiole), always_redraw(becher), always_redraw(pipette), always_redraw(eau)
        l_b = self.epingle(tx("solution mère", 22, BLEU_M), B + np.array([0, -0.8, 0]), DOWN * 0.42)
        l_b2 = self.epingle(tx("(concentrée)", 18, SOFT), B + np.array([0, -0.8, 0]), DOWN * 0.75)
        l_f = self.epingle(tx("fiole jaugée", 22, WHITE), F + np.array([0, -0.9, 0]), DOWN * 0.42)
        self.add(be, fi, pi_, ea)
        self.p(FadeIn(be), FadeIn(fi), FadeIn(l_b), FadeIn(l_b2), FadeIn(l_f), rt=1.2)
        self.balancement = (-90 * DEGREES, 10 * DEGREES, 0.25, self.horloge)
        self.dire("Objectif : préparer une solution moins concentrée (la solution fille) à partir d'une solution mère.", lire=2.2)
        self.p(FadeIn(pi_), rt=0.6)
        self.dire(r"Étape 1 : on prélève un volume précis $V_{\text{pipette}}$ de solution mère, avec une pipette jaugée.", lire=0.3)
        self.p(pz.animate.set_value(0.12), rt=1.4)
        self.p(n_p.animate.set_value(self.Z_TRAIT_P + 0.18), rt=2.0)
        self.dire("On ajuste le bas du ménisque sur le trait de jauge : le volume est connu très précisément.", c="#FF5555", lire=0.3)
        self.p(n_p.animate.set_value(self.Z_TRAIT_P), rt=1.2)
        self.pause(1.0)
        self.p(pz.animate.set_value(1.85), rt=1.2)
        self.p(px.animate.set_value(F[0]), rt=1.6)
        self.dire("Étape 2 : on verse ce prélèvement dans une fiole jaugée.", lire=0.3)
        self.p(pz.animate.set_value(1.55), rt=0.8)
        self.p(n_p.animate.set_value(0.0), n_f.animate.set_value(h1), rt=2.6, rate_func=linear)
        self.p(pz.animate.set_value(3.6), rt=1.0)
        self.p(FadeOut(pi_), rt=0.4)
        visp.set_value(0.0)
        self.dire("Étape 3 : on ajoute de l'eau distillée jusqu'aux trois quarts environ, puis on agite.", c=EAU_L, lire=0.3)
        self.p(jet.animate.set_value(1.0), rt=0.4)
        self.p(n_f.animate.set_value(self.niveau_fiole(0.75)), mix.animate.set_value(0.15), rt=3.0, rate_func=linear)
        self.p(jet.animate.set_value(0.0), rt=0.3)
        self.p(ang.animate.set_value(0.25), rt=0.35)
        self.p(ang.animate.set_value(-0.25), mix.animate.set_value(0.5), rt=0.7)
        self.p(ang.animate.set_value(0.0), rt=0.35)
        # complément au trait de jauge
        self.dire("Étape 4 : on complète à l'eau, à la fin goutte à goutte, jusqu'au trait de jauge.", lire=0.3)
        self.p(jet.animate.set_value(1.0), rt=0.3)
        z98 = self.niveau_fiole(0.985)
        self.p(n_f.animate.set_value(z98), rt=2.0, rate_func=linear)
        self.p(jet.animate.set_value(0.0), rt=0.2)
        self.viser(F + np.array([0, 0, self.Z_TRAIT_F]), zoom=2.4, phi=82, rt=1.8)
        for k in range(3):
            zg = ValueTracker(4.0)
            e["gouttes"] = [4.0]

            def chute(m, a, zg=zg, k=k):
                e["gouttes"] = [4.0 - a * (4.0 - n_f.get_value())]
            niv_cible = z98 + (self.Z_TRAIT_F - z98) * (k + 1) / 3
            self.p(UpdateFromAlphaFunc(zg, chute), rt=0.5, rate_func=rush_into)
            e["gouttes"] = []
            self.p(n_f.animate.set_value(niv_cible), rt=0.35)
        self.dire("Le bas du ménisque est sur le trait : la fiole contient exactement son volume $V_{\\text{fiole}}$.", c="#FF5555", lire=2.2)
        self.viser([-1.1, 0, 2.3], zoom=0.68, phi=78, rt=1.6)
        # bouchon, retournements
        e["bouchon"] = True
        self.dire("Étape 5 : on bouche et on retourne plusieurs fois la fiole pour homogénéiser.", lire=0.3)
        self.p(ang.animate.set_value(PI), mix.animate.set_value(0.8), rt=1.1)
        self.p(ang.animate.set_value(0.0), rt=1.1)
        self.p(ang.animate.set_value(PI), mix.animate.set_value(1.0), rt=1.1)
        self.p(ang.animate.set_value(0.0), rt=1.1)
        l_f2 = self.epingle(tx("solution fille (diluée)", 22, BLEU_C), F + np.array([0, -0.9, 0]), DOWN * 0.42)
        self.p(FadeOut(l_f), FadeIn(l_f2), rt=0.6)
        self.dire("La solution fille est plus claire : elle est moins concentrée que la solution mère.", c=BLEU_C, lire=2.4)
        self.effacer_sous_titre()
        self.balancement = None
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  2. CE QUI SE PASSE À L'ÉCHELLE DES PARTICULES
    # =================================================================
    def microscopique(self):
        self.set_q("2. Côté particules")
        self.nouvelle_scene()
        self.placer_vue([0.0, -0.35, 0], [0, 0, 1.3], 70, -90, 0.95)
        A = np.array([-3.4, 0, 0])
        Bc = np.array([1.6, 0, 0])
        rA, hA = 0.62, 1.0
        rB, hB = 1.25, 2.45
        n = 30
        rng = np.random.default_rng(7)

        def tirer(r, h, k):
            out = []
            while len(out) < k:
                p = rng.uniform([-r, -r, 0.1], [r, r, h - 0.1])
                if math.hypot(p[0], p[1]) < r - 0.12:
                    out.append(p)
            return np.array(out)
        PA = A + tirer(rA, hA, n)
        PB = Bc + tirer(rB, hB, n)
        w_j = rng.uniform(1.5, 3.0, (n, 3))
        ph_j = rng.uniform(0, TAU, (n, 3))
        trans = ValueTracker(0.0)
        eauB = ValueTracker(0.0)
        vis = ValueTracker(0.0)
        dots = VGroup(*[Dot(radius=0.07, fill_color=BLEU_M, stroke_width=0).set_sheen(-0.4, DR) for _ in range(n)])

        def placer(g, dt=0):
            T = self.T()
            a = trans.get_value()
            s = a * a * (3 - 2 * a)
            arc = np.zeros((n, 3))
            arc[:, 2] = 0.8 * math.sin(PI * s)
            P = (1 - s) * PA + s * PB + arc + 0.04 * np.sin(w_j * self.horloge + ph_j)
            S = T(P)
            for i, d in enumerate(g):
                d.move_to(S[i])
                d.set_fill(BLEU_M, opacity=vis.get_value())
        dots.add_updater(placer)
        placer(dots)

        def volumes():
            T = self.T()
            M = np.eye(3)
            ra, rb = (lambda z: rA), (lambda z: rB)
            g = VGroup(self.revol(T, A, M, ra, 0, hA, EAU_L, 0.16, res=(2, 22), sw=0.2, sc=WHITE, so=0.15),
                       self.disque3(T, A, M, rA, hA, EAU_L, 0.12), self.silhouette(T, A, M, ra, 0, hA),
                       self.revol(T, Bc, M, rb, 0, hB, VERRE, 0.04, res=(3, 26), sw=0.2, sc=WHITE, so=0.12),
                       self.silhouette(T, Bc, M, rb, 0, hB))
            hb = eauB.get_value() * hB
            if hb > 0.02:
                g.add(self.revol(T, Bc, M, lambda z: rB - 0.02, 0.01, hb, EAU_L, 0.16, res=(3, 26), sw=0.2, sc=EAU_L, so=0.2))
                g.add(self.disque3(T, Bc, M, rB - 0.02, hb, EAU_L, 0.12, n=26))
            return g
        vol = always_redraw(volumes)
        lA = VGroup(txm(r"prélèvement : volume $V_{\text{pipette}}$", 22, WHITE),
                    txm(r"masse de soluté : $m$", 22, BLEU_C)).arrange(DOWN, buff=0.12)
        lB = VGroup(txm(r"fiole : volume $V_{\text{fiole}} = 10\,V_{\text{pipette}}$", 22, WHITE),
                    txm(r"masse de soluté : toujours $m$", 22, BLEU_C)).arrange(DOWN, buff=0.12)
        lA_e = self.epingle(lA, A + np.array([0, 0, hA]), UP * 1.1)
        lB_e = self.epingle(lB, Bc + np.array([0, 0, hB]), UP * 1.05)
        compteur = always_redraw(lambda: txm(r"particules de soluté : %d" % n, 22, BLEU_C).to_corner(UR, buff=0.35).shift(DOWN * 0.45))
        self.add(vol, dots)
        self.p(FadeIn(vol), vis.animate.set_value(1.0), FadeIn(lA_e), rt=1.4)
        self.rotation_auto = 0.0
        self.balancement = (-90 * DEGREES, 14 * DEGREES, 0.2, self.horloge)
        self.dire("Zoom sur le prélèvement : les particules de soluté (en bleu) sont dispersées dans l'eau.", lire=2.2)
        self.p(FadeIn(compteur), rt=0.5)
        self.dire("Chaque particule a une masse : leur ensemble forme la masse de soluté m.", c=BLEU_C, lire=2.0)
        self.dire("On les transvase dans la fiole, puis on ajoute de l'eau, et seulement de l'eau.", lire=0.3)
        self.p(trans.animate.set_value(1.0), rt=2.6)
        self.p(eauB.animate.set_value(1.0), FadeIn(lB_e), rt=2.2)
        self.dire("Aucune particule de soluté n'a été ajoutée ni perdue : la masse de soluté m est CONSERVÉE.", c=BLEU_C, lire=2.6)
        self.dire("Mais elles occupent maintenant un volume 10 fois plus grand : elles sont 10 fois moins serrées.", lire=2.4)
        self.dire("Moins de soluté par litre : la concentration en masse a diminué.", c=BLEU_C, lire=2.0)
        self.effacer_sous_titre()
        dots.clear_updaters()
        self.balancement = None
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  3. LA RELATION, ÉTAPE PAR ÉTAPE
    # =================================================================
    def relation(self):
        self.set_q("3. La relation")
        fs = 42
        P, F_ = r"\text{pipette}", r"\text{fiole}"
        d1 = row(mx(r"C_m", BLEU_C, fs), mx("=", WHITE, fs), frac(mx("m", MASSE, fs), mx("V", VOL, fs)), buff=0.15)
        d2 = row(mx("m", MASSE, fs), mx("=", WHITE, fs), mx(r"C_m", BLEU_C, fs), mx(r"\times", WHITE, fs), mx("V", VOL, fs), buff=0.15)
        haut_ = row(tx("Définition :", 24, SOFT), d1, mx(r"\Longrightarrow", SOFT, fs), d2, buff=0.45)
        g1 = row(mx(r"m_{%s}" % P, MASSE, fs), mx("=", WHITE, fs), mx(r"C_{%s}" % P, BLEU_C, fs), mx(r"\times", WHITE, fs),
                 mx(r"V_{%s}" % P, VOL, fs), buff=0.15)
        g2 = row(mx(r"m_{%s}" % F_, MASSE, fs), mx("=", WHITE, fs), mx(r"C_{%s}" % F_, BLEU_C, fs), mx(r"\times", WHITE, fs),
                 mx(r"V_{%s}" % F_, VOL, fs), buff=0.15)
        milieu = row(VGroup(tx("dans le prélèvement", 20, SOFT), g1).arrange(DOWN, buff=0.15),
                     VGroup(tx("dans la fiole", 20, SOFT), g2).arrange(DOWN, buff=0.15), buff=1.2)
        cons = row(mx(r"m_{%s}" % F_, MASSE, fs), mx("=", WHITE, fs), mx(r"m_{%s}" % P, MASSE, fs), buff=0.15)
        E = row(mx(r"C_{%s}" % P, BLEU_C, fs + 4), mx(r"\times", WHITE, fs + 4), mx(r"V_{%s}" % P, VOL, fs + 4), mx("=", WHITE, fs + 4),
                mx(r"C_{%s}" % F_, BLEU_C, fs + 4), mx(r"\times", WHITE, fs + 4), mx(r"V_{%s}" % F_, VOL, fs + 4), buff=0.15)
        bas = VGroup(row(tx("Conservation de la masse de soluté :", 24, MASSE), cons, buff=0.4), E).arrange(DOWN, buff=1.05)
        page = VGroup(haut_, milieu, bas).arrange(DOWN, buff=0.75)
        self.caser(page, top=3.0, x=0.0, w=12.8)
        self.dire("Point de départ : la définition de la concentration en masse d'un soluté.", lire=0.3)
        self.p(FadeIn(haut_[0]), Write(d1), rt=1.4)
        self.dire("Masse de soluté divisée par le volume de solution. On en tire la masse de soluté :", lire=0.3)
        self.p(FadeIn(haut_[2]), rt=0.3)
        self.morph([(d1[0], d2[2]), (d1[2][0], d2[0]), (d1[2][2], d2[4])], FadeIn(VGroup(d2[1], d2[3])), rt=1.4)
        self.pause(1.0)
        self.dire("On l'écrit pour le prélèvement, puis pour la solution contenue dans la fiole.", lire=0.3)
        self.p(FadeIn(milieu[0][0]), TransformFromCopy(d2, g1, path_arc=-0.4), rt=1.4)
        self.p(FadeIn(milieu[1][0]), TransformFromCopy(d2, g2, path_arc=-0.4), rt=1.4)
        self.pause(1.0)
        self.dire("Tout le soluté du prélèvement se retrouve dans la fiole (on n'a ajouté que de l'eau) :", c=MASSE, lire=0.3)
        self.p(FadeIn(bas[0][0]), rt=0.6)
        self.morph([(g2[0], cons[0]), (g1[0], cons[2])], FadeIn(cons[1]), rt=1.4)
        self.pause(1.0)
        self.dire("On remplace chaque masse par son expression :", lire=0.3)
        self.morph([(g1[2], E[0]), (g1[4], E[2]), (g2[2], E[4]), (g2[4], E[6])], FadeIn(VGroup(E[1], E[3], E[5])), rt=1.8)
        self.encadre(E)
        self.dire("C'est la relation de la dilution : une conséquence directe de la conservation de la masse.", c=BOX, lire=2.4)
        self.effacer_sous_titre()
        self.pause(1.0)
        self.vider()

    # =================================================================
    #  4. EXEMPLE CHIFFRÉ (rédaction complète)
    # =================================================================
    def exemple(self):
        self.set_q("4. Exemple chiffré")
        self.question([r"On veut $V_{\text{fiole}} = 100{,}0$ mL de solution à $C_{\text{fiole}} = 5{,}0\ \mathrm{g\cdot L^{-1}}$, à partir d'une solution mère",
                       r"à $C_{\text{pipette}} = 50\ \mathrm{g\cdot L^{-1}}$. Quel volume $V_{\text{pipette}}$ faut-il prélever ?"])
        fs = 40
        P, F_ = r"\text{pipette}", r"\text{fiole}"
        rel = row(mx(r"C_{%s}" % P, BLEU_C, fs), mx(r"\times", WHITE, fs), mx(r"V_{%s}" % P, VOL, fs), mx("=", WHITE, fs),
                  mx(r"C_{%s}" % F_, BLEU_C, fs), mx(r"\times", WHITE, fs), mx(r"V_{%s}" % F_, VOL, fs), buff=0.12)
        E = row(mx(r"V_{%s}" % P, VOL, fs), mx("=", WHITE, fs),
                frac(row(mx(r"C_{%s}" % F_, BLEU_C, fs), mx(r"\times", WHITE, fs), mx(r"V_{%s}" % F_, VOL, fs), buff=0.1),
                     mx(r"C_{%s}" % P, BLEU_C, fs)), buff=0.15)
        tete = row(rel, mx(r"\Longrightarrow", SOFT, fs), E, buff=0.5)
        num = row(val(r"5{,}0", (r"\mathrm{g\cdot L^{-1}}",), BLEU_C, fs), mx(r"\times", WHITE, fs), val(r"100{,}0", r"\mathrm{mL}", VOL, fs), buff=0.12)
        den = val("50", (r"\mathrm{g\cdot L^{-1}}",), BLEU_C, fs)
        AN = row(mx(r"V_{%s}" % P, VOL, fs), mx("=", WHITE, fs), frac(num, den), buff=0.15)
        RR = row(mx(r"V_{%s}" % P, VOL, fs), mx("=", WHITE, fs), val(r"10{,}0", r"\mathrm{mL}", RES, fs + 4), buff=0.15)
        verif = row(tx("Vérification de la masse de soluté :", 20, SOFT),
                    mx(r"50\ \mathrm{g\cdot L^{-1}} \times 0{,}0100\ \mathrm{L} = 0{,}50\ \mathrm{g}"
                       r"\quad\text{et}\quad 5{,}0\ \mathrm{g\cdot L^{-1}} \times 0{,}1000\ \mathrm{L} = 0{,}50\ \mathrm{g}", SOFT, 28), buff=0.3)
        bloc_r = row(AN, RR, buff=1.2)
        page = VGroup(tete, bloc_r, verif).arrange(DOWN, aligned_edge=LEFT, buff=0.9)
        self.caser(page, top=self.haut() - 0.6, x=0.0, w=12.8)
        self.dire("On part de la relation de dilution et on isole la grandeur cherchée : le volume à prélever.", c=BOX, lire=0.3)
        self.p(Write(rel), rt=1.4)
        self.p(FadeIn(tete[1]), rt=0.3)
        self.morph([(rel[2], E[0]), (rel[4], E[2][0][0]), (rel[6], E[2][0][2]), (rel[0], E[2][2])],
                   FadeIn(VGroup(E[1], E[2][0][1], E[2][1])), rt=1.8)
        self.encadre(E)
        self.pause(1.0)
        self.tag_an(AN)
        self.p(FadeIn(VGroup(AN[0], AN[1], AN[2][1], num[1])), rt=0.5)
        self.morph([(E[2][0][0], num[0]), (E[2][0][2], num[2]), (E[2][2], den)], rt=1.6)
        self.barrer(num[0][1], den[1])
        self.dire(r"Les $\mathrm{g\cdot L^{-1}}$ se simplifient : le résultat est dans l'unité de $V_{\text{fiole}}$, en mL.", c=UNIT, lire=2.2)
        self.p(Write(RR), rt=1.2)
        self.p(Circumscribe(RR[2], color=RES), rt=0.8)
        self.dire("Contrôle : la masse de soluté est bien la même avant et après (0,50 g).", c=MASSE, lire=0.3)
        self.p(FadeIn(verif, shift=UP * 0.1), rt=1.0)
        self.pause(2.5)
        self.effacer_sous_titre()
        self.reponse("On prélève 10,0 mL de solution mère à la pipette jaugée, puis on complète à 100,0 mL en fiole jaugée.")
        self.pause(4.5)
        self.vider_tout()
        self.cur_q = None

    # =================================================================
    #  À RETENIR
    # =================================================================
    def retenir(self):
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 42, WHITE, bold=True)
        items = VGroup(
            row(etiquette("1", BLEU_C).scale(1.4), txm("Diluer, c'est ajouter du solvant (de l'eau) : la concentration diminue.", 24), buff=0.3),
            row(etiquette("2", MASSE).scale(1.4), txm("La masse de soluté se conserve : rien n'est ajouté ni perdu.", 24), buff=0.3),
            row(etiquette("3", BOX).scale(1.4), txm(r"$C_{\text{pipette}} \times V_{\text{pipette}} = C_{\text{fiole}} \times V_{\text{fiole}}$", 24), buff=0.3),
            row(etiquette("4", VOL).scale(1.4), txm("Verrerie de précision : pipette jaugée pour prélever, fiole jaugée pour compléter.", 24), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        g = VGroup(t, items).arrange(DOWN, buff=0.55)
        ajuster(g, 13.0, 6.4)
        g.move_to(DOWN * 0.2)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=2.4)
        self.pause(6.0)
