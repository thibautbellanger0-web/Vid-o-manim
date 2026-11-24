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
#  Calée sur le SRT de l'enregistrement (6 min 37 s).
#  Charte graphique 3Blue1Brown (style-3b1b.md) : écran épuré, blanc et gris pour le neutre,
#  3 couleurs d'accent seulement (ρ rose, m orange, V vert), jaune réservé aux mises en évidence,
#  vert vif pour le résultat, or pour l'expression littérale. Les objets dessinés (taches de CCM,
#  flamme, eau, huile, pépite, molécule) gardent leur couleur réelle.
# =====================================================================

# ---------- Neutres ----------
CLAIR = "#E6E8EB"    # particules, secteurs clairs
GRIS2 = "#6B7280"    # gris moyen
GRIS3 = "#3A3F48"    # gris foncé
PUCE_F = "#2A2F38"   # fond des pastilles d'en-tête
HL = ABSO            # jaune : « regardez ici » (mises en évidence uniquement)
INK = "#111318"

# ---------- Couleurs réelles des objets dessinés ----------
EAU_N = "#4FA3E0"
HUILE = "#E9C46A"
SABLE = "#B08D57"
OR_N = "#FFC83D"
O_ROUGE = "#FF6F61"
JAUNE = "#FFD60A"
BLEU = "#3A86FF"
VERT = "#2DC653"
PLAQUE = "#ECEFF1"
ELUANT = "#9ED8F7"
CUIVRE_BLEU = "#1E6FFF"

# ---------- Calage sur le SRT (secondes) ----------
T = {
    "titre": 0.00, "question": 7.40, "m1": 10.00, "m2": 13.16, "m3": 16.16,
    "vocab": 18.76, "entites": 21.46, "atomes": 23.46, "ions": 25.20, "molecules": 26.06,
    "espece": 27.48, "eau": 32.82, "h2o": 34.98,
    "corps_pur": 38.40, "pepite": 40.62, "melange": 42.94, "ex_mel": 45.28,
    "deux_cas": 48.70, "homogene": 52.12, "homog_ex": 55.48, "hetero": 60.12, "hetero_ex": 63.70,
    "air": 67.20, "air_n2": 70.32, "air_o2": 72.94, "air_autres": 76.14,
    "prop": 79.08, "rho": 86.92, "rho_rel": 90.14, "rho_m": 94.88, "rho_v": 97.44, "rho_gl": 98.94,
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
    "aff_plaque": 310.58, "aff_eluant": 312.36,
    "monte_haut": 314.34, "monte_peu": 317.34, "sortie": 320.78, "front": 323.50, "chromato": 325.90,
    "interp": 328.08, "verticale": 330.08, "col_j": 335.64, "col_b": 339.68, "col_s": 341.92,
    "horizontale": 345.70, "meme": 350.92, "ici": 354.88, "ici_b": 358.00, "concl": 360.68, "vert": 365.00,
    "resume": 371.74, "r_mel": 375.12, "r_ident": 377.28, "r_rho": 380.50, "r_temp": 382.20,
    "r_test": 385.46, "r_ccm": 387.46, "r_eau": 389.64, "r_air": 392.52, "fin_audio": 396.96,
}


# ---------- Petits dessins (2D) ----------
def particule(c=CLAIR, r=0.28):
    return Circle(radius=r, stroke_color=WHITE, stroke_width=1.5, fill_color=c, fill_opacity=0.95)


def ion(r=0.38):
    a = Circle(radius=r, stroke_color=WHITE, stroke_width=1.5, fill_color=GRIS2, fill_opacity=0.95)
    plus = mx("+", WHITE, 44).move_to(a)
    return VGroup(a, plus)


def h2o(s=1.0):
    o = Circle(radius=0.36, stroke_width=0, fill_color=O_ROUGE, fill_opacity=1)
    h1 = Circle(radius=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(
        o.get_center() + 0.42 * np.array([math.cos(math.radians(-38)), math.sin(math.radians(-38)), 0]))
    h2 = Circle(radius=0.2, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(
        o.get_center() + 0.42 * np.array([math.cos(math.radians(218)), math.sin(math.radians(218)), 0]))
    return VGroup(h1, h2, o).scale(s)


def pepite(s=1.0):
    pts = [[-0.7, -0.3, 0], [-0.5, 0.25, 0], [-0.1, 0.45, 0], [0.45, 0.35, 0], [0.75, -0.05, 0],
           [0.5, -0.42, 0], [-0.2, -0.5, 0]]
    p = Polygon(*pts, stroke_color="#B8860B", stroke_width=2, fill_color=OR_N, fill_opacity=1)
    reflet = Polygon([-0.35, 0.15, 0], [-0.1, 0.3, 0], [0.1, 0.18, 0], [-0.2, 0.05, 0], stroke_width=0,
                     fill_color=WHITE, fill_opacity=0.6)
    return VGroup(p, reflet).scale(s)


def boite(particules, w=4.4, h=2.4):
    cadre = RoundedRectangle(corner_radius=0.15, width=w, height=h, stroke_color=GRIS2, stroke_width=2)
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
                   Line([w / 2, -h / 2, 0], [w / 2, h / 2, 0])).set_stroke(WHITE, 3)
    bec = Line([-w / 2, h / 2, 0], [-w / 2 - 0.2, h / 2 + 0.15, 0], color=WHITE, stroke_width=3)
    return VGroup(g, paroi, bec)


def tube(liquide, op=0.5, h=1.9, w=0.55):
    corps = RoundedRectangle(corner_radius=w / 2 - 0.01, width=w, height=h, stroke_color=WHITE, stroke_width=2.5)
    liq = RoundedRectangle(corner_radius=w / 2 - 0.06, width=w - 0.1, height=h * 0.45, stroke_width=0,
                           fill_color=liquide, fill_opacity=op)
    liq.move_to(corps.get_bottom() + UP * (h * 0.45 / 2 + 0.05))
    return VGroup(corps, liq)


def flamme(s=1.0):
    ext = Ellipse(width=0.42, height=0.8, stroke_width=0, fill_color="#FF8C1A", fill_opacity=1)
    inte = Ellipse(width=0.2, height=0.42, stroke_width=0, fill_color="#FFE066", fill_opacity=1)
    inte.move_to(ext.get_center() + DOWN * 0.12)
    return VGroup(ext, inte).scale(s)


def allumette():
    baton = Line([0, -0.9, 0], [0, 0.45, 0], color="#C8A165", stroke_width=10)
    tete = Circle(radius=0.12, stroke_width=0, fill_color="#5A3A2A", fill_opacity=1).move_to([0, 0.52, 0])
    return VGroup(baton, tete)


def bouteille():
    corps = RoundedRectangle(corner_radius=0.15, width=0.8, height=1.3, stroke_color=WHITE, stroke_width=2.5,
                             fill_color=EAU_N, fill_opacity=0.45)
    col = Rectangle(width=0.32, height=0.35, stroke_color=WHITE, stroke_width=2.5).next_to(corps, UP, buff=0)
    return VGroup(corps, col)


def contour(m, w=5):
    """Contour sombre derrière un texte posé sur un graphe ou un dessin."""
    m.set_stroke(BLACK, width=w, background=True)
    return m


def lignes(*textes, fs=30, c=WHITE, w=LARGEUR, buff=0.14):
    return VGroup(*[tx(t, fs, c, w=w) for t in textes]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def tache(c, w=0.42, h=0.32):
    return Ellipse(width=w, height=h, stroke_width=0, fill_color=c, fill_opacity=1)


def axes(xr, yr, xl, yl, centre):
    a = Axes(x_range=xr, y_range=yr, x_length=xl, y_length=yl, tips=True,
             axis_config={"color": GRIS2, "stroke_width": 2, "include_ticks": False})
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
        """Pastille de partie, discrète (le jaune est réservé aux mises en évidence)."""
        t = Text(label, font_size=20, color=CLAIR, weight=BOLD)
        r = RoundedRectangle(corner_radius=0.12, width=t.width + 0.35, height=t.height + 0.2,
                             stroke_width=0, fill_color=PUCE_F, fill_opacity=1)
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

    def titre(self, s, fs=38, y=2.85):
        t = tx(s, fs, WHITE, bold=True).move_to(UP * y)
        self.p(FadeIn(t, shift=DOWN * 0.15), rt=0.6)
        return t

    def apparait(self, m, rt=0.8, shift=UP * 0.15):
        self.p(FadeIn(m, shift=shift), rt=rt)
        return m

    def encadre(self, eq, rt=1.0):
        rect = SurroundingRectangle(eq, color=BOX, buff=0.2, corner_radius=0.08, stroke_width=3)
        lab = etiquette("Expression littérale", BOX).next_to(rect, UP, buff=0.06).align_to(rect, LEFT)
        self.p(Create(rect), FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return VGroup(rect, lab)

    def tag_an(self, m, rt=0.4):
        lab = etiquette("Application numérique", SOFT).next_to(m, UP, buff=0.08).align_to(m, LEFT)
        self.p(FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return lab

    def reponse(self, s, rt=1.2, fs=26):
        t = tx(s, fs, RES, w=12.4)
        box = SurroundingRectangle(t, color=RES, buff=0.2, corner_radius=0.12, stroke_width=2.5)
        box.set_fill(RES, opacity=0.08)
        g = VGroup(box, t).to_edge(DOWN, buff=0.4)
        lab = etiquette("Phrase réponse", RES).next_to(box, UP, buff=0.06).align_to(box, LEFT)
        self.p(Create(box), FadeIn(lab), FadeIn(t, shift=UP * 0.15), rt=rt)
        return VGroup(g, lab)

    # ---------------- Charte 3Blue1Brown ----------------
    def designer(self, m, c=HL, echelle=1.1, rt=1.0):
        """« On parle de lui » : m grossit un instant en jaune puis revient."""
        self.p(Indicate(m, scale_factor=echelle, color=c), rt=rt)

    def grossir(self, m, *extra, f=1.25, rt=0.8):
        """Un dessin (tache, molécule…) grossit un instant puis revient, en gardant ses couleurs."""
        self.p(m.animate(rate_func=there_and_back).scale(f), *extra, rt=rt)

    def vol(self, source, cible, *extra, arc=-60 * DEGREES, rt=1.0):
        self.p(TransformFromCopy(source, cible, path_arc=arc), *extra, rt=rt)

    def deduire(self, ancienne, nouvelle, *extra, rt=1.5, **kw):
        self.p(TransformMatchingTex(ancienne, nouvelle, path_arc=-20 * DEGREES, **kw), *extra, rt=rt)

    def eclair(self, m, c=HL, rt=1.0):
        self.p(Circumscribe(m, color=c, buff=0.1), rt=rt)

    def souligner(self, m, c=HL, rt=0.6):
        u = Underline(m, color=c, buff=0.06, stroke_width=3)
        self.p(Create(u), rt=rt)
        return u

    def estomper(self, *mobs, op=0.2, rt=0.6, extra=()):
        self.p(*[m.animate.set_opacity(op) for m in mobs], *extra, rt=rt)

    def raviver(self, *mobs, rt=0.6, extra=()):
        self.p(*[m.animate.set_opacity(1) for m in mobs], *extra, rt=rt)

    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.hdr_ex = tx("Chapitre 2.1 · Identification des espèces chimiques", 22, SOFT).to_corner(UL, buff=0.35)

        # ---------- Titre ----------
        self.at(T["titre"])
        TIT = VGroup(tx("Bilan · Chapitre 2.1", 32, SOFT),
                     tx("Identification des", 64, WHITE, bold=True),
                     tx("espèces chimiques", 64, WHITE, bold=True)).arrange(DOWN, buff=0.25)
        self.p(FadeIn(TIT, shift=UP * 0.2, lag_ratio=0.1), rt=1.5)
        self.at(T["question"] - 0.6)
        self.p(FadeOut(TIT), FadeIn(self.hdr_ex), rt=0.6)
        self.at(T["question"])
        Q = tx("Comment savoir de quoi est faite une substance ?", 40, WHITE, bold=True, w=12.2).move_to(UP * 2.5)
        self.apparait(Q)

        def carte(icone, titre):
            cadre = RoundedRectangle(corner_radius=0.2, width=3.9, height=3.4, stroke_color=GRIS2, stroke_width=2)
            t = lignes(*titre, fs=32, c=WHITE, buff=0.08)
            for l in t:
                l.set_x(0)
            g = VGroup(icone, t).arrange(DOWN, buff=0.35).move_to(cadre)
            return VGroup(cadre, g)
        ic1 = VGroup(mx(r"\rho", RHO, 96), mx(r"\theta", WHITE, 96)).arrange(RIGHT, buff=0.5)
        ic2 = VGroup(tube(EAU_N, 0.5, h=1.4, w=0.45), tube("#E0E0E0", 0.8, h=1.4, w=0.45)).arrange(RIGHT, buff=0.4)
        mini = Rectangle(width=1.2, height=1.5, stroke_width=0, fill_color=PLAQUE, fill_opacity=1)
        ic3 = VGroup(mini, tache(JAUNE, 0.25, 0.2).move_to(mini.get_center() + LEFT * 0.3 + UP * 0.35),
                     tache(BLEU, 0.25, 0.2).move_to(mini.get_center() + RIGHT * 0.3 + DOWN * 0.2))
        C1 = carte(ic1, ["Propriétés", "physiques"]).move_to([-4.4, -0.7, 0])
        C2 = carte(ic2, ["Tests", "chimiques"]).move_to([0, -0.7, 0])
        C3 = carte(ic3, ["Chromatographie", "(CCM)"]).move_to([4.4, -0.7, 0])
        self.at(T["m1"])
        self.apparait(C1)
        self.at(T["m2"])
        self.p(FadeIn(C2, shift=UP * 0.15), C1.animate.set_opacity(0.35), rt=0.8)
        self.at(T["m3"])
        self.p(FadeIn(C3, shift=UP * 0.15), C2.animate.set_opacity(0.35), rt=0.8)

        # ---------- 1 · Vocabulaire ----------
        self.at(T["vocab"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("1 · Vocabulaire")
        self.at(T["entites"])
        TE = tx("La matière est faite d'entités chimiques", 38, WHITE, bold=True).move_to(UP * 2.75)
        self.apparait(TE)
        E1 = VGroup(particule(CLAIR, 0.38), tx("atomes", 32, WHITE)).arrange(DOWN, buff=0.25)
        E2 = VGroup(ion(), tx("ions", 32, WHITE)).arrange(DOWN, buff=0.25)
        E3 = VGroup(h2o(1.0), tx("molécules", 32, WHITE)).arrange(DOWN, buff=0.25)
        ENT = VGroup(E1, E2, E3).arrange(RIGHT, buff=2.4).move_to(UP * 1.2)
        self.at(T["atomes"])
        self.apparait(E1, rt=0.6)
        self.at(T["ions"])
        self.apparait(E2, rt=0.6)
        self.at(T["molecules"])
        self.apparait(E3, rt=0.6)
        self.at(T["espece"])
        DEF = row(tx("Espèce chimique :", 36, WHITE, bold=True), tx("ensemble d'entités identiques", 36, WHITE),
                  buff=0.3).move_to(DOWN * 0.4)
        ajuster(DEF, 12.6)
        self.p(FadeIn(DEF, shift=UP * 0.15), ENT.animate.set_opacity(0.2), TE.animate.set_opacity(0.2), rt=0.8)
        self.souligner(DEF[0])
        self.at(T["eau"])
        MOL = grille(lambda i, j: h2o(0.75), 5, 2, dx=1.15, dy=0.95)
        BX = boite(MOL, w=6.6, h=2.2).move_to([-1.6, -2.35, 0])
        self.p(FadeIn(BX), rt=1.0)
        self.at(T["h2o"])
        LEAU = mx(r"\text{eau : } \mathrm{H_2O}", WHITE, 60).next_to(BX, RIGHT, buff=0.45)
        ajuster(LEAU, 6.6 - BX.get_right()[0] - 0.45)
        self.p(FadeIn(LEAU), rt=0.6)
        self.grossir(MOL[2], f=1.4, rt=0.9)

        # Corps pur / mélange
        self.at(T["corps_pur"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["corps_pur"])
        CPT = VGroup(tx("Corps pur", 46, WHITE, bold=True), tx("1 seule espèce chimique", 30, SOFT)).arrange(
            DOWN, buff=0.2).move_to([-3.5, 2.3, 0])
        ORS = grille(lambda i, j: particule(OR_N, 0.28), 5, 3, dx=0.7, dy=0.6)
        BOR = boite(ORS, w=4.4, h=2.3).move_to([-3.5, 0.0, 0])
        self.p(FadeIn(CPT), FadeIn(BOR), rt=1.0)
        self.at(T["pepite"])
        PEP = VGroup(pepite(1.2), tx("pépite d'or", 30, WHITE)).arrange(DOWN, buff=0.2).move_to([-3.5, -2.45, 0])
        self.apparait(PEP)
        self.at(T["melange"])
        MT = VGroup(tx("Mélange", 46, WHITE, bold=True), tx("plusieurs espèces chimiques", 30, SOFT)).arrange(
            DOWN, buff=0.2).move_to([3.5, 2.3, 0])
        teintes = [(CLAIR, 0.28), (GRIS2, 0.22), (O_ROUGE, 0.2)]
        MIX = grille(lambda i, j: particule(*teintes[(i + 2 * j) % 3]), 5, 3, dx=0.7, dy=0.6)
        BMI = boite(MIX, w=4.4, h=2.3).move_to([3.5, 0.0, 0])
        self.p(FadeIn(MT), FadeIn(BMI), VGroup(CPT, BOR, PEP).animate.set_opacity(0.2), rt=1.0)
        self.at(T["ex_mel"])
        EXM = lignes("jus d'orange", "acier", "eau de Javel", fs=30, c=WHITE, buff=0.1).move_to([3.5, -2.45, 0])
        self.p(LaggedStart(*[FadeIn(l, shift=UP * 0.1) for l in EXM], lag_ratio=0.4), rt=1.5)

        # Homogène / hétérogène
        self.at(T["deux_cas"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["deux_cas"])
        self.titre("Deux sortes de mélanges")
        self.at(T["homogene"])
        BH = becher([(1.9, EAU_N, 0.5)]).move_to([-3.5, 0.45, 0])
        LH = VGroup(tx("Homogène", 42, WHITE, bold=True), tx("1 seule phase visible", 30, SOFT)).arrange(
            DOWN, buff=0.12).next_to(BH, DOWN, buff=0.35)
        self.p(FadeIn(BH, shift=UP * 0.2), FadeIn(LH), rt=1.0)
        self.at(T["homog_ex"])
        EXH = tx("eau salée · eau + éthanol", 28, WHITE).next_to(LH, DOWN, buff=0.25)
        self.apparait(EXH, rt=0.6)
        self.at(T["hetero"])
        BT = becher([(0.3, SABLE, 1.0), (1.0, EAU_N, 0.5), (0.6, HUILE, 0.85)]).move_to([3.5, 0.45, 0])
        LT = VGroup(tx("Hétérogène", 42, WHITE, bold=True), tx("plusieurs phases visibles", 30, SOFT)).arrange(
            DOWN, buff=0.12).next_to(BT, DOWN, buff=0.35)
        self.p(FadeIn(BT, shift=UP * 0.2), FadeIn(LT), VGroup(BH, LH, EXH).animate.set_opacity(0.2), rt=1.0)
        self.eclair(BT, rt=1.0)
        self.at(T["hetero_ex"])
        EXT = tx("huile + eau · eau + sable", 28, WHITE).next_to(LT, DOWN, buff=0.25)
        self.apparait(EXT, rt=0.6)

        # L'air : diagramme circulaire en nuances de gris (composition en volume)
        self.at(T["air"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["air"])
        self.titre("L'air : un mélange homogène de gaz")
        R, CENT = 2.3, np.array([-3.3, -0.6, 0])
        def part(debut, frac_, c):
            return AnnularSector(inner_radius=0, outer_radius=R, angle=frac_ * TAU, start_angle=debut * TAU + PI / 2,
                                 fill_color=c, fill_opacity=1, stroke_color=INK, stroke_width=3).shift(CENT)
        SN2, SO2, SAU = part(0, 0.78, GRIS2), part(0.78, 0.21, CLAIR), part(0.99, 0.01, GRIS3)
        def legende(c, pct, nom, form=None):
            items = [Square(0.42, stroke_width=0, fill_color=c, fill_opacity=1), tx(pct, 50, WHITE, bold=True),
                     tx(nom, 34, WHITE)]
            if form:
                items.append(mx(form, WHITE, 48))
            return row(*items, buff=0.3)
        LN2 = legende(GRIS2, "78 %", "diazote", r"\mathrm{N_2}")
        LO2 = legende(CLAIR, "21 %", "dioxygène", r"\mathrm{O_2}")
        LAU = legende(GRIS3, "< 1 %", "autres gaz")
        LEG = VGroup(LN2, LO2, LAU).arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([3.0, -0.4, 0])
        VOL_ = tx("(pourcentages en volume)", 26, SOFT).next_to(LEG, DOWN, buff=0.5).align_to(LEG, LEFT)
        self.at(T["air_n2"])
        self.p(Create(SN2), FadeIn(LN2), FadeIn(VOL_), rt=1.5)
        self.at(T["air_o2"])
        self.p(Create(SO2), FadeIn(LO2), LN2.animate.set_opacity(0.35), rt=1.0)
        self.at(T["air_autres"])
        self.p(FadeIn(SAU), FadeIn(LAU), LO2.animate.set_opacity(0.35), rt=0.8)
        self.p(LN2.animate.set_opacity(1), LO2.animate.set_opacity(1), rt=0.6)

        # ---------- 2 · Propriétés physiques ----------
        self.at(T["prop"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("2 · Propriétés physiques")
        M1 = VGroup(tx("Méthode 1", 32, SOFT),
                    tx("Mesurer ses propriétés physiques", 44, WHITE, bold=True),
                    tx("et les comparer à des valeurs de référence", 40, WHITE)).arrange(DOWN, buff=0.3)
        self.at(T["prop"])
        self.apparait(M1)
        self.souligner(M1[2])
        self.at(T["rho"] - 0.5)
        self.vider(rt=0.5)
        self.at(T["rho"])
        TR = row(tx("La masse volumique", 42, WHITE, bold=True), mx(r"\rho", RHO, 80), buff=0.4).move_to(UP * 2.6)
        self.apparait(TR)
        self.at(T["rho_rel"])
        REL = row(mx(r"\rho", RHO, 140), mx("=", WHITE, 140),
                  frac(mx("m", MASSE, 140), mx("V", VOL, 140)), buff=0.35).move_to([-2.8, -0.3, 0])
        self.p(Write(REL), rt=1.5)
        U1 = row(mx("m", MASSE, 60), tx(": masse en grammes (g)", 34, WHITE), buff=0.25)
        U2 = row(mx("V", VOL, 60), tx(": volume en litres (L)", 34, WHITE), buff=0.25)
        U3 = row(mx(r"\rho", RHO, 60), tx(": en", 34, WHITE), mx(r"\mathrm{g\cdot L^{-1}}", WHITE, 60), buff=0.25)
        UN = VGroup(U1, U2, U3).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.4, -0.3, 0])
        self.at(T["rho_m"])
        self.p(FadeIn(U1, shift=LEFT * 0.2), Indicate(REL[2][0], scale_factor=1.15, color=HL), rt=1.0)
        self.at(T["rho_v"])
        self.p(FadeIn(U2, shift=LEFT * 0.2), Indicate(REL[2][2], scale_factor=1.15, color=HL), rt=1.0)
        self.at(T["rho_gl"] + 0.6)
        self.p(FadeIn(U3, shift=LEFT * 0.2), Indicate(REL[0], scale_factor=1.15, color=HL), rt=1.0)

        # Comparaison des masses volumiques (barres)
        self.at(T["eau_rho"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["eau_rho"])
        TB = row(tx("Masses volumiques", 38, WHITE, bold=True), mx(r"(\mathrm{g\cdot L^{-1}})", SOFT, 42), buff=0.3)
        TB.move_to(UP * 2.85)
        X0, K = -2.6, 8.4 / 7870
        rangs = {"eau": 1.55, "eth": 0.45, "fer": -0.65, "air": -1.75}

        def barre_h(cle, valeur, nom):
            y = rangs[cle]
            L = max(valeur * K, 0.04)
            r = Rectangle(width=L, height=0.62, stroke_width=0, fill_color=RHO, fill_opacity=0.85)
            r.move_to([X0 + L / 2, y, 0])
            n = tx(nom, 32, WHITE)
            n.move_to([X0 - 0.3 - n.width / 2, y, 0])
            return r, n
        rE, nE = barre_h("eau", 1000, "eau liquide")
        vE = mx(r"1\,000", WHITE, 48).next_to(rE, RIGHT, buff=0.25)
        self.p(FadeIn(TB), FadeIn(nE), GrowFromEdge(rE, LEFT), rt=1.0)
        self.p(FadeIn(vE), rt=0.5)
        self.at(T["bouteille"])
        BOU = VGroup(bouteille(), tx("1 L d'eau = 1 kg", 32, WHITE)).arrange(RIGHT, buff=0.35)
        BOU.move_to([3.6, 1.55, 0])
        self.apparait(BOU)
        self.designer(vE, rt=0.9)
        self.at(T["ethanol"])
        rT, nT = barre_h("eth", 789, "éthanol")
        vT = mx("789", WHITE, 48).next_to(rT, RIGHT, buff=0.25)
        self.p(FadeIn(nT), GrowFromEdge(rT, LEFT), VGroup(rE, nE, vE, BOU).animate.set_opacity(0.35), rt=1.0)
        self.p(FadeIn(vT), rt=0.5)
        self.at(T["fer"])
        rF, nF = barre_h("fer", 7870, "fer")
        vF = mx(r"7\,870", INK, 48).move_to(rF.get_right() + LEFT * 1.1)
        self.p(FadeIn(nF), GrowFromEdge(rF, LEFT), VGroup(rT, nT, vT).animate.set_opacity(0.35), rt=1.5)
        self.p(FadeIn(vF), rt=0.5)
        self.at(T["fer8"])
        vF8 = mx(r"\approx 8\ \mathrm{kg\cdot L^{-1}}", WHITE, 42).next_to(rF, UP, buff=0.05).align_to(rF, RIGHT)
        self.apparait(vF8, rt=0.6)
        self.at(T["air_rho"])
        rA, nA = barre_h("air", 1.3, "air (mélange)")
        vA = mx(r"1{,}3", WHITE, 48).next_to(rA, RIGHT, buff=0.25)
        self.p(FadeIn(nA), FadeIn(rA), FadeIn(vA), VGroup(rF, nF, vF, vF8).animate.set_opacity(0.35), rt=0.8)
        self.at(T["air800"])
        A800 = tx("≈ 800 fois moins que l'eau", 32, WHITE, bold=True).next_to(vA, RIGHT, buff=0.5)
        self.p(FadeIn(A800), VGroup(rE, nE, vE).animate.set_opacity(1), rt=0.8)
        self.p(Indicate(vE, scale_factor=1.1, color=HL), Indicate(vA, scale_factor=1.2, color=HL), rt=1.0)

        # Identifier un liquide grâce à sa masse volumique
        self.at(T["ident"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["ident"])
        TI = row(tx("Identifier un liquide grâce à", 38, WHITE, bold=True), mx(r"\rho", RHO, 64), buff=0.25)
        TI.move_to(UP * 2.85)
        self.apparait(TI, rt=0.6)
        self.at(T["liquide"])
        BI = becher([(1.6, "#DDEEFF", 0.15)], w=2.2, h=2.6).move_to([-4.6, 0.2, 0])
        QI = tx("?", 90, WHITE, bold=True).move_to(BI[0])
        LI = tx("liquide incolore", 30, WHITE).next_to(BI, DOWN, buff=0.3)
        self.p(FadeIn(BI, shift=UP * 0.2), FadeIn(QI), FadeIn(LI), rt=1.0)
        self.at(T["vol50"])
        DV = row(mx("V", VOL, 62), mx("=", WHITE, 62), val("50", r"\mathrm{mL}", WHITE, 62)).move_to([1.4, 1.5, 0])
        self.apparait(DV)
        self.at(T["m395"])
        DM = row(mx("m", MASSE, 62), mx("=", WHITE, 62), val(r"39{,}5", r"\mathrm{g}", WHITE, 62))
        DM.next_to(DV, DOWN, buff=0.45).align_to(DV, LEFT)
        self.apparait(DM)
        # Conversion : 50 × 1 mL, puis « 1 mL » devient « 10⁻³ L »
        self.at(T["conv"])
        CV = MathTex("V", "=", "50", r"\times", r"1\ \mathrm{mL}", font_size=52)
        CV[0].set_color(VOL)
        CV.move_to([0.0, -1.3, 0]).align_to([-2.9, 0, 0], LEFT)
        ETQ_C = tx("Conversion en litres", 24, SOFT).next_to(CV, UP, buff=0.15).align_to(CV, LEFT)
        self.p(FadeIn(ETQ_C), Write(CV), Indicate(DV[2], scale_factor=1.1, color=HL), rt=1.0)
        self.at(T["conv2"])
        CV2 = MathTex("V", "=", "50", r"\times", r"10^{-3}\ \mathrm{L}", font_size=52)
        CV2[0].set_color(VOL)
        CV2.move_to(CV).align_to(CV, LEFT)
        self.deduire(CV, CV2, rt=0.8)
        self.at(T["conv3"])
        CV3 = row(mx("=", WHITE, 52), val(r"0{,}050", r"\mathrm{L}", WHITE, 52)).next_to(CV2, RIGHT, buff=0.25)
        self.p(Write(CV3), rt=0.8)

        # Calcul de ρ : les données se rangent dans une carte, puis volent dans l'application numérique
        self.at(T["lit"] - 0.9)
        DON = VGroup(row(mx("m", MASSE, 38), mx("=", WHITE, 38), val(r"39{,}5", r"\mathrm{g}", WHITE, 38)),
                     row(mx("V", VOL, 38), mx("=", WHITE, 38), val(r"0{,}050", r"\mathrm{L}", WHITE, 38))).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3)
        DON_B = SurroundingRectangle(DON, color=GRIS2, buff=0.25, corner_radius=0.12, stroke_width=2)
        DON_T = tx("Données", 22, SOFT).next_to(DON_B, UP, buff=0.08).align_to(DON_B, LEFT)
        VGroup(DON, DON_B, DON_T).move_to([-4.6, 1.15, 0])
        restes = [m for m in self.mobjects if m not in (self.hdr_ex, self.hdr_q, DM, CV2, CV3, CV)]
        self.p(ReplacementTransform(DM, DON[0]), FadeTransform(VGroup(CV2, CV3), DON[1]),
               FadeIn(DON_B), FadeIn(DON_T), *[FadeOut(m) for m in restes], rt=0.8)
        self.remove(CV, CV2, CV3)
        LIT = row(mx(r"\rho", RHO, 76), mx("=", WHITE, 76), frac(mx("m", MASSE, 76), mx("V", VOL, 76)))
        LIT.move_to([-1.3, 1.15, 0])
        self.at(T["lit"])
        self.p(Write(LIT), rt=1.0)
        self.encadre(LIT, rt=0.8)
        self.at(T["an"])
        AN = row(mx(r"\rho", RHO, 64), mx("=", WHITE, 64),
                 frac(val(r"39{,}5", r"\mathrm{g}", WHITE, 64), val(r"0{,}050", r"\mathrm{L}", WHITE, 64)))
        AN.move_to([3.7, 1.15, 0])
        self.tag_an(AN)
        self.p(Write(AN[0]), Write(AN[1]), Write(AN[2][1]), rt=0.5)
        self.vol(DON[0][2], AN[2][0], rt=0.9)
        self.vol(DON[1][2], AN[2][2], rt=0.9)
        self.at(T["res"])
        RS = row(mx(r"\rho", RHO, 76), mx("=", WHITE, 76),
                 val("790", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), RES, 76)).move_to([-2.6, -1.0, 0])
        self.p(Write(RS), rt=1.0)
        self.eclair(RS[2], RES)
        self.at(T["ref"])
        REF = VGroup(tx("Valeur de référence", 26, SOFT),
                     row(tx("éthanol :", 34, WHITE, bold=True),
                         val("789", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), WHITE, 54), buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12)
        REF.move_to([3.3, -1.0, 0])
        EQ = mx(r"\approx", WHITE, 84).move_to([(RS.get_right()[0] + REF.get_left()[0]) / 2, -1.0, 0])
        self.p(FadeIn(REF), FadeIn(EQ), rt=1.0)
        self.designer(REF[1][1], rt=0.9)
        self.at(T["rep"])
        self.reponse("Ce liquide est sans doute de l'éthanol (790 g/L ≈ 789 g/L).", rt=1.0)

        # Température de changement d'état : courbe de chauffage de l'eau pure
        self.at(T["temp"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["temp"])
        self.titre("La température de changement d'état")
        AX = axes([0, 10, 1], [0, 165, 10], 7.0, 4.4, [-1.0, -0.75, 0])

        def cp(x, th):
            return AX.c2p(x, th + 30)            # données décalées de 30 °C : l'axe des temps reste en bas
        YT = mx(r"\theta\ (^\circ\mathrm{C})", WHITE, 40).next_to(AX, UP, buff=0.05).align_to(AX, LEFT)
        XT = tx("temps", 24, SOFT).next_to(AX.c2p(10, 0), DOWN, buff=0.15)
        pts = [(0, -25), (1.2, 0), (3.4, 0), (5.4, 100), (8.2, 100), (9.4, 128)]
        COURBE = VMobject(color=WHITE, stroke_width=5).set_points_as_corners([cp(x, y) for x, y in pts])
        self.at(T["palier_txt"])
        self.p(Create(AX), FadeIn(YT), FadeIn(XT), rt=1.0)
        self.p(Create(COURBE), rt=3.0)
        self.at(T["palier"])
        P1 = Line(cp(1.2, 0), cp(3.4, 0), color=HL, stroke_width=10)
        P2 = Line(cp(5.4, 100), cp(8.2, 100), color=HL, stroke_width=10)
        LP = contour(tx("paliers", 32, WHITE, bold=True).move_to(cp(3.0, 122)))
        self.p(Create(P1), Create(P2), FadeIn(LP), rt=1.0)
        self.eclair(VGroup(P1, P2), rt=1.0)
        self.at(T["fusion"])
        G0 = DashedLine(cp(0, 0), cp(1.2, 0), color=GRIS2, stroke_width=2)
        V0 = mx(r"0\ ^\circ\mathrm{C}", WHITE, 42).next_to(cp(0, 0), LEFT, buff=0.15)
        F0 = contour(tx("fusion de la glace", 26, WHITE).next_to(P1, DOWN, buff=0.2).shift(RIGHT * 0.3))
        self.p(Create(G0), FadeIn(V0), FadeIn(F0), rt=0.8)
        self.designer(V0, rt=0.8)
        self.at(T["ebullition"])
        G100 = DashedLine(cp(0, 100), cp(5.4, 100), color=GRIS2, stroke_width=2)
        V100 = mx(r"100\ ^\circ\mathrm{C}", WHITE, 42).next_to(cp(0, 100), LEFT, buff=0.15)
        F100 = contour(tx("ébullition de l'eau", 26, WHITE).next_to(P2, UP, buff=0.2))
        self.p(Create(G100), FadeIn(V100), FadeIn(F100), rt=0.8)
        self.designer(V100, rt=0.8)
        self.at(T["melange_temp"])
        CM = AX.plot(lambda x: 5 + 16 * x - 0.15 * x * x, x_range=[0, 8.5], color=GRIS2, stroke_width=4)
        CMD = DashedVMobject(CM, num_dashes=40)
        LM = VGroup(tx("Mélange :", 30, SOFT, bold=True), tx("pas de palier", 30, SOFT)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1).move_to([4.75, 0.6, 0])
        self.p(Create(CMD), FadeIn(LM), rt=1.5)
        self.at(T["tables"])
        TAB = lignes("Température mesurée", "= valeur des tables", "→ corps pur identifié", fs=28, c=WHITE, w=3.6)
        TAB.move_to([4.65, -1.3, 0])
        self.apparait(TAB)
        self.souligner(TAB[2])

        # ---------- 3 · Tests chimiques ----------
        self.at(T["tests"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("3 · Tests chimiques")
        self.at(T["tests"])
        TT = row(tx("Méthode 2 :", 36, SOFT), tx("4 tests chimiques à connaître", 36, WHITE, bold=True),
                 buff=0.3).move_to(UP * 2.85)
        self.apparait(TT)
        POS = [(-3.4, 0.95), (3.4, 0.95), (-3.4, -2.05), (3.4, -2.05)]

        def cadre_test(k):
            return RoundedRectangle(corner_radius=0.15, width=6.5, height=2.75, stroke_color=GRIS2,
                                    stroke_width=2).move_to([POS[k][0], POS[k][1], 0])

        def texte_test(k, formule, nom, reactif, obs):
            g = VGroup(row(mx(formule, WHITE, 56), tx(nom, 28, WHITE), buff=0.25),
                       tx(reactif, 22, SOFT, w=4.1), tx(obs, 26, WHITE, bold=True, w=4.1)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.18)
            ajuster(g, 4.2)
            g.move_to([POS[k][0] + 0.95, POS[k][1], 0])
            return g

        # Eau : sulfate de cuivre anhydre
        self.at(T["t_eau"])
        K1 = cadre_test(0)
        X1 = POS[0][0] - 2.1
        coupe = Ellipse(width=1.5, height=0.5, stroke_color=WHITE, stroke_width=2.5).move_to([X1, POS[0][1] - 0.6, 0])
        poudre = Ellipse(width=1.1, height=0.3, stroke_width=0, fill_color=WHITE, fill_opacity=1).move_to(coupe)
        goutte = Circle(radius=0.12, stroke_width=0, fill_color=EAU_N, fill_opacity=1).move_to([X1, POS[0][1] + 0.9, 0])
        T1 = texte_test(0, r"\mathrm{H_2O}", "eau", "sulfate de cuivre anhydre (poudre blanche)", "→ devient bleu")
        self.p(FadeIn(K1), FadeIn(coupe), FadeIn(poudre), FadeIn(T1[0]), FadeIn(T1[1]), rt=1.0)
        self.at(T["t_eau_bleu"] - 0.8)
        self.p(FadeIn(goutte), rt=0.3)
        self.p(goutte.animate.move_to(poudre.get_center()).set_opacity(0), rt=0.5)
        self.at(T["t_eau_bleu"])
        self.p(poudre.animate.set_fill(CUIVRE_BLEU, opacity=1), FadeIn(T1[2]), rt=1.0)
        G1 = VGroup(K1, coupe, poudre, T1)
        # CO2 : eau de chaux
        self.at(T["t_co2"])
        K2 = cadre_test(1)
        X2 = POS[1][0] - 2.1
        TU2 = tube("#DDEEFF", 0.35).move_to([X2, POS[1][1], 0])
        BULLES = VGroup(*[Circle(radius=0.06, stroke_color=WHITE, stroke_width=2).move_to(
            TU2[1].get_bottom() + UP * (0.15 + 0.2 * k) + RIGHT * (0.08 if k % 2 else -0.08)) for k in range(4)])
        T2 = texte_test(1, r"\mathrm{CO_2}", "dioxyde de carbone", "eau de chaux", "→ se trouble")
        self.p(FadeIn(K2), FadeIn(TU2), FadeIn(T2[0]), FadeIn(T2[1]), G1.animate.set_opacity(0.2), rt=1.0)
        self.at(T["t_co2_trouble"] - 0.8)
        self.p(FadeIn(BULLES, shift=UP * 0.2), rt=0.8)
        self.p(TU2[1].animate.set_fill("#F5F5F5", opacity=0.95), FadeOut(BULLES), FadeIn(T2[2]), rt=1.0)
        G2 = VGroup(K2, TU2, T2)
        # H2 : détonation
        self.at(T["t_h2"])
        K3 = cadre_test(2)
        X3 = POS[2][0] - 2.1
        TU3 = tube(WHITE, 0.0).rotate(PI).move_to([X3, POS[2][1] + 0.25, 0])
        FL3 = flamme(0.8).move_to([X3, POS[2][1] - 1.0, 0])
        T3 = texte_test(2, r"\mathrm{H_2}", "dihydrogène", "flamme approchée (test à la flamme)",
                        "→ petite détonation")
        self.p(FadeIn(K3), FadeIn(TU3), FadeIn(T3[0]), FadeIn(T3[1]), G2.animate.set_opacity(0.2), rt=1.0)
        self.p(FadeIn(FL3, shift=UP * 0.2), rt=0.6)
        self.at(T["t_h2_pop"])
        POP = VGroup(Star(n=10, outer_radius=0.75, inner_radius=0.4, stroke_width=0, fill_color=WHITE,
                          fill_opacity=1), tx("POP !", 24, INK, bold=True)).move_to([X3, POS[2][1] - 0.35, 0])
        POP[1].move_to(POP[0])
        self.p(GrowFromCenter(POP), FadeIn(T3[2]), rt=0.6)
        G3 = VGroup(K3, TU3, FL3, POP, T3)
        # O2 : allumette incandescente
        self.at(T["t_o2"])
        K4 = cadre_test(3)
        X4 = POS[3][0] - 2.1
        AL = allumette().move_to([X4, POS[3][1], 0])
        T4 = texte_test(3, r"\mathrm{O_2}", "dioxygène", "allumette incandescente (point rouge)", "→ se rallume")
        self.p(FadeIn(K4), FadeIn(AL), FadeIn(T4[0]), FadeIn(T4[1]), G3.animate.set_opacity(0.2), rt=1.0)
        self.at(T["t_o2_braise"])
        BR = Circle(radius=0.16, stroke_width=0, fill_color="#FF3B30", fill_opacity=1).move_to(AL[1])
        self.p(FadeIn(BR), rt=0.5)
        self.designer(BR, c="#FF8C1A", echelle=1.4, rt=1.0)
        self.at(T["t_o2_feu"])
        FL4 = flamme(0.9).next_to(AL[1], UP, buff=-0.15)
        self.p(GrowFromEdge(FL4, DOWN), FadeIn(T4[2]), rt=0.8)
        self.p(G1.animate.set_opacity(1), G2.animate.set_opacity(1), G3.animate.set_opacity(1), rt=0.6)

        # ---------- 4 · Chromatographie sur couche mince ----------
        self.at(T["ccm"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("4 · Chromatographie")
        self.at(T["ccm"])
        M3 = VGroup(tx("Méthode 3", 32, SOFT),
                    tx("La chromatographie sur couche mince", 46, WHITE, bold=True)).arrange(DOWN, buff=0.3)
        M3.move_to(UP * 1.6)
        self.apparait(M3)
        self.at(T["ccm_sigle"])
        SIG = row(tx("C", 120, WHITE, bold=True), tx("C", 120, WHITE, bold=True), tx("M", 120, WHITE, bold=True),
                  buff=0.5).move_to(DOWN * 0.6)
        self.p(LaggedStart(*[FadeIn(l, scale=1.5) for l in SIG], lag_ratio=0.4), M3.animate.set_opacity(0.35), rt=1.2)
        self.at(T["ccm_but"])
        BUT = tx("séparer et identifier les espèces d'un mélange homogène", 32, WHITE).move_to(DOWN * 2.6)
        self.apparait(BUT)
        self.souligner(BUT)

        # Exemple : sirop de menthe
        self.at(T["sirop"] - 0.5)
        self.vider(rt=0.5)
        self.at(T["sirop"])
        VERRE = becher([(1.8, VERT, 0.9)], w=1.9, h=2.4).move_to([-3.5, 0.1, 0])
        SIR = tx("sirop de menthe", 38, WHITE, bold=True).next_to(VERRE, DOWN, buff=0.35)
        self.p(FadeIn(VERRE, shift=UP * 0.2), FadeIn(SIR), rt=1.0)
        self.at(T["quels"])
        QC = VGroup(tx("Quels colorants", 46, WHITE, bold=True), tx("contient-il ?", 46, WHITE, bold=True)).arrange(
            DOWN, buff=0.2).move_to([2.6, 0.2, 0])
        self.apparait(QC)

        # La plaque (à gauche) et la colonne d'explications (à droite, entre x = 0,6 et x = 6,6)
        self.at(T["plaque"] - 0.5)
        self.vider(rt=0.5)
        PX, PY, PW, PH = -3.4, -0.45, 3.9, 5.4
        BAS, HAUT = PY - PH / 2, PY + PH / 2
        YD = BAS + 0.6                       # ligne de dépôt (1 cm du bas)
        YF = HAUT - 0.5                      # front final de l'éluant
        XCOL = [PX - 1.2, PX, PX + 1.2]      # jaune, bleu, sirop
        XR = 0.2
        PL = Rectangle(width=PW, height=PH, stroke_color=GRIS2, stroke_width=2, fill_color=PLAQUE, fill_opacity=1)
        PL.move_to([PX, PY, 0])
        self.at(T["plaque"])
        self.p(FadeIn(PL, shift=UP * 0.2), rt=0.8)
        self.at(T["ligne"])
        LD = Line([PX - PW / 2 + 0.15, YD, 0], [PX + PW / 2 - 0.15, YD, 0], color="#555555", stroke_width=3)
        LLD = lignes("ligne de dépôt", "au crayon, à 1 cm du bas", fs=30, c=WHITE, buff=0.1, w=5.8)
        LLD.move_to([0, YD + 0.25, 0]).align_to([XR, 0, 0], LEFT)
        FLD = Arrow(start=[XR - 0.1, YD + 0.25, 0], end=[PX + PW / 2 + 0.05, YD, 0], color=WHITE, buff=0.05,
                    stroke_width=3, max_tip_length_to_length_ratio=0.15)
        self.p(Create(LD), FadeIn(LLD), GrowArrow(FLD), rt=1.0)
        self.at(T["depots"])
        self.p(FadeOut(LLD), FadeOut(FLD), rt=0.5)
        TD = tx("3 dépôts côte à côte", 34, WHITE, bold=True).move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(TD, rt=0.6)
        DJ = tache(JAUNE).move_to([XCOL[0], YD, 0])
        DB = tache(BLEU).move_to([XCOL[1], YD, 0])
        DS = tache(VERT).move_to([XCOL[2], YD, 0])
        NJ = tx("J", 30, WHITE, bold=True).move_to([XCOL[0], BAS - 0.35, 0])
        NB = tx("B", 30, WHITE, bold=True).move_to([XCOL[1], BAS - 0.35, 0])
        NS = tx("S", 30, WHITE, bold=True).move_to([XCOL[2], BAS - 0.35, 0])
        LEGD = VGroup(row(tache(JAUNE), tx("J : colorant jaune", 30, WHITE), buff=0.3),
                      row(tache(BLEU), tx("B : colorant bleu", 30, WHITE), buff=0.3),
                      row(tache(VERT), tx("S : sirop de menthe", 30, WHITE), buff=0.3)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35)
        LEGD.next_to(TD, DOWN, buff=0.5).align_to(TD, LEFT)
        self.at(T["dep_j"])
        self.p(FadeIn(DJ, scale=0.3), FadeIn(NJ), FadeIn(LEGD[0]), rt=0.6)
        self.at(T["dep_b"])
        self.p(FadeIn(DB, scale=0.3), FadeIn(NB), FadeIn(LEGD[1]), rt=0.6)
        self.at(T["dep_s"])
        self.p(FadeIn(DS, scale=0.3), FadeIn(NS), FadeIn(LEGD[2]), rt=0.6)

        # La cuve et l'éluant (étiquette « éluant » dans la colonne de droite : jamais près du bord)
        self.at(T["cuve"])
        CB = BAS - 0.3
        CUVE = VGroup(Line([PX - PW / 2 - 0.35, 0.9, 0], [PX - PW / 2 - 0.35, CB, 0]),
                      Line([PX - PW / 2 - 0.35, CB, 0], [PX + PW / 2 + 0.35, CB, 0]),
                      Line([PX + PW / 2 + 0.35, CB, 0], [PX + PW / 2 + 0.35, 0.9, 0])).set_stroke(WHITE, 3)
        EL = Rectangle(width=PW + 0.62, height=0.6, stroke_width=0, fill_color=ELUANT, fill_opacity=0.55)
        EL.move_to([PX, CB + 0.3 + 0.02, 0])
        LEL = tx("éluant", 30, WHITE, bold=True).move_to([0, CB + 0.3, 0]).align_to([XR + 0.4, 0, 0], LEFT)
        FEL = Arrow(start=[XR + 0.3, CB + 0.3, 0], end=[PX + PW / 2 + 0.1, CB + 0.3, 0], color=WHITE, buff=0.05,
                    stroke_width=3, max_tip_length_to_length_ratio=0.15)
        self.p(FadeOut(TD), FadeOut(LEGD), Create(CUVE), FadeIn(EL), FadeIn(LEL), GrowArrow(FEL),
               NJ.animate.set_opacity(0), NB.animate.set_opacity(0), NS.animate.set_opacity(0), rt=1.2)
        self.at(T["attention"])
        ATT = VGroup(tx("Attention :", 36, WHITE, bold=True),
                     lignes("l'éluant reste sous", "la ligne de dépôt", fs=30, c=WHITE, buff=0.08)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        ATT.move_to([0, YD + 1.4, 0]).align_to([XR, 0, 0], LEFT)
        ECART = DoubleArrow(start=[PX + PW / 2 + 0.6, EL.get_top()[1], 0], end=[PX + PW / 2 + 0.6, YD, 0], buff=0,
                            color=HL, stroke_width=4, tip_length=0.15)
        self.p(FadeIn(ATT), GrowFromCenter(ECART), rt=0.8)
        self.p(Indicate(LD, color=HL, scale_factor=1.05), rt=0.8)

        # Élution : le front monte, les taches se séparent
        self.at(T["elution"])
        self.p(FadeOut(ATT), FadeOut(ECART), FadeOut(LEL), FadeOut(FEL), rt=0.4)
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
        MONTE = tx("L'éluant monte…", 34, WHITE, bold=True, w=5.6).move_to([0, 1.8, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Transform(FRONT0, FRONT1),
               DJ.animate.move_to([XCOL[0], YJ, 0]).stretch(1.15, 1), SJ.animate.move_to([XCOL[2], YJ, 0]).stretch(1.15, 1),
               DB.animate.move_to([XCOL[1], YB_, 0]), SB.animate.move_to([XCOL[2], YB_, 0]),
               FadeIn(MONTE), rt=4.0)
        self.at(T["vitesse"])
        VIT = tx("… mais pas à la même vitesse", 30, WHITE, w=6.0).next_to(MONTE, DOWN, buff=0.25).align_to(MONTE, LEFT)
        self.apparait(VIT, rt=0.6)
        self.at(T["affinite"])
        self.p(FadeOut(MONTE), FadeOut(VIT), rt=0.4)
        AF1 = row(tx("phase fixe", 30, WHITE, bold=True), tx("= la plaque", 30, SOFT), buff=0.25)
        AF2 = row(tx("phase mobile", 30, WHITE, bold=True), tx("= l'éluant", 30, SOFT), buff=0.25)
        AFF = VGroup(AF1, AF2).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, 2.0, 0]).align_to(
            [XR, 0, 0], LEFT)
        self.at(T["aff_plaque"])
        self.p(FadeIn(AF1, shift=LEFT * 0.2), Circumscribe(PL, color=HL, buff=0.05), rt=0.9)
        self.at(T["aff_eluant"])
        self.p(FadeIn(AF2, shift=LEFT * 0.2), Circumscribe(FRONT0, color=HL, buff=0.05), rt=0.9)
        self.at(T["monte_haut"])
        H1 = row(Arrow(start=DOWN * 0.6, end=UP * 0.6, color=WHITE, buff=0, stroke_width=6),
                 lignes("préfère l'éluant", "→ monte haut", fs=30, c=WHITE, buff=0.06), buff=0.35)
        H1.move_to([0, 0.1, 0]).align_to([XR, 0, 0], LEFT)
        self.p(FadeIn(H1), DJ.animate(rate_func=there_and_back).scale(1.4),
               SJ.animate(rate_func=there_and_back).scale(1.4), rt=1.0)
        self.at(T["monte_peu"])
        H2 = row(Arrow(start=DOWN * 0.25, end=UP * 0.25, color=WHITE, buff=0, stroke_width=6),
                 lignes("accrochée à la plaque", "→ monte peu", fs=30, c=WHITE, buff=0.06), buff=0.35)
        H2.move_to([0, -1.5, 0]).align_to([XR, 0, 0], LEFT)
        self.p(FadeIn(H2), DB.animate(rate_func=there_and_back).scale(1.4),
               SB.animate(rate_func=there_and_back).scale(1.4), H1.animate.set_opacity(0.35), rt=1.0)

        # On sort la plaque, on marque le front
        self.at(T["sortie"])
        self.p(FadeOut(CUVE), FadeOut(EL), FadeOut(AFF), FadeOut(H1), FadeOut(H2),
               FRONT0.animate.set_opacity(0.12), rt=0.8)
        self.at(T["front"])
        LF = DashedLine([PX - PW / 2 + 0.1, YF, 0], [PX + PW / 2 - 0.1, YF, 0], color="#555555", stroke_width=3)
        LLF = tx("front de l'éluant", 30, WHITE).move_to([0, YF, 0]).align_to([XR + 0.4, 0, 0], LEFT)
        FLF = Arrow(start=[XR + 0.3, YF, 0], end=[PX + PW / 2 + 0.05, YF, 0], color=WHITE, buff=0.05, stroke_width=3,
                    max_tip_length_to_length_ratio=0.15)
        self.p(Create(LF), FadeIn(LLF), GrowArrow(FLF), NJ.animate.set_opacity(1), NB.animate.set_opacity(1),
               NS.animate.set_opacity(1), rt=1.0)
        self.at(T["chromato"])
        CHR = tx("Le chromatogramme", 36, WHITE, bold=True).move_to([0, 0.6, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(CHR)
        self.souligner(CHR)

        # Lecture verticale : la colonne étudiée reste allumée, les autres pâlissent
        self.at(T["verticale"] - 0.5)
        self.vider(rt=0.5, garder=(PL, LD, LF, FRONT0, DJ, DB, SJ, SB, NJ, NB, NS))
        self.at(T["verticale"])
        LV = row(tx("Lecture verticale", 34, WHITE, bold=True),
                 Arrow(start=UP * 0.4, end=DOWN * 0.4, color=WHITE, buff=0, stroke_width=6), buff=0.3)
        LV.move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(LV)
        YC = (YD + YF) / 2 - 0.1

        def colonne(k):
            return Rectangle(width=1.0, height=YF - YD + 0.8, stroke_color=HL, stroke_width=3).move_to(
                [XCOL[k], YC, 0])
        self.at(T["col_j"])
        COL = colonne(0)
        RJ = row(tx("J :", 30, WHITE, bold=True), tx("1 tache → corps pur", 30, WHITE), buff=0.25)
        RJ.move_to([0, 1.1, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Create(COL), FadeIn(RJ), DB.animate.set_opacity(0.2), SJ.animate.set_opacity(0.2),
               SB.animate.set_opacity(0.2), rt=0.8)
        self.grossir(DJ, f=1.4, rt=0.8)
        self.at(T["col_b"])
        RB = row(tx("B :", 30, WHITE, bold=True), tx("1 tache → corps pur", 30, WHITE), buff=0.25)
        RB.next_to(RJ, DOWN, buff=0.35).align_to(RJ, LEFT)
        self.p(COL.animate.move_to([XCOL[1], YC, 0]), FadeIn(RB), DB.animate.set_opacity(1),
               DJ.animate.set_opacity(0.2), RJ.animate.set_opacity(0.35), rt=0.8)
        self.at(T["col_s"])
        RSI = row(tx("S :", 30, WHITE, bold=True), tx("2 taches → mélange", 30, WHITE, bold=True), buff=0.25)
        RSI.next_to(RB, DOWN, buff=0.35).align_to(RJ, LEFT)
        self.p(COL.animate.move_to([XCOL[2], YC, 0]), FadeIn(RSI), SJ.animate.set_opacity(1),
               SB.animate.set_opacity(1), DB.animate.set_opacity(0.2), RB.animate.set_opacity(0.35), rt=0.8)
        self.grossir(SJ, SB.animate(rate_func=there_and_back).scale(1.4), f=1.4, rt=0.8)

        # Lecture horizontale
        self.at(T["horizontale"] - 0.5)
        self.p(FadeOut(COL), FadeOut(LV), FadeOut(RJ), FadeOut(RB), FadeOut(RSI), DJ.animate.set_opacity(1),
               DB.animate.set_opacity(1), rt=0.5)
        self.at(T["horizontale"])
        LH_ = row(tx("Lecture horizontale", 34, WHITE, bold=True),
                  Arrow(start=LEFT * 0.4, end=RIGHT * 0.4, color=WHITE, buff=0, stroke_width=6), buff=0.3)
        LH_.move_to([0, 2.2, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(LH_)
        self.at(T["meme"])
        MH = lignes("même hauteur", "= même espèce chimique", fs=30, c=WHITE, buff=0.08)
        MH.move_to([0, 1.1, 0]).align_to([XR, 0, 0], LEFT)
        self.apparait(MH)
        self.at(T["ici"])
        HJ = DashedLine([PX - PW / 2, YJ, 0], [PX + PW / 2 + 0.3, YJ, 0], color=WHITE, stroke_width=3)
        HJT = tx("S contient J", 30, WHITE, bold=True).move_to([0, -0.4, 0]).align_to([XR, 0, 0], LEFT)
        self.p(Create(HJ), FadeIn(HJT), DB.animate.set_opacity(0.2), SB.animate.set_opacity(0.2),
               MH.animate.set_opacity(0.35), rt=0.8)
        self.eclair(VGroup(DJ, SJ), rt=0.8)
        self.at(T["ici_b"])
        HB = DashedLine([PX - PW / 2, YB_, 0], [PX + PW / 2 + 0.3, YB_, 0], color=WHITE, stroke_width=3)
        HBT = tx("S contient B", 30, WHITE, bold=True).next_to(HJT, DOWN, buff=0.35).align_to(HJT, LEFT)
        self.p(Create(HB), FadeIn(HBT), DB.animate.set_opacity(1), SB.animate.set_opacity(1),
               DJ.animate.set_opacity(0.2), SJ.animate.set_opacity(0.2), HJ.animate.set_opacity(0.35),
               HJT.animate.set_opacity(0.35), rt=0.8)
        self.eclair(VGroup(DB, SB), rt=0.8)

        # Conclusion : jaune + bleu = vert
        self.at(T["concl"])
        self.p(FadeOut(LH_), FadeOut(MH), FadeOut(HJT), FadeOut(HBT), DJ.animate.set_opacity(1),
               SJ.animate.set_opacity(1), HJ.animate.set_opacity(1), rt=0.5)
        EQC = row(Circle(radius=0.5, stroke_width=0, fill_color=JAUNE, fill_opacity=1), mx("+", WHITE, 76),
                  Circle(radius=0.5, stroke_width=0, fill_color=BLEU, fill_opacity=1), mx("=", WHITE, 76),
                  Circle(radius=0.5, stroke_width=0, fill_color=VERT, fill_opacity=1), buff=0.35)
        EQC.move_to([0, 1.3, 0]).align_to([XR + 0.3, 0, 0], LEFT)
        EQT = VGroup(tx("J", 30, WHITE), tx("B", 30, WHITE), tx("sirop", 30, WHITE))
        for k, idx in enumerate([0, 2, 4]):
            EQT[k].next_to(EQC[idx], DOWN, buff=0.2)
        self.p(FadeIn(EQC[0]), FadeIn(EQC[1]), FadeIn(EQC[2]), FadeIn(EQT[0]), FadeIn(EQT[1]), rt=1.0)
        self.at(T["vert"])
        self.p(FadeIn(EQC[3]), FadeIn(EQC[4], scale=0.5), FadeIn(EQT[2]), rt=1.0)
        CC_ = lignes("Le sirop de menthe contient", "le colorant jaune", "et le colorant bleu.", fs=28, c=RES,
                     buff=0.08)
        CC_B = SurroundingRectangle(CC_, color=RES, buff=0.2, corner_radius=0.12, stroke_width=2.5)
        CC_B.set_fill(RES, opacity=0.08)
        CCG = VGroup(CC_B, CC_).move_to([0, -1.55, 0]).align_to([XR + 0.1, 0, 0], LEFT)
        CCL = etiquette("Phrase réponse", RES).next_to(CC_B, UP, buff=0.06).align_to(CC_B, LEFT)
        self.p(Create(CC_B), FadeIn(CCL), FadeIn(CC_), rt=1.0)

        # ---------- À retenir ----------
        self.at(T["resume"] - 1.1)
        self.vider(rt=0.6)
        self.set_q("À retenir")
        self.at(T["resume"])
        TR_ = tx("À retenir", 46, WHITE, bold=True).move_to(UP * 2.8)
        self.apparait(TR_, rt=0.5)
        RP = row(tx("Corps pur :", 34, WHITE, bold=True), tx("1 seule espèce chimique", 34, WHITE), buff=0.25)
        RM = row(tx("Mélange :", 34, WHITE, bold=True), tx("plusieurs espèces chimiques", 34, WHITE), buff=0.25)
        VGroup(RP, RM).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([0, 1.65, 0])
        self.p(FadeIn(RP), rt=0.6)
        self.at(T["r_mel"])
        self.p(FadeIn(RM), rt=0.6)
        self.at(T["r_ident"])
        RI = tx("Identifier = comparer à des valeurs de référence :", 32, WHITE, bold=True).move_to([0, 0.5, 0])
        self.p(FadeIn(RI), VGroup(RP, RM).animate.set_opacity(0.35), rt=0.6)

        def puce(contenu):
            r = RoundedRectangle(corner_radius=0.15, width=contenu.width + 0.45, height=contenu.height + 0.35,
                                 stroke_color=GRIS2, stroke_width=2)
            return VGroup(r, contenu.move_to(r))
        PU = VGroup(puce(row(tx("masse volumique", 28, WHITE), mx(r"\rho", RHO, 44), buff=0.15)),
                    puce(tx("température de changement d'état", 28, WHITE)),
                    puce(tx("test chimique", 28, WHITE)),
                    puce(tx("hauteur des taches (CCM)", 28, WHITE)))
        L1_ = VGroup(PU[0], PU[1]).arrange(RIGHT, buff=0.4)
        L2_ = VGroup(PU[2], PU[3]).arrange(RIGHT, buff=0.4)
        VGroup(L1_, L2_).arrange(DOWN, buff=0.3).move_to([0, -1.05, 0])
        for cle, k in [("r_rho", 0), ("r_temp", 1), ("r_test", 2), ("r_ccm", 3)]:
            self.at(T[cle])
            self.p(FadeIn(PU[k], scale=0.8), rt=0.6)
        self.at(T["r_eau"])
        RE = row(mx(r"\rho_{\text{eau}} =", RHO, 54), val(r"1\,000", (r"\mathrm{g\cdot}", r"\mathrm{L^{-1}}"), WHITE, 54),
                 buff=0.25)
        RA = row(tx("air (en volume) :", 30, WHITE), mx(r"78\,\%\ \mathrm{N_2}", WHITE, 48),
                 mx(r"21\,\%\ \mathrm{O_2}", WHITE, 48), buff=0.35)
        BLOC3 = VGroup(RE, RA).arrange(RIGHT, buff=0.9).move_to([0, -2.85, 0])
        ajuster(BLOC3, 12.6)
        CAD3 = SurroundingRectangle(BLOC3, color=GRIS2, buff=0.2, corner_radius=0.12, stroke_width=2)
        self.p(FadeIn(RE), Create(CAD3), VGroup(RI, PU).animate.set_opacity(0.35), rt=0.8)
        self.designer(RE[1], rt=0.9)
        self.at(T["r_air"])
        self.p(FadeIn(RA), rt=0.8)
        self.designer(RA[1], rt=0.9)
        self.p(VGroup(RP, RM, RI, PU).animate.set_opacity(1), rt=0.6)
        # Fin : marge de 10 s après la fin du SRT, à couper au montage
        self.at(T["fin_audio"])
        self.pause(10.0)
