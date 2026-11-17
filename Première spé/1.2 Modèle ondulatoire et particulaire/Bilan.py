from manim import *
import math

# =====================================================================
#  Première – Chapitre 1.2 : MODÈLES ONDULATOIRE ET PARTICULAIRE DE LA LUMIÈRE (bilan)
#  Vidéo muette à caler sur la voix du professeur (script « Script vidéo – Lumière »).
#  Minutage calé sur le SRT de l'enregistrement (≈ 4 min 55).
#  3D utilisée une seule fois, là où elle apporte quelque chose : l'onde électromagnétique
#  (champs E et B perpendiculaires), dessinée en traits seulement (rendu rapide).
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
JAUNE_L = "#FFE066"   # lumière
ONDE_C = "#58C4DD"    # modèle ondulatoire
PHOT_C = "#FFD166"    # photon, énergie
E_COL = "#FFD166"     # champ électrique
B_COL = "#58C4DD"     # champ magnétique
LAM_C = "#83C167"     # longueur d'onde
NU_C = "#C77DFF"      # fréquence
H_C = "#FF8C42"       # constante de Planck
ABS_C = "#E05A4F"     # absorption (flèche vers le haut)
EM_C = "#4F86E0"      # émission (flèche vers le bas)

# ---------- Minutage : début de chaque passage lu, d'après le SRT (TurboScribe) ----------
T = {
    "intro": 0.46,
    "o1": 15.26, "o2": 26.04, "o3": 31.22, "o4": 37.32,
    "w1": 45.36, "w2": 54.24, "w3": 64.24,
    "s1": 73.74, "s2": 78.46, "s3": 85.72, "s4": 89.72, "s5": 94.38, "s6": 98.46, "s7": 103.64, "s8": 107.66,
    "p1": 117.38, "p2": 127.42, "p3": 136.68,
    "e1": 152.22, "e2": 161.42, "e3": 168.18,
    "n1": 180.36, "n2": 188.08, "n3": 193.80, "n4": 201.44, "n5": 207.26, "n6": 218.76,
    "r1": 225.34,
    "h1": 233.68, "h2": 246.20, "h3": 256.68, "h4": 265.14,
    "c1": 270.32, "c2": 278.98, "c3": 286.50,
    "fin": 294.5,
}


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
        self.horloge = 0.0
        self.chrono = Dot(radius=0.001, fill_opacity=0, stroke_width=0)
        self.chrono.add_updater(lambda m, dt: self._tick(dt))
        self.add(self.chrono)
        self.intro()
        self.onde()
        self.wifi()
        self.spectre_em()
        self.photon()
        self.calcul_photon()
        self.niveaux()
        self.raies()
        self.calcul_hydrogene()
        self.conclusion()
        self.at(T["fin"])

    def _tick(self, dt):
        if dt > 0:
            self.horloge += dt

    def vider(self, rt=0.6, garder=()):
        proteges = set()
        for g in (self.hdr_ex, self.hdr_q, self.chrono, *garder):
            if g is not None:
                proteges.update(id(x) for x in g.get_family())
        mobs = [m for m in self.mobjects if id(m) not in proteges]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    # ---------- petits objets ----------
    def paquet(self, centre, lam=0.35, larg=1.1, col=JAUNE_L, amp=0.22, sw=3.5):
        """Photon dessiné comme un petit train d'onde (enveloppe gaussienne)."""
        xs = np.linspace(-larg, larg, 90)
        pts = [np.array(centre) + np.array([x, amp * math.exp(-(x / (0.45 * larg)) ** 2) * math.sin(TAU * x / lam), 0]) for x in xs]
        m = VMobject(stroke_color=col, stroke_width=sw)
        m.set_points_smoothly(pts)
        halo = m.copy().set_stroke(col, width=sw * 4, opacity=0.18)
        return VGroup(halo, m)

    def icone_wifi(self, c, col=WHITE, s=1.0):
        g = VGroup(Dot(c, radius=0.07 * s, color=col))
        for k in range(1, 4):
            g.add(Arc(radius=0.18 * k * s, start_angle=PI / 4, angle=PI / 2, arc_center=c, color=col, stroke_width=3))
        return g

    def bloc(self, titre, contenu, col):
        cad = SurroundingRectangle(contenu, color=col, buff=0.25, corner_radius=0.12, stroke_width=2.5).set_fill("#1B1F27", 0.92)
        t = tx(titre, 20, col, bold=True).next_to(cad, UP, buff=0.08).align_to(cad, LEFT)
        return VGroup(cad, contenu, t)

    # =================================================================
    #  0. INTRODUCTION
    # =================================================================
    def intro(self):
        self.at(T["intro"])
        t1 = tx("La lumière : onde ou particule ?", 50, WHITE, bold=True).move_to(UP * 2.3)
        t2 = tx("Chapitre 1.2 · Modèles ondulatoire et particulaire de la lumière", 24, SOFT).next_to(t1, DOWN, buff=0.25)
        faisceau = Line(LEFT * 7.2 + DOWN * 0.6, LEFT * 1.6 + DOWN * 0.6, color=JAUNE_L, stroke_width=8)
        halo = faisceau.copy().set_stroke(JAUNE_L, width=26, opacity=0.2)
        xs = np.linspace(-1.6, 6.5, 200)
        onde = VMobject(stroke_color=ONDE_C, stroke_width=4)
        onde.set_points_smoothly([np.array([x, 0.35 + 0.35 * math.sin(4 * (x + 1.6)) * min(1, (x + 1.6) / 0.8), 0]) for x in xs])
        photons = VGroup(*[self.paquet([0.2 + 1.35 * k, -1.55, 0], lam=0.3, larg=0.45, amp=0.16, col=PHOT_C) for k in range(5)])
        l_o = tx("une onde ?", 26, ONDE_C).next_to(onde, UP, buff=0.15).align_to(onde, RIGHT)
        l_p = tx("des particules ?", 26, PHOT_C).next_to(photons, DOWN, buff=0.25).align_to(photons, RIGHT)
        self.p(Write(t1), rt=1.0)
        self.p(FadeIn(t2, shift=UP * 0.2), rt=0.6)
        self.p(Create(faisceau), FadeIn(halo), rt=0.8)
        self.p(Create(onde), FadeIn(l_o), rt=1.2)
        self.p(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.6) for p in photons], lag_ratio=0.2), FadeIn(l_p), rt=1.2)
        rep = tx("… les deux !", 34, JAUNE_L, bold=True).move_to([3.0, -2.6, 0])
        self.at(T["intro"] + 5.8)
        self.p(Write(rep), rt=0.8)
        self.hdr_ex = tx("La lumière : modèles ondulatoire et particulaire", 20, SOFT).to_corner(UL, buff=0.3)
        self.at(T["o1"] - 1.1)
        self.p(ReplacementTransform(t1, self.hdr_ex), FadeOut(VGroup(t2, faisceau, halo, onde, photons, l_o, l_p, rep)), rt=1.0)

    # =================================================================
    #  1. LE MODÈLE ONDULATOIRE (onde électromagnétique en 3D, puis à plat)
    # =================================================================
    def onde(self):
        self.at(T["o1"])
        self.set_q("1. Le modèle ondulatoire")
        A = 1.0
        O = np.array([0.0, -0.3, 0])
        k3 = 2 * PI / 2.6
        k = ValueTracker(k3)
        cv = 1.4
        etat = {"phase": 0.0}

        # la phase avance au rythme ω = k·c : changer k ne fait que resserrer l'onde, sans à-coup
        def avance(m, dt):
            etat["phase"] += k.get_value() * cv * dt
        porteur = Dot(radius=0.001, fill_opacity=0, stroke_width=0)
        porteur.add_updater(avance)
        self.add(porteur)

        def onde2d():
            kk, ph = k.get_value(), etat["phase"]
            m = VMobject(stroke_color=ONDE_C, stroke_width=4)
            m.set_points_smoothly([O + np.array([x, A * math.sin(kk * x - ph), 0]) for x in np.linspace(-5.2, 5.2, 220)])
            return m
        o2 = always_redraw(onde2d)
        axe = Arrow(O + LEFT * 5.4, O + RIGHT * 5.6, buff=0, color=SOFT, stroke_width=2, max_tip_length_to_length_ratio=0.02)
        prop = Arrow(O + np.array([2.6, -A - 0.55, 0]), O + np.array([4.6, -A - 0.55, 0]), buff=0, color=WHITE, stroke_width=3)
        l_prop = txm(r"propagation à la célérité $c$", 22, WHITE).next_to(prop, LEFT, buff=0.2)
        cval = row(mx("c", WHITE, 40), mx("=", WHITE, 40), val(r"3{,}00\times10^{8}", r"\mathrm{m\cdot s^{-1}}", JAUNE_L, 40), buff=0.15)
        cval.to_corner(UR, buff=0.4).shift(DOWN * 0.5)
        titre_o = tx("onde électromagnétique", 26, ONDE_C, bold=True).to_corner(UL, buff=0.4).shift(DOWN * 0.6)
        self.add(o2)
        self.p(GrowArrow(axe), Create(o2), FadeIn(titre_o), rt=1.6)
        self.p(GrowArrow(prop), FadeIn(l_prop), rt=0.8)
        self.p(Write(cval), rt=1.2)
        self.pause(2.0)

        def cretes():
            kk, ph = k.get_value(), etat["phase"]
            n0 = math.ceil((kk * (-3.0) + ph - PI / 2) / TAU)
            x1 = (PI / 2 + TAU * n0 + ph) / kk
            return x1, x1 + TAU / kk

        def fleche_lambda():
            x1, x2 = cretes()
            y = O[1] + A + 0.35
            return VGroup(DoubleArrow(np.array([x1, y, 0]), np.array([x2, y, 0]), buff=0, color=LAM_C, stroke_width=3, tip_length=0.18),
                          DashedLine(np.array([x1, O[1] + A, 0]), np.array([x1, y + 0.15, 0]), color=LAM_C, stroke_width=1.5),
                          DashedLine(np.array([x2, O[1] + A, 0]), np.array([x2, y + 0.15, 0]), color=LAM_C, stroke_width=1.5),
                          mx(r"\lambda", LAM_C, 40).move_to(np.array([(x1 + x2) / 2, y + 0.4, 0])))
        self.at(T["o2"])
        fl = always_redraw(fleche_lambda)
        d_l = tx("longueur d'onde λ : distance entre deux crêtes (en m)", 22, LAM_C).to_edge(DOWN, buff=0.55)
        self.p(FadeOut(VGroup(prop, l_prop)), FadeIn(fl), rt=0.8)
        self.p(FadeIn(d_l, shift=UP * 0.1), rt=0.6)
        # fréquence : un point qui monte et descend
        self.at(T["o3"])
        x_p = 0.0
        pt = always_redraw(lambda: Dot(O + np.array([x_p, A * math.sin(k.get_value() * x_p - etat["phase"]), 0]), radius=0.11, color=NU_C))
        guide_ = DashedLine(O + np.array([x_p, -A - 0.2, 0]), O + np.array([x_p, A + 0.1, 0]), color=NU_C, stroke_width=1.5)
        d_n = tx("fréquence ν : nombre d'oscillations par seconde (en Hz)", 22, NU_C).move_to(d_l)
        self.p(FadeIn(guide_), FadeIn(pt), ReplacementTransform(d_l, d_n), rt=0.8)
        # relation λ = c / ν, puis on augmente la fréquence LENTEMENT
        self.at(T["o4"])
        rel = row(mx(r"\lambda", LAM_C, 52), mx("=", WHITE, 52), frac(mx("c", WHITE, 52), mx(r"\nu", NU_C, 52)), buff=0.18)
        rel.move_to(cval, aligned_edge=UR)
        cad = SurroundingRectangle(rel, color=BOX, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.p(FadeOut(cval), Write(rel), rt=1.2)
        self.p(Create(cad), rt=0.5)
        tend = VGroup(mx(r"\nu \nearrow", NU_C, 36), mx(r"\Rightarrow", WHITE, 36), mx(r"\lambda \searrow", LAM_C, 36)).arrange(RIGHT, buff=0.2)
        tend.next_to(cad, DOWN, buff=0.35)
        self.p(k.animate.set_value(k3 * 1.8), FadeIn(tend, shift=UP * 0.1), rt=4.5)
        self.pause(1.0)
        for m in (o2, fl, pt):
            m.clear_updaters()
        porteur.clear_updaters()
        self.remove(porteur)
        self.vider()

    # =================================================================
    #  Exemple : le wifi (rédaction)
    # =================================================================
    def wifi(self):
        self.at(T["w1"])
        self.question(r"Le wifi émet à $\nu = 2{,}4$ GHz. Quelle est la longueur d'onde $\lambda$ de ces ondes ?")
        fs = 44
        E = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), frac(mx("c", WHITE, fs), mx(r"\nu", NU_C, fs)), buff=0.15)
        conv = row(mx(r"\nu", NU_C, 36), mx("=", WHITE, 36), val(r"2{,}4", r"\mathrm{GHz}", NU_C, 36), mx("=", WHITE, 36),
                   val(r"2{,}4\times10^{9}", r"\mathrm{Hz}", NU_C, 36), buff=0.15)
        AN = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs),
                 frac(val(r"3{,}00\times10^{8}", (r"\mathrm{m}\cdot", r"\mathrm{s^{-1}}"), WHITE, fs), val(r"2{,}4\times10^{9}", r"\mathrm{Hz}", NU_C, fs)),
                 buff=0.15)
        RR = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), val(r"0{,}13", r"\mathrm{m}", RES, fs + 4), mx(r"\approx", WHITE, fs),
                 val("13", r"\mathrm{cm}", RES, fs), buff=0.15)
        page = VGroup(row(E, conv, buff=1.4), AN, RR).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
        self.caser(page, top=self.haut() - 0.6, x=-0.6, w=11.0)
        wifi = self.icone_wifi(np.array([5.4, 0.3, 0]), WHITE, 1.6)
        self.p(FadeIn(wifi), rt=0.6)
        self.p(Write(E), rt=1.2)
        self.encadre(E)
        self.at(T["w2"])
        self.p(Write(conv), rt=1.2)
        self.tag_an(AN)
        self.p(FadeIn(VGroup(AN[0], AN[1], AN[2][1], AN[2][0])), rt=0.8)
        self.morph([(conv[4], AN[2][2])], rt=1.0)
        self.pause(2.0)
        self.p(Indicate(VGroup(AN[2][0][1][1], AN[2][2][1]), color=UNIT), rt=0.8)
        tx_u = mx(r"\mathrm{s^{-1}} = \mathrm{Hz}", UNIT, 30).next_to(AN, RIGHT, buff=0.6)
        self.p(FadeIn(tx_u), rt=0.5)
        self.barrer(AN[2][0][1][1], AN[2][2][1])
        self.at(T["w3"])
        self.p(Write(RR), rt=1.2)
        self.p(Circumscribe(RR[2], color=RES), rt=0.8)
        self.pause(3.0)
        self.reponse("Les ondes wifi ont une longueur d'onde d'environ 13 cm : de l'ordre de la dizaine de centimètres.")
        self.pause(2.0)
        self.vider_tout()
        self.cur_q = None

    # =================================================================
    #  2. LE SPECTRE DES ONDES ÉLECTROMAGNÉTIQUES
    # =================================================================
    def spectre_em(self):
        self.at(T["s1"])
        self.set_q("2. Le spectre électromagnétique")
        x0, x1 = -6.2, 6.2
        e0, e1 = -12, 2
        X = lambda e: x0 + (x1 - x0) * (e - e0) / (e1 - e0)
        y0, h = 0.6, 1.1
        cadre = Rectangle(width=x1 - x0, height=h, stroke_color=WHITE, stroke_width=2).move_to([0, y0, 0])
        grad = VGroup()
        for e in range(e0, e1 + 1, 2):
            grad.add(Line([X(e), y0 - h / 2, 0], [X(e), y0 - h / 2 - 0.12, 0], color=WHITE, stroke_width=2))
            grad.add(mx(r"10^{%d}" % e if e != 0 else "1", SOFT, 26).next_to([X(e), y0 - h / 2 - 0.12, 0], DOWN, buff=0.08))
        unite = mx(r"\lambda\ (\mathrm{m})", LAM_C, 30).next_to([x1, y0 - h / 2 - 0.12, 0], DOWN, buff=0.08).shift(RIGHT * 0.1 + DOWN * 0.45)
        doms = [("Rayons X", -11, -8, "#C8D7F5"), ("UV", -8, math.log10(4e-7), "#D2DEEE"), ("IR", math.log10(8e-7), -3, "#F2CBCB"),
                ("Micro-ondes", -3, -1, "#FCE4CC"), ("Ondes radio", -1, 2, "#D8EAD3")]
        rects = {}
        for nom, a, b, col in doms:
            r = Rectangle(width=X(b) - X(a), height=h, stroke_width=1.5, stroke_color=WHITE, fill_color=col, fill_opacity=0.85)
            r.move_to([(X(a) + X(b)) / 2, y0, 0])
            t = tx(nom, 20, BLACK).move_to(r)
            if t.width > r.width - 0.1:
                t.scale_to_fit_width(r.width - 0.1)
            rects[nom] = VGroup(r, t)
        a_v, b_v = math.log10(4e-7), math.log10(8e-7)
        arc_en_ciel = VGroup(*[Rectangle(width=(X(b_v) - X(a_v)) / 20 + 0.005, height=h, stroke_width=0,
                                         fill_color=wl_color(400 + 20 * i + 10), fill_opacity=1)
                               .move_to([X(a_v) + (X(b_v) - X(a_v)) * (i + 0.5) / 20, y0, 0]) for i in range(20)])
        self.p(Create(cadre), FadeIn(grad), FadeIn(unite), rt=1.0)
        self.p(FadeIn(arc_en_ciel), rt=0.8)
        self.p(Flash(arc_en_ciel.get_center(), color=WHITE, flash_radius=0.5), rt=0.6)
        # zoom sur le visible
        zoom = VGroup(*[Rectangle(width=0.4, height=0.55, stroke_width=0, fill_color=wl_color(400 + 20 * i + 10), fill_opacity=1)
                        for i in range(20)]).arrange(RIGHT, buff=0).move_to([0, -1.55, 0])
        z_l = VGroup(mx(r"400\ \mathrm{nm}", SOFT, 26).next_to(zoom, LEFT, buff=0.2), mx(r"800\ \mathrm{nm}", SOFT, 26).next_to(zoom, RIGHT, buff=0.2),
                     tx("visible", 22, WHITE).next_to(zoom, DOWN, buff=0.12))
        y_l = y0 - h / 2 - 0.75
        liens = VGroup(DashedLine([arc_en_ciel.get_left()[0], y_l, 0], zoom.get_corner(UL), color=SOFT, stroke_width=1.5),
                       DashedLine([arc_en_ciel.get_right()[0], y_l, 0], zoom.get_corner(UR), color=SOFT, stroke_width=1.5))
        self.p(Create(liens), TransformFromCopy(arc_en_ciel, zoom), FadeIn(z_l), rt=1.2)
        # les domaines un par un
        icones = {
            "Rayons X": tx("radiographie", 18, "#C8D7F5"),
            "UV": tx("bronzage", 18, "#D2DEEE"),
            "IR": tx("télécommande", 18, "#F2CBCB"),
            "Micro-ondes": tx("four, wifi", 18, "#FCE4CC"),
            "Ondes radio": tx("radio FM, TV", 18, "#D8EAD3"),
        }
        hauts = {"Rayons X": 1.55, "UV": 1.95, "IR": 1.55, "Micro-ondes": 1.95, "Ondes radio": 1.55}
        for nom in icones:
            icones[nom].move_to([rects[nom].get_x(), y0 + h / 2 + hauts[nom] - 0.9, 0])
        for cle, noms in (("s2", ["Rayons X"]), ("s3", ["UV"]), ("s5", ["IR"]), ("s6", ["Micro-ondes"]), ("s7", ["Ondes radio"])):
            self.at(T[cle])
            for nom in noms:
                self.p(FadeIn(rects[nom], shift=DOWN * 0.15), rt=0.7)
                self.p(FadeIn(icones[nom], shift=DOWN * 0.1), rt=0.5)
            if cle == "s3":
                self.at(T["s4"])
                self.p(Indicate(zoom, scale_factor=1.06), rt=1.2)
        # sens de variation
        self.at(T["s8"])
        y_f = -2.75
        f1 = Arrow([1.0, y_f, 0], [6.0, y_f, 0], buff=0, color=LAM_C, stroke_width=3)
        f2 = Arrow([-1.0, y_f, 0], [-6.0, y_f, 0], buff=0, color=NU_C, stroke_width=3)
        l1 = txm(r"$\lambda$ croissante", 22, LAM_C).next_to(f1, DOWN, buff=0.08)
        l2 = txm(r"$\nu$ et énergie du photon croissantes", 22, NU_C).next_to(f2, DOWN, buff=0.08)
        self.p(FadeOut(VGroup(zoom, z_l, liens)), rt=0.5)
        self.p(GrowArrow(f1), FadeIn(l1), rt=0.8)
        self.p(GrowArrow(f2), FadeIn(l2), rt=0.8)
        self.pause(3.0)
        self.p(Indicate(rects["Rayons X"], color=NU_C, scale_factor=1.05), rt=1.0)
        self.pause(3.0)
        self.vider()

    # =================================================================
    #  3. LE MODÈLE PARTICULAIRE : LE PHOTON
    # =================================================================
    def photon(self):
        self.at(T["p1"])
        self.set_q("3. Le modèle particulaire")
        y = 1.0
        xs = np.linspace(-6.5, 6.5, 300)
        onde = VMobject(stroke_color=JAUNE_L, stroke_width=4)
        onde.set_points_smoothly([np.array([x, y + 0.35 * math.sin(TAU * x / 0.6), 0]) for x in xs])
        self.p(Create(onde), rt=1.2)
        paquets = VGroup(*[self.paquet([-5.4 + 2.2 * i, y, 0], lam=0.6, larg=0.75, amp=0.35, col=JAUNE_L) for i in range(6)])
        self.p(ReplacementTransform(onde, paquets), rt=1.6)
        self.p(paquets.animate.shift(RIGHT * 1.5), rt=1.5, rate_func=linear)
        l_ph = tx("des photons : sans masse, chacun porte une énergie précise", 22, JAUNE_L).next_to(paquets, DOWN, buff=0.35)
        self.p(FadeIn(l_ph), rt=0.6)
        # E = h ν
        self.at(T["p2"])
        fs = 52
        E1 = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx(r"\nu", NU_C, fs), buff=0.15)
        E1.move_to([-2.6, -1.2, 0])
        self.p(FadeOut(VGroup(paquets, l_ph)), Write(E1), rt=1.4)
        cad = SurroundingRectangle(E1, color=BOX, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.p(Create(cad), rt=0.5)
        hval = row(mx("h", H_C, 34), mx("=", WHITE, 34), val(r"6{,}63\times10^{-34}", r"\mathrm{J\cdot s}", H_C, 34), buff=0.12)
        hval.next_to(cad, DOWN, buff=0.35).align_to(cad, LEFT)
        nom_h = tx("constante de Planck", 20, H_C).next_to(hval, DOWN, buff=0.1).align_to(hval, LEFT)
        self.p(FadeIn(hval, shift=UP * 0.1), FadeIn(nom_h), rt=0.8)
        self.pause(2.0)
        # E = h c / λ
        self.at(T["p3"])
        rel = row(mx(r"\nu", NU_C, 40), mx("=", WHITE, 40), frac(mx("c", WHITE, 40), mx(r"\lambda", LAM_C, 40)), buff=0.12)
        rel.next_to(cad, RIGHT, buff=0.9)
        E2 = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), frac(row(mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx("c", WHITE, fs), buff=0.1),
                                                                  mx(r"\lambda", LAM_C, fs)), buff=0.15)
        E2.next_to(rel, RIGHT, buff=0.9)
        ajuster(VGroup(cad, rel, E2), 13.0)
        self.p(FadeIn(rel, shift=LEFT * 0.2), rt=0.8)
        self.morph([(E1[0], E2[0]), (E1[2], E2[2][0][0]), (rel[2][0], E2[2][0][2]), (rel[2][2], E2[2][2])],
                   FadeIn(VGroup(E2[1], E2[2][0][1], E2[2][1])), rt=1.8)
        cad2 = SurroundingRectangle(E2, color=BOX, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.p(Create(cad2), rt=0.5)
        self.pause(2.0)
        # deux photons : rouge et violet
        ph_r = self.paquet([-3.0, 1.6, 0], lam=0.7, larg=1.3, amp=0.3, col="#FF4040")
        ph_v = self.paquet([2.4, 1.6, 0], lam=0.3, larg=1.3, amp=0.3, col="#9B6BFF")
        def jauge(c, f, col):
            fond = RoundedRectangle(corner_radius=0.06, width=2.2, height=0.22, stroke_color=SOFT, stroke_width=1.2).move_to(c)
            bar = Rectangle(width=2.2 * f, height=0.16, stroke_width=0, fill_color=col, fill_opacity=0.9).move_to(fond.get_left(), aligned_edge=LEFT).shift(RIGHT * 0.03)
            return VGroup(fond, bar)
        j_r = jauge([-3.0, 0.85, 0], 0.4, "#FF4040")
        j_v = jauge([2.4, 0.85, 0], 0.85, "#9B6BFF")
        l_r = tx("rouge : λ grande, E petite", 20, "#FF4040").next_to(j_r, DOWN, buff=0.12)
        l_v = tx("ultraviolet : λ petite, E grande", 20, "#9B6BFF").next_to(j_v, DOWN, buff=0.12)
        self.p(FadeIn(ph_r, shift=RIGHT * 0.3), FadeIn(ph_v, shift=RIGHT * 0.3), rt=0.8)
        self.p(GrowFromEdge(j_r, LEFT), GrowFromEdge(j_v, LEFT), FadeIn(l_r), FadeIn(l_v), rt=1.2)
        self.pause(4.0)
        self.vider()

    # =================================================================
    #  Exemple : énergie d'un photon (rédaction)
    # =================================================================
    def calcul_photon(self):
        self.at(T["e1"])
        self.question(r"Quelle est l'énergie d'un photon de longueur d'onde $\lambda = 600$ nm ?")
        fs = 44
        E = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), frac(row(mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx("c", WHITE, fs), buff=0.1),
                                                                 mx(r"\lambda", LAM_C, fs)), buff=0.15)
        conv = row(mx(r"\lambda", LAM_C, 36), mx("=", WHITE, 36), val("600", r"\mathrm{nm}", LAM_C, 36), mx("=", WHITE, 36),
                   val(r"600\times10^{-9}", r"\mathrm{m}", LAM_C, 36), buff=0.15)
        num = row(val(r"6{,}63\times10^{-34}", (r"\mathrm{J}\cdot", r"\mathrm{s}"), H_C, fs), mx(r"\times", WHITE, fs),
                  val(r"3{,}00\times10^{8}", (r"\mathrm{m}\cdot", r"\mathrm{s^{-1}}"), WHITE, fs), buff=0.12)
        den = val(r"600\times10^{-9}", r"\mathrm{m}", LAM_C, fs)
        AN = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), frac(num, den), buff=0.15)
        RR = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), val(r"3{,}32\times10^{-19}", r"\mathrm{J}", RES, fs + 4), buff=0.15)
        page = VGroup(row(E, conv, buff=1.4), AN, RR).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
        self.caser(page, top=self.haut() - 0.6, x=0.0, w=12.0)
        self.p(Write(E), rt=1.2)
        self.encadre(E)
        self.pause(1.0)
        self.at(T["e2"])
        self.p(Write(conv), rt=1.4)
        self.p(Circumscribe(conv[4], color=LAM_C), rt=0.8)
        self.tag_an(AN)
        self.p(FadeIn(VGroup(AN[0], AN[1], AN[2][1], num)), rt=0.8)
        self.morph([(conv[4], den)], rt=1.0)
        self.barrer(num[0][1][1], num[2][1][1], num[2][1][0], den[1])
        self.at(T["e3"])
        self.p(Write(RR), rt=1.2)
        self.p(Circumscribe(RR[2], color=RES), rt=0.8)
        self.pause(3.0)
        self.reponse(r"Un photon de 600 nm transporte une énergie $E = 3{,}32\times10^{-19}$ J : une énergie minuscule.")
        self.pause(2.5)
        self.vider_tout()
        self.cur_q = None

    # =================================================================
    #  4. LES NIVEAUX D'ÉNERGIE
    # =================================================================
    def diagramme(self, niveaux, x_g=-5.6, x_d=-0.4, y_bas=-2.2, h=4.4, noms=None, cols=None):
        """niveaux : énergies (unités arbitraires croissantes) → lignes horizontales."""
        e0, e1 = niveaux[0], niveaux[-1]
        Y = lambda e: y_bas + h * (e - e0) / (e1 - e0)
        axe = Arrow([x_g - 0.4, y_bas - 0.25, 0], [x_g - 0.4, y_bas + h + 0.45, 0], buff=0, color=SOFT, stroke_width=2,
                    max_tip_length_to_length_ratio=0.04)
        lab = mx("E", SOFT, 34).next_to(axe.get_end(), LEFT, buff=0.12)
        lignes = VGroup(*[Line([x_g, Y(e), 0], [x_d, Y(e), 0], color=WHITE, stroke_width=4) for e in niveaux])
        etiq = VGroup()
        if noms:
            for e, n, c in zip(niveaux, noms, cols or [WHITE] * len(noms)):
                etiq.add(txm(n, 20, c).next_to([x_d, Y(e), 0], RIGHT, buff=0.15))
        return VGroup(axe, lab, lignes, etiq), Y

    def niveaux(self):
        self.at(T["n1"])
        self.set_q("4. Les niveaux d'énergie")
        niv = [0.0, 2.6, 4.0]
        diag, Y = self.diagramme(niv, noms=[r"$E_1$ : état fondamental", r"$E_2$ : état excité", r"$E_3$ : état excité"],
                                 cols=[RES, WHITE, WHITE])
        self.p(GrowArrow(diag[0]), FadeIn(diag[1]), rt=0.6)
        self.p(LaggedStart(*[Create(l) for l in diag[2]], lag_ratio=0.3), rt=1.4)
        quant = ajuster(tx("énergie quantifiée : seules ces valeurs sont possibles", 22, SOFT), 6.0).move_to([3.7, 2.95, 0])
        self.p(FadeIn(quant), rt=0.6)
        self.at(T["n2"])
        self.p(FadeIn(diag[3][0], shift=LEFT * 0.2), rt=0.6)
        self.p(FadeIn(diag[3][1:], shift=LEFT * 0.2), rt=0.8)
        xa = -3.2
        etat = Dot([xa, Y(0.0), 0], radius=0.14, color=JAUNE_L).set_sheen(-0.3, DR)
        glow = Circle(radius=0.28, stroke_width=0, fill_color=JAUNE_L, fill_opacity=0.25).move_to(etat)
        atome = VGroup(glow, etat)
        self.p(GrowFromCenter(atome), rt=0.6)
        # absorption
        self.at(T["n3"])
        ph = self.paquet([-7.4, Y(1.3), 0], lam=0.35, larg=0.6, amp=0.2, col=ABS_C)
        self.p(ph.animate.move_to([xa - 0.4, Y(0.0) + 0.35, 0]), rt=1.6, rate_func=linear)
        f_abs = Arrow([xa - 0.45, Y(0.0), 0], [xa - 0.45, Y(2.6), 0], buff=0.05, color=ABS_C, stroke_width=6)
        self.p(FadeOut(ph, scale=0.3), atome.animate.move_to([xa, Y(2.6), 0]), GrowArrow(f_abs), rt=1.0)
        l_abs = tx("absorption", 22, ABS_C).next_to(f_abs, LEFT, buff=0.1).shift(DOWN * 0.6)
        self.p(FadeIn(l_abs), rt=0.5)
        self.p(Flash(atome, color=ABS_C, flash_radius=0.4), rt=0.6)
        # émission
        self.at(T["n4"])
        # un autre atome, déjà dans l'état excité E3 (l'atome précédent s'efface : pas de saut sans photon)
        atome2 = atome.copy().move_to([xa + 1.0, Y(4.0), 0])
        l_autre = txm(r"un atome dans l'état excité $E_3$", 20, EM_C).next_to(atome2, UP, buff=0.2)
        self.p(FadeOut(atome, scale=0.5), rt=0.4)
        self.p(FadeIn(atome2, scale=1.6), FadeIn(l_autre, shift=DOWN * 0.1), rt=0.6)
        atome = atome2
        f_em = Arrow([xa + 1.45, Y(4.0), 0], [xa + 1.45, Y(0.0), 0], buff=0.05, color=EM_C, stroke_width=6)
        ph2 = self.paquet([xa + 1.6, Y(1.6), 0], lam=0.28, larg=0.6, amp=0.2, col=EM_C)
        self.p(atome.animate.move_to([xa + 1.0, Y(0.0), 0]), GrowArrow(f_em), FadeIn(ph2), FadeOut(l_autre), rt=1.0)
        l_em = tx("émission", 22, EM_C).next_to(f_em, RIGHT, buff=0.1).shift(UP * 1.1)
        self.p(ph2.animate.move_to([6.6, Y(1.6), 0]), FadeIn(l_em), rt=1.6, rate_func=linear)
        self.remove(ph2)
        # ΔE = h ν
        self.at(T["n5"])
        de = DoubleArrow([-1.0, Y(0.0), 0], [-1.0, Y(2.6), 0], buff=0, color=BOX, stroke_width=3, tip_length=0.18)
        l_de = mx(r"\Delta E", BOX, 34).next_to(de, RIGHT, buff=0.1)
        self.p(FadeOut(quant), GrowFromCenter(de), FadeIn(l_de), rt=0.8)
        fs = 44
        regle = row(mx(r"\Delta E", BOX, fs), mx("=", WHITE, fs), mx(r"E_{\text{sup}} - E_{\text{inf}}", WHITE, fs), mx("=", WHITE, fs),
                    mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx(r"\nu", NU_C, fs), buff=0.12)
        ajuster(regle, 6.0)
        regle.move_to([3.7, -0.15, 0])
        cadr = SurroundingRectangle(regle, color=BOX, buff=0.2, corner_radius=0.1, stroke_width=3)
        self.p(Write(regle), rt=1.6)
        self.p(Create(cadr), rt=0.5)
        cons = ajuster(tx("énergie du photon = écart entre les deux niveaux", 22, BOX), 6.0).next_to(cadr, DOWN, buff=0.3)
        self.p(FadeIn(cons), rt=0.6)
        # photon non absorbé
        self.at(T["n6"])
        self.p(FadeOut(VGroup(f_abs, f_em, l_abs, l_em, cons)), rt=0.4)
        ph3 = self.paquet([-7.4, Y(1.0), 0], lam=0.5, larg=0.6, amp=0.2, col=SOFT)
        self.p(ph3.animate.move_to([xa + 0.4, Y(1.0), 0]), rt=1.2, rate_func=linear)
        self.p(Wiggle(atome), rt=0.5)
        self.p(ph3.animate.move_to([6.6, Y(1.0), 0]), rt=1.4, rate_func=linear)
        non = ajuster(tx("ne correspond à aucun écart : pas absorbé", 22, "#FF5555"), 6.0).move_to([3.7, -1.85, 0])
        self.p(FadeIn(non), rt=0.5)
        self.remove(ph3)
        self.pause(2.0)
        self.vider()

    # =================================================================
    #  5. LE SPECTRE DE RAIES (hydrogène)
    # =================================================================
    def raies(self):
        self.at(T["r1"])
        self.set_q("5. Le spectre de raies")
        # niveaux de l'hydrogène (en 10^-19 J), E1 hors champ
        En = {2: -5.45, 3: -2.42, 4: -1.36, 5: -0.87, 6: -0.61}
        y_b, hh = -2.0, 4.2
        Y = lambda e: y_b + hh * (e - En[2]) / (0 - En[2])
        axe = Arrow([-6.3, y_b - 0.5, 0], [-6.3, y_b + hh + 0.4, 0], buff=0, color=SOFT, stroke_width=2, max_tip_length_to_length_ratio=0.04)
        lab = mx(r"E\ (10^{-19}\ \mathrm{J})", SOFT, 28).next_to(axe.get_end(), RIGHT, buff=0.1)
        lignes = VGroup()
        etiq = VGroup()
        for n, e in En.items():
            lignes.add(Line([-5.9, Y(e), 0], [-1.4, Y(e), 0], color=WHITE, stroke_width=3.5))
            if n <= 4:
                etiq.add(mx(r"E_%d = %s" % (n, ("%.2f" % e).replace(".", "{,}")), WHITE, 24).next_to([-1.4, Y(e), 0], RIGHT, buff=0.12))
        etiq.add(tx("…", 22, WHITE).next_to([-1.4, Y(-0.7), 0], RIGHT, buff=0.15))
        coupure = VGroup(Line([-6.45, y_b - 0.32, 0], [-6.15, y_b - 0.22, 0], color=SOFT), Line([-6.45, y_b - 0.42, 0], [-6.15, y_b - 0.32, 0], color=SOFT))
        l1 = txm(r"($E_1 = -21{,}8$, plus bas)", 18, SOFT).move_to([-3.6, y_b - 0.5, 0])
        titre_h = tx("atome d'hydrogène", 22, JAUNE_L, bold=True).move_to([-2.4, y_b + hh + 0.45, 0])
        self.p(GrowArrow(axe), FadeIn(lab), FadeIn(titre_h), LaggedStart(*[Create(l) for l in lignes], lag_ratio=0.15),
               FadeIn(etiq), FadeIn(coupure), FadeIn(l1), rt=1.2)
        # spectre (bande noire 380–700 nm)
        sx0, sx1, sy = 1.4, 6.6, 1.1
        Xs = lambda wl: sx0 + (sx1 - sx0) * (wl - 380) / (700 - 380)
        bande = Rectangle(width=sx1 - sx0, height=1.3, stroke_color=SOFT, stroke_width=1.5, fill_color=BLACK, fill_opacity=1).move_to([(sx0 + sx1) / 2, sy, 0])
        fond_c = VGroup(*[Rectangle(width=(sx1 - sx0) / 32 + 0.005, height=0.12, stroke_width=0, fill_color=wl_color(380 + 10 * i + 5), fill_opacity=0.9)
                          .move_to([Xs(380 + 10 * i + 5), sy - 0.8, 0]) for i in range(32)])
        gr = VGroup(*[mx(r"%d" % w, SOFT, 22).next_to([Xs(w), sy - 0.86, 0], DOWN, buff=0.06) for w in (400, 500, 600, 700)])
        t_s = tx("spectre d'émission", 22, WHITE).next_to(bande, UP, buff=0.15)
        u_s = mx(r"\lambda\ (\mathrm{nm})", SOFT, 24).next_to(gr, DOWN, buff=0.12).align_to(bande, RIGHT)
        self.p(FadeIn(bande), FadeIn(fond_c), FadeIn(gr), FadeIn(t_s), FadeIn(u_s), rt=0.6)
        trans = [(3, 656), (4, 486), (5, 434), (6, 410)]
        xa = [-4.8, -4.0, -3.2, -2.4]
        for (n, wl), x in zip(trans, xa):
            col = wl_color(wl)
            f = Arrow([x, Y(En[n]), 0], [x, Y(En[2]), 0], buff=0.03, color=col, stroke_width=5)
            raie = Rectangle(width=0.06, height=1.3, stroke_width=0, fill_color=col, fill_opacity=1).move_to([Xs(wl), sy, 0])
            halo_r = raie.copy().set_fill(col, 0.3).stretch(4, 0)
            self.p(GrowArrow(f), rt=0.3)
            self.p(TransformFromCopy(f, raie, path_arc=-0.6), FadeIn(halo_r), rt=0.45)
            if n == 3:
                self.f_rouge = f
                self.raie_rouge = VGroup(raie, halo_r)
        empreinte = ajuster(tx("chaque élément a ses raies : son « empreinte digitale »", 22, JAUNE_L), 5.4).move_to([4.0, -1.6, 0])
        self.p(FadeIn(empreinte, shift=UP * 0.1), rt=0.6)
        self.at(T["h1"] - 0.5)
        self.vider(rt=0.5)

    def calcul_hydrogene(self):
        self.at(T["h1"])
        self.question([r"Hydrogène : la transition $E_3 \to E_2$ libère un photon d'énergie $\Delta E = 3{,}03\times10^{-19}$ J.",
                       r"Quelle est sa longueur d'onde $\lambda$ ?"])
        fs = 44
        d1 = row(mx(r"\Delta E", BOX, fs), mx("=", WHITE, fs), frac(row(mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx("c", WHITE, fs), buff=0.1),
                                                                     mx(r"\lambda", LAM_C, fs)), buff=0.15)
        E = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), frac(row(mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx("c", WHITE, fs), buff=0.1),
                                                                     mx(r"\Delta E", BOX, fs)), buff=0.15)
        tete = row(d1, mx(r"\Longrightarrow", SOFT, fs), E, buff=0.6)
        num = row(val(r"6{,}63\times10^{-34}", (r"\mathrm{J}", r"\cdot\mathrm{s}"), H_C, fs), mx(r"\times", WHITE, fs),
                  val(r"3{,}00\times10^{8}", (r"\mathrm{m}\cdot", r"\mathrm{s^{-1}}"), WHITE, fs), buff=0.12)
        den = val(r"3{,}03\times10^{-19}", r"\mathrm{J}", BOX, fs)
        AN = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), frac(num, den), buff=0.15)
        RR = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), val(r"6{,}56\times10^{-7}", r"\mathrm{m}", RES, fs + 4), mx("=", WHITE, fs),
                 val("656", r"\mathrm{nm}", RES, fs), buff=0.15)
        page = VGroup(tete, AN, RR).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
        self.caser(page, top=self.haut() - 0.6, x=-0.4, w=11.6)
        self.p(Write(d1), rt=1.4)
        self.at(T["h2"])
        self.p(FadeIn(tete[1]), rt=0.3)
        self.morph([(d1[2][2], E[0]), (d1[0], E[2][2]), (d1[2][0], E[2][0])], FadeIn(VGroup(E[1], E[2][1])), rt=1.6)
        self.encadre(E)
        self.at(T["h3"])
        self.tag_an(AN)
        self.p(FadeIn(VGroup(AN[0], AN[1], AN[2][1], num, den)), rt=1.0)
        self.barrer(num[0][1][0], den[1], num[0][1][1], num[2][1][1])
        self.p(Write(RR), rt=1.2)
        self.at(T["h4"])
        raie = Rectangle(width=0.12, height=1.1, stroke_width=0, fill_color=wl_color(656), fill_opacity=1).next_to(RR, RIGHT, buff=0.8)
        halo_r = raie.copy().set_fill(wl_color(656), 0.3).stretch(4, 0)
        self.p(Circumscribe(RR[4], color=RES), FadeIn(raie), FadeIn(halo_r), rt=1.0)
        self.reponse(r"La transition $E_3 \to E_2$ de l'hydrogène émet une lumière rouge, de longueur d'onde 656 nm.")
        self.pause(1.6)
        self.vider_tout()
        self.cur_q = None

    # =================================================================
    #  6. CONCLUSION
    # =================================================================
    def conclusion(self):
        self.at(T["c1"])
        if self.hdr_q is not None:
            self.p(FadeOut(self.hdr_q), rt=0.3)
            self.hdr_q = None
        t = tx("À retenir", 42, WHITE, bold=True).move_to(UP * 2.6)
        fs = 46
        r1 = row(mx(r"\lambda", LAM_C, fs), mx("=", WHITE, fs), frac(mx("c", WHITE, fs), mx(r"\nu", NU_C, fs)), buff=0.15)
        r2 = row(mx("E", PHOT_C, fs), mx("=", WHITE, fs), mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx(r"\nu", NU_C, fs), buff=0.15)
        r3 = row(mx(r"\Delta E", BOX, fs), mx("=", WHITE, fs), mx(r"E_{\text{sup}} - E_{\text{inf}}", WHITE, fs), mx("=", WHITE, fs),
                 mx("h", H_C, fs), mx(r"\times", WHITE, fs), mx(r"\nu", NU_C, fs), buff=0.12)
        b1 = self.bloc("onde", r1, ONDE_C)
        b2 = self.bloc("photon", r2, PHOT_C)
        b3 = self.bloc("transition entre niveaux", r3, BOX)
        haut_ = VGroup(b1, b2).arrange(RIGHT, buff=1.2)
        g = VGroup(haut_, b3).arrange(DOWN, buff=0.75).move_to(DOWN * 0.1)
        ajuster(g, 12.5, 4.6)
        self.p(Write(t), rt=0.8)
        self.p(FadeIn(b1, shift=UP * 0.15), rt=0.8)
        self.p(FadeIn(b2, shift=UP * 0.15), rt=0.8)
        self.at(T["c2"])
        self.p(FadeIn(b3, shift=UP * 0.15), rt=0.8)
        self.at(T["c3"])
        unites = VGroup(tx("Unités :", 24, UNIT, bold=True), mx(r"E\ \text{en J},\quad \nu\ \text{en Hz},\quad \lambda\ \text{en m}", UNIT, 36)).arrange(RIGHT, buff=0.3)
        unites.next_to(g, DOWN, buff=0.45)
        if unites.get_bottom()[1] < -3.5:
            unites.shift(UP * (-3.5 - unites.get_bottom()[1]))
        self.p(FadeIn(unites, shift=UP * 0.1), rt=0.8)
        self.p(Circumscribe(unites, color=UNIT), rt=1.0)
