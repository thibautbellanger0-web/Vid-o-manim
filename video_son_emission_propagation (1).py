from manim import *
import math

# =====================================================================
#  Vidéo de cours (Seconde, « Ondes et signaux ») – LE SON : ÉMISSION ET PROPAGATION, ≈ 5 min.
#  Vidéo autonome sous-titrée, en 3D. Manim Community, rendu sur GitHub.
#  Programme : émission par un objet qui vibre, intérêt d'une caisse de résonance,
#  rôle du milieu matériel, vitesse du son dans l'air comparée à d'autres vitesses.
#  Technique : la caméra de Manim reste fixe ; le « monde » 3D est projeté par la vue
#  (phi, theta) animable (comme frame.reorient chez 3B1B) : les textes restent plats.
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
SONC = "#F4D03F"     # ondes sonores
COMP = "#FF7B54"     # air comprimé
RARE = "#4FC3F7"     # air dilaté
NEUTRE = "#D7E3F0"   # air au repos
METAL = "#C9D3DD"
BOIS = "#B5733F"
BOIS_F = "#7A4A24"
HPC = "#2A2F3A"      # caisse du haut-parleur
PALETTE = [interpolate_color(ManimColor(RARE), ManimColor(NEUTRE), k / 10) for k in range(10)] + \
          [interpolate_color(ManimColor(NEUTRE), ManimColor(COMP), k / 10) for k in range(11)]


class Source:
    """Source sonore : amplitude a(t) (animable), historique (pour la propagation à vitesse finie),
    instants d'émission des fronts d'onde dessinés."""

    def __init__(self, intervalle=0.4, tau=None, A=0.11, omega=3.8):
        self.a = ValueTracker(0.0)
        self.tau = tau
        self.intervalle = intervalle
        self.A = A
        self.omega = omega
        self.emis = []
        self.prochaine = 0.0
        self.ht = [-1000.0, 0.0]
        self.ha = [0.0, 0.0]

    def tick(self, t, dt):
        if self.tau is not None:
            self.a.set_value(self.a.get_value() * math.exp(-dt / self.tau))
        a = self.a.get_value()
        if t > self.ht[-1]:
            self.ht.append(t)
            self.ha.append(a)
        if len(self.ht) > 6000:
            del self.ht[1:2000]
            del self.ha[1:2000]
        if t >= self.prochaine:
            if a > 0.03:
                self.emis.append((t, a))
            self.prochaine = t + self.intervalle
        self.emis = [e for e in self.emis if t - e[0] < 10]

    def amp(self, tau):
        return np.interp(tau, self.ht, self.ha, left=0.0)

    def membrane(self, t):
        return self.A * self.a.get_value() * math.sin(self.omega * t)


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
        q = (txm(s, 25, WHITE, w=12.8) if "$" in s else tx(s, 25, WHITE, w=12.8)).to_edge(UP, buff=0.78).to_edge(LEFT, buff=0.45)
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
        # « caméra » : on garde la caméra de Manim fixe et on projette nous-mêmes le monde 3D
        self.O = np.zeros(3)
        self.phi = ValueTracker(72 * DEGREES)
        self.theta = ValueTracker(-70 * DEGREES)
        self.zv = ValueTracker(1.0)
        self.horloge = 0.0
        self.rotation_auto = 0.0
        self.balancement = None
        self.taches = []
        self.chrono = Dot(radius=0.001, fill_opacity=0, stroke_width=0)
        self.chrono.add_updater(lambda m, dt: self._tick(dt))
        self.add(self.chrono)
        self.titre()
        self.emission()
        self.propagation()
        self.cloche_a_vide()
        self.milieux()
        self.comparaison()
        self.orage()
        self.calcul_orage()
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

        def f(p):
            return O + z * (np.asarray(p, dtype=float) @ R.T)
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

    # ---------- objets ----------
    def haut_parleur(self, T, c, xi):
        c = np.array(c, dtype=float)
        dx, h = 0.9, 1.7
        xf = c[0] + dx / 2
        caisse = self.boite(T, c, (dx, h, h), HPC, sans=("+x",), sw=0.8, sc="#3D4452")
        rt = 0.58
        s = lambda v: (h / 2) / max(abs(math.cos(v)), abs(math.sin(v)))
        facade = Surface(lambda u, v: T(np.array([xf, (rt + u * (s(v) - rt)) * math.cos(v), (rt + u * (s(v) - rt)) * math.sin(v)])),
                         u_range=[0, 1], v_range=[0, TAU], resolution=(2, 32), checkerboard_colors=False,
                         fill_color="#3A4150", fill_opacity=1, stroke_color="#3A4150", stroke_width=0.3)
        cone = Surface(lambda u, v: T(np.array([xf - 0.32 * (1 - u) + xi * (1 - 0.25 * u), (0.16 + u * (rt - 0.16)) * math.cos(v),
                                                (0.16 + u * (rt - 0.16)) * math.sin(v)])),
                       u_range=[0, 1], v_range=[0, TAU], resolution=(4, 28), checkerboard_colors=False,
                       fill_color="#A7B0BD", fill_opacity=1, stroke_color="#8C95A3", stroke_width=0.4)
        cache = Surface(lambda u, v: T(np.array([xf - 0.32 + xi + 0.07 * (1 - u * u), 0.16 * u * math.cos(v), 0.16 * u * math.sin(v)])),
                        u_range=[0, 1], v_range=[0, TAU], resolution=(3, 20), checkerboard_colors=False,
                        fill_color="#5A6270", fill_opacity=1, stroke_color="#5A6270", stroke_width=0.3)
        return VGroup(caisse, facade, cone, cache)

    # =================================================================
    #  TITRE
    # =================================================================
    def titre(self):
        self.nouvelle_scene()
        self.vue([0.6, -1.05, 0], 72, -62, 0.95)
        src = Source(intervalle=0.42)
        self.taches.append(src.tick)
        C = np.array([-2.6, 0, 0])
        xf = C[0] + 0.45
        X, Y, Z = RIGHT, UP, OUT
        d1, d2 = normalize(Y + Z), normalize(Y - Z)
        plans = [(X, Y, -1.25, 1.25), (X, Z, -0.55, 0.55), (X, d1, -0.8, 0.8), (X, d2, -0.8, 0.8)]
        hp = always_redraw(lambda: self.haut_parleur(self.T(), C, src.membrane(self.horloge)))
        fr = always_redraw(lambda: self.fronts(self.T(), src, np.array([xf, 0, 0]), plans, v=1.1, rmin=0.35, rmax=5.2, sw=2.5))
        t1 = tx("Le son", 64, WHITE, bold=True)
        t2 = tx("émission et propagation", 32, SONC)
        t3 = tx("Physique-chimie · Seconde · Ondes et signaux", 20, SOFT)
        bloc = VGroup(t1, t2, t3).arrange(DOWN, buff=0.22).move_to([0, 2.35, 0])
        for t in bloc:
            t.set_stroke(BLACK, width=6, background=True)
        self.add(hp, fr)
        src.a.set_value(1.0)
        self.rotation_auto = 0.05
        self.p(FadeIn(hp), rt=1.0)
        self.p(Write(t1), rt=1.2)
        self.p(FadeIn(t2, shift=UP * 0.2), FadeIn(t3), rt=1.0)
        self.pause(5.0)
        self.hdr_ex = tx("Le son : émission et propagation", 20, SOFT).to_corner(UL, buff=0.3)
        self.p(ReplacementTransform(t1, self.hdr_ex), FadeOut(VGroup(t2, t3)), FadeOut(hp), FadeOut(fr), rt=1.0)
        self.nouvelle_scene()

    # =================================================================
    #  1. L'ÉMISSION : le diapason et la caisse de résonance
    # =================================================================
    def prong(self, T, xc, sgn, depl):
        """Branche du diapason : 3 tronçons de plus en plus déplacés (flexion)."""
        g = VGroup()
        z0, z1 = -0.70, 1.10
        hx, hy = 0.065, 0.075
        for k in range(3):
            za, zb = z0 + (z1 - z0) * k / 3, z0 + (z1 - z0) * (k + 1) / 3
            da = sgn * depl * ((za - z0) / (z1 - z0)) ** 1.6
            db = sgn * depl * ((zb - z0) / (z1 - z0)) ** 1.6
            P = lambda x, y, z, d: np.array([xc + x + d, y, z])
            corners_a = [P(-hx, -hy, za, da), P(hx, -hy, za, da), P(hx, hy, za, da), P(-hx, hy, za, da)]
            corners_b = [P(-hx, -hy, zb, db), P(hx, -hy, zb, db), P(hx, hy, zb, db), P(-hx, hy, zb, db)]
            for i in range(4):
                j = (i + 1) % 4
                g.add(self.poly3(T, [corners_a[i], corners_a[j], corners_b[j], corners_b[i]], METAL, 1, 0.4, "#9AA5B1"))
            if k == 2:
                g.add(self.poly3(T, corners_b, METAL, 1, 0.4, "#9AA5B1"))
        return g

    def diapason(self, T, depl):
        g = VGroup()
        g.add(self.cylindre3(T, [0, 0, -1.35], [0, 0, -0.85], 0.055, METAL, res=(14, 1)))
        g.add(self.boite(T, [0, 0, -0.775], (0.53, 0.15, 0.15), METAL, sw=0.4, sc="#9AA5B1"))
        g.add(self.prong(T, -0.2, -1, depl))
        g.add(self.prong(T, 0.2, 1, depl))
        return g

    def maillet(self, T, s):
        repos, contact = np.array([1.5, -0.6, 0.75]), np.array([0.43, 0.0, 0.75])
        c = repos + s * (contact - repos)
        return VGroup(self.cylindre3(T, c + np.array([0.12, -0.03, 0.05]), c + np.array([0.95, -0.25, 0.35]), 0.035, BOIS, res=(10, 1)),
                      self.sphere3(T, c, 0.16, "#C0392B", res=(14, 7)))

    def emission(self):
        self.set_q("1. L'émission")
        self.nouvelle_scene()
        self.vue([-1.1, 0.35, 0], 76, -68, 0.95)
        src = Source(intervalle=0.22, tau=2.6)
        self.taches.append(src.tick)
        s_m = ValueTracker(0.0)
        gain = {"seul": 0.38, "caisse": 0.0}
        w_f = 2 * PI * 3.0
        depl = lambda: 0.11 * src.a.get_value() * math.sin(w_f * self.horloge)
        dia = always_redraw(lambda: self.diapason(self.T(), depl()))
        mal = always_redraw(lambda: self.maillet(self.T(), s_m.get_value()))
        X, Y = RIGHT, UP
        fr1 = always_redraw(lambda: self.fronts(self.T(), src, np.array([0, 0, 0.45]), [(X, Y, 0, 0)], v=1.3, rmin=0.55,
                                                rmax=3.1, gain=gain["seul"], sw=2.6, complet=True))
        fr2 = always_redraw(lambda: self.fronts(self.T(), src, np.array([0, 0, -1.7]), [(X, Y, 0, 0)], v=1.3, rmin=1.4,
                                                rmax=3.4, gain=gain["caisse"], sw=3.2, complet=True))
        jg = self.jauge(lambda: (gain["seul"] + gain["caisse"]) * src.a.get_value(), [5.7, 0.1, 0])
        l_dia = self.epingle(tx("diapason", 22, METAL), [0, 0, 1.1], UP * 0.35)
        self.add(fr1, fr2)
        self.p(FadeIn(dia), FadeIn(l_dia), rt=1.0)
        self.balancement = (-68 * DEGREES, 14 * DEGREES, 0.22, self.horloge)
        self.dire("Un diapason : deux branches métalliques, reliées à une tige.", lire=1.6)
        self.p(FadeIn(mal), FadeIn(jg), rt=0.6)
        # premier coup
        self.dire("On le frappe : ses branches se mettent à VIBRER (mouvement très exagéré ici).", lire=0.2)
        self.p(s_m.animate.set_value(1.0), rt=0.35, rate_func=rush_into)
        src.a.set_value(1.0)
        self.p(s_m.animate.set_value(0.0), rt=0.6)
        self.pause(1.8)
        self.dire("En s'écartant et en se rapprochant, les branches poussent et tirent l'air autour d'elles.", lire=2.4)
        self.dire("Ce mouvement de l'air arrive jusqu'à nos oreilles : on entend un son.", c=SONC, lire=1.6)
        src.tau = 0.12
        self.dire("Si on pince les branches pour les immobiliser, le son s'arrête aussitôt !", c=COMP, lire=2.0)
        idee = VGroup(tx("Un son est toujours émis", 24, WHITE, bold=True), tx("par un objet qui vibre.", 24, WHITE, bold=True))
        idee.arrange(DOWN, buff=0.1)
        cadre_i = SurroundingRectangle(idee, color=SONC, buff=0.2, corner_radius=0.12, stroke_width=2.5).set_fill("#1B1F27", 0.9)
        carte_i = VGroup(cadre_i, idee).move_to([4.15, 2.45, 0])
        self.p(FadeIn(carte_i, shift=DOWN * 0.15), rt=0.8)
        self.dire("Cordes vocales, corde de guitare, membrane d'un haut-parleur : toujours une vibration.", lire=2.2)
        # caisse de résonance
        src.tau = 1.2
        caisse = always_redraw(lambda: self.boite(self.T(), [0, 0, -1.7], (2.4, 1.1, 0.7), BOIS, sw=0.8, sc=BOIS_F,
                                                  couleurs={"+x": "#2B1A0E"}))
        l_cai = self.epingle(tx("caisse de résonance", 22, BOIS), [0, -0.55, -2.05], DOWN * 0.32)
        self.p(FadeIn(caisse, shift=UP * 0.3), FadeIn(l_cai), rt=1.0)
        gain["seul"], gain["caisse"] = 0.55, 1.0
        self.dire("Posons le diapason sur une caisse de résonance : une boîte en bois ouverte d'un côté.", lire=1.6)
        self.p(s_m.animate.set_value(1.0), rt=0.35, rate_func=rush_into)
        src.a.set_value(1.0)
        self.p(s_m.animate.set_value(0.0), rt=0.6)
        self.dire("Le même coup donne un son beaucoup plus fort !", c=SONC, lire=1.6)
        self.dire("La caisse vibre avec le diapason : sa grande surface met en mouvement bien plus d'air.", lire=2.2)
        self.p(s_m.animate.set_value(1.0), rt=0.35, rate_func=rush_into)
        src.a.set_value(1.0)
        self.p(s_m.animate.set_value(0.0), rt=0.6)
        self.dire("Contrepartie : le son dure moins longtemps, l'énergie de vibration part plus vite dans l'air.", c=SOFT, lire=2.4)
        self.dire("C'est le rôle de la caisse d'une guitare ou d'un violon : sans elle, les cordes s'entendent à peine.", lire=2.4)
        self.effacer_sous_titre()
        self.rotation_auto = 0.0
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  2. LA PROPAGATION : vue microscopique de l'air
    # =================================================================
    def propagation(self):
        self.set_q("2. La propagation")
        self.nouvelle_scene()
        self.vue([0.35, -0.25, 0], 74, -88, 0.92)
        c_ = 1.2
        omega = PI * c_                  # longueur d'onde affichée : 2 unités
        src = Source(intervalle=1.0, A=0.12, omega=omega)
        self.taches.append(src.tick)
        C = np.array([-3.75, 0, 0])
        xf = C[0] + 0.45
        xs = np.arange(xf + 0.3, 4.25, 0.25)
        ys = np.array([-0.57, -0.19, 0.19, 0.57])
        P0 = np.array([[x, y, z] for x in xs for y in ys for z in ys])
        n = len(P0)
        rng = np.random.default_rng(4)
        w_j = rng.uniform(1.5, 3.5, (n, 3))
        ph_j = rng.uniform(0, TAU, (n, 3))
        dots = VGroup(*[Dot(radius=0.048, fill_color=NEUTRE, stroke_width=0).set_sheen(-0.35, DR) for _ in range(n)])
        # molécule suivie : première rangée, au milieu de la colonne
        ih = int(np.argmin(np.abs(P0[:, 0] - 0.55) + np.abs(P0[:, 1] + 0.57) + np.abs(P0[:, 2] - 0.19)))
        etat = {"suivi": 0.0, "crete": None}
        vis = ValueTracker(0.0)
        jaune = Dot(radius=0.085, fill_color=SONC, stroke_width=0).set_sheen(-0.3, DR)
        maison = Circle(radius=0.14, stroke_color=SONC, stroke_width=2.5)

        def placer(g, dt=0):
            T = self.T()
            t = self.horloge
            tau = t - (P0[:, 0] - xf) / c_
            a = src.amp(tau)
            xi = src.A * a * np.sin(omega * tau)
            s = a * np.cos(omega * tau)
            J = 0.024 * np.sin(w_j * t + ph_j)
            W = P0 + J
            W[:, 0] += xi
            S = T(W)
            idx = np.clip(np.round((s + 1) * 10).astype(int), 0, 20)
            for i, d in enumerate(g):
                d.move_to(S[i])
                d.set_fill(PALETTE[idx[i]], opacity=0.0 if (i == ih and etat["suivi"] > 0.5) else vis.get_value())
            pj = P0[ih].copy()
            pj[0] += xi[ih]
            jaune.move_to(T(pj))
            maison.move_to(T(P0[ih]))
        dots.add_updater(placer)
        placer(dots)
        hp = always_redraw(lambda: self.haut_parleur(self.T(), C, src.membrane(self.horloge)))

        def plan_crete():
            if etat["crete"] is None:
                return self.vide()
            x = xf + c_ * (self.horloge - etat["crete"])
            if not (xf + 0.1 < x < 4.2):
                return self.vide()
            T = self.T()
            return Polygon(*T(np.array([[x, -0.85, -0.85], [x, 0.85, -0.85], [x, 0.85, 0.85], [x, -0.85, 0.85]])),
                           fill_color=COMP, fill_opacity=0.16, stroke_color=COMP, stroke_width=2)
        crete = always_redraw(plan_crete)
        self.add(hp, dots)
        self.p(FadeIn(hp), vis.animate.set_value(1.0), rt=2.0)
        self.dire("Zoomons sur l'air devant un haut-parleur : des molécules, agitées en permanence.", lire=2.0)
        leg = VGroup(row(Dot(radius=0.09, fill_color=COMP).set_sheen(-0.3, DR), tx("air comprimé", 20, COMP), buff=0.15),
                     row(Dot(radius=0.09, fill_color=RARE).set_sheen(-0.3, DR), tx("air dilaté", 20, RARE), buff=0.15)
                     ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.35).shift(DOWN * 0.45)
        self.p(src.a.animate.set_value(1.0), FadeIn(leg), rt=1.0)
        self.dire("La membrane avance : elle comprime l'air devant elle. Elle recule : l'air se dilate.", lire=2.6)
        self.dire("Chaque couche d'air pousse la suivante : la perturbation se propage de proche en proche.", c=SONC, lire=0.3)
        self.bouger_vue(rt=4.0, phi=66, theta=-58)
        self.pause(1.5)
        # une molécule suivie
        etat["suivi"] = 1.0
        self.add(maison, jaune)
        self.p(GrowFromCenter(jaune), Create(maison), rt=0.6)
        self.dire("Suivons UNE molécule : elle oscille autour de sa position… mais n'avance pas !", c=SONC, lire=3.6)
        tn = 2 * PI * math.ceil(omega * self.horloge / (2 * PI) + 0.3) / omega
        etat["crete"] = tn
        self.add(crete)
        self.dire("Pendant ce temps, la zone comprimée, elle, traverse toute la colonne d'air.", c=COMP, lire=4.5)
        idee = VGroup(tx("Le son est une perturbation qui se propage", 22, WHITE, bold=True),
                      tx("dans un milieu matériel : il transporte de", 22, WHITE, bold=True),
                      tx("l'énergie, mais pas de matière.", 22, WHITE, bold=True)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        cadre_i = SurroundingRectangle(idee, color=SONC, buff=0.2, corner_radius=0.12, stroke_width=2.5).set_fill("#1B1F27", 0.92)
        carte_i = VGroup(cadre_i, idee).move_to([0.4, 2.45, 0])
        self.p(FadeIn(carte_i, shift=DOWN * 0.15), rt=0.8)
        self.bouger_vue(rt=3.0, phi=72, theta=-84)
        self.dire("La membrane s'arrête : la dernière perturbation poursuit sa route, puis l'air redevient calme.", lire=0.3)
        self.p(src.a.animate.set_value(0.0), rt=0.8)
        self.pause(4.0)
        self.effacer_sous_titre()
        dots.clear_updaters()
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  3. PAS DE SON SANS MILIEU : la cloche à vide
    # =================================================================
    def cloche_a_vide(self):
        self.set_q("3. Et dans le vide ?")
        self.nouvelle_scene()
        self.vue([-1.3, -0.55, 0], 70, -78, 1.0)
        src = Source(intervalle=0.3)
        self.taches.append(src.tick)
        air = ValueTracker(1.0)
        rng = np.random.default_rng(11)
        P0 = []
        while len(P0) < 70:
            p = rng.uniform([-1.3, -1.3, 0.08], [1.3, 1.3, 1.32])
            if np.linalg.norm(p) < 1.3 and not (math.hypot(p[0], p[1]) < 0.5 and p[2] < 1.0):
                P0.append(p)
        P0 = np.array(P0)
        seuil = rng.random(len(P0))
        w_j = rng.uniform(2, 4, P0.shape)
        ph_j = rng.uniform(0, TAU, P0.shape)
        dots = VGroup(*[Dot(radius=0.05, fill_color=NEUTRE, stroke_width=0).set_sheen(-0.35, DR) for _ in P0])
        vis = ValueTracker(0.0)

        def placer(g, dt=0):
            T = self.T()
            S = T(P0 + 0.05 * np.sin(w_j * self.horloge + ph_j))
            f = air.get_value()
            for i, d in enumerate(g):
                d.move_to(S[i])
                d.set_fill(NEUTRE, opacity=vis.get_value() if seuil[i] < f else 0.0)
        dots.add_updater(placer)
        placer(dots)

        def montage():
            T = self.T()
            sec = 0.03 * src.a.get_value() * math.sin(2 * PI * 7 * self.horloge)
            return VGroup(
                self.cylindre3(T, [0, 0, -0.16], [0, 0, 0], 1.75, "#4A5160", res=(28, 1)),
                self.cylindre3(T, [1.6, 0, -0.08], [3.2, 0, -0.08], 0.08, "#6B7280", res=(10, 1)),
                self.cylindre3(T, [0, 0, 0], [0, 0, 0.55], 0.05, METAL, res=(10, 1)),
                self.sphere3(T, [sec, 0, 0.55], 0.36, "#E5B53A", res=(18, 6), demi=True),
                self.sphere3(T, [0.42 + 4 * sec, 0, 0.62], 0.07, METAL, res=(8, 4)),
                self.sphere3(T, [0, 0, 0], 1.45, "#BFE6FF", res=(28, 8), op=0.08, demi=True, sw=0.6, sc=WHITE, so=0.25),
            )
        mont = always_redraw(montage)
        X, Y = RIGHT, UP
        fr = always_redraw(lambda: self.fronts(self.T(), src, np.array([0, 0, 0.6]), [(X, Y, 0, 0)], v=1.2, rmin=1.55,
                                               rmax=4.0, gain=air.get_value() ** 1.5, sw=3.0, complet=True))
        jg = self.jauge(lambda: src.a.get_value() * air.get_value() ** 1.5, [5.7, 0.1, 0])
        l_p = self.epingle(tx("vers la pompe à vide", 20, SOFT), [3.2, 0, -0.08], DOWN * 0.35 + RIGHT * 0.3)
        l_c = self.epingle(tx("cloche en verre", 20, "#BFE6FF"), [-1.0, -1.0, 1.0], UP * 0.25 + LEFT * 1.2)
        self.add(fr, dots)
        self.p(FadeIn(mont), FadeIn(l_c), FadeIn(l_p), vis.animate.set_value(1.0), rt=1.6)
        self.p(src.a.animate.set_value(1.0), FadeIn(jg), rt=0.6)
        self.dire("Une sonnette qui sonne, sous une cloche en verre remplie d'air : on l'entend bien.", lire=2.2)
        self.dire("On pompe l'air hors de la cloche…", lire=0.2)
        self.p(air.animate.set_value(0.03), rt=5.0, rate_func=linear)
        self.dire("… le son devient presque inaudible, alors que la sonnette vibre toujours !", c=COMP, lire=2.4)
        self.dire("On laisse rentrer l'air : le son revient.", lire=0.2)
        self.p(air.animate.set_value(1.0), rt=2.5)
        self.pause(1.0)
        idee = tx("Sans milieu matériel, pas de son.", 24, WHITE, bold=True)
        cadre_i = SurroundingRectangle(idee, color=SONC, buff=0.2, corner_radius=0.12, stroke_width=2.5).set_fill("#1B1F27", 0.92)
        carte_i = VGroup(cadre_i, idee).move_to([3.6, 2.5, 0])
        self.p(FadeIn(carte_i, shift=DOWN * 0.15), rt=0.8)
        self.dire("Dans l'espace (le vide), aucun son ne se propage… contrairement à ce que montrent les films !", lire=2.4)
        self.effacer_sous_titre()
        dots.clear_updaters()
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  4. DANS LES LIQUIDES ET LES SOLIDES
    # =================================================================
    def milieux(self):
        self.set_q("4. Dans les autres milieux")
        self.nouvelle_scene()
        self.vue([0.35, -0.35, 0], 64, -80, 0.95)
        tau = ValueTracker(0.0)
        L, x0 = 7.4, -3.7
        donnees = [("acier", METAL, 1.0, 1.35, 5900, r"\approx 5\,900\ \mathrm{m\cdot s^{-1}}"),
                   ("eau", "#2E86DE", 0.55, 0.0, 1500, r"\approx 1\,500\ \mathrm{m\cdot s^{-1}}"),
                   ("air", "#BFE6FF", 0.14, -1.35, 340, r"\approx 340\ \mathrm{m\cdot s^{-1}}")]
        k = L / 1.2 / 5900

        def barres():
            T = self.T()
            g = VGroup()
            for nom, col, op, z, v, _ in donnees:
                g.add(self.boite(T, [x0 + L / 2, 0, z], (L, 0.9, 0.55), col, op=op, sw=0.8, sc=col))
                x = min(x0 + L - 0.06, x0 + 0.06 + k * v * tau.get_value())
                if tau.get_value() > 0:
                    g.add(self.boite(T, [x, 0, z], (0.12, 0.96, 0.6), SONC, op=0.95, sw=0))
            return g
        b = always_redraw(barres)
        noms = VGroup(*[self.epingle(tx(nom, 24, col, bold=True), [x0, -0.45, z], LEFT * 0.75) for nom, col, op, z, v, _ in donnees])
        vit = [mx(s, col if nom != "air" else "#BFE6FF", 30) for nom, col, op, z, v, s in donnees]
        vit_e = VGroup(*[self.epingle(m, [x0 + L, -0.45, z], RIGHT * 1.5) for m, (nom, col, op, z, v, _) in zip(vit, donnees)])
        self.p(FadeIn(b), FadeIn(noms), rt=1.2)
        self.dire("Le son se propage aussi dans les liquides et dans les solides. Faisons la course !", lire=1.6)
        self.p(tau.animate.set_value(1.2), rt=1.2, rate_func=linear)
        self.p(FadeIn(vit_e[0], shift=LEFT * 0.2), tau.animate.set_value(1.2 * 5900 / 1500), rt=3.4, rate_func=linear)
        self.p(FadeIn(vit_e[1], shift=LEFT * 0.2), FadeIn(vit_e[2], shift=LEFT * 0.2), rt=0.8)
        self.dire(r"Dans l'air : environ $340\ \mathrm{m\cdot s^{-1}}$. Bien plus rapide dans l'eau, et encore plus dans l'acier.", lire=2.6)
        self.dire("Oreille collée au rail, on entend le train arriver bien avant que son bruit arrive par l'air.", c=SOFT, lire=2.4)
        self.effacer_sous_titre()
        self.vider()
        self.nouvelle_scene()

    # =================================================================
    #  5. COMPARER LA VITESSE DU SON
    # =================================================================
    def comparaison(self):
        self.set_q("5. 340 m/s, c'est rapide ?")
        x_of = lambda v: -6.0 + 1.3 * math.log10(v)
        y0 = -1.4
        axe = Arrow([-6.3, y0, 0], [6.4, y0, 0], buff=0, color=SOFT, stroke_width=2, max_tip_length_to_length_ratio=0.02)
        grad = VGroup()
        for e in range(0, 10):
            x = -6.0 + 1.3 * e
            grad.add(Line([x, y0 - 0.08, 0], [x, y0 + 0.08, 0], color=SOFT, stroke_width=2))
            grad.add(mx(r"10^{%d}" % e if e > 1 else ("1" if e == 0 else "10"), SOFT, 24).next_to([x, y0 - 0.08, 0], DOWN, buff=0.1))
        u_l = mx(r"v\ (\mathrm{m\cdot s^{-1}})", SOFT, 26).next_to([6.4, y0, 0], DOWN, buff=0.45).shift(LEFT * 0.5)
        items = [("piéton", 1.4, "1,4 m/s", 0.9, WHITE), ("voiture", 36, "36 m/s", 1.9, WHITE),
                 ("avion de ligne", 250, "250 m/s", 2.9, WHITE), ("son (air)", 340, "340 m/s", 1.0, SONC),
                 ("station spatiale", 7700, "7 700 m/s", 2.2, WHITE), ("lumière", 3.0e8, "300 000 000 m/s", 1.6, "#FFF59D")]
        pts = VGroup()
        for nom, v, s, h, col in items:
            x = x_of(v)
            vedette = nom in ("son (air)", "lumière")      # (Manim refuse de comparer une couleur à du texte)
            tige = Line([x, y0, 0], [x, y0 + h, 0], color=col, stroke_width=3 if vedette else 2, stroke_opacity=0.7)
            pt = Dot([x, y0 + h, 0], radius=0.11 if vedette else 0.07, color=col)
            lab = VGroup(tx(nom, 20, col, bold=vedette), tx(s, 18, col)).arrange(DOWN, buff=0.06)
            if nom == "son (air)":
                lab.next_to(pt, RIGHT, buff=0.15)
            elif nom == "avion de ligne":
                lab.next_to(pt, LEFT, buff=0.15)
            else:
                lab.next_to(pt, UP, buff=0.12)
            pts.add(VGroup(tige, pt, lab))
        self.p(GrowArrow(axe), FadeIn(grad), FadeIn(u_l), rt=1.0)
        self.dire("Plaçons quelques vitesses sur une échelle « logarithmique » : chaque graduation, ×10.", lire=2.0)
        self.p(LaggedStart(*[FadeIn(p, shift=DOWN * 0.2) for k_, p in enumerate(pts) if k_ != 3], lag_ratio=0.3), rt=2.4)
        self.p(FadeIn(pts[3], shift=DOWN * 0.2), rt=0.8)
        self.p(Flash(pts[3][1], color=SONC, flash_radius=0.35), rt=0.8)
        self.dire(r"Dans l'air, le son va à environ $340\ \mathrm{m\cdot s^{-1}}$ : plus de 1 200 km/h, à peine plus qu'un avion de ligne.", c=SONC, lire=2.6)
        self.dire("La lumière est près d'un million de fois plus rapide… c'est ce qu'on remarque pendant un orage.", lire=2.4)
        self.effacer_sous_titre()
        self.vider()

    # =================================================================
    #  6. L'ORAGE
    # =================================================================
    def orage(self):
        self.set_q("6. L'éclair et le tonnerre")
        self.nouvelle_scene()
        self.vue([0.0, -0.55, 0], 66, -86, 0.8)
        R_ = ValueTracker(0.0)
        D = 7.0
        obs = np.array([-3.6, 0, 0])
        imp = np.array([3.4, 0, 0])

        def decor():
            T = self.T()
            sol = Surface(lambda u, v: T(np.array([u, v, 0.0])), u_range=[-5.2, 5.2], v_range=[-3, 3], resolution=(12, 7),
                          checkerboard_colors=False, fill_color="#1C2A23", fill_opacity=1, stroke_color="#33493C", stroke_width=0.8)
            perso = VGroup(self.cylindre3(T, obs, obs + np.array([0, 0, 0.75]), 0.13, "#5DADE2", res=(12, 1)),
                           self.sphere3(T, obs + np.array([0, 0, 0.92]), 0.14, "#F5CBA7", res=(12, 6)))
            nuage = VGroup(*[self.sphere3(T, imp + np.array(o), r, "#6B7280", res=(12, 6), sw=0.2)
                             for o, r in (([0, 0.3, 2.75], 0.7), ([-0.75, 0.2, 2.6], 0.55), ([0.75, 0.4, 2.6], 0.6),
                                          ([0.3, -0.2, 2.95], 0.5), ([-0.3, 0.5, 3.05], 0.5))])
            return VGroup(sol, perso, nuage)
        dec = always_redraw(decor)

        def onde():
            r = R_.get_value()
            if r < 0.05:
                return self.vide()
            return self.sphere3(self.T(), imp, r, SONC, res=(26, 6), op=0.10, demi=True, sw=0.8, sc=SONC, so=0.55)
        ond = always_redraw(onde)
        T = self.T()
        zz = [imp + np.array(p) for p in ([0, 0.1, 2.2], [0.25, 0.1, 1.7], [-0.15, 0.05, 1.25], [0.2, 0, 0.75], [-0.1, 0, 0.35], [0, 0, 0])]
        eclair = VMobject(stroke_color="#FFF59D", stroke_width=6)
        eclair.set_points_as_corners(T(np.array(zz)))
        halo = eclair.copy().set_stroke("#FFF59D", width=18, opacity=0.25)
        flash = Rectangle(width=15, height=9, stroke_width=0, fill_color=WHITE, fill_opacity=0.0)
        rayon = DashedLine(T(zz[1]), T(obs + np.array([0, 0, 0.92])), color="#FFF59D", stroke_width=2.5)
        l_o = self.epingle(tx("observateur", 20, "#5DADE2"), obs, DOWN * 0.4)
        compteur = always_redraw(lambda: txm(r"$\Delta t$ = %s s" % ("%.1f" % (6.0 * R_.get_value() / D)).replace(".", ","), 30, SONC)
                                 .to_corner(UR, buff=0.4).shift(DOWN * 0.45))
        self.add(ond)
        self.p(FadeIn(dec), FadeIn(l_o), rt=1.2)
        self.dire("Un orage : la foudre tombe à une certaine distance d'un observateur.", lire=1.4)
        self.p(Create(eclair), FadeIn(halo), flash.animate.set_fill(opacity=0.35), rt=0.25)
        self.p(Create(rayon), flash.animate.set_fill(opacity=0.0), rt=0.3)
        self.dire("La lumière de l'éclair lui parvient quasi instantanément (quelques microsecondes).", c="#FFF59D", lire=1.8)
        self.p(FadeOut(eclair), FadeOut(halo), FadeOut(rayon), FadeIn(compteur), rt=0.5)
        self.dire("Le son du tonnerre, lui, voyage à 340 m/s… comptons les secondes.", c=SONC, lire=0.2)
        self.p(R_.animate.set_value(D), rt=6.0, rate_func=linear)
        boum = tx("BOUM !", 30, SONC, bold=True).set_stroke(BLACK, 5, background=True).move_to(self.T()(obs + np.array([0, 0, 1.35])))
        self.p(FadeIn(boum, scale=1.6), Flash(self.T()(obs + np.array([0, 0, 0.92])), color=SONC, flash_radius=0.5), rt=0.6)
        self.p(R_.animate.set_value(D + 1.2), FadeOut(boum), rt=1.0, rate_func=linear)
        compteur.clear_updaters()
        self.dire(r"Le tonnerre arrive $\Delta t = 6{,}0$ s après l'éclair. À quelle distance la foudre est-elle tombée ?", c=SONC, lire=2.4)
        self.effacer_sous_titre()
        self.vider()
        self.nouvelle_scene()

    def calcul_orage(self):
        self.question(r"On entend le tonnerre $\Delta t = 6{,}0$ s après avoir vu l'éclair. À quelle distance $d$ la foudre est-elle tombée ?")
        fs = 44
        l1 = row(mx("v", SONC, fs), mx("=", WHITE, fs), frac(mx("d", VOL, fs), mx(r"\Delta t", TCOL, fs)), buff=0.15)
        fl = mx(r"\Longrightarrow", SOFT, fs)
        E = row(mx("d", VOL, fs), mx("=", WHITE, fs), mx("v", SONC, fs), mx(r"\times", WHITE, fs), mx(r"\Delta t", TCOL, fs), buff=0.15)
        haut_ = row(l1, fl, E, buff=0.6)
        AN = row(mx("d", VOL, fs), mx("=", WHITE, fs), val("340", (r"\mathrm{m}\cdot", r"\mathrm{s^{-1}}"), SONC, fs),
                 mx(r"\times", WHITE, fs), val(r"6{,}0", r"\mathrm{s}", TCOL, fs), buff=0.18)
        RR = row(mx("d", VOL, fs), mx("=", WHITE, fs), val(r"2{,}0\times10^{3}", r"\mathrm{m}", RES, fs), mx("=", WHITE, fs),
                 val(r"2{,}0", r"\mathrm{km}", RES, fs), buff=0.18)
        astuce = VGroup(tx("Astuce :", 22, ABSO, bold=True),
                        txm(r"3 s entre l'éclair et le tonnerre $\approx$ 1 km  ($340 \times 3 \approx 1\,000$ m)", 22, ABSO)).arrange(RIGHT, buff=0.25)
        cad_a = SurroundingRectangle(astuce, color=ABSO, buff=0.18, corner_radius=0.1, stroke_width=2)
        g_a = VGroup(cad_a, astuce)
        page = VGroup(haut_, AN, RR, g_a).arrange(DOWN, aligned_edge=LEFT, buff=0.85)
        self.caser(page, top=self.haut() - 0.6, x=-0.3, w=11.5)
        self.dire(r"Le son parcourt la distance $d$ pendant la durée $\Delta t$, à la vitesse $v$.", lire=0.3)
        self.p(Write(l1), rt=1.2)
        self.dire(r"On isole d'abord la grandeur cherchée, $d$ : c'est l'expression littérale.", c=BOX, lire=0.3)
        self.p(FadeIn(fl), rt=0.3)
        self.morph([(l1[0], E[2]), (l1[2][0], E[0]), (l1[2][2], E[4])], FadeIn(VGroup(E[1], E[3])), rt=1.4)
        self.encadre(E)
        self.pause(1.0)
        self.tag_an(AN)
        self.p(Write(VGroup(AN[0], AN[1], AN[3])), rt=0.6)
        self.morph([(E[2], AN[2]), (E[4], AN[4])], rt=1.2)
        self.barrer(AN[2][1][1], AN[4][1])
        self.dire(r"Les secondes se simplifient : il reste des mètres. Deux chiffres significatifs, comme $6{,}0$ s.", c=UNIT, lire=2.2)
        self.p(Write(RR), rt=1.2)
        self.p(Circumscribe(RR[4], color=RES), rt=0.8)
        self.p(FadeIn(g_a, shift=UP * 0.1), rt=0.8)
        self.pause(1.5)
        self.effacer_sous_titre()
        self.reponse("La foudre est tombée à environ 2,0 km de l'observateur.")
        self.pause(4.0)
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
            row(etiquette("1", SONC).scale(1.4), txm("Un son est émis par un objet qui vibre ; une caisse de résonance l'amplifie.", 24), buff=0.3),
            row(etiquette("2", COMP).scale(1.4), txm("Le son est une perturbation (compressions, dilatations) qui se propage de proche en proche.", 24), buff=0.3),
            row(etiquette("3", COMP).scale(1.4), txm("Il transporte de l'énergie, pas de matière : les molécules oscillent sur place.", 24), buff=0.3),
            row(etiquette("4", RARE).scale(1.4), txm("Il lui faut un milieu matériel : pas de son dans le vide.", 24), buff=0.3),
            row(etiquette("5", RES).scale(1.4), txm(r"Dans l'air, $v \approx 340\ \mathrm{m\cdot s^{-1}}$ ; plus rapide dans l'eau et les solides ; $d = v \times \Delta t$.", 24), buff=0.3),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32)
        g = VGroup(t, items).arrange(DOWN, buff=0.5)
        ajuster(g, 13.0, 6.6)
        g.move_to(DOWN * 0.2)
        self.p(Write(t), rt=0.8)
        self.p(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.2) for i in items], lag_ratio=0.3), rt=2.4)
        self.pause(6.0)
