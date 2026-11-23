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
#  VIDÉO : Marx, la baisse tendancielle du taux de profit (Capital, livre III)
#  Audio en anglais (SRT TurboScribe, 17 min 51 s) : textes à l'écran en anglais.
#  Exemples chiffrés : ceux de l'audio (burger : v = 0,50 $, c = 1,00 $, prix 2,00 $),
#  puis capital d'une entreprise en milliers de dollars pour les étapes de l'accumulation.
# =====================================================================

# ---------- Couleurs propres à cette vidéo ----------
CC = "#58C4DD"     # capital constant c (bleu)
VC = "#83C167"     # capital variable v (vert)
SC = "#F4D03F"     # plus-value s (jaune)
PC = "#FF7B54"     # taux de profit p' (orange)
BAD = "#FF5555"    # crise, barres, correction
INK = "#111318"    # texte sombre sur les barres colorées

# ---------- Calage sur le SRT (secondes) ----------
T = {
    "titre": 0.30, "vol3": 5.11, "plan": 13.35, "plan_fin": 63.60,
    "corpus": 64.81, "livres": 73.29, "livre3": 81.41, "partie3": 85.00,
    "idee": 95.01, "enonce": 98.59, "graphe_taux": 101.31, "baisse": 104.70,
    "contre": 110.53, "masse": 113.91, "different": 119.79, "magnitude": 125.25,
    "formule_intro": 132.61, "formule": 146.67, "c": 152.95, "c_ex": 156.83, "v": 164.09,
    "s": 167.51, "prix": 176.41,
    "valeur": 181.53, "smith": 187.61, "source": 193.59, "richesse": 198.83,
    "machines": 208.77, "pas_valeur": 214.41, "precision": 222.21,
    "achat": 232.53, "dix_ans": 245.27, "transfert": 255.13, "prix_marche": 263.61,
    "copie": 295.85, "bilan_c": 308.65,
    "travail": 332.41, "journee": 336.83, "plus_dur": 340.43, "moins_paye": 343.91,
    "taux_s": 350.79, "s_def": 356.91, "s_prime": 363.71,
    "burger": 374.05, "salaire": 376.91, "vente": 379.41, "double": 393.85, "s_an": 401.79,
    "s_bar": 405.50, "s_res": 413.51, "s_rep": 415.19,
    "c_burger": 418.75, "c_mat": 426.13, "prix2": 429.19, "decomp": 434.05, "cout": 444.19,
    "plusvalue": 449.53, "taux_p": 455.43, "cmp_2": 469.01, "s_toujours": 476.79,
    "p_lit": 483.35, "p_an": 493.05, "p_bar": 495.20, "p_res": 497.09, "p_note": 499.63,
    "pourquoi": 514.05, "patron": 524.53, "yacht": 535.15, "yacht_x": 537.30, "reinvest": 540.71,
    "moins_ouvriers": 549.19, "moins_salaires": 554.05, "plus_machines": 557.93,
    "proportion": 566.39, "etape2": 574.51, "etape3": 579.87, "moins_travail": 596.01,
    "valeur_travail": 607.37, "taux_calc": 619.97, "ecart_txt": 631.27,
    "ecart": 659.33, "graphe_cv": 667.31, "points": 674.77, "derivation": 685.75, "tendance": 691.81,
    "contradiction": 697.05, "surprod": 709.27, "acheteurs": 715.95, "crise": 725.91,
    "crise2": 728.69, "prix_bas": 736.53,
    "s_monte": 745.15, "avant": 753.03, "apres": 758.63, "apres_s": 768.93, "masse_val": 773.49,
    "s_haut": 801.81, "p_bas": 806.19, "important": 809.49,
    "intenable": 817.71, "attenuer": 829.31, "six": 836.63,
    "f1": 849.87, "f2": 873.69, "f3": 892.69, "f4": 908.49, "f5": 920.27, "f6": 926.23,
    "strategies": 934.37,
    "limites": 943.19, "lim_travail": 951.33, "lim_ress": 959.35, "canette": 963.07,
    "question": 971.11, "gig": 978.21, "uber": 987.15, "salaires_uber": 993.17,
    "sens": 1000.77, "hypothese": 1004.89, "issue": 1013.41, "pas_profit": 1019.41, "airbnb": 1036.53,
    "fin": 1051.19, "fin_audio": 1070.91,
}


# ---------- Petits dessins ----------
def burger(s=1.0):
    pain_h = RoundedRectangle(corner_radius=0.24, width=1.2, height=0.48, fill_color="#E0A040",
                              fill_opacity=1, stroke_width=0)
    salade = RoundedRectangle(corner_radius=0.05, width=1.32, height=0.12, fill_color="#7CC36E",
                              fill_opacity=1, stroke_width=0)
    steak = RoundedRectangle(corner_radius=0.1, width=1.26, height=0.24, fill_color="#7A4A2A",
                             fill_opacity=1, stroke_width=0)
    pain_b = RoundedRectangle(corner_radius=0.1, width=1.2, height=0.22, fill_color="#E0A040",
                              fill_opacity=1, stroke_width=0)
    return VGroup(pain_h, salade, steak, pain_b).arrange(DOWN, buff=0.03).scale(s)


def ouvrier(c=VC, s=1.0):
    tete = Circle(radius=0.18, stroke_width=0, fill_color=c, fill_opacity=1)
    corps = RoundedRectangle(corner_radius=0.2, width=0.5, height=0.55, stroke_width=0,
                             fill_color=c, fill_opacity=1)
    return VGroup(tete, corps).arrange(DOWN, buff=0.06).scale(s)


def machine(c=CC, s=1.0):
    corps = RoundedRectangle(corner_radius=0.1, width=1.6, height=1.0, stroke_color=c, stroke_width=3,
                             fill_color=c, fill_opacity=0.15)
    r1 = Circle(radius=0.24, stroke_color=c, stroke_width=3).move_to(corps.get_center() + LEFT * 0.4)
    r2 = Circle(radius=0.16, stroke_color=c, stroke_width=3).move_to(corps.get_center() + RIGHT * 0.35 + UP * 0.12)
    pied = Line(corps.get_corner(DL) + RIGHT * 0.2 + DOWN * 0.12, corps.get_corner(DR) + LEFT * 0.2 + DOWN * 0.12,
                color=c, stroke_width=3)
    return VGroup(corps, r1, r2, pied).scale(s)


def usine(c=CC, s=1.0):
    pts = [[-1, -0.5, 0], [-1, 0.2, 0], [-0.6, 0.5, 0], [-0.6, 0.2, 0], [-0.2, 0.5, 0], [-0.2, 0.2, 0],
           [0.2, 0.5, 0], [0.2, 0.2, 0], [1, 0.2, 0], [1, -0.5, 0]]
    corps = Polygon(*pts, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.15)
    chem = Rectangle(width=0.22, height=0.6, stroke_color=c, stroke_width=3).move_to([0.65, 0.5, 0])
    return VGroup(corps, chem).scale(s)


def matieres(c=CC, s=1.0):
    def cube():
        return Square(side_length=0.36, stroke_color=c, stroke_width=3, fill_color=c, fill_opacity=0.3)
    bas = VGroup(cube(), cube()).arrange(RIGHT, buff=0.06)
    haut = cube().next_to(bas, UP, buff=0.06)
    return VGroup(bas, haut).scale(s)


def livre(vol, annee, c=SOFT):
    cadre = RoundedRectangle(corner_radius=0.12, width=2.3, height=3.0, stroke_color=c, stroke_width=3,
                             fill_color=c, fill_opacity=0.12)
    dos = Line(cadre.get_corner(UL) + RIGHT * 0.25, cadre.get_corner(DL) + RIGHT * 0.25, color=c, stroke_width=3)
    t = VGroup(tx("CAPITAL", 26, WHITE, bold=True), tx(vol, 24, c), tx(annee, 20, SOFT)).arrange(DOWN, buff=0.25)
    t.move_to(cadre.get_center() + RIGHT * 0.12)
    return VGroup(cadre, dos, t)


# ---------- Écriture ----------
def dol(x, c=WHITE, fs=40):
    """Montant en dollars : [0] = « $ » (barrable), [1] = nombre."""
    m = MathTex(r"\$", x, font_size=fs)
    m[0].set_color(UNIT)
    m[1].set_color(c)
    return m


def ligne(label, tex, c=WHITE, fs_t=24, fs_m=40):
    """« label » en texte suivi d'une formule (pas de $ dans txm à cause des dollars)."""
    return row(tx(label, fs_t, SOFT), mx(tex, c, fs_m), buff=0.25)


def lignes(*textes, fs=24, c=WHITE, w=LARGEUR, buff=0.12):
    return VGroup(*[tx(t, fs, c, w=w) for t in textes]).arrange(DOWN, aligned_edge=LEFT, buff=buff)


def segment(x0, x1, y, h, col, label=None, fs=30):
    r = Rectangle(width=x1 - x0, height=h, stroke_width=0, fill_color=col, fill_opacity=1)
    r.move_to([(x0 + x1) / 2, y, 0])
    if label is None:
        return VGroup(r)
    lab = mx(label, INK, fs).move_to(r.get_center())
    ajuster(lab, (x1 - x0) - 0.15)
    return VGroup(r, lab)


def pile(x, base, c, v, s, u, w=1.3):
    """Barre verticale c | v | s (du bas vers le haut), étiquettes à droite."""
    hc, hv, hs = c * u, v * u, s * u
    rc = Rectangle(width=w, height=hc, stroke_width=0, fill_color=CC, fill_opacity=1).move_to([x, base + hc / 2, 0])
    rv = Rectangle(width=w, height=hv, stroke_width=0, fill_color=VC, fill_opacity=1).move_to([x, base + hc + hv / 2, 0])
    rs = Rectangle(width=w, height=hs, stroke_width=0, fill_color=SC, fill_opacity=1).move_to(
        [x, base + hc + hv + hs / 2, 0])
    xl = x + w / 2 + 0.15
    lc = mx(r"c = %d" % c, CC, 26)
    lv = mx(r"v = %d" % v, VC, 26)
    ls = mx(r"s = %d" % s, SC, 26)
    lc.move_to([xl + lc.width / 2, base + hc / 2, 0])
    lv.move_to([xl + lv.width / 2, base + hc + hv / 2 - 0.03, 0])
    ls.move_to([xl + ls.width / 2, base + hc + hv + hs / 2 + 0.03, 0])
    return VGroup(VGroup(rc, rv, rs), VGroup(lc, lv, ls))


def carte_def(sym, col, titre, icones, desc):
    cadre = RoundedRectangle(corner_radius=0.15, width=4.0, height=3.3, stroke_color=col, stroke_width=2.5,
                             fill_color=col, fill_opacity=0.06)
    tete = VGroup(mx(sym, col, 60), tx(titre, 24, col, bold=True)).arrange(DOWN, buff=0.12)
    bas = VGroup(icones, lignes(*desc, fs=19, c=WHITE, w=3.6)).arrange(DOWN, buff=0.2)
    contenu = VGroup(tete, bas).arrange(DOWN, buff=0.25).move_to(cadre)
    ajuster(contenu, 3.7, 3.0)
    return VGroup(cadre, tete, bas)


def carte_facteur(n, titre, effet, marx):
    cadre = RoundedRectangle(corner_radius=0.15, width=4.1, height=2.05, stroke_color=SOFT, stroke_width=2,
                             fill_color=SOFT, fill_opacity=0.05)
    num = VGroup(Circle(radius=0.22, stroke_width=0, fill_color=PC, fill_opacity=1),
                 tx(str(n), 20, INK, bold=True))
    num[1].move_to(num[0])
    tit = lignes(*titre, fs=22, c=WHITE, w=3.2, buff=0.06)
    haut = row(num, tit, buff=0.2)
    eff = effet if isinstance(effet, Mobject) else mx(effet, PC, 34)
    note = tx(marx, 15, SOFT, w=3.8)
    contenu = VGroup(haut, eff, note).arrange(DOWN, buff=0.18)
    ajuster(contenu, 3.8, 1.85)
    contenu.move_to(cadre)
    return VGroup(cadre, contenu)


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
        """Attend jusqu'à l'instant t (en secondes) de l'audio."""
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
        """Efface tout sauf l'en-tête et les objets de « garder »."""
        proteges = set()
        for g in (self.hdr_ex, self.hdr_q, *garder):
            if g is not None:
                proteges.update(id(x) for x in g.get_family())
        mobs = [m for m in self.mobjects if id(m) not in proteges]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def barrer(self, *mobs, rt=0.6):
        traits = VGroup(*[barre(m) for m in mobs])
        self.p(LaggedStart(*[Create(l) for l in traits], lag_ratio=0.3), rt=rt)
        return traits

    def encadre(self, eq, texte="Formula", rt=1.0):
        rect = SurroundingRectangle(eq, color=BOX, buff=0.2, corner_radius=0.08, stroke_width=4)
        lab = etiquette(texte, BOX).next_to(rect, UP, buff=0.06).align_to(rect, LEFT)
        self.p(Create(rect), FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return VGroup(rect, lab)

    def tag_an(self, m, rt=0.4):
        lab = etiquette("Calculation", AN_C).next_to(m, UP, buff=0.08).align_to(m, LEFT)
        self.p(FadeIn(lab, shift=DOWN * 0.1), rt=rt)
        return lab

    def reponse(self, s, rt=1.2, fs=23):
        t = txm(s, fs, RES, w=12.0) if "$" in s else tx(s, fs, RES, w=12.0)
        box = SurroundingRectangle(t, color=RES, buff=0.2, corner_radius=0.12, stroke_width=3)
        box.set_fill(RES, opacity=0.08)
        g = VGroup(box, t).to_edge(DOWN, buff=0.28)
        lab = etiquette("Answer", RES).next_to(box, UP, buff=0.06).align_to(box, LEFT)
        self.p(Create(box), FadeIn(lab), FadeIn(t, shift=UP * 0.15), rt=rt)
        return VGroup(g, lab)

    def apparait(self, m, rt=0.8, shift=UP * 0.15):
        self.p(FadeIn(m, shift=shift), rt=rt)
        return m

    # =================================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None
        self.hdr_ex = tx("Marx · Capital, Volume III", 22, SOFT).to_corner(UL, buff=0.3)

        # ---------- Titre et plan (présentation de la chaîne : écran calme) ----------
        self.at(T["titre"])
        TIT = VGroup(tx("The Tendential Fall", 54, WHITE, bold=True),
                     tx("in the Rate of Profit", 54, WHITE, bold=True)).arrange(DOWN, buff=0.2).move_to(UP * 0.6)
        self.p(FadeIn(TIT, shift=UP * 0.2), rt=1.2)
        self.at(T["vol3"])
        SOUS = tx("Karl Marx · Capital, Volume III (1894)", 28, SOFT).next_to(TIT, DOWN, buff=0.5)
        self.p(FadeIn(SOUS), rt=0.8)
        self.at(T["plan"])
        HAUT = VGroup(TIT, SOUS)
        self.p(HAUT.animate.scale(0.6).to_edge(UP, buff=0.55), FadeIn(self.hdr_ex), rt=1.0)
        PLAN = VGroup(
            txm(r"1.  The formula  $c + v + s$", 28),
            tx("2.  Rate of surplus value vs rate of profit", 28),
            tx("3.  Why the rate of profit tends to fall", 28),
            tx("4.  Counteracting factors", 28),
            tx("5.  An open question: the gig economy", 28),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to(DOWN * 0.9)
        self.p(LaggedStart(*[FadeIn(l, shift=RIGHT * 0.2) for l in PLAN], lag_ratio=0.5), rt=4.0)
        self.at(T["plan_fin"])
        self.p(FadeOut(TIT), FadeOut(SOUS), FadeOut(PLAN), rt=0.8)

        # ---------- Le Capital : trois livres ----------
        self.at(T["corpus"])
        CLE = tx("A key concept of Capital", 34, WHITE).move_to(UP * 2.6)
        self.apparait(CLE)
        self.at(T["livres"])
        L1 = livre("Volume I", "1867")
        L2 = livre("Volume II", "1885")
        L3 = livre("Volume III", "1894", PC)
        LIV = VGroup(L1, L2, L3).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.2)
        self.p(LaggedStart(*[FadeIn(l, shift=UP * 0.3) for l in LIV], lag_ratio=0.4), rt=2.0)
        self.at(T["livre3"])
        self.p(VGroup(L1, L2).animate.set_opacity(0.3), L3.animate.scale(1.12), rt=1.0)
        self.at(T["partie3"])
        P3 = lignes("Part III: the law of the tendency", "of the rate of profit to fall (ch. 13–15)",
                    fs=22, c=PC, w=5.0).next_to(L3, DOWN, buff=0.3)
        P3.set_x(L3.get_center()[0])
        self.apparait(P3)

        # ---------- 1 · L'idée ----------
        self.at(T["idee"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("1 · The idea")
        self.at(T["enonce"])
        ENO = tx("As capitalist production grows, the rate of profit tends to fall.", 30, WHITE).move_to(UP * 2.6)
        self.apparait(ENO)
        self.at(T["graphe_taux"])
        AXR = axes([0, 10, 1], [0, 1, 0.25], 5.2, 3.2, [3.3, -0.4, 0])
        YR = tx("rate of profit", 22, PC).next_to(AXR, UP, buff=0.1).align_to(AXR, LEFT)
        XR = tx("development of production", 20, SOFT).next_to(AXR, DOWN, buff=0.15)
        self.p(Create(AXR), FadeIn(YR), FadeIn(XR), rt=1.0)
        self.at(T["baisse"])
        CR = AXR.plot(lambda x: 0.8 * math.exp(-x / 7) + 0.05 * math.sin(2.2 * x), x_range=[0, 10], color=PC,
                      stroke_width=4)
        self.p(Create(CR), rt=3.0)
        self.at(T["contre"])
        CONTRE = tx("Counter-intuitive?", 26, SOFT).next_to(ENO, DOWN, buff=0.3)
        self.apparait(CONTRE, rt=0.6)
        self.at(T["masse"])
        AXL = axes([0, 10, 1], [0, 1, 0.25], 5.2, 3.2, [-3.3, -0.4, 0])
        YL = tx("total profit (mass)", 22, RES).next_to(AXL, UP, buff=0.1).align_to(AXL, LEFT)
        XL = tx("development of production", 20, SOFT).next_to(AXL, DOWN, buff=0.15)
        CL = AXL.plot(lambda x: 0.12 + 0.075 * x + 0.02 * math.sin(2 * x), x_range=[0, 10], color=RES, stroke_width=4)
        self.p(Create(AXL), FadeIn(YL), FadeIn(XL), rt=1.0)
        self.p(Create(CL), rt=2.5)
        self.at(T["different"])
        NEQ = mx(r"\neq", WHITE, 80).move_to([0, -0.4, 0])
        self.p(Write(NEQ), rt=0.8)
        self.at(T["magnitude"])
        DIFF = tx("Rate of profit ≠ total amount of profit", 26, WHITE).move_to(DOWN * 3.0)
        self.apparait(DIFF)

        # ---------- 2 · c + v + s ----------
        self.at(T["formule_intro"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("2 · c + v + s")
        self.at(T["formule"])
        FORM = MathTex("c", "+", "v", "+", "s", "=", "C", font_size=96).move_to([-1.8, 2.05, 0])
        FORM[0].set_color(CC)
        FORM[2].set_color(VC)
        FORM[4].set_color(SC)
        self.p(Write(FORM), rt=1.5)
        KC = carte_def("c", CC, "Constant capital",
                       VGroup(usine(s=0.42), machine(s=0.42), matieres(s=0.8)).arrange(RIGHT, buff=0.25),
                       ["factories, machines,", "raw materials"]).move_to([-4.45, -1.0, 0])
        KV = carte_def("v", VC, "Variable capital",
                       VGroup(*[ouvrier(s=0.7) for _ in range(3)]).arrange(RIGHT, buff=0.2),
                       ["labour:", "the wages paid"]).move_to([0, -1.0, 0])
        KS = carte_def("s", SC, "Surplus value",
                       mx(r"+", SC, 60),
                       ["extracted on top of", "what is paid in wages"]).move_to([4.45, -1.0, 0])
        self.at(T["c"])
        self.p(Indicate(FORM[0], color=CC), FadeIn(KC[0]), FadeIn(KC[1]), rt=1.0)
        self.at(T["c_ex"])
        self.p(FadeIn(KC[2], shift=UP * 0.1), rt=0.8)
        self.at(T["v"])
        self.p(Indicate(FORM[2], color=VC), FadeIn(KV), rt=1.0)
        self.at(T["s"])
        self.p(Indicate(FORM[4], color=SC), FadeIn(KS), rt=1.0)
        self.at(T["prix"])
        FL_C = Arrow(start=FORM[6].get_right() + RIGHT * 0.1, end=FORM[6].get_right() + RIGHT * 1.1,
                     color=WHITE, buff=0, stroke_width=4)
        LC = lignes("value of the product", "(its price)", fs=24, c=WHITE, w=3.4).next_to(FL_C, RIGHT, buff=0.2)
        self.p(Indicate(FORM[6]), GrowArrow(FL_C), FadeIn(LC), rt=1.0)

        # ---------- 3 · D'où vient la valeur ----------
        self.at(T["valeur"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("3 · Where value comes from")
        self.at(T["smith"])
        AXE = Line([-5.2, 1.2, 0], [5.2, 1.2, 0], color=SOFT, stroke_width=3)
        AUT = VGroup()
        for x, nom, ref in [(-4.0, "Adam Smith", "1776 · Wealth of Nations"),
                            (0.0, "David Ricardo", "1817 · Principles"),
                            (4.0, "Karl Marx", "1867 · Capital, Vol. I")]:
            d = Dot([x, 1.2, 0], radius=0.11, color=WHITE)
            t = VGroup(tx(nom, 26, WHITE, bold=True), tx(ref, 19, SOFT)).arrange(DOWN, buff=0.1)
            t.next_to(d, DOWN, buff=0.3)
            AUT.add(VGroup(d, t))
        self.p(Create(AXE), rt=0.6)
        self.p(LaggedStart(*[FadeIn(a, shift=UP * 0.15) for a in AUT], lag_ratio=0.5), rt=2.2)
        self.at(T["source"])
        SRC = tx("Labour is the source of value", 40, RES, bold=True).move_to(DOWN * 1.7)
        SRC_B = SurroundingRectangle(SRC, color=RES, buff=0.25, corner_radius=0.12, stroke_width=3)
        self.p(FadeIn(SRC, shift=UP * 0.15), Create(SRC_B), rt=1.0)
        self.at(T["richesse"])
        RIC = tx("(and of wealth)", 24, SOFT).next_to(SRC_B, DOWN, buff=0.2)
        self.apparait(RIC, rt=0.6)

        # Les machines ne créent pas de valeur : elles transmettent la leur
        self.at(T["machines"] - 0.6)
        self.vider(rt=0.6)
        MAC = machine(s=1.4).move_to([-4.3, 0.8, 0])
        self.p(FadeIn(MAC, shift=UP * 0.2), rt=0.8)
        self.at(T["pas_valeur"])
        PV = lignes("Machines and raw materials (c)", "create no new value…", fs=32, c=WHITE, w=7.6)
        PV.move_to([1.6, 1.2, 0])
        self.apparait(PV)
        self.at(T["precision"])
        PV2 = tx("…they pass their own value on to the products", 26, CC, w=7.6).next_to(PV, DOWN, buff=0.4)
        PV2.align_to(PV, LEFT)
        self.apparait(PV2)

        self.at(T["achat"])
        self.p(FadeOut(PV), FadeOut(PV2), MAC.animate.scale(0.55).move_to([-5.4, 1.9, 0]), rt=0.8)
        X0, LT = -3.9, 9.0
        TR = VGroup(*[Rectangle(width=LT / 10 - 0.04, height=0.6, stroke_width=0, fill_color=CC, fill_opacity=1)
                      .move_to([X0 + LT / 20 + k * LT / 10, 1.9, 0]) for k in range(10)])
        LV = tx("value of the machine", 22, CC).next_to(TR, UP, buff=0.12).align_to(TR, LEFT)
        self.p(FadeIn(TR), FadeIn(LV), rt=0.8)
        self.at(T["dix_ans"])
        BR = Brace(TR, DOWN, color=SOFT)
        BRT = tx("used for 10 years", 22, SOFT).next_to(BR, DOWN, buff=0.1)
        self.p(GrowFromCenter(BR), FadeIn(BRT), rt=0.8)
        BURG = VGroup(*[burger(0.42).move_to([X0 + LT / 20 + k * LT / 10, -0.9, 0]) for k in range(10)])
        self.p(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in BURG], lag_ratio=0.15), rt=1.5)
        self.at(T["transfert"])
        PARTS = TR.copy()
        self.p(LaggedStart(*[PARTS[k].animate.scale(0.5).next_to(BURG[k], UP, buff=0.12) for k in range(10)],
                           lag_ratio=0.15), TR.animate.set_opacity(0.25), rt=2.5)
        CAP = VGroup()
        self.at(T["prix_marche"] - 0.4)
        CAP1 = tx("Each product carries a share of the machine's value: nothing is added", 24, WHITE).move_to(
            DOWN * 2.3)
        self.apparait(CAP1)
        self.at(T["copie"])
        CAP2 = tx("Machines can be copied: a competitor would undercut a higher price", 24, WHITE).move_to(DOWN * 2.3)
        self.p(FadeOut(CAP1), FadeIn(CAP2, shift=UP * 0.15), rt=0.8)
        self.at(T["bilan_c"])
        CAP3 = tx("Constant capital c is passed on, unchanged: it does not grow", 26, CC, bold=True).move_to(
            DOWN * 3.05)
        CAP3_B = SurroundingRectangle(CAP3, color=CC, buff=0.15, corner_radius=0.1, stroke_width=2.5)
        self.p(FadeIn(CAP3), Create(CAP3_B), rt=1.0)

        # Le travail : partie payée (v) et partie non payée (s)
        self.at(T["travail"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["travail"])
        TRV = txm(r"Value grows through labour $v$", 34, WHITE).move_to(UP * 2.5)
        self.apparait(TRV)
        self.at(T["journee"])
        Y0, H0 = 0.7, 0.8
        SV = segment(-5.0, -1.0, Y0, H0, VC, r"\text{paid}")
        SS = segment(-1.0, 3.0, Y0, H0, SC, r"\text{unpaid}")
        LJ = VGroup(mx("v", VC, 40).next_to(SV, DOWN, buff=0.15), mx("s", SC, 40).next_to(SS, DOWN, buff=0.15))
        BJ = Brace(VGroup(SV, SS), UP, color=SOFT)
        BJT = tx("working day", 22, SOFT).next_to(BJ, UP, buff=0.08)
        self.p(FadeIn(SV), FadeIn(SS), FadeIn(LJ), GrowFromCenter(BJ), FadeIn(BJT), rt=1.2)
        self.at(T["plus_dur"])
        SS2 = segment(-1.0, 5.0, Y0, H0, SC, r"\text{unpaid}")
        BJ2 = Brace(VGroup(SV, SS2), UP, color=SOFT)
        BJT2 = tx("working day", 22, SOFT).next_to(BJ2, UP, buff=0.08)
        LS2 = mx("s", SC, 40).next_to(SS2, DOWN, buff=0.15)
        C1 = txm(r"Work longer, harder  →  $s \uparrow$", 26, WHITE).move_to([0, -1.3, 0])
        self.p(Transform(SS, SS2), Transform(BJ, BJ2), Transform(BJT, BJT2), Transform(LJ[1], LS2),
               FadeIn(C1, shift=UP * 0.1), rt=1.2)
        self.at(T["moins_paye"])
        SV3 = segment(-5.0, -2.0, Y0, H0, VC, r"\text{paid}")
        SS3 = segment(-2.0, 5.0, Y0, H0, SC, r"\text{unpaid}")
        LV3 = mx("v", VC, 40).next_to(SV3, DOWN, buff=0.15)
        LS3 = mx("s", SC, 40).next_to(SS3, DOWN, buff=0.15)
        C2 = txm(r"Pay less  →  $v \downarrow$,  $s \uparrow$", 26, WHITE).move_to([0, -2.1, 0])
        self.p(Transform(SV, SV3), Transform(SS, SS3), Transform(LJ[0], LV3), Transform(LJ[1], LS3),
               FadeIn(C2, shift=UP * 0.1), rt=1.2)

        # ---------- 4 · Taux de plus-value et taux de profit ----------
        self.at(T["taux_s"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("4 · Surplus value and profit")
        F2 = MathTex("c", "+", "v", "+", "s", "=", "C", font_size=64).move_to(UP * 2.3)
        F2[0].set_color(CC)
        F2[2].set_color(VC)
        F2[4].set_color(SC)
        self.p(FadeIn(F2), rt=0.8)
        self.at(T["s_def"])
        self.p(Indicate(F2[4], color=SC), rt=1.0)
        self.at(T["s_prime"])
        LIT_S = row(mx("s'", WHITE, 60), mx("=", WHITE, 60), frac(mx("s", SC, 60), mx("v", VC, 60)))
        LIT_S.move_to([2.6, 1.1, 0])
        self.p(FadeOut(F2), Write(LIT_S), rt=1.0)
        self.encadre(LIT_S, "Formula", rt=0.8)
        NOM_S = tx("rate of surplus value", 22, SC).next_to(LIT_S, DOWN, buff=0.35)
        self.apparait(NOM_S, rt=0.5)
        self.at(T["burger"])
        BG = burger(1.3).move_to([-4.4, 1.5, 0])
        WK = ouvrier(s=1.2).next_to(BG, LEFT, buff=0.5)
        self.p(FadeIn(BG, shift=UP * 0.2), FadeIn(WK, shift=UP * 0.2), rt=0.8)
        self.at(T["salaire"])
        LW = ligne("wage paid:", r"v = \$0.50", VC).move_to([-3.6, 0.2, 0])
        LW.align_to(WK, LEFT)
        self.apparait(LW)
        self.at(T["vente"])
        LP = ligne("selling price:", r"\$1.00", WHITE).next_to(LW, DOWN, buff=0.4).align_to(LW, LEFT)
        self.apparait(LP)
        self.at(T["double"])
        LSV = ligne("surplus:", r"s = \$1.00 - \$0.50 = \$0.50", SC).next_to(LP, DOWN, buff=0.4).align_to(LW, LEFT)
        ajuster(LSV, 6.6)
        self.apparait(LSV)
        self.at(T["s_an"])
        nS, dS = dol("0.50", SC, 48), dol("0.50", VC, 48)
        AN_S = row(mx("s'", WHITE, 48), mx("=", WHITE, 48), frac(nS, dS)).move_to([1.2, -1.6, 0])
        self.p(Write(AN_S), rt=1.0)
        self.tag_an(AN_S)
        self.at(T["s_bar"])
        self.barrer(nS[0], dS[0], rt=0.6)
        self.at(T["s_res"])
        RS = row(mx("=", WHITE, 48), mx(r"1 = 100\,\%", RES, 48)).next_to(AN_S, RIGHT, buff=0.2)
        self.p(Write(RS), rt=0.8)
        self.at(T["s_rep"])
        self.reponse("The burger sells for twice what its labour cost: rate of surplus value = 100 %", rt=1.0)

        # Prix complet : c + v + s = 2,00 $
        self.at(T["c_burger"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["c_burger"])
        TB = tx("The price also covers machines and raw materials", 26, WHITE).move_to(UP * 2.9)
        self.apparait(TB)
        YB, HB = 1.15, 0.75
        BC = segment(-4.0, 0.0, YB, HB, CC, r"c = \$1.00")
        BV = segment(0.0, 2.0, YB, HB, VC, r"v = \$0.50")
        BS = segment(2.0, 4.0, YB, HB, SC, r"s = \$0.50")
        self.at(T["c_mat"])
        self.p(FadeIn(BC, shift=RIGHT * 0.2), rt=0.8)
        self.at(T["prix2"])
        CAD = DashedVMobject(Rectangle(width=8.0, height=HB, stroke_color=WHITE, stroke_width=2).move_to([0, YB, 0]),
                             num_dashes=40)
        BP = Brace(CAD, UP, color=WHITE, buff=0.08)
        BPT = mx(r"\text{price: }\$2.00", WHITE, 34).next_to(BP, UP, buff=0.06)
        self.p(Create(CAD), GrowFromCenter(BP), FadeIn(BPT), rt=1.0)
        self.at(T["decomp"])
        self.p(FadeIn(BV, shift=RIGHT * 0.2), rt=0.8)
        self.at(T["cout"])
        BK = Brace(VGroup(BC, BV), DOWN, color=SOFT, buff=0.08)
        BKT = mx(r"\text{cost of production: } c + v = \$1.50", WHITE, 30).next_to(BK, DOWN, buff=0.06)
        self.p(GrowFromCenter(BK), FadeIn(BKT), rt=1.0)
        self.at(T["plusvalue"])
        self.p(FadeIn(BS, shift=RIGHT * 0.2), rt=0.8)
        self.at(T["taux_p"])
        self.p(FadeOut(TB), rt=0.4)
        TP = tx("Rate of profit: profit compared with all the capital advanced", 24, PC).move_to(UP * 2.9)
        self.apparait(TP)
        self.at(T["cmp_2"])
        self.p(Indicate(VGroup(BC, BV, BS), scale_factor=1.03), rt=1.0)
        self.at(T["s_toujours"])
        PUCE = VGroup(mx(r"s' = 100\,\%", SC, 32), tx("(unchanged)", 18, SOFT)).arrange(DOWN, buff=0.06)
        PUCE.next_to(BS, RIGHT, buff=0.35)
        self.apparait(PUCE, rt=0.6)
        self.at(T["p_lit"])
        LIT_P = row(mx("p'", WHITE, 54), mx("=", WHITE, 54),
                    frac(mx("s", SC, 54), MathTex("c", "+", "v", font_size=54)))
        LIT_P[2][2][0].set_color(CC)
        LIT_P[2][2][2].set_color(VC)
        LIT_P.move_to([-4.2, -1.45, 0])
        self.p(Write(LIT_P), rt=1.0)
        self.encadre(LIT_P, "Formula", rt=0.8)
        self.at(T["p_an"])
        nP, dP = dol("0.50", SC, 46), dol("1.50", WHITE, 46)
        AN_P = row(mx("p'", WHITE, 46), mx("=", WHITE, 46), frac(nP, dP)).move_to([0.2, -1.45, 0])
        self.p(Write(AN_P), rt=1.0)
        self.tag_an(AN_P)
        self.at(T["p_bar"])
        self.barrer(nP[0], dP[0], rt=0.6)
        self.at(T["p_res"])
        RP = row(mx(r"\approx", WHITE, 46), mx(r"0.33 = 33\,\%", RES, 46)).next_to(AN_P, RIGHT, buff=0.2)
        self.p(Write(RP), rt=0.8)
        self.at(T["p_note"])
        NOTE = VGroup(
            tx("Audio: “50 cents to $2 = 25 %” is the profit's share of the selling price.", 20, WHITE, w=11.8),
            tx("Marx divides s by the capital advanced, c + v = $1.50:  p' ≈ 33 %  (and s' = 100 %).", 20, ABSO,
               w=11.8),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        NOTE_B = SurroundingRectangle(NOTE, color=ABSO, buff=0.15, corner_radius=0.1, stroke_width=2)
        VGroup(NOTE, NOTE_B).move_to(DOWN * 3.0)
        self.p(Create(NOTE_B), FadeIn(NOTE), rt=1.0)

        # ---------- 5 · Pourquoi le taux baisse ----------
        self.at(T["pourquoi"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("5 · Why the rate falls")
        QP = tx("Why would the rate of profit fall?", 32, WHITE).move_to(UP * 2.6)
        self.apparait(QP, rt=0.6)
        self.at(T["patron"])
        XL0 = -5.6
        B5 = burger(0.6)
        L1 = row(B5, tx("Profit:", 26, SOFT), mx(r"\$0.50", SC, 42), tx("per burger", 26, SOFT), buff=0.22)
        L1.move_to([0, 1.45, 0]).align_to([XL0, 0, 0], LEFT)
        self.apparait(L1)
        self.at(T["yacht"])
        L2 = tx("Spend it on a yacht?", 28, WHITE).move_to([0, 0.55, 0]).align_to([XL0, 0, 0], LEFT)
        self.apparait(L2, rt=0.6)
        self.at(T["yacht_x"])
        self.p(Create(Cross(L2, stroke_color=BAD, stroke_width=5)), rt=0.6)
        self.at(T["reinvest"])
        L3 = tx("Reinvest it in the business", 28, RES, bold=True).move_to([0, -0.35, 0]).align_to([XL0, 0, 0], LEFT)
        self.apparait(L3)
        self.at(T["moins_ouvriers"])
        L4 = row(tx("More burgers with fewer workers", 28, WHITE), mx(r"\rightarrow", WHITE, 40),
                 mx(r"v \downarrow", VC, 44), buff=0.3)
        L4.move_to([0, -1.25, 0]).align_to([XL0, 0, 0], LEFT)
        self.p(FadeIn(L4[0]), rt=0.8)
        self.at(T["moins_salaires"])
        self.p(FadeIn(L4[1]), FadeIn(L4[2]), rt=0.8)
        self.at(T["plus_machines"])
        L5 = row(tx("More machines, buildings, upkeep", 28, WHITE), mx(r"\rightarrow", WHITE, 40),
                 mx(r"c \uparrow", CC, 44), buff=0.3)
        L5.move_to([0, -2.15, 0]).align_to([XL0, 0, 0], LEFT)
        self.apparait(L5)

        # Évolution de la composition du capital (en milliers de dollars), s' = 100 %
        self.at(T["proportion"] - 0.6)
        self.vider(rt=0.6)
        TC = tx("Capital advanced per year (in $1,000) as the industry grows", 26, WHITE).move_to(UP * 2.7)
        BASE, U = -2.3, 0.0075
        PA = pile(-4.6, BASE, 100, 50, 50, U)
        PB = pile(-0.9, BASE, 200, 50, 50, U)
        PCc = pile(2.8, BASE, 450, 50, 50, U)
        NOMS = VGroup(*[tx(n, 22, SOFT).move_to([x, BASE - 0.35, 0])
                        for n, x in [("early", -4.6), ("later", -0.9), ("mature industry", 2.8)]])
        self.at(T["proportion"])
        self.p(FadeIn(TC), FadeIn(PA), FadeIn(NOMS[0]), rt=1.0)
        self.at(T["etape2"])
        self.p(FadeIn(PB, shift=UP * 0.2), FadeIn(NOMS[1]), rt=1.0)
        self.at(T["etape3"])
        self.p(FadeIn(PCc, shift=UP * 0.2), FadeIn(NOMS[2]), rt=1.2)
        self.at(T["moins_travail"])
        MT = txm(r"$c$ grows, $v$ does not: more output with less labour", 22, SOFT).move_to(DOWN * 3.25)
        self.apparait(MT, rt=0.6)
        self.at(T["valeur_travail"])
        NV = VGroup(PA[0][1], PA[0][2], PB[0][1], PB[0][2], PCc[0][1], PCc[0][2])
        self.p(Indicate(NV, color=WHITE), rt=1.2)
        self.at(T["taux_calc"] - 0.4)
        self.p(FadeOut(TC), rt=0.4)
        PP = VGroup()
        for pl, txt in [(PA, r"p' = \tfrac{50}{150} \approx 33\,\%"), (PB, r"p' = \tfrac{50}{250} = 20\,\%"),
                        (PCc, r"p' = \tfrac{50}{500} = 10\,\%")]:
            m = mx(txt, PC, 32).next_to(pl[0], UP, buff=0.25)
            PP.add(m)
        self.p(LaggedStart(*[FadeIn(m, shift=DOWN * 0.1) for m in PP], lag_ratio=0.4), rt=1.5)
        self.at(T["ecart_txt"])
        ET = txm(r"Same $s' = 100\,\%$, but $c$ grows faster than $v + s$", 24, WHITE, w=7.0).move_to([-2.4, 2.75, 0])
        self.apparait(ET)

        # Graphe p' en fonction de c/v
        self.at(T["ecart"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["graphe_cv"])
        AXG = axes([0, 10, 1], [0, 1.1, 0.25], 6.6, 4.4, [-2.6, -0.25, 0])
        YG = mx(r"p'", PC, 40).next_to(AXG, UP, buff=0.05).align_to(AXG, LEFT).shift(LEFT * 0.1)
        XG = txm(r"organic composition $c/v$", 22, SOFT).next_to(AXG, DOWN, buff=0.15)
        G100 = mx(r"100\,\%", SOFT, 24).next_to(AXG.c2p(0, 1), LEFT, buff=0.12)
        G50 = mx(r"50\,\%", SOFT, 24).next_to(AXG.c2p(0, 0.5), LEFT, buff=0.12)
        CG = AXG.plot(lambda x: 1 / (1 + x), x_range=[0, 10], color=PC, stroke_width=4)
        self.p(Create(AXG), FadeIn(YG), FadeIn(XG), FadeIn(G100), FadeIn(G50), rt=1.0)
        self.p(Create(CG), rt=2.5)
        self.at(T["points"])
        PTS = VGroup()
        for x, nom in [(2, "early"), (4, "later"), (9, "mature")]:
            d = Dot(AXG.c2p(x, 1 / (1 + x)), radius=0.09, color=WHITE)
            lab = tx(nom, 18, WHITE).next_to(d, UR, buff=0.08)
            PTS.add(VGroup(d, lab))
        self.p(LaggedStart(*[FadeIn(pt, scale=0.5) for pt in PTS], lag_ratio=0.5), rt=1.6)
        self.at(T["derivation"])
        D1 = row(mx("p'", WHITE, 44), mx("=", WHITE, 44), frac(mx("s", SC, 44), mx("c+v", WHITE, 44)),
                 mx("=", WHITE, 44), frac(mx("s/v", WHITE, 44), mx("c/v + 1", WHITE, 44)))
        D1.move_to([4.2, 1.75, 0])
        ajuster(D1, 5.2)
        self.p(Write(D1), rt=1.5)
        self.at(T["tendance"])
        D2 = row(mx("p'", WHITE, 52), mx("=", WHITE, 52), frac(mx("s'", SC, 52), mx("1 + c/v", WHITE, 52)))
        D2.move_to([4.2, -0.8, 0])
        self.p(Write(D2), rt=1.0)
        self.encadre(D2, "Key relation", rt=0.8)
        D3 = txm(r"$s'$ fixed, $c/v \uparrow$  →  $p' \downarrow$", 24, PC, w=5.0).move_to([4.2, -2.4, 0])
        self.apparait(D3, rt=0.6)

        # ---------- 6 · Contradiction et crise ----------
        self.at(T["contradiction"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("6 · Contradiction and crisis")
        TCR = tx("An internal contradiction of capitalist production", 30, WHITE).move_to(UP * 2.65)
        self.apparait(TCR, rt=0.6)
        self.at(T["surprod"])
        AXT = axes([0, 10, 1], [0, 1, 0.25], 7.0, 3.6, [-2.2, -0.8, 0])
        XT = tx("time", 20, SOFT).next_to(AXT, DOWN, buff=0.12)
        CPROD = AXT.plot(lambda x: 0.2 + 0.075 * x, x_range=[0, 10], color=SC, stroke_width=4)
        CACH = AXT.plot(lambda x: 0.3 + 0.03 * x - 0.004 * x ** 2, x_range=[0, 10], color=VC, stroke_width=4)
        LEG1 = row(Line(ORIGIN, RIGHT * 0.5, color=SC, stroke_width=5), tx("goods produced", 20, WHITE), buff=0.15)
        LEG2 = row(Line(ORIGIN, RIGHT * 0.5, color=VC, stroke_width=5), tx("workers' purchasing power", 20, WHITE),
                   buff=0.15)
        LEG = row(LEG1, LEG2, buff=0.6).move_to([-2.2, 1.65, 0])
        self.p(Create(AXT), FadeIn(XT), FadeIn(LEG1), rt=1.0)
        self.p(Create(CPROD), rt=2.0)
        self.at(T["acheteurs"])
        self.p(FadeIn(LEG2), Create(CACH), rt=2.0)
        self.at(T["crise"])
        AIRE = AXT.get_area(CPROD, x_range=[2, 10], bounded_graph=CACH, color=BAD, opacity=0.35)
        R1 = lignes("Overproduction:", "unsold goods", fs=26, c=BAD, w=3.6).move_to([4.9, 0.6, 0])
        self.p(FadeIn(AIRE), FadeIn(R1), rt=1.0)
        self.at(T["crise2"])
        R2 = tx("→ crisis", 34, BAD, bold=True).next_to(R1, DOWN, buff=0.4).align_to(R1, LEFT)
        self.apparait(R2, rt=0.6)
        self.at(T["prix_bas"])
        R3 = lignes("prices forced", "below value", fs=24, c=WHITE, w=3.6).next_to(R2, DOWN, buff=0.4)
        R3.align_to(R1, LEFT)
        self.apparait(R3, rt=0.6)

        # ---------- 7 · s' monte, p' baisse ----------
        self.at(T["s_monte"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("7 · s′ up, p′ down")
        TS = txm(r"The rate of surplus value $s'$ can rise while $p'$ falls", 28, WHITE).move_to(UP * 2.6)
        self.apparait(TS, rt=0.6)
        XS, XA, XB = -3.6, 0.6, 3.9
        YS = {"t": 1.65, "c": 0.95, "v": 0.35, "s": -0.25, "sp": -1.05, "pp": -1.85}
        ETQ = VGroup(
            mx("c", CC, 40).move_to([XS, YS["c"], 0]), mx("v", VC, 40).move_to([XS, YS["v"], 0]),
            mx("s", SC, 40).move_to([XS, YS["s"], 0]),
            mx(r"s' = s/v", SC, 36).move_to([XS, YS["sp"], 0]),
            mx(r"p' = s/(c+v)", PC, 36).move_to([XS, YS["pp"], 0]))
        SEP = Line([XS - 1.6, (YS["s"] + YS["sp"]) / 2, 0], [XB + 1.4, (YS["s"] + YS["sp"]) / 2, 0], color=SOFT,
                   stroke_width=1.5)
        HA = tx("before", 24, SOFT).move_to([XA, YS["t"], 0])
        HB = tx("after", 24, SOFT).move_to([XB, YS["t"], 0])
        AV = VGroup(*[mx(t, WHITE, 36).move_to([XA, YS[k], 0]) for k, t in
                      [("c", "100"), ("v", "50"), ("s", "50"), ("sp", r"100\,\%"), ("pp", r"33\,\%")]])
        AP = VGroup(*[mx(t, WHITE, 36).move_to([XB, YS[k], 0]) for k, t in [("c", "460"), ("v", "40"), ("s", "100")]])
        UNITE = tx("($1,000 per year)", 18, SOFT).next_to(HA, LEFT, buff=0.9)
        self.at(T["avant"])
        self.p(FadeIn(ETQ), FadeIn(SEP), FadeIn(HA), FadeIn(UNITE), FadeIn(AV), rt=1.2)
        self.at(T["apres"])
        CAPT_A = tx("fewer workers", 18, VC).next_to(AP[1], RIGHT, buff=0.3)
        self.p(FadeIn(HB), FadeIn(AP[0]), FadeIn(AP[1]), FadeIn(CAPT_A), rt=1.0)
        self.at(T["apres_s"])
        CAPT_S = tx("worked harder", 18, SC).next_to(AP[2], RIGHT, buff=0.3)
        self.p(FadeIn(AP[2]), FadeIn(CAPT_S), rt=0.8)
        self.at(T["masse_val"])
        MV = txm(r"New value $v + s$ is small compared with $c$", 22, SOFT).move_to(DOWN * 2.65)
        self.apparait(MV, rt=0.6)
        self.at(T["s_haut"])
        SH = row(mx(r"\tfrac{100}{40} = 250\,\%", RES, 36), mx(r"\uparrow", RES, 44)).move_to([XB, YS["sp"], 0])
        self.p(FadeIn(SH, shift=UP * 0.15), rt=0.8)
        self.at(T["p_bas"])
        PB_ = row(mx(r"\tfrac{100}{500} = 20\,\%", BAD, 36), mx(r"\downarrow", BAD, 44)).move_to([XB, YS["pp"], 0])
        self.p(FadeIn(PB_, shift=DOWN * 0.15), rt=0.8)
        self.at(T["important"])
        CCL = tx("Exploitation rises while the rate of profit falls", 24, WHITE, bold=True)
        CCL_B = SurroundingRectangle(CCL, color=PC, buff=0.15, corner_radius=0.1, stroke_width=2.5)
        VGroup(CCL, CCL_B).move_to(DOWN * 3.3)
        self.p(FadeIn(CCL), Create(CCL_B), rt=0.8)

        # ---------- 8 · Causes qui contrecarrent la loi ----------
        self.at(T["intenable"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("8 · Counteracting factors")
        QI = tx("If p′ keeps falling, is the system sustainable?", 30, WHITE).move_to(UP * 2.6)
        self.apparait(QI, rt=0.6)
        self.at(T["attenuer"])
        TF = tx("Counteracting factors (Capital III, ch. 14)", 28, WHITE).move_to([-1.6, 2.6, 0])
        FP = mx(r"p' = \frac{s}{c+v}", PC, 44).move_to([5.2, 2.55, 0])
        self.p(FadeOut(QI), FadeIn(TF), FadeIn(FP), rt=0.8)
        XC, YC = [-4.5, 0.0, 4.5], [0.7, -1.6]
        FACT = [
            (["Intensify", "exploitation"], r"s' \uparrow", "Marx: raising the intensity of exploitation"),
            (["Rely on credit"], tx("borrow to keep paying for labour", 18, PC),
             "not in Marx's list as such (closest: share capital)"),
            (["Keep cheap labour", "instead of machines"], r"c/v \text{ stays low}",
             "Marx: relative overpopulation"),
            (["Cheaper machines"], r"c \downarrow", "Marx: cheapening of constant capital"),
            (["Lower wages"], r"v \downarrow,\ s \uparrow", "Marx: wages pushed below their value"),
            (["Foreign trade"], tx("cheaper inputs, higher sale prices", 18, PC), "Marx: foreign trade"),
        ]
        CARTES = VGroup()
        for i, (tit, eff, note) in enumerate(FACT):
            k = carte_facteur(i + 1, tit, eff, note).move_to([XC[i % 3], YC[i // 3], 0])
            CARTES.add(k)
        for i, cle in enumerate(["f1", "f2", "f3", "f4", "f5", "f6"]):
            self.at(T[cle])
            self.p(FadeIn(CARTES[i], shift=UP * 0.2), rt=0.8)
        self.at(T["strategies"])
        RAL = tx("They slow the fall; they do not cancel it", 24, RES).move_to(DOWN * 3.2)
        self.apparait(RAL, rt=0.6)

        self.at(T["limites"] - 0.6)
        self.vider(rt=0.6)
        self.at(T["limites"])
        AXF = axes([0, 10, 1], [0, 1, 0.25], 8.0, 4.0, [-1.9, -0.3, 0])
        YF = tx("rate of profit", 22, PC).next_to(AXF, UP, buff=0.1).align_to(AXF, LEFT)
        XF = tx("time", 20, SOFT).next_to(AXF, DOWN, buff=0.12)
        TEND = DashedLine(AXF.c2p(0, 0.88), AXF.c2p(10, 0.22), color=SOFT, stroke_width=3)
        CF = AXF.plot(lambda x: 0.85 - 0.066 * x + 0.07 * math.sin(1.7 * x), x_range=[0, 10], color=PC,
                      stroke_width=4)
        LT_ = tx("tendency", 20, SOFT).next_to(TEND.get_end(), UP, buff=0.15)
        self.p(Create(AXF), FadeIn(YF), FadeIn(XF), rt=1.0)
        self.p(Create(TEND), FadeIn(LT_), rt=1.0)
        self.p(Create(CF), rt=3.0)
        LIM = tx("Limits:", 26, WHITE, bold=True).move_to([4.9, 1.2, 0])
        self.p(FadeIn(LIM), rt=0.5)
        self.at(T["lim_travail"])
        LIM1 = lignes("labour can only", "work so hard", fs=22, c=WHITE, w=3.6).next_to(LIM, DOWN, buff=0.3)
        LIM1.align_to(LIM, LEFT)
        self.apparait(LIM1, rt=0.6)
        self.at(T["lim_ress"])
        LIM2 = lignes("resources are", "limited", fs=22, c=WHITE, w=3.6).next_to(LIM1, DOWN, buff=0.3)
        LIM2.align_to(LIM, LEFT)
        self.apparait(LIM2, rt=0.6)
        self.at(T["canette"])
        LIM3 = lignes("→ the problem is", "only postponed", fs=24, c=BAD, w=3.6).next_to(LIM2, DOWN, buff=0.4)
        LIM3.align_to(LIM, LEFT)
        self.apparait(LIM3, rt=0.6)

        # ---------- 9 · Question ouverte : l'économie des plateformes ----------
        self.at(T["question"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("9 · An open question")
        self.at(T["gig"])
        TG = txm(r"The gig economy: what happens to $c/v$?", 30, WHITE).move_to(UP * 2.6)
        self.apparait(TG)
        self.at(T["uber"])
        BASE2, W2 = -2.3, 1.6
        FC = segment(-5.6, -5.6 + W2, BASE2 + 1.6, 3.2, CC, "c", 40)
        FV = segment(-5.6, -5.6 + W2, BASE2 + 3.4, 0.4, VC, "v", 28)
        UC = segment(-2.4, -2.4 + W2, BASE2 + 0.08, 0.16, CC)
        UCT = tx("c ≈ 0: no cars owned", 18, CC).next_to(UC, RIGHT, buff=0.15)
        UV = segment(-2.4, -2.4 + W2, BASE2 + 0.16 + 1.4, 2.8, VC, "v", 40)
        NF = lignes("classic", "factory", fs=20, c=SOFT).next_to(VGroup(FC, FV), DOWN, buff=0.2)
        NU = lignes("platform", "(as described)", fs=20, c=SOFT).next_to(UC, DOWN, buff=0.2)
        self.p(FadeIn(FC), FadeIn(FV), FadeIn(NF), rt=1.0)
        self.p(FadeIn(UC), FadeIn(UCT), FadeIn(NU), rt=0.8)
        self.at(T["salaires_uber"])
        UVT = tx("payments to drivers", 18, VC).next_to(UV, RIGHT, buff=0.15)
        self.p(FadeIn(UV, shift=UP * 0.2), FadeIn(UVT), rt=1.0)
        self.at(T["sens"])
        K2 = row(mx("p'", WHITE, 46), mx("=", WHITE, 46), frac(mx("s'", SC, 46), mx("1 + c/v", WHITE, 46)))
        K2.move_to([4.6, 1.1, 0])
        self.p(Write(K2), rt=1.0)
        self.at(T["hypothese"])
        H1 = txm(r"The law assumes $c/v \uparrow$", 22, WHITE, w=4.2).move_to([4.6, 0.0, 0])
        self.apparait(H1, rt=0.6)
        self.at(T["issue"])
        H2 = txm(r"Here $c/v$ is low: a way out?", 22, ABSO, w=4.2).move_to([4.6, -0.75, 0])
        self.apparait(H2, rt=0.6)
        self.at(T["pas_profit"])
        H3 = tx("“Uber doesn't really turn a profit”", 20, WHITE, w=4.2).move_to([4.6, -1.5, 0])
        H3N = tx("Update: Uber has reported an annual profit since 2023.", 18, ABSO).move_to(DOWN * 3.3)
        self.p(FadeIn(H3), FadeIn(H3N), rt=0.8)
        self.at(T["airbnb"])
        H4 = tx("Same question for Uber, Airbnb…", 20, SOFT, w=4.2).move_to([4.6, -2.2, 0])
        self.apparait(H4, rt=0.6)

        # ---------- Bilan ----------
        self.at(T["fin"] - 0.6)
        self.vider(rt=0.6)
        self.set_q("Recap")
        TR_ = tx("To remember", 36, WHITE, bold=True).move_to(UP * 2.4)
        BIL = VGroup(
            txm(r"Rate of surplus value $s' = s/v$;  rate of profit $p' = s/(c+v)$", 26, WHITE),
            txm(r"Mechanisation raises $c/v$, so $p' = s'/(1 + c/v)$ tends to fall", 26, WHITE),
            tx("Counteracting factors slow the fall but cannot stop it", 26, WHITE),
            tx("For Marx, this contradiction leads to overproduction and crises", 26, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(DOWN * 0.4)
        ajuster(BIL, 12.6)
        PUCES = VGroup(*[Dot(radius=0.07, color=ABSO).next_to(l, LEFT, buff=0.25) for l in BIL])
        self.p(FadeIn(TR_), rt=0.6)
        self.p(LaggedStart(*[FadeIn(VGroup(d, l), shift=RIGHT * 0.2) for d, l in zip(PUCES, BIL)], lag_ratio=0.6),
               rt=3.5)
        # Fin : l'audio se termine à 17:50,9 ; marge de 10 s sur la dernière image, à couper au montage
        self.at(T["fin_audio"])
        self.pause(10.0)
