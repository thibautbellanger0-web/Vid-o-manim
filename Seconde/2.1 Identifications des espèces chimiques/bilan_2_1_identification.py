from manim import *
import math

# =====================================================================
#  BOÎTE À OUTILS – vidéos de correction et de cours (Manim Community 0.22, rendu sur GitHub)
#  Base à copier en tête de chaque nouvelle vidéo : mise en forme, unités, puissances de 10,
#  rédaction (expression littérale encadrée, application numérique, phrase réponse),
#  calage sur le SRT (self.at), sous-titres (self.dire) pour les vidéos autonomes.
#  Pour une nouvelle vidéo : remplir T (débuts des passages lus, d'après le SRT) puis construct().
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
ZONE_BAS = -2.55     # bas de la zone de travail (en dessous : phrase réponse ou sous-titres)
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




# =====================================================================
#  VIDÉO : bilan du chapitre 2.1 (Seconde) – Identification des espèces chimiques
#  Calée sur le SRT de l'enregistrement (6 min 37 s) ; textes en gros, en couleur.
# =====================================================================

# ---------- Couleurs propres à cette vidéo ----------
OR_ = "#FFC83D"      # or, corps pur
N2C = "#4FA3E0"      # diazote
O2C = "#FF6F61"      # dioxygène
AUTRE = "#9AA0A6"    # autres gaz
JAUNE = "#FFD60A"    # colorant jaune
BLEU = "#3A86FF"     # colorant bleu
VERT = "#2DC653"     # sirop de menthe
PLAQUE = "#ECEFF1"   # plaque de CCM
ELUANT = "#9ED8F7"   # éluant
INK = "#111318"
BAD = "#FF5555"

# ---------- Calage sur le SRT (secondes) ----------
T = {
    "titre": 0.00, "question": 7.40, "m1": 10.00, "m2": 13.16, "m3": 16.16,
    "vocab": 18.76, "entites": 21.46, "espece": 27.48, "eau": 32.82, "h2o": 34.98,
    "corps_pur": 38.40, "pepite": 40.62, "melange": 42.94, "ex_mel": 45.28,
    "deux_cas": 48.70, "homogene": 52.12, "homog_ex": 55.48, "hetero": 60.12, "hetero_ex": 63.70,
    "air": 67.20, "air_n2": 70.32, "air_o2": 72.94, "air_autres": 76.14,
    "prop": 79.08, "rho": 86.92, "rho_rel": 90.14, "rho_unites": 94.88, "rho_gl": 98.94,
    "eau_rho": 105.08, "bouteille": 110.34, "ethanol": 115.60, "fer": 120.12, "fer8": 123.42,
    "air_rho": 127.40, "air800": 131.26,
    "ident": 134.06, "liquide": 137.46, "vol50": 142.64, "m395": 145.50,
    "conv": 148.04, "conv2": 149.98, "conv3": 151.40,
    "lit": 153.44, "an": 157.18, "res": 165.80, "ref": 169.06, "rep": 174.78,
    "temp": 178.22, "palier_txt": 183.22, "palier": 188.06, "fusion": 191.50, "ebullition": 194.30,
    "melange_temp": 196.82, "tables": 200.24,
    "tests": 207.36, "t_eau": 215.84, "t_eau_bleu": 221.00, "t_co2": 224.50, "t_co2_trouble": 229.52,
    "t_h2": 233.02, "t_h2_pop": 236.88, "t_o2": 242.52, "t_o2_braise": 247.90, "t_o2_feu": 254.20,
    "ccm": 256.74, "ccm_sigle": 265.10, "ccm_but": 268.32, "sirop": 272.84, "quels": 275.82,
    "plaque": 278.42, "ligne": 281.70, "depots": 286.28, "dep_j": 289.58, "dep_b": 291.00, "dep_s": 292.60,
    "cuve": 294.60, "attention": 298.72, "elution": 302.36, "vitesse": 306.74, "affinite": 308.96,
    "monte_haut": 314.34, "monte_peu": 317.34, "sortie": 320.78, "front": 323.50, "chromato": 325.90,
    "interp": 328.08, "verticale": 330.08, "col_j": 335.64, "col_b": 339.68, "col_s": 341.92,
    "horizontale": 345.70, "meme": 350.92, "ici": 354.88, "ici_b": 358.00, "concl": 360.68, "vert": 365.00,
    "resume": 371.74, "r_mel": 375.12, "r_ident": 377.28, "r_rho": 380.50, "r_temp": 382.20,
    "r_test": 385.46, "r_ccm": 387.46, "r_eau": 389.64, "r_air": 392.52, "fin_audio": 396.96,
}


# ---------- Petits dessins (2D) ----------
def atome(c=CONC, r=0.38):
    return Circle(radius=r, stroke_color=WHITE, stroke_width=2, fill_color=c, fill_opacity=0.9)


def ion(r=0.38):
    a = Circle(radius=r, stroke_color=WHITE, stroke_width=2, fill_color=MAGENTA, fill_opacity=0.9)
    plus = mx("+", WHITE, 44).move_to(a)
    return VGroup(a, plus)


def h2o(s=1.0):
    o = Circle(radius=0.36, stroke_width=0, fill_color=O2C, fill_opacity=1)
    h1 = Circle(radius=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(
        o.get_center() + 0.42 * np.array([math.cos(math.radians(-38)), math.sin(math.radians(-38)), 0]))
    h2 = Circle(radius=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(
        o.get_center() + 0.42 * np.array([math.cos(math.radians(218)), math.sin(math.radians(218)), 0]))
    return VGroup(h1, h2, o).scale(s)


def pepite(s=1.0):
    pts = [[-0.7, -0.3, 0], [-0.5, 0.25, 0], [-0.1, 0.45, 0], [0.45, 0.35, 0], [0.75, -0.05, 0],
           [0.5, -0.42, 0], [-0.2, -0.5, 0]]
    p = Polygon(*pts, stroke_color="#B8860B", stroke_width=3, fill_color=OR_, fill_opacity=1)
    reflet = Polygon([-0.35, 0.15, 0], [-0.1, 0.3, 0], [0.1, 0.18, 0], [-0.2, 0.05, 0], stroke_width=0,
                     fill_color=WHITE, fill_opacity=0.6)
    return VGroup(p, reflet).scale(s)


def boite(particules, w=4.4, h=2.4):
    cadre = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=SOFT, stroke_width=2)
    particules.move_to(cadre)
    return VGroup(cadre, particules)


def grille(fabrique, n_col, n_lig, dx=0.95, dy=0.85):
    g = VGroup()
    for i in range(n_lig):
        for j in range(n_col):
            m = fabrique(i, j)
            m.move_to([j * dx + (0.3 if i % 2 else 0), -i * dy, 0])
            g.add(m)
    return g


def becher(couches, w=2.4, h=2.8):
    """couches : liste de (hauteur, couleur, opacité) du bas vers le haut."""
    g = VGroup()
    y = -h / 2
    for (hc, c, op) in couches:
        r = Rectangle(width=w - 0.08, height=hc, stroke_width=0, fill_color=c, fill_opacity=op)
        r.move_to([0, y + hc / 2 + 0.04, 0])
        g.add(r)
        y += hc
    paroi = VGroup(Line([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0]), Line([-w / 2, -h / 2, 0], [w / 2, -h / 2, 0]),
                   Line([w / 2, -h / 2, 0], [w / 2, h / 2, 0])).set_stroke(WHITE, 4)
    bec = Line([-w / 2, h / 2, 0], [-w / 2 - 0.2, h / 2 + 0.15, 0], color=WHITE, stroke_width=4)
    return VGroup(g, paroi, bec)


def tube(liquide, op=0.5, h=1.9, w=0.55):
    corps = RoundedRectangle(corner_radius=w / 2 - 0.01, width=w, height=h, stroke_color=WHITE, stroke_width=3)
    liq = RoundedRectangle(corner_radius=w / 2 - 0.06, width=w - 0.1, height=h * 0.45, stroke_width=0,
                           fill_color=liquide, fill_opacity=op)
    liq.move_to(corps.get_bottom() + UP * (h * 0.45 / 2 + 0.05))
    return VGroup(corps, liq)


def flamme(s=1.0):
    ext = Ellipse(width=0.42, height=0.8, stroke_width=0, fill_color="#FF8C1A", fill_opacity=1)
    inte = Ellipse(width=0.2, height=0.42, stroke_width=0, fill_color="#FFE066", fill_opacity=1)
    inte.move_to(ext.get_center() + DOWN * 0.12)
    return VGroup(ext, inte).scale(s)


def allumette(braise=True):
    baton = Line([0, -0.9, 0], [0, 0.45, 0], color="#C8A165", stroke_width=10)
    tete = Circle(radius=0.12, stroke_width=0, fill_color="#FF3B30" if braise else "#5A3A2A",
                  fill_opacity=1).move_to([0, 0.52, 0])
    return VGroup(baton, tete)


def bouteille(c=EAU):
    corps = RoundedRectangle(corner_radius=0.15, width=0.8, height=1.3, stroke_color=WHITE, stroke_width=3,
                             fill_color=c, fill_opacity=0.5)
    col = Rectangle(width=0.32, height=0.35, stroke_color=WHITE, stroke_width=3).next_to(corps, UP, buff=0)
    return VGroup(corps, col)


def lignes(*textes, fs=28, c=WHITE, w=LARGEUR, buff=0.14):
    return VGroup(*[tx(t, fs, c, w=w) for t in textes]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def tache(c, w=0.42, h=0.32):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=1)


def axes(xr, yr, xl, yl, centre):
    a = Axes(x_range=xr, y_range=yr, x_length=xl, y_length=yl, tips=True,
             axis_config={"color": SOFT, "stroke_width": 2, "include_ticks": False})
    a.move_to(centre)
    return a


class Correction(Scene):
    # ---------------- Calage sur l'audio ----------------
    def p(self, *anims, rt=1.0, **kw):
        self.play(*anims, run_time=rt, **kw)
        self.t += rt

    def at(self, t):
        if t > self.t + 0.02:
            self.wait(t - self.t)
            self.t = t

    def pause(self, d):
        if d > 0:
            self.wait(d)
            self.t += d

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
        proteges = set()
        for g in (self.hdr_ex, self.hdr_q, *garder):
            if g is not None:
                proteges.update(id(x) for x in g.get_family())
        mobs = [m for m in self.mobjects if id(m) not in proteges]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def titre(self, s, fs=36, c=WHITE, y=2.85):
        t = tx(s, fs, c, bold=True).move_to(UP * y)
        self.p(FadeIn(t, shift=DOWN * 0.15), rt=0.6)
        return t

    def apparait(self, m, rt=0.8, shift=UP * 0.15):
        self.p(FadeIn(m, shift=shift), rt=rt)
        return m

    def encadre(self, eq, rt=1.0):
        rect = SurroundingRectangle(eq, color=BOX, buff=0.2, corner_radius=0.08, stroke_width=4)
        lab = etiquette("Expression littérale", BOX).next_to(rect, UP, buff=0.06).align_to(rect, LEFT)
        self.p(Create(rect), FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return VGroup(rect, lab)

    def tag_an(self, m, rt=0.4):
        lab = etiquette("Application numérique", AN_C).next_to(m, UP, buff=0.08).align_to(m, LEFT)
        self.p(FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return lab

    def reponse(self, s, rt=1.2, fs=26):
        t = txm(s, fs, RES, w=12.4) if "$" in s else tx(s, fs, RES, w=12.4)
        box = SurroundingRectangle(t, color=RES, buff=0.2, corner_radius=0.12, stroke_width=3)
        box.set_fill(RES, opacity=0.08)
        g = VGroup(box, t).to_edge(DOWN, buff=0.28)
        lab = etiquette("Phrase réponse", RES).next_to(box, UP, buff=0.06).align_to(box, LEFT)
        self.p(Create(box), FadeIn(lab), FadeIn(t, shift=UP * 0.15), rt=rt)
        return VGroup(g, lab)

    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.hdr_ex = tx("Chapitre 2.1 · Identification des espèces chimiques", 22, SOFT).to_corner(UL, buff=0.3)

        # ---------- Titre ----------
        self.at(T["titre"])
        TIT = VGroup(tx("Bilan · Chapitre 2.1", 34, ABSO, bold=True),
                     tx("Identification des", 60, WHITE, bold=True),
                     tx("espèces chimiques", 60, WHITE, bold=True)).arrange(DOWN, buff=0.25)
        self.p(FadeIn(TIT, shift=UP * 0.2), rt=1.2)
        self.at(T["question"] - 0.6)
        self.p(FadeOut(TIT), FadeIn(self.hdr_ex), rt=0.6)
        self.at(T["question"])
        Q = tx("Comment savoir de quoi est faite une substance ?", 38, WHITE, bold=True).move_to(UP * 2.5)
        self.apparait(Q)
        # Les trois méthodes
        def carte(icone, titre, c):
            cadre = RoundedRectangle(corner_radius=0.2, width=4.0, height=3.4, stroke_color=c, stroke_width=3,
                                     fill_color=c, fill_opacity=0.08)
            t = lignes(*titre, fs=30, c=c, buff=0.08)
            for l in t:
                l.set_x(0)
            g = VGroup(icone, t).arrange(DOWN, buff=0.35).move_to(cadre)
            return VGroup(cadre, g)
        ic1 = VGroup(mx(r"\rho", RHO, 90), mx(r"\theta", TCOL, 90)).arrange(RIGHT, buff=0.5)
        ic2 = VGroup(tube(EAU, 0.5, h=1.4, w=0.45), tube("#E0E0E0", 0.8, h=1.4, w=0.45)).arrange(RIGHT, buff=0.4)
        mini = Rectangle(width=1.2, height=1.5, stroke_width=0, fill_color=PLAQUE, fill_opacity=1)
        ic3 = VGroup(mini, tache(JAUNE, 0.25, 0.2).move_to(mini.get_center() + LEFT * 0.3 + UP * 0.35),
                     tache(BLEU, 0.25, 0.2).move_to(mini.get_center() + RIGHT * 0.3 + DOWN * 0.2))
        C1 = carte(ic1, ["Propriétés", "physiques"], RHO).move_to([-4.5, -0.6, 0])
        C2 = carte(ic2, ["Tests", "chimiques"], EAU).move_to([0, -0.6, 0])
        C3 = carte(ic3, ["Chromatographie", "(CCM)"], VERT).move_to([4.5, -0.6, 0])
        self.at(T["m1"])
        self.apparait(C1)
        self.at(T["m2"])
        self.apparait(C2)
        self.at(T["m3"])
        self.apparait(C3)

        # ---------- 1 · Vocabulaire ----------
        self.at(T["vocab"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("1 · Vocabulaire")
        self.at(T["entites"])
        TE = tx("La matière est faite d'entités chimiques", 36, WHITE, bold=True).move_to(UP * 2.75)
        self.apparait(TE)
        ENT = VGroup()
        for obj, nom, c in [(atome(), "atomes", CONC), (ion(), "ions", MAGENTA), (h2o(1.0), "molécules", O2C)]:
            ENT.add(VGroup(obj, tx(nom, 30, c, bold=True)).arrange(DOWN, buff=0.25))
        ENT.arrange(RIGHT, buff=2.2).move_to(UP * 1.2)
        self.p(LaggedStart(*[FadeIn(e, shift=UP * 0.2) for e in ENT], lag_ratio=0.5), rt=2.5)
        self.at(T["espece"])
        DEF = txm(r"Espèce chimique : ensemble d'entités identiques", 34, ABSO).move_to(DOWN * 0.3)
        self.apparait(DEF)
        self.at(T["eau"])
        MOL = grille(lambda i, j: h2o(0.75), 5, 2, dx=1.15, dy=0.95)
        BX = boite(MOL, w=6.6, h=2.2).move_to([-1.6, -2.3, 0])
        self.p(FadeIn(BX), rt=1.0)
        self.at(T["h2o"])
        LEAU = mx(r"\text{eau : } \mathrm{H_2O}", WHITE, 56).next_to(BX, RIGHT, buff=0.4)
        ajuster(LEAU, 6.9 - BX.get_right()[0] - 0.4)
        self.apparait(LEAU)

        # Corps pur / mélange
        self.at(T["corps_pur"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["corps_pur"])
        CPT = VGroup(tx("Corps pur", 44, OR_, bold=True), tx("1 seule espèce chimique", 28, WHITE)).arrange(
            DOWN, buff=0.2).move_to([-3.6, 2.3, 0])
        self.apparait(CPT)
        ORS = grille(lambda i, j: atome(OR_, 0.28), 5, 3, dx=0.7, dy=0.6)
        BOR = boite(ORS, w=4.4, h=2.3).move_to([-3.6, 0.0, 0])
        self.p(FadeIn(BOR), rt=0.8)
        self.at(T["pepite"])
        PEP = VGroup(pepite(1.2), tx("pépite d'or", 28, OR_)).arrange(DOWN, buff=0.2).move_to([-3.6, -2.4, 0])
        self.apparait(PEP)
        self.at(T["melange"])
        MT = VGroup(tx("Mélange", 44, VERT, bold=True), tx("plusieurs espèces chimiques", 28, WHITE)).arrange(
            DOWN, buff=0.2).move_to([3.6, 2.3, 0])
        cols = [O2C, CONC, OR_]
        MIX = grille(lambda i, j: atome(cols[(i + 2 * j) % 3], 0.28), 5, 3, dx=0.7, dy=0.6)
        BMI = boite(MIX, w=4.4, h=2.3).move_to([3.6, 0.0, 0])
        SEPV = DashedLine([0, 2.6, 0], [0, -3.3, 0], color=SOFT, stroke_width=2)
        self.p(FadeIn(MT), FadeIn(BMI), Create(SEPV), rt=1.0)
        self.at(T["ex_mel"])
        EXM = lignes("jus d'orange", "acier", "eau de Javel", fs=28, c=WHITE, buff=0.1).move_to([3.6, -2.4, 0])
        self.apparait(EXM)

        # Homogène / hétérogène
        self.at(T["deux_cas"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["deux_cas"])
        self.titre("Deux sortes de mélanges")
        self.at(T["homogene"])
        BH = becher([(1.9, EAU, 0.55)]).move_to([-3.6, 0.5, 0])
        LH = VGroup(tx("Homogène", 40, EAU, bold=True), tx("1 seule phase visible", 28, WHITE)).arrange(
            DOWN, buff=0.12).next_to(BH, DOWN, buff=0.35)
        self.p(FadeIn(BH, shift=UP * 0.2), rt=0.8)
        self.apparait(LH, rt=0.8)
        self.at(T["homog_ex"])
        EXH = tx("eau salée · eau + éthanol", 26, SOFT).next_to(LH, DOWN, buff=0.25)
        self.apparait(EXH, rt=0.6)
        self.at(T["hetero"])
        BT = becher([(0.3, "#C2A36B", 1.0), (1.0, EAU, 0.55), (0.6, "#F2C94C", 0.85)]).move_to([3.6, 0.5, 0])
        LT = VGroup(tx("Hétérogène", 40, "#F2C94C", bold=True), tx("plusieurs phases visibles", 28, WHITE)).arrange(
            DOWN, buff=0.12).next_to(BT, DOWN, buff=0.35)
        self.p(FadeIn(BT, shift=UP * 0.2), rt=0.8)
        self.apparait(LT, rt=0.8)
        self.at(T["hetero_ex"])
        EXT = tx("huile + eau · eau + sable", 26, SOFT).next_to(LT, DOWN, buff=0.25)
        self.apparait(EXT, rt=0.6)

        # L'air : diagramme circulaire (composition en volume)
        self.at(T["air"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["air"])
        self.titre("L'air : un mélange homogène de gaz")
        R, CENT = 2.3, np.array([-3.3, -0.5, 0])
        def part(debut, frac_, c):
            return AnnularSector(inner_radius=0, outer_radius=R, angle=frac_ * TAU, start_angle=debut * TAU + PI / 2,
                                 fill_color=c, fill_opacity=1, stroke_color=INK, stroke_width=2).shift(CENT)
        SN2, SO2, SAU = part(0, 0.78, N2C), part(0.78, 0.21, O2C), part(0.99, 0.01, AUTRE)
        LN2 = row(Square(0.4, stroke_width=0, fill_color=N2C, fill_opacity=1), tx("78 %", 48, N2C, bold=True),
                  tx("diazote", 32, WHITE), mx(r"\mathrm{N_2}", N2C, 46), buff=0.3)
        LO2 = row(Square(0.4, stroke_width=0, fill_color=O2C, fill_opacity=1), tx("21 %", 48, O2C, bold=True),
                  tx("dioxygène", 32, WHITE), mx(r"\mathrm{O_2}", O2C, 46), buff=0.3)
        LAU = row(Square(0.4, stroke_width=0, fill_color=AUTRE, fill_opacity=1), tx("< 1 %", 48, AUTRE, bold=True),
                  tx("autres gaz", 32, WHITE), buff=0.3)
        LEG = VGroup(LN2, LO2, LAU).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.2, -0.3, 0])
        VOL_ = tx("(pourcentages en volume)", 24, SOFT).next_to(LEG, UP, buff=0.4).align_to(LEG, LEFT)
        self.at(T["air_n2"])
        self.p(Create(SN2), FadeIn(LN2), FadeIn(VOL_), rt=1.5)
        self.at(T["air_o2"])
        self.p(Create(SO2), FadeIn(LO2), rt=1.0)
        self.at(T["air_autres"])
        self.p(FadeIn(SAU), FadeIn(LAU), rt=0.8)

        # ---------- 2 · Propriétés physiques ----------
        self.at(T["prop"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("2 · Propriétés physiques")
        M1 = VGroup(tx("Méthode 1", 34, RHO, bold=True),
                    tx("Mesurer ses propriétés physiques", 40, WHITE, bold=True),
                    tx("et les comparer à des valeurs de référence", 40, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        self.at(T["prop"])
        self.apparait(M1)
        self.at(T["rho"] - 0.5)
        self.p(FadeOut(M1), rt=0.5)
        self.at(T["rho"])
        TR = row(tx("La masse volumique", 40, WHITE, bold=True), mx(r"\rho", RHO, 72), buff=0.4).move_to(UP * 2.6)
        self.apparait(TR)
        self.at(T["rho_rel"])
        REL = row(mx(r"\rho", RHO, 130), mx("=", WHITE, 130),
                  frac(mx("m", MASSE, 130), mx("V", VOL, 130)), buff=0.35).move_to([-2.6, -0.2, 0])
        self.p(Write(REL), rt=1.5)
        self.at(T["rho_unites"])
        U1 = row(mx("m", MASSE, 56), tx(": masse en grammes (g)", 32, WHITE), buff=0.25)
        U2 = row(mx("V", VOL, 56), tx(": volume en litres (L)", 32, WHITE), buff=0.25)
        UN = VGroup(U1, U2).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.6, 0.3, 0])
        self.p(FadeIn(U1, shift=LEFT * 0.2), rt=0.8)
        self.p(FadeIn(U2, shift=LEFT * 0.2), rt=0.8)
        self.at(T["rho_gl"])
        U3 = row(mx(r"\rho", RHO, 56), tx(":  en", 32, WHITE), val("", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), RHO, 56),
                 buff=0.25)
        U3[2][1].set_color(RHO)
        U3.next_to(UN, DOWN, buff=0.45).align_to(UN, LEFT)
        self.apparait(U3)

        # Comparaison des masses volumiques (diagramme en barres)
        self.at(T["eau_rho"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["eau_rho"])
        TB = row(tx("Masses volumiques", 36, WHITE, bold=True), mx(r"(\mathrm{g\cdot L^{-1}})", SOFT, 40), buff=0.3)
        TB.move_to(UP * 2.85)
        X0, K = -3.0, 8.8 / 7870
        rangs = {"eau": 1.55, "eth": 0.45, "fer": -0.65, "air": -1.75}
        def barre_h(cle, valeur, c, nom):
            y = rangs[cle]
            L = max(valeur * K, 0.04)
            r = Rectangle(width=L, height=0.62, stroke_width=0, fill_color=c, fill_opacity=1)
            r.move_to([X0 + L / 2, y, 0])
            n = tx(nom, 32, c, bold=True)
            n.move_to([X0 - 0.3 - n.width / 2, y, 0])
            return r, n
        rE, nE = barre_h("eau", 1000, EAU, "eau liquide")
        vE = mx(r"1\,000", EAU, 46).next_to(rE, RIGHT, buff=0.25)
        self.p(FadeIn(TB), FadeIn(nE), GrowFromEdge(rE, LEFT), rt=1.0)
        self.p(FadeIn(vE), rt=0.5)
        self.at(T["bouteille"])
        BOU = VGroup(bouteille(), tx("1 L d'eau = 1 kg", 30, EAU, bold=True)).arrange(RIGHT, buff=0.35)
        BOU.move_to([3.9, 1.55, 0])
        self.apparait(BOU)
        self.at(T["ethanol"])
        rT, nT = barre_h("eth", 789, "#C77DFF", "éthanol")
        vT = mx("789", "#C77DFF", 46).next_to(rT, RIGHT, buff=0.25)
        self.p(FadeIn(nT), GrowFromEdge(rT, LEFT), rt=1.0)
        self.p(FadeIn(vT), rt=0.5)
        self.at(T["fer"])
        rF, nF = barre_h("fer", 7870, "#B0BEC5", "fer")
        vF = mx(r"7\,870", INK, 46).move_to(rF.get_right() + LEFT * 1.1)
        self.p(FadeIn(nF), GrowFromEdge(rF, LEFT), rt=1.5)
        self.p(FadeIn(vF), rt=0.5)
        self.at(T["fer8"])
        vF8 = mx(r"\approx 8\ \mathrm{kg\cdot L^{-1}}", "#B0BEC5", 40).next_to(rF, UP, buff=0.05).align_to(rF, RIGHT)
        self.apparait(vF8, rt=0.6)
        self.at(T["air_rho"])
        rA, nA = barre_h("air", 1.3, WHITE, "air (mélange)")
        vA = mx(r"1{,}3", WHITE, 46).next_to(rA, RIGHT, buff=0.25)
        self.p(FadeIn(nA), FadeIn(rA), FadeIn(vA), rt=0.8)
        self.at(T["air800"])
        A800 = tx("≈ 800 fois moins que l'eau !", 32, ABSO, bold=True).next_to(vA, RIGHT, buff=0.5)
        self.apparait(A800)

        # Identifier un liquide grâce à sa masse volumique
        self.at(T["ident"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["ident"])
        self.titre("Identifier un liquide grâce à ρ")
        self.at(T["liquide"])
        BI = becher([(1.6, "#DDEEFF", 0.18)], w=2.2, h=2.6).move_to([-4.6, 0.3, 0])
        QI = tx("?", 90, ABSO, bold=True).move_to(BI[0])
        LI = tx("liquide incolore", 30, WHITE).next_to(BI, DOWN, buff=0.3)
        self.p(FadeIn(BI, shift=UP * 0.2), FadeIn(QI), FadeIn(LI), rt=1.0)
        self.at(T["vol50"])
        DV = row(mx("V", VOL, 60), mx("=", WHITE, 60), val("50", r"\mathrm{mL}", VOL, 60)).move_to([1.6, 1.5, 0])
        self.apparait(DV)
        self.at(T["m395"])
        DM = row(mx("m", MASSE, 60), mx("=", WHITE, 60), val(r"39{,}5", r"\mathrm{g}", MASSE, 60))
        DM.next_to(DV, DOWN, buff=0.45).align_to(DV, LEFT)
        self.apparait(DM)
        # Conversion : 50 × 1 mL, puis 1 mL remplacé par 10⁻³ L
        self.at(T["conv"])
        c1 = mx(r"1\ \mathrm{mL}", WHITE, 50)
        CV = row(mx("V", VOL, 50), mx("=", WHITE, 50), mx("50", VOL, 50), mx(r"\times", WHITE, 50), c1)
        CV.move_to([0.0, -1.3, 0]).align_to([-2.9, 0, 0], LEFT)
        ETQ_C = tx("Conversion en litres", 24, SOFT).next_to(CV, UP, buff=0.15).align_to(CV, LEFT)
        self.p(FadeIn(ETQ_C), Write(CV), rt=1.0)
        self.at(T["conv2"])
        c2 = mx(r"10^{-3}\ \mathrm{L}", WHITE, 50).move_to(c1).align_to(c1, LEFT)
        self.p(Transform(c1, c2), rt=0.8)
        self.at(T["conv3"])
        CV3 = row(mx("=", WHITE, 50), val(r"0{,}050", r"\mathrm{L}", VOL, 50)).next_to(CV, RIGHT, buff=0.25)
        self.p(Write(CV3), rt=0.8)

        # Calcul de ρ
        self.at(T["lit"] - 0.5)
        self.vider(rt=0.5)
        LIT = row(mx(r"\rho", RHO, 72), mx("=", WHITE, 72), frac(mx("m", MASSE, 72), mx("V", VOL, 72)))
        LIT.move_to([-3.6, 1.2, 0])
        self.at(T["lit"])
        self.p(Write(LIT), rt=1.0)
        self.encadre(LIT, rt=0.8)
        self.at(T["an"])
        AN = row(mx(r"\rho", RHO, 64), mx("=", WHITE, 64),
                 frac(val(r"39{,}5", r"\mathrm{g}", MASSE, 64), val(r"0{,}050", r"\mathrm{L}", VOL, 64)))
        AN.move_to([2.6, 1.2, 0])
        self.p(Write(AN), rt=1.2)
        self.tag_an(AN)
        self.at(T["res"])
        RS = row(mx(r"\rho", RHO, 72), mx("=", WHITE, 72),
                 val("790", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), RES, 72)).move_to([-2.6, -0.9, 0])
        self.p(Write(RS), rt=1.0)
        self.at(T["ref"])
        REF = VGroup(tx("Valeur de référence :", 26, SOFT),
                     row(tx("éthanol", 32, "#C77DFF", bold=True),
                         val("789", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), "#C77DFF", 52), buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        REF.move_to([3.6, -0.9, 0])
        EQ = mx(r"\approx", ABSO, 80).move_to([(RS.get_right()[0] + REF.get_left()[0]) / 2, -0.9, 0])
        self.p(FadeIn(REF), FadeIn(EQ), rt=1.0)
        self.at(T["rep"])
        self.reponse("Ce liquide est sans doute de l'éthanol (790 g/L ≈ 789 g/L).", rt=1.0)

        # Température de changement d'état : courbe de chauffage de l'eau pure
        self.at(T["temp"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["temp"])
        self.titre("La température de changement d'état")
        AX = axes([0, 10, 1], [0, 165, 10], 7.2, 4.4, [-1.2, -0.75, 0])

        def cp(x, th):
            return AX.c2p(x, th + 30)
        YT = mx(r"\theta\ (^\circ\mathrm{C})", TCOL, 40).next_to(AX, UP, buff=0.05).align_to(AX, LEFT)
        XT = tx("temps", 24, SOFT).next_to(AX.c2p(10, 0), DOWN, buff=0.15)
        pts = [(0, -25), (1.2, 0), (3.4, 0), (5.4, 100), (8.2, 100), (9.4, 128)]
        COURBE = VMobject(color=TCOL, stroke_width=6).set_points_as_corners([cp(x, y) for x, y in pts])
        self.at(T["palier_txt"])
        self.p(Create(AX), FadeIn(YT), FadeIn(XT), rt=1.0)
        self.p(Create(COURBE), rt=3.0)
        self.at(T["palier"])
        P1 = Line(cp(1.2, 0), cp(3.4, 0), color=ABSO, stroke_width=14)
        P2 = Line(cp(5.4, 100), cp(8.2, 100), color=ABSO, stroke_width=14)
        LP = tx("paliers", 30, ABSO, bold=True).move_to(cp(3.0, 122))
        self.p(Create(P1), Create(P2), FadeIn(LP), rt=1.0)
        self.at(T["fusion"])
        G0 = DashedLine(cp(0, 0), cp(1.2, 0), color=SOFT, stroke_width=2)
        V0 = mx(r"0\ ^\circ\mathrm{C}", WHITE, 40).next_to(cp(0, 0), LEFT, buff=0.15)
        F0 = tx("fusion de la glace", 24, WHITE).next_to(P1, DOWN, buff=0.2).shift(RIGHT * 0.3)
        self.p(Create(G0), FadeIn(V0), FadeIn(F0), rt=0.8)
        self.at(T["ebullition"])
        G100 = DashedLine(cp(0, 100), cp(5.4, 100), color=SOFT, stroke_width=2)
        V100 = mx(r"100\ ^\circ\mathrm{C}", WHITE, 40).next_to(cp(0, 100), LEFT, buff=0.15)
        F100 = tx("ébullition de l'eau", 24, WHITE).next_to(P2, UP, buff=0.2)
        self.p(Create(G100), FadeIn(V100), FadeIn(F100), rt=0.8)
        EP = tx("Eau pure : paliers", 28, TCOL, bold=True, w=3.9).move_to([4.8, 1.6, 0])
        self.p(FadeIn(EP), rt=0.5)
        self.at(T["melange_temp"])
        CM = AX.plot(lambda x: 5 + 16 * x - 0.15 * x * x, x_range=[0, 8.5], color=SOFT, stroke_width=4)
        CMD = DashedVMobject(CM, num_dashes=40)
        LM = VGroup(tx("Mélange :", 28, SOFT, bold=True), tx("pas de palier", 28, SOFT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.8, 0.3, 0])
        self.p(Create(CMD), FadeIn(LM), rt=1.5)
        self.at(T["tables"])
        TAB = lignes("θ mesurée = valeur", "de référence", "→ corps pur identifié", fs=26, c=RES, w=3.9)
        TAB.move_to([4.8, -1.5, 0])
        self.apparait(TAB)

        # ---------- 3 · Tests chimiques ----------
        self.at(T["tests"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("3 · Tests chimiques")
        self.at(T["tests"])
        TT = row(tx("Méthode 2 :", 34, EAU, bold=True), tx("4 tests chimiques à connaître", 34, WHITE, bold=True),
                 buff=0.3).move_to(UP * 2.85)
        self.apparait(TT)
        POS = [(-3.45, 0.95), (3.45, 0.95), (-3.45, -2.05), (3.45, -2.05)]

        def cadre_test(k, c):
            r = RoundedRectangle(corner_radius=0.15, width=6.6, height=2.75, stroke_color=c, stroke_width=2.5,
                                 fill_color=c, fill_opacity=0.06).move_to([POS[k][0], POS[k][1], 0])
            return r

        def texte_test(k, formule, nom, c, reactif, obs):
            g = VGroup(row(mx(formule, c, 54), tx(nom, 28, c, bold=True), buff=0.25),
                       tx(reactif, 22, WHITE, w=4.0), tx(obs, 22, RES, w=4.0)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.18)
            ajuster(g, 4.3)
            g.move_to([POS[k][0] + 0.95, POS[k][1], 0])
            return g

        # Eau : sulfate de cuivre anhydre
        self.at(T["t_eau"])
        K1 = cadre_test(0, EAU)
        X1 = POS[0][0] - 2.15
        coupe = Ellipse(width=1.5, height=0.5, stroke_color=WHITE, stroke_width=3).move_to([X1, POS[0][1] - 0.6, 0])
        poudre = Ellipse(width=1.1, height=0.3, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(coupe)
        goutte = Circle(radius=0.12, stroke_width=0, fill_color=EAU, fill_opacity=1).move_to([X1, POS[0][1] + 0.9, 0])
        T1 = texte_test(0, r"\mathrm{H_2O}", "eau", EAU, "Sulfate de cuivre anhydre (poudre blanche)",
                        "→ devient bleu")
        self.p(FadeIn(K1), FadeIn(coupe), FadeIn(poudre), FadeIn(T1[0]), FadeIn(T1[1]), rt=1.0)
        self.at(T["t_eau_bleu"] - 0.8)
        self.p(FadeIn(goutte), rt=0.3)
        self.p(goutte.animate.move_to(poudre.get_center()).set_opacity(0), rt=0.5)
        self.at(T["t_eau_bleu"])
        self.p(poudre.animate.set_fill("#1E6FFF", opacity=1), FadeIn(T1[2]), rt=1.0)
        # CO2 : eau de chaux
        self.at(T["t_co2"])
        K2 = cadre_test(1, SOFT)
        X2 = POS[1][0] - 2.15
        TU2 = tube("#DDEEFF", 0.35).move_to([X2, POS[1][1], 0])
        BULLES = VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=2).move_to(
            TU2[1].get_bottom() + UP * (0.15 + 0.2 * k) + RIGHT * (0.08 if k % 2 else -0.08)) for k in range(4)])
        T2 = texte_test(1, r"\mathrm{CO_2}", "dioxyde de carbone", SOFT, "Eau de chaux", "→ se trouble")
        self.p(FadeIn(K2), FadeIn(TU2), FadeIn(T2[0]), FadeIn(T2[1]), rt=1.0)
        self.at(T["t_co2_trouble"] - 0.8)
        self.p(FadeIn(BULLES, shift=UP * 0.2), rt=0.8)
        self.p(TU2[1].animate.set_fill("#F5F5F5", opacity=0.95), FadeOut(BULLES), FadeIn(T2[2]), rt=1.0)
        # H2 : détonation
        self.at(T["t_h2"])
        K3 = cadre_test(2, O2C)
        X3 = POS[2][0] - 2.15
        TU3 = tube(WHITE, 0.0).rotate(PI).move_to([X3, POS[2][1] + 0.25, 0])
        FL3 = flamme(0.8).move_to([X3, POS[2][1] - 1.0, 0])
        T3 = texte_test(2, r"\mathrm{H_2}", "dihydrogène", O2C, "Flamme approchée (test à la flamme)",
                        "→ petite détonation")
        self.p(FadeIn(K3), FadeIn(TU3), FadeIn(T3[0]), FadeIn(T3[1]), rt=1.0)
        self.p(FadeIn(FL3, shift=UP * 0.2), rt=0.6)
        self.at(T["t_h2_pop"])
        POP = VGroup(Star(n=10, outer_radius=0.75, inner_radius=0.4, stroke_width=0, fill_color=ABSO,
                          fill_opacity=1), tx("POP !", 24, INK, bold=True)).move_to([X3, POS[2][1] - 0.35, 0])
        POP[1].move_to(POP[0])
        self.p(GrowFromCenter(POP), FadeIn(T3[2]), rt=0.6)
        # O2 : allumette incandescente
        self.at(T["t_o2"])
        K4 = cadre_test(3, VERT)
        X4 = POS[3][0] - 2.15
        AL = allumette(braise=False).move_to([X4, POS[3][1], 0])
        T4 = texte_test(3, r"\mathrm{O_2}", "dioxygène", VERT, "Allumette incandescente (point rouge)",
                        "→ se rallume")
        self.p(FadeIn(K4), FadeIn(AL), FadeIn(T4[0]), FadeIn(T4[1]), rt=1.0)
        self.at(T["t_o2_braise"])
        BR = Circle(radius=0.16, stroke_width=0, fill_color="#FF3B30", fill_opacity=1).move_to(AL[1])
        self.p(FadeIn(BR), rt=0.5)
        self.p(Indicate(BR, color="#FF8C1A", scale_factor=1.4), rt=1.0)
        self.at(T["t_o2_feu"])
        FL4 = flamme(0.9).next_to(AL[1], UP, buff=-0.15)
        self.p(GrowFromEdge(FL4, DOWN), FadeIn(T4[2]), rt=0.8)

        # ---------- 4 · Chromatographie sur couche mince ----------
        self.at(T["ccm"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("4 · Chromatographie")
        self.at(T["ccm"])
        M3 = VGroup(tx("Méthode 3", 34, VERT, bold=True),
                    tx("La chromatographie sur couche mince", 44, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        M3.move_to(UP * 1.6)
        self.apparait(M3)
        self.at(T["ccm_sigle"])
        SIG = row(tx("C", 110, VERT, bold=True), tx("C", 110, VERT, bold=True), tx("M", 110, VERT, bold=True),
                  buff=0.5).move_to(DOWN * 0.6)
        self.p(LaggedStart(*[FadeIn(l, scale=1.5) for l in SIG], lag_ratio=0.4), rt=1.2)
        self.at(T["ccm_but"])
        BUT = tx("séparer et identifier les espèces d'un mélange homogène", 30, ABSO).move_to(DOWN * 2.5)
        self.apparait(BUT)

        # Exemple : sirop de menthe
        self.at(T["sirop"] - 0.5)
        self.vider(rt=0.5)
        self.at(T["sirop"])
        VERRE = becher([(1.8, VERT, 0.9)], w=1.9, h=2.4).move_to([-3.5, 0.0, 0])
        SIR = tx("sirop de menthe", 36, VERT, bold=True).next_to(VERRE, DOWN, buff=0.35)
        self.p(FadeIn(VERRE, shift=UP * 0.2), FadeIn(SIR), rt=1.0)
        self.at(T["quels"])
        QC = VGroup(tx("Quels colorants", 44, WHITE, bold=True), tx("contient-il ?", 44, WHITE, bold=True)).arrange(
            DOWN, buff=0.2).move_to([2.6, 0.2, 0])
        self.apparait(QC)

        # La plaque
        self.at(T["plaque"] - 0.5)
        self.vider(rt=0.5)
        PX, PY, PW, PH = -3.0, -0.45, 3.9, 5.4
        BAS, HAUT = PY - PH / 2, PY + PH / 2
        YD = BAS + 0.6                       # ligne de dépôt (1 cm du bas)
        YF = HAUT - 0.5                      # front final de l'éluant
        XCOL = [PX - 1.2, PX, PX + 1.2]      # jaune, bleu, sirop
        PL = Rectangle(width=PW, height=PH, stroke_color=SOFT, stroke_width=2, fill_color=PLAQUE, fill_opacity=1)
        PL.move_to([PX, PY, 0])
        self.at(T["plaque"])
        self.p(FadeIn(PL, shift=UP * 0.2), rt=0.8)
        XR = 0.6                              # bord gauche de la colonne d'explications
        self.at(T["ligne"])
        LD = Line([PX - PW / 2 + 0.15, YD, 0], [PX + PW / 2 - 0.15, YD, 0], color="#555555", stroke_width=3)
        LLD = lignes("ligne de dépôt", "au crayon, à 1 cm du bas", fs=30, c=WHITE, buff=0.1)
        LLD.move_to([0, YD + 0.2, 0]).align_to([XR, 0, 0], LEFT)
        FLD = Arrow(start=[XR - 0.1, YD + 0.2, 0], end=[PX + PW / 2 + 0.05, YD, 0], color=WHITE, buff=0.05,
                    stroke_width=3)
        self.p(Create(LD), FadeIn(LLD), GrowArrow(FLD), rt=1.0)
        self.at(T["depots"])
        self.p(FadeOut(LLD), FadeOut(FLD), rt=0.5)
        TD = tx("3 dépôts côte à côte", 36, WHITE, bold=True).move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(TD, rt=0.6)
        DJ = tache(JAUNE).move_to([XCOL[0], YD, 0])
        DB = tache(BLEU).move_to([XCOL[1], YD, 0])
        DS = tache(VERT).move_to([XCOL[2], YD, 0])
        NJ = tx("J", 34, JAUNE, bold=True).move_to([XCOL[0], BAS - 0.35, 0])
        NB = tx("B", 34, BLEU, bold=True).move_to([XCOL[1], BAS - 0.35, 0])
        NS = tx("S", 34, VERT, bold=True).move_to([XCOL[2], BAS - 0.35, 0])
        LEGD = VGroup(row(tache(JAUNE), tx("J : colorant jaune", 32, JAUNE), buff=0.3),
                      row(tache(BLEU), tx("B : colorant bleu", 32, BLEU), buff=0.3),
                      row(tache(VERT), tx("S : sirop de menthe", 32, VERT), buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35)
        LEGD.next_to(TD, DOWN, buff=0.5).align_to(TD, LEFT)
        self.at(T["dep_j"])
        self.p(FadeIn(DJ, scale=0.3), FadeIn(NJ), FadeIn(LEGD[0]), rt=0.6)
        self.at(T["dep_b"])
        self.p(FadeIn(DB, scale=0.3), FadeIn(NB), FadeIn(LEGD[1]), rt=0.6)
        self.at(T["dep_s"])
        self.p(FadeIn(DS, scale=0.3), FadeIn(NS), FadeIn(LEGD[2]), rt=0.6)

        # La cuve et l'éluant
        self.at(T["cuve"])
        CB = BAS - 0.3
        CUVE = VGroup(Line([PX - PW / 2 - 0.35, 0.9, 0], [PX - PW / 2 - 0.35, CB, 0]),
                      Line([PX - PW / 2 - 0.35, CB, 0], [PX + PW / 2 + 0.35, CB, 0]),
                      Line([PX + PW / 2 + 0.35, CB, 0], [PX + PW / 2 + 0.35, 0.9, 0])).set_stroke(WHITE, 4)
        EL = Rectangle(width=PW + 0.62, height=0.6, stroke_width=0, fill_color=ELUANT, fill_opacity=0.55)
        EL.move_to([PX, CB + 0.3 + 0.02, 0])
        LEL = tx("éluant", 32, ELUANT, bold=True).next_to(EL, LEFT, buff=0.35)
        self.p(FadeOut(TD), FadeOut(LEGD), Create(CUVE), FadeIn(EL), FadeIn(LEL), NJ.animate.set_opacity(0),
               NB.animate.set_opacity(0), NS.animate.set_opacity(0), rt=1.2)
        self.at(T["attention"])
        ATT = VGroup(tx("Attention !", 36, BAD, bold=True),
                     lignes("l'éluant reste sous", "la ligne de dépôt", fs=30, c=WHITE, buff=0.08)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        ATT.move_to([0, YD + 0.3, 0]).align_to([XR, 0, 0], LEFT)
        ECART = DoubleArrow(start=[PX + PW / 2 + 0.6, EL.get_top()[1], 0], end=[PX + PW / 2 + 0.6, YD, 0], buff=0,
                            color=BAD, stroke_width=4, tip_length=0.15)
        self.p(FadeIn(ATT), GrowFromCenter(ECART), rt=0.8)

        # Élution : le front monte, les taches se séparent
        self.at(T["elution"])
        self.p(FadeOut(ATT), FadeOut(ECART), rt=0.4)
        FRONT0 = Rectangle(width=PW, height=0.01, stroke_width=0, fill_color=ELUANT, fill_opacity=0.35)
        FRONT0.move_to([PX, BAS + 0.005, 0])
        HF = YF - BAS
        FRONT1 = Rectangle(width=PW, height=HF, stroke_width=0, fill_color=ELUANT, fill_opacity=0.35)
        FRONT1.move_to([PX, BAS + HF / 2, 0])
        YJ, YB_ = YD + 0.72 * (YF - YD), YD + 0.33 * (YF - YD)
        SJ = tache(JAUNE).move_to(DS)
        SB = tache(BLEU).move_to(DS)
        self.add(FRONT0)
        self.add(SB, SJ)
        self.remove(DS)
        MONTE = tx("L'éluant monte…", 36, ELUANT, bold=True).move_to([0, 1.8, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Transform(FRONT0, FRONT1),
               DJ.animate.move_to([XCOL[0], YJ, 0]).stretch(1.15, 1), SJ.animate.move_to([XCOL[2], YJ, 0]).stretch(1.15, 1),
               DB.animate.move_to([XCOL[1], YB_, 0]), SB.animate.move_to([XCOL[2], YB_, 0]),
               FadeIn(MONTE), rt=4.0)
        self.at(T["vitesse"])
        VIT = tx("… mais pas à la même vitesse", 32, WHITE).next_to(MONTE, DOWN, buff=0.25).align_to(MONTE, LEFT)
        self.apparait(VIT, rt=0.6)
        self.at(T["affinite"])
        self.p(FadeOut(MONTE), FadeOut(VIT), rt=0.4)
        AF1 = row(tx("phase fixe", 32, SOFT, bold=True), tx("= la plaque", 32, WHITE), buff=0.25)
        AF2 = row(tx("phase mobile", 32, ELUANT, bold=True), tx("= l'éluant", 32, WHITE), buff=0.25)
        AFF = VGroup(AF1, AF2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 2.0, 0]).align_to(
            [XR, 0, 0], LEFT)
        self.p(FadeIn(AF1, shift=LEFT * 0.2), rt=0.7)
        self.p(FadeIn(AF2, shift=LEFT * 0.2), rt=0.7)
        self.at(T["monte_haut"])
        H1 = row(Arrow(start=DOWN * 0.6, end=UP * 0.6, color=JAUNE, buff=0, stroke_width=8),
                 lignes("préfère l'éluant", "→ monte haut", fs=30, c=JAUNE, buff=0.06), buff=0.35)
        H1.move_to([0, 0.1, 0]).align_to([XR, 0, 0], LEFT)
        self.p(FadeIn(H1), Indicate(VGroup(DJ, SJ), color=WHITE), rt=1.0)
        self.at(T["monte_peu"])
        H2 = row(Arrow(start=DOWN * 0.25, end=UP * 0.25, color=BLEU, buff=0, stroke_width=8),
                 lignes("accrochée à la plaque", "→ monte peu", fs=30, c=BLEU, buff=0.06), buff=0.35)
        H2.move_to([0, -1.5, 0]).align_to([XR, 0, 0], LEFT)
        self.p(FadeIn(H2), Indicate(VGroup(DB, SB), color=WHITE), rt=1.0)

        # On sort la plaque, on marque le front
        self.at(T["sortie"])
        self.p(FadeOut(CUVE), FadeOut(EL), FadeOut(LEL), FadeOut(AFF), FadeOut(H1), FadeOut(H2),
               FRONT0.animate.set_opacity(0.12), rt=0.8)
        self.at(T["front"])
        LF = DashedLine([PX - PW / 2 + 0.1, YF, 0], [PX + PW / 2 - 0.1, YF, 0], color="#555555", stroke_width=3)
        LLF = tx("front de l'éluant", 30, WHITE).move_to([0, YF, 0]).align_to([XR, 0, 0], LEFT)
        FLF = Arrow(start=[XR - 0.1, YF, 0], end=[PX + PW / 2 + 0.05, YF, 0], color=WHITE, buff=0.05, stroke_width=3)
        self.p(Create(LF), FadeIn(LLF), GrowArrow(FLF), NJ.animate.set_opacity(1), NB.animate.set_opacity(1),
               NS.animate.set_opacity(1), rt=1.0)
        self.at(T["chromato"])
        CHR = tx("Le chromatogramme", 40, VERT, bold=True).move_to([0, 0.6, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(CHR)

        # Lecture verticale
        self.at(T["verticale"] - 0.5)
        self.p(FadeOut(CHR), FadeOut(LLF), FadeOut(FLF), rt=0.5)
        self.at(T["verticale"])
        LV = row(tx("Lecture verticale", 38, ABSO, bold=True),
                 Arrow(start=UP * 0.4, end=DOWN * 0.4, color=ABSO, buff=0, stroke_width=6), buff=0.3)
        LV.move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(LV)
        YC = (YD + YF) / 2 - 0.1
        def colonne(k):
            return Rectangle(width=1.0, height=YF - YD + 0.8, stroke_color=ABSO, stroke_width=4).move_to(
                [XCOL[k], YC, 0])
        self.at(T["col_j"])
        COL = colonne(0)
        RJ = row(tx("J :", 32, JAUNE, bold=True), tx("1 tache → corps pur", 32, WHITE), buff=0.25)
        RJ.move_to([0, 1.1, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Create(COL), FadeIn(RJ), rt=0.8)
        self.at(T["col_b"])
        RB = row(tx("B :", 32, BLEU, bold=True), tx("1 tache → corps pur", 32, WHITE), buff=0.25)
        RB.next_to(RJ, DOWN, buff=0.35).align_to(RJ, LEFT)
        self.p(COL.animate.move_to([XCOL[1], YC, 0]), FadeIn(RB), rt=0.8)
        self.at(T["col_s"])
        RSI = row(tx("S :", 32, VERT, bold=True), tx("2 taches → mélange", 32, ABSO, bold=True), buff=0.25)
        RSI.next_to(RB, DOWN, buff=0.35).align_to(RJ, LEFT)
        self.p(COL.animate.move_to([XCOL[2], YC, 0]), FadeIn(RSI), rt=0.8)

        # Lecture horizontale
        self.at(T["horizontale"] - 0.5)
        self.p(FadeOut(COL), FadeOut(LV), FadeOut(RJ), FadeOut(RB), FadeOut(RSI), rt=0.5)
        self.at(T["horizontale"])
        LH_ = row(tx("Lecture horizontale", 38, ABSO, bold=True),
                  Arrow(start=LEFT * 0.4, end=RIGHT * 0.4, color=ABSO, buff=0, stroke_width=6), buff=0.3)
        LH_.move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(LH_)
        self.at(T["meme"])
        MH = lignes("même hauteur", "= même espèce chimique", fs=32, c=WHITE, buff=0.08)
        MH.move_to([0, 1.1, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(MH)
        self.at(T["ici"])
        HJ = DashedLine([PX - PW / 2, YJ, 0], [PX + PW / 2 + 0.3, YJ, 0], color=JAUNE, stroke_width=4)
        HJT = tx("S contient J", 32, JAUNE, bold=True).move_to([0, -0.4, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Create(HJ), FadeIn(HJT), Indicate(VGroup(DJ, SJ), color=WHITE), rt=1.2)
        self.at(T["ici_b"])
        HB = DashedLine([PX - PW / 2, YB_, 0], [PX + PW / 2 + 0.3, YB_, 0], color=BLEU, stroke_width=4)
        HBT = tx("S contient B", 32, BLEU, bold=True).next_to(HJT, DOWN, buff=0.35).align_to(HJT, LEFT)
        self.p(Create(HB), FadeIn(HBT), Indicate(VGroup(DB, SB), color=WHITE), rt=1.2)

        # Conclusion : jaune + bleu = vert
        self.at(T["concl"])
        self.p(FadeOut(LH_), FadeOut(MH), FadeOut(HJT), FadeOut(HBT), rt=0.5)
        EQC = row(Circle(radius=0.5, stroke_width=0, fill_color=JAUNE, fill_opacity=1), mx("+", WHITE, 72),
                  Circle(radius=0.5, stroke_width=0, fill_color=BLEU, fill_opacity=1), mx("=", WHITE, 72),
                  Circle(radius=0.5, stroke_width=0, fill_color=VERT, fill_opacity=1), buff=0.35)
        EQC.move_to([0, 1.2, 0]).align_to([XR + 0.3, 0, 0], LEFT)
        EQT = row(tx("colorant jaune", 24, JAUNE), tx("colorant bleu", 24, BLEU), tx("sirop", 24, VERT), buff=0.6)
        for k, idx in enumerate([0, 2, 4]):
            EQT[k].next_to(EQC[idx], DOWN, buff=0.2)
        self.p(FadeIn(EQC[0]), FadeIn(EQC[1]), FadeIn(EQC[2]), FadeIn(EQT[0]), FadeIn(EQT[1]), rt=1.0)
        self.at(T["vert"])
        self.p(FadeIn(EQC[3]), FadeIn(EQC[4], scale=0.5), FadeIn(EQT[2]), rt=1.0)
        CC_ = lignes("Le sirop de menthe contient", "le colorant jaune", "et le colorant bleu.", fs=28, c=RES,
                     buff=0.08)
        CC_B = SurroundingRectangle(CC_, color=RES, buff=0.2, corner_radius=0.12, stroke_width=3)
        CC_B.set_fill(RES, opacity=0.08)
        CCG = VGroup(CC_B, CC_).move_to([0, -1.6, 0]).align_to([XR + 0.1, 0, 0], LEFT)
        CCL = etiquette("Phrase réponse", RES).next_to(CC_B, UP, buff=0.06).align_to(CC_B, LEFT)
        self.p(Create(CC_B), FadeIn(CCL), FadeIn(CC_), rt=1.0)

        # ---------- À retenir ----------
        self.at(T["resume"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("À retenir")
        self.at(T["resume"])
        TR_ = tx("À retenir", 44, ABSO, bold=True).move_to(UP * 2.8)
        self.apparait(TR_, rt=0.5)
        RP = row(tx("Corps pur :", 32, OR_, bold=True), tx("1 seule espèce chimique", 32, WHITE), buff=0.25)
        RM = row(tx("Mélange :", 32, VERT, bold=True), tx("plusieurs espèces chimiques", 32, WHITE), buff=0.25)
        BLOC1 = VGroup(RP, RM).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 1.65, 0])
        self.p(FadeIn(RP), rt=0.6)
        self.at(T["r_mel"])
        self.p(FadeIn(RM), rt=0.6)
        self.at(T["r_ident"])
        RI = tx("Identifier = comparer à des valeurs de référence :", 30, WHITE, bold=True).move_to([0, 0.35, 0])
        self.apparait(RI, rt=0.6)
        def puce(txt, c):
            t = tx(txt, 26, c, bold=True)
            r = RoundedRectangle(corner_radius=0.15, width=t.width + 0.4, height=t.height + 0.35, stroke_color=c,
                                 stroke_width=2.5, fill_color=c, fill_opacity=0.12)
            return VGroup(r, t.move_to(r))
        PU = VGroup(puce("masse volumique ρ", RHO), puce("température de changement d'état", TCOL),
                    puce("test chimique", EAU), puce("hauteur des taches (CCM)", VERT))
        L1_, L2_ = VGroup(PU[0], PU[1]).arrange(RIGHT, buff=0.4), VGroup(PU[2], PU[3]).arrange(RIGHT, buff=0.4)
        VGroup(L1_, L2_).arrange(DOWN, buff=0.3).move_to([0, -0.85, 0])
        for cle, k in [("r_rho", 0), ("r_temp", 1), ("r_test", 2), ("r_ccm", 3)]:
            self.at(T[cle])
            self.p(FadeIn(PU[k], scale=0.8), rt=0.6)
        self.at(T["r_eau"])
        RE = row(mx(r"\rho_{\text{eau}} =", EAU, 52), val(r"1\,000", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), EAU, 52),
                 buff=0.25)
        RA = row(tx("Air (en volume) :", 28, WHITE), mx(r"78\,\%\ \mathrm{N_2}", N2C, 46),
                 mx(r"21\,\%\ \mathrm{O_2}", O2C, 46), buff=0.35)
        BLOC3 = VGroup(RE, RA).arrange(RIGHT, buff=0.9).move_to([0, -2.85, 0])
        ajuster(BLOC3, 13.0)
        CAD3 = SurroundingRectangle(BLOC3, color=ABSO, buff=0.2, corner_radius=0.12, stroke_width=2.5)
        self.p(FadeIn(RE), Create(CAD3), rt=0.8)
        self.at(T["r_air"])
        self.p(FadeIn(RA), rt=0.8)
        # Fin : marge de 10 s après la fin du SRT, à couper au montage
        self.at(T["fin_audio"])
        self.pause(10.0)
