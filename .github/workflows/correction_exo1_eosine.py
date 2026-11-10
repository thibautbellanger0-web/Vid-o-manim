from manim import *
import math

# ============================================================
#  Correction – Exercice 1 : L'éosine (spectrophotométrie)
#  Vidéo MUETTE calée sur l'audio (fichier SRT) : ajouter la voix au montage,
#  vidéo et audio démarrent tous les deux à 0 s.
# ============================================================

# ---------- Code couleur (constant dans toute la vidéo) ----------
CONC = "#58C4DD"   # concentrations (bleu)
VOL = "#83C167"    # volumes (vert)
MASSE = "#FF862F"  # masses (orange)
ABSO = "#F4D03F"   # absorbance (jaune)
KCOL = "#C77DFF"   # coefficient k / epsilon (violet)
RHO = "#FF6F91"    # masse volumique (rose)
RES = "#3BE07A"    # résultats / phrases réponses (vert vif)
BOX = "#FFD166"    # cadre des expressions littérales (or)
UNIT = "#D0D0D0"   # unités (gris clair)
MAGENTA = "#E040FB"


# ---------- Petits outils ----------
def tx(s, fs=28, c=WHITE, w=12.6):
    t = Text(s, font_size=fs, color=c)
    if t.width > w:
        t.scale_to_fit_width(w)
    return t


def mx(s, c=WHITE, fs=40):
    return MathTex(s, color=c, font_size=fs)


def val(num, unit, c=WHITE, fs=40):
    """Valeur numérique + unité. unit : texte ou tuple de morceaux (pour barrer une partie).
    val(...)[1] = groupe de l'unité ; val(...)[1][i] = i-ème morceau de l'unité."""
    parts = unit if isinstance(unit, tuple) else (unit,)
    u = VGroup(*[mx(x, UNIT, fs) for x in parts]).arrange(RIGHT, buff=0.04)
    return VGroup(mx(num, c, fs), u).arrange(RIGHT, buff=0.12)


def frac(n, d, c=WHITE):
    w = max(n.width, d.width) + 0.2
    bar = Line(LEFT * w / 2, RIGHT * w / 2, color=c, stroke_width=3)
    return VGroup(n, bar, d).arrange(DOWN, buff=0.12)


def row(*m, buff=0.18):
    return VGroup(*m).arrange(RIGHT, buff=buff)


def barre(m, c=RED):
    return Line(m.get_corner(DL), m.get_corner(UR), color=c, stroke_width=5)


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
    return (1.13 * math.exp(-((x - 528) / 15) ** 2) + 0.33 * math.exp(-((x - 498) / 15) ** 2)
            + 0.16 * math.exp(-((x - 312) / 14) ** 2) + 0.07 * math.exp(-((x - 346) / 7) ** 2))


def trace(ax, f, x0, x1, color=WHITE, sw=4, n=240):
    """Courbe construite point par point à partir de ax.c2p (indépendante des axes)."""
    pts = [ax.c2p(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    m = VMobject(stroke_color=color, stroke_width=sw)
    m.set_points_as_corners(pts)
    return m


def aire(ax, f, x0, x1, color, op=0.5, n=12):
    """Surface sous la courbe entre x0 et x1."""
    pts = [ax.c2p(x0 + (x1 - x0) * i / n, f(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
    return Polygon(ax.c2p(x0, 0), *pts, ax.c2p(x1, 0), stroke_width=0, fill_color=color, fill_opacity=op)


def aire_couleurs(ax, f, x0=380, x1=650, pas=5, op=0.75):
    """Surface sous le spectre colorée selon la longueur d'onde."""
    return VGroup(*[aire(ax, f, w, w + pas, wl_color(w + pas / 2), op, n=2) for w in range(x0, x1, pas)])


C_ETALON = [0, 0.005, 0.007, 0.010, 0.012, 0.015, 0.017, 0.020]
A_ETALON = [0, 0.50, 0.65, 0.95, 1.14, 1.42, 1.63, 1.90]
C_TXT = ["0", "0{,}005", "0{,}007", "0{,}010", "0{,}012", "0{,}015", "0{,}017", "0{,}020"]
A_TXT = ["0", "0{,}50", "0{,}65", "0{,}95", "1{,}14", "1{,}42", "1{,}63", "1{,}90"]
A_S0 = ["1{,}571", "1{,}506", "1{,}540", "1{,}506", "1{,}571", "1{,}541", "1{,}571", "1{,}523", "1{,}517"]
A_S0_NUM = [1.571, 1.506, 1.540, 1.506, 1.571, 1.541, 1.571, 1.523, 1.517]


class Correction(Scene):
    # ---------- gestion du temps (calage sur l'audio) ----------
    def p(self, *anims, rt=1.0):
        self.play(*anims, run_time=rt)
        self.t += rt

    def at(self, t):
        """Attend jusqu'à l'instant t (en secondes) de l'audio."""
        if t > self.t + 0.02:
            self.wait(t - self.t)
            self.t = t

    # ---------- éléments récurrents ----------
    def set_q(self, label):
        new = tx(label, 22, ABSO).next_to(self.hdr_ex, RIGHT, buff=0.3)
        if self.hdr_q is None:
            self.p(FadeIn(new), rt=0.5)
        else:
            self.p(ReplacementTransform(self.hdr_q, new), rt=0.5)
        self.hdr_q = new

    def vider(self, rt=0.6, garder=()):
        mobs = [m for m in self.mobjects if m not in (self.hdr_ex, self.hdr_q) and m not in garder]
        if mobs:
            self.p(*[FadeOut(m) for m in mobs], rt=rt)

    def question(self, s, rt=1.5):
        q = tx(s, 26, WHITE).to_edge(UP, buff=0.85)
        self.p(FadeIn(q, shift=DOWN * 0.2), rt=rt)
        self.cur_q = q
        return q

    def morph(self, pairs, *extra, rt=1.0):
        """Fait « voler » une copie de chaque source vers sa cible.
        La cible d'origine n'est jamais modifiée par l'animation (on anime un fantôme),
        ce qui permet de continuer à l'indexer ensuite."""
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
        """Barre des unités qui se simplifient."""
        traits = VGroup(*[barre(m) for m in mobs])
        self.p(*[Create(l) for l in traits], rt=rt)
        return traits

    def encadre(self, eq, rt=1.2):
        rect = SurroundingRectangle(eq, color=BOX, buff=0.22, stroke_width=4)
        lab = tx("Expression littérale", 18, BOX).next_to(rect, UP, buff=0.08).align_to(rect, LEFT)
        self.p(Create(rect), FadeIn(lab), rt=rt)
        return VGroup(rect, lab)

    def reponse(self, s, rt=2.0, fs=24):
        t = tx(s, fs, RES, w=12.2)
        box = SurroundingRectangle(t, color=RES, buff=0.22, stroke_width=3)
        g = VGroup(box, t).to_edge(DOWN, buff=0.3)
        self.p(Create(box), FadeIn(t, shift=UP * 0.15), rt=rt)
        return g

    def graphe(self, x_len=8.0, y_len=4.3):
        ax = Axes(x_range=[0, 0.022, 0.005], y_range=[0, 2.1, 0.5], x_length=x_len, y_length=y_len,
                  tips=True, axis_config={"color": GREY_B, "include_ticks": True})
        labs = VGroup()
        for v, s in [(0.005, "0{,}005"), (0.010, "0{,}010"), (0.015, "0{,}015"), (0.020, "0{,}020")]:
            labs.add(mx(s, GREY_B, 24).next_to(ax.c2p(v, 0), DOWN, buff=0.15))
        for v, s in [(0.5, "0{,}5"), (1.0, "1{,}0"), (1.5, "1{,}5"), (2.0, "2{,}0")]:
            labs.add(mx(s, GREY_B, 24).next_to(ax.c2p(0, v), LEFT, buff=0.15))
        xl = mx(r"C_m\ (\mathrm{g\cdot L^{-1}})", CONC, 28).next_to(ax.c2p(0.022, 0), DOWN, buff=0.45).shift(LEFT * 0.6)
        yl = mx("A", ABSO, 32).next_to(ax.c2p(0, 2.1), LEFT, buff=0.2)
        pts = VGroup(*[Dot(ax.c2p(c, a), radius=0.07, color=WHITE) for c, a in zip(C_ETALON, A_ETALON)])
        droite = Line(ax.c2p(0, 0), ax.c2p(0.0215, 95 * 0.0215), color=KCOL, stroke_width=4)
        return ax, VGroup(labs, xl, yl), pts, droite

    # ============================================================
    def construct(self):
        self.t = 0.0
        self.hdr_q = None

        # ---------------- INTRODUCTION ----------------
        self.at(0.8)
        titre = tx("Exercice 1 : L'éosine", 56, WHITE)
        sous = tx("Correction", 32, ABSO).next_to(titre, DOWN, buff=0.3)
        self.p(Write(titre), FadeIn(sous, shift=UP * 0.2), rt=2.0)
        self.hdr_ex = tx("Exercice 1 – L'éosine", 22, GREY_B).to_corner(UL, buff=0.3)
        self.at(4.0)
        self.p(ReplacementTransform(titre, self.hdr_ex), FadeOut(sous), rt=0.9)

        self.at(5.0)
        dos = RoundedRectangle(width=0.7, height=1.6, corner_radius=0.15, color=WHITE,
                               fill_color=MAGENTA, fill_opacity=0.85).shift(LEFT * 4 + UP * 0.6)
        bouchon = Rectangle(width=0.3, height=0.35, color=WHITE, fill_color=GREY_B, fill_opacity=1).next_to(dos, UP, buff=0)
        dosette = VGroup(dos, bouchon)
        d_lab = tx("dosette", 22, GREY_B).next_to(dosette, DOWN)
        infos = VGroup(
            tx("Antiseptique local", 32, WHITE),
            tx("vendu en dosettes en pharmacie", 28, GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(dosette, RIGHT, buff=1.0)
        self.p(DrawBorderThenFill(dosette), FadeIn(d_lab), rt=1.5)
        self.p(FadeIn(infos, shift=LEFT * 0.3), rt=1.2)

        self.at(12.0)
        obj = VGroup(
            tx("Objectif :", 30, ABSO),
            tx("déterminer la concentration massique d'éosine", 30, WHITE),
            row(tx("de la solution commerciale ", 30, WHITE), mx("C_m", CONC, 44)),
        ).arrange(DOWN, buff=0.2).shift(DOWN * 2.0)
        self.p(FadeIn(obj, shift=UP * 0.3), rt=1.5)
        self.at(18.0)
        self.p(Indicate(obj[2][1], color=CONC, scale_factor=1.4), rt=1.2)

        # Documents 1 et 2
        self.at(21.4)
        self.vider()
        doc1_t = tx("Document 1 : solutions étalons", 24, ABSO)
        cells = VGroup()
        h1 = mx(r"C_m\,(\mathrm{g\cdot L^{-1}})", CONC, 24)
        h2 = mx("A", ABSO, 26)
        for i in range(8):
            cells.add(mx(C_TXT[i], WHITE, 24).move_to(RIGHT * (0.78 * i)))
        cells2 = VGroup(*[mx(A_TXT[i], WHITE, 24).move_to(RIGHT * (0.78 * i) + DOWN * 0.6) for i in range(8)])
        h1.next_to(cells[0], LEFT, buff=0.35)
        h2.next_to(cells2[0], LEFT, buff=0.35).align_to(h1, RIGHT)
        tab1 = VGroup(h1, h2, cells, cells2)
        tab1_box = SurroundingRectangle(tab1, color=GREY_B, buff=0.2)
        doc1 = VGroup(doc1_t, VGroup(tab1, tab1_box)).arrange(DOWN, buff=0.25)
        doc1.scale_to_fit_width(6.4).move_to(LEFT * 3.35 + UP * 0.2)
        self.p(FadeIn(doc1_t), Create(tab1_box), rt=0.8)
        self.p(LaggedStart(FadeIn(h1), FadeIn(h2), *[FadeIn(VGroup(a, b)) for a, b in zip(cells, cells2)],
                           lag_ratio=0.15), rt=2.0)

        self.at(27.4)
        ax_s = Axes(x_range=[300, 650, 50], y_range=[0, 1.3, 0.4], x_length=5.4, y_length=2.8,
                    tips=False, axis_config={"color": GREY_B}).move_to(RIGHT * 3.6 + DOWN * 0.1)
        doc2_t = tx("Document 2 : spectre d'absorption", 24, ABSO).next_to(ax_s, UP, buff=0.35)
        lx_s = VGroup(*[mx(str(v), GREY_B, 20).next_to(ax_s.c2p(v, 0), DOWN, buff=0.12) for v in (300, 400, 500, 600)])
        lab_s = VGroup(mx(r"\lambda\ (\mathrm{nm})", GREY_B, 20).next_to(ax_s.c2p(650, 0), DOWN, buff=0.12).shift(RIGHT * 0.2),
                       mx("A", ABSO, 24).next_to(ax_s.c2p(300, 1.3), LEFT, buff=0.1))
        fond_s = aire(ax_s, spectre, 300, 640, MAGENTA, 0.25, n=140)
        courbe_s = trace(ax_s, spectre, 300, 640, MAGENTA, 3)
        self.p(FadeIn(doc2_t), Create(ax_s), FadeIn(lx_s), FadeIn(lab_s), rt=0.8)
        self.p(Create(courbe_s), FadeIn(fond_s), rt=1.5)

        # Les dilutions -> S0
        self.at(31.8)
        self.vider()
        def fiole(vol, op, r=0.5):
            ballon = Circle(radius=r, color=WHITE, fill_color=MAGENTA, fill_opacity=op)
            col = Rectangle(width=0.22, height=0.9, color=WHITE).next_to(ballon, UP, buff=-0.05)
            trait = Line(LEFT * 0.16, RIGHT * 0.16, color=RED, stroke_width=3).move_to(col.get_center() + UP * 0.15)
            lab = mx(vol, VOL, 28).next_to(ballon, DOWN, buff=0.15)
            return VGroup(ballon, col, trait, lab)
        dos2 = VGroup(RoundedRectangle(width=0.45, height=1.0, corner_radius=0.1, color=WHITE,
                                       fill_color=MAGENTA, fill_opacity=0.9))
        dos2.add(mx(r"2{,}00\ \mathrm{mL}", VOL, 28).next_to(dos2[0], DOWN, buff=0.15))
        f1 = fiole(r"1{,}00\ \mathrm{L}", 0.45, 0.65)
        f2 = fiole(r"25{,}0\ \mathrm{mL}", 0.2, 0.42)
        schema = VGroup(dos2, f1, f2).arrange(RIGHT, buff=2.6).shift(UP * 0.9)
        fl1 = Arrow(dos2.get_right() + UP * 0.2, f1.get_left() + UP * 0.2, color=GREY_B, buff=0.25)
        fl2 = Arrow(f1.get_right() + UP * 0.2, f2.get_left() + UP * 0.2, color=GREY_B, buff=0.25)
        e1 = tx("dilution 1", 20, GREY_B).next_to(fl1, UP, buff=0.1)
        e2 = VGroup(tx("dilution 2", 20, GREY_B), mx(r"V = 10{,}0\ \mathrm{mL}", VOL, 26)).arrange(DOWN, buff=0.08).next_to(fl2, UP, buff=0.1)
        s0 = tx("S0", 28, CONC).next_to(f2, RIGHT, buff=0.3)
        self.p(FadeIn(dos2), rt=0.8)
        self.at(36.2)
        self.p(GrowArrow(fl1), FadeIn(e1), FadeIn(f1), rt=1.5)
        self.at(38.4)
        self.p(GrowArrow(fl2), FadeIn(e2), FadeIn(f2), rt=1.5)
        self.p(Write(s0), Indicate(f2), rt=1.2)

        self.at(43.5)
        # tableau des 9 binômes
        bin_lab = tx("Binôme", 22, GREY_B)
        a_lab = mx("A", ABSO, 30)
        nums = VGroup(*[mx(str(i + 1), GREY_B, 26) for i in range(9)])
        vals = VGroup(*[mx(A_S0[i], ABSO, 26) for i in range(9)])
        for i in range(9):
            nums[i].move_to(RIGHT * 1.15 * i)
            vals[i].move_to(RIGHT * 1.15 * i + DOWN * 0.6)
        bin_lab.next_to(nums[0], LEFT, buff=0.4)
        a_lab.next_to(vals[0], LEFT, buff=0.4).align_to(bin_lab, RIGHT)
        tab9 = VGroup(bin_lab, a_lab, nums, vals).move_to(DOWN * 2.2)
        tab9_t = tx("Absorbance de S0 mesurée par chaque binôme", 22, WHITE).next_to(tab9, UP, buff=0.3)
        self.p(FadeIn(tab9_t), FadeIn(bin_lab), FadeIn(a_lab), FadeIn(nums), rt=1.2)
        self.at(49.1)
        self.p(LaggedStart(*[FadeIn(v, shift=DOWN * 0.2) for v in vals], lag_ratio=0.2), rt=2.5)

        self.at(55.5)
        self.vider()
        comment = tx("Comment s'y prendre ?", 44, WHITE)
        self.p(Write(comment), rt=1.5)
        self.at(59.6)
        self.p(FadeOut(comment), rt=0.6)

        # ---------------- QUESTION 1 ----------------
        self.at(60.8)
        self.set_q("Question 1")
        q = self.question("1) Déterminer la couleur d'une solution d'éosine. Justifier avec son spectre.")
        self.at(68.1)
        ax = Axes(x_range=[300, 660, 50], y_range=[0, 1.3, 0.4], x_length=9.5, y_length=3.6,
                  tips=True, axis_config={"color": GREY_B}).shift(DOWN * 0.1 + RIGHT * 0.3)
        lx = VGroup(*[mx(str(v), GREY_B, 22).next_to(ax.c2p(v, 0), DOWN, buff=0.45) for v in (300, 400, 500, 600)])
        ly = VGroup(*[mx(s, GREY_B, 22).next_to(ax.c2p(300, v), LEFT, buff=0.12) for v, s in ((0.4, "0{,}4"), (0.8, "0{,}8"), (1.2, "1{,}2"))])
        ax_lab = VGroup(mx(r"\lambda\ (\mathrm{nm})", WHITE, 26).next_to(ax.c2p(660, 0), DOWN, buff=0.45),
                        mx("A", ABSO, 30).next_to(ax.c2p(300, 1.3), LEFT, buff=0.15))
        courbe = trace(ax, spectre, 300, 645, WHITE, 4)
        couleurs = aire_couleurs(ax, spectre, 380, 645, 5, 0.8)
        self.p(Create(ax), FadeIn(lx), FadeIn(ly), FadeIn(ax_lab), rt=1.2)
        self.p(Create(courbe), rt=1.0)

        self.at(70.4)
        dx = ax.c2p(285, 0)[0] - ax.c2p(280, 0)[0]
        bande = VGroup(*[Rectangle(width=dx * 1.02, height=0.22, stroke_width=0, fill_color=wl_color(w), fill_opacity=1)
                         .move_to(ax.c2p(w + 2.5, 0) + DOWN * 0.2) for w in range(380, 660, 5)])
        vis = tx("lumière visible", 20, GREY_B).next_to(bande, DOWN, buff=0.38)
        self.p(LaggedStart(*[FadeIn(b) for b in bande], lag_ratio=0.03), FadeIn(vis), rt=2.0)
        self.p(LaggedStart(*[FadeIn(c) for c in couleurs], lag_ratio=0.05), rt=1.5)

        self.at(74.3)
        pic = DashedLine(ax.c2p(528, 0), ax.c2p(528, 1.13), color=GREEN)
        lmax = mx(r"\lambda_{max}\approx 530\ \mathrm{nm}", GREEN, 30).next_to(ax.c2p(528, 1.13), RIGHT, buff=0.3)
        zone = SurroundingRectangle(VGroup(*couleurs[23:37]), color=GREEN, buff=0.08, stroke_width=3)
        self.p(Create(pic), Write(lmax), rt=1.2)
        self.at(76.3)
        absvert = tx("absorbe dans le VERT", 28, GREEN).next_to(lmax, DOWN, buff=0.3).align_to(lmax, LEFT)
        self.p(FadeIn(zone), Write(absvert), rt=1.4)

        # synthèse additive
        self.at(78.6)
        self.p(*[FadeOut(m) for m in (ax, lx, ly, ax_lab, courbe, couleurs, bande, vis, pic, lmax, zone, absvert)], rt=0.8)
        cuve = Rectangle(width=1.4, height=2.2, color=WHITE, fill_color=MAGENTA, fill_opacity=0.35).shift(DOWN * 0.4)
        cuve_l = tx("solution d'éosine", 20, GREY_B).next_to(cuve, DOWN, buff=0.15)
        blanc = Arrow(LEFT * 6 + DOWN * 0.4, cuve.get_left(), color=WHITE, buff=0.1, stroke_width=8)
        bl_lab = tx("lumière blanche", 22, WHITE).next_to(blanc, UP, buff=0.1)
        self.p(FadeIn(cuve), FadeIn(cuve_l), rt=0.8)
        self.p(GrowArrow(blanc), FadeIn(bl_lab), rt=1.2)

        self.at(85.7)
        ys = [0.35, 0.0, -0.35]
        cols = [RED, GREEN, BLUE]
        rvb = VGroup(*[Arrow(LEFT * 6 + DOWN * 0.4 + UP * y, cuve.get_left() + UP * y, color=c, buff=0.1, stroke_width=7)
                       for y, c in zip(ys, cols)])
        eq_rvb = row(tx("blanc", 24, WHITE), tx("=", 24), tx("rouge", 24, RED), tx("+", 24),
                     tx("vert", 24, GREEN), tx("+", 24), tx("bleu", 24, BLUE), buff=0.15).move_to(UP * 2.0)
        self.p(ReplacementTransform(blanc, rvb), FadeOut(bl_lab), Write(eq_rvb), rt=1.6)

        self.at(90.2)
        vert_abs = rvb[1]
        croix = Cross(stroke_color=GREEN, stroke_width=6).scale(0.25).move_to(cuve.get_center() + UP * 0.0)
        sortie = VGroup(
            Arrow(cuve.get_right() + UP * 0.35, RIGHT * 3.6 + DOWN * 0.05, color=RED, buff=0.1, stroke_width=7),
            Arrow(cuve.get_right() + DOWN * 0.35, RIGHT * 3.6 + DOWN * 0.75, color=BLUE, buff=0.1, stroke_width=7),
        )
        self.p(vert_abs.animate.put_start_and_end_on(vert_abs.get_start(), cuve.get_center()), rt=1.0)
        self.p(FadeIn(croix), Indicate(eq_rvb[4], color=GREEN), rt=0.8)
        self.p(GrowArrow(sortie[0]), GrowArrow(sortie[1]), rt=1.2)

        self.at(94.4)
        c_r = Circle(radius=0.55, color=RED, fill_color=RED, fill_opacity=0.8).move_to(RIGHT * 4.6 + UP * 0.2)
        c_b = Circle(radius=0.55, color=BLUE, fill_color=BLUE, fill_opacity=0.8).move_to(RIGHT * 4.6 + DOWN * 1.0)
        c_m = Circle(radius=0.7, color=MAGENTA, fill_color=MAGENTA, fill_opacity=1).move_to(RIGHT * 4.9 + DOWN * 0.4)
        m_lab = tx("magenta", 26, MAGENTA).next_to(c_m, DOWN, buff=0.2)
        self.p(FadeIn(c_r), FadeIn(c_b), rt=0.5)
        self.p(ReplacementTransform(VGroup(c_r, c_b), c_m), Write(m_lab), rt=0.9)
        self.at(95.4)
        self.reponse("La solution absorbe le vert (λmax ≈ 530 nm) : seuls le rouge et le bleu sont transmis.\n"
                     "La solution d'éosine est donc de couleur MAGENTA (couleur complémentaire du vert).", rt=2.5)

        # ---------------- QUESTION 2 ----------------
        self.at(105.9)
        self.vider()
        self.set_q("Question 2")
        self.question("2) La gamme d'étalonnage permet-elle d'exploiter les résultats expérimentaux ?")
        self.at(111.8)
        x0, x1 = -5.5, 5.5
        f = lambda a: x0 + (x1 - x0) * a / 2.0
        axe = Arrow(RIGHT * (x0 - 0.2), RIGHT * (x1 + 0.4), color=GREY_B, buff=0, stroke_width=3)
        ticks = VGroup()
        for a, s in [(0, "0"), (0.5, "0{,}50"), (1.0, "1{,}00"), (1.5, "1{,}50"), (1.9, "1{,}90")]:
            ticks.add(VGroup(Line(UP * 0.12, DOWN * 0.12, color=GREY_B).move_to(RIGHT * f(a)),
                             mx(s, GREY_B, 26).move_to(RIGHT * f(a) + DOWN * 0.45)))
        a_ax = mx("A", ABSO, 34).next_to(axe, RIGHT, buff=0.15)
        ligne = VGroup(axe, ticks, a_ax).shift(DOWN * 0.3)
        self.p(GrowArrow(axe), FadeIn(ticks), FadeIn(a_ax), rt=1.5)
        gamme = Rectangle(width=f(1.9) - f(0.5), height=0.5, stroke_width=0, fill_color=ABSO, fill_opacity=0.3)
        gamme.move_to(RIGHT * (f(0.5) + f(1.9)) / 2 + DOWN * 0.3)
        g_lab = tx("gamme des solutions étalons", 24, ABSO).next_to(gamme, UP, buff=0.9)
        g_arr = Arrow(g_lab.get_bottom(), gamme.get_top(), color=ABSO, buff=0.1)
        self.at(114.0)
        self.p(FadeIn(gamme), FadeIn(g_lab), GrowArrow(g_arr), rt=1.5)
        self.at(119.0)
        pts_s0 = VGroup(*[Dot(RIGHT * f(a) + DOWN * 0.3, radius=0.07, color=CONC) for a in A_S0_NUM])
        s0_lab = VGroup(tx("S0 :", 24, CONC), mx(r"A \approx 1{,}5", CONC, 32)).arrange(RIGHT, buff=0.15)
        s0_lab.next_to(pts_s0, DOWN, buff=0.9)
        self.p(LaggedStart(*[GrowFromCenter(d) for d in pts_s0], lag_ratio=0.1), rt=1.5)
        self.p(FadeIn(s0_lab, shift=UP * 0.2), rt=0.8)
        self.at(122.0)
        self.p(Circumscribe(pts_s0, color=CONC), rt=1.2)
        self.at(124.0)
        self.reponse("Oui : l'absorbance de S0 (A ≈ 1,5) est comprise entre 0,50 et 1,90 (absorbances des étalons).\n"
                     "On pourra placer ce point sur la droite d'étalonnage : les résultats sont exploitables.", rt=2.5)

        # ---------------- QUESTION 3 ----------------
        self.at(133.2)
        self.vider()
        self.set_q("Question 3")
        self.question("3) Tracer la droite d'étalonnage A = f(Cm).")
        ax3, deco3, pts3, droite3 = self.graphe(x_len=7.2, y_len=4.3)
        VGroup(ax3, deco3, pts3, droite3).shift(DOWN * 0.35 + LEFT * 2.4)
        self.p(Create(ax3), FadeIn(deco3), rt=1.8)
        self.at(138.9)
        self.p(LaggedStart(*[GrowFromCenter(d) for d in pts3], lag_ratio=0.25), rt=3.0)
        self.at(142.4)
        self.p(Create(droite3), rt=2.0)
        orig = Circle(radius=0.25, color=RES).move_to(ax3.c2p(0, 0))
        self.at(144.2)
        self.p(Create(orig), rt=0.6)
        self.at(146.9)
        bl = VGroup(tx("Droite passant par l'origine", 24, KCOL),
                    tx("donc A est proportionnelle à Cm", 24, WHITE),
                    tx("(loi de Beer-Lambert vérifiée)", 22, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        bl.to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        self.p(FadeIn(bl, shift=LEFT * 0.3), rt=1.5)
        self.at(152.4)
        pente = row(mx("A", ABSO, 40), mx("=", WHITE, 40), mx("k", KCOL, 40), mx(r"\times", WHITE, 40),
                    mx("C_m", CONC, 40), buff=0.15).next_to(bl, DOWN, buff=0.5)
        self.p(Write(pente), rt=1.5)
        self.p(Indicate(droite3, color=KCOL), rt=1.2)

        # ---------------- QUESTION 4 ----------------
        self.at(158.4)
        self.vider()
        self.set_q("Question 4")
        self.question("4) Énoncer la loi de Beer-Lambert, détailler les grandeurs et unités, calculer k.")
        self.at(167.1)
        bl_t = tx("Loi de Beer-Lambert", 34, KCOL).shift(UP * 1.6)
        bl_d = tx("L'absorbance est proportionnelle à la concentration de l'espèce colorée.", 24, WHITE).next_to(bl_t, DOWN, buff=0.25)
        self.p(Write(bl_t), rt=1.2)
        self.p(FadeIn(bl_d), rt=1.2)

        self.at(177.9)
        self.p(FadeOut(bl_d), rt=0.4)
        loi1 = row(mx("A", ABSO, 54), mx("=", WHITE, 54), mx(r"\varepsilon", KCOL, 54), mx(r"\times", WHITE, 54),
                   mx(r"\ell", VOL, 54), mx(r"\times", WHITE, 54), mx("C", CONC, 54), buff=0.22).move_to(LEFT * 3.6 + UP * 0.4)
        self.p(Write(loi1), rt=1.5)
        def leg(sym, nom, unite, c):
            return row(mx(sym, c, 34), tx(": " + nom, 21, c), tx("(" + unite + ")", 21, UNIT), buff=0.15)
        legs = VGroup(
            leg("A", "absorbance", "sans unité", ABSO),
            leg(r"\varepsilon", "coefficient d'absorption molaire", "L·mol⁻¹·cm⁻¹", KCOL),
            leg(r"\ell", "largeur de la cuve", "cm", VOL),
            leg("C", "concentration en quantité de matière", "mol·L⁻¹", CONC),
            leg("k", "coefficient de proportionnalité", "L·g⁻¹", KCOL),
            leg("C_m", "concentration massique", "g·L⁻¹", CONC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        if legs.width > 7.4:
            legs.scale_to_fit_width(7.4)
        legs.to_edge(RIGHT, buff=0.3).shift(DOWN * 0.45)
        for k_, t_ in enumerate((179.5, 181.3, 183.0, 184.5)):
            self.at(t_)
            self.p(FadeIn(legs[k_], shift=LEFT * 0.2), rt=0.8)

        self.at(188.3)
        ou = tx("ou", 26, GREY_B).next_to(loi1, DOWN, buff=0.35)
        loi2 = row(mx("A", ABSO, 54), mx("=", WHITE, 54), mx("k", KCOL, 54), mx(r"\times", WHITE, 54),
                   mx("C_m", CONC, 54), buff=0.22).next_to(ou, DOWN, buff=0.35)
        self.p(FadeIn(ou), Write(loi2), rt=1.5)
        self.at(193.0)
        self.p(FadeIn(legs[4], shift=LEFT * 0.2), rt=0.8)
        self.p(FadeIn(legs[5], shift=LEFT * 0.2), rt=0.8)

        # calcul de k
        self.at(198.0)
        self.p(FadeOut(loi1), FadeOut(ou), FadeOut(legs), FadeOut(bl_t), loi2.animate.scale(0.8).move_to(UP * 1.6 + LEFT * 3.5), rt=1.0)
        pt = VGroup(tx("Point choisi (dernier étalon) :", 24, WHITE),
                    row(mx(r"C_m = ", CONC, 38), val(r"0{,}020", r"\mathrm{g\cdot L^{-1}}", CONC, 38)),
                    row(mx("A = ", ABSO, 38), mx(r"1{,}90", ABSO, 38))).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        pt.move_to(RIGHT * 3.3 + UP * 1.2)
        self.at(203.5)
        self.p(FadeIn(pt[0]), rt=0.6)
        self.p(FadeIn(pt[1], shift=LEFT * 0.2), rt=0.8)
        self.at(208.0)
        self.p(FadeIn(pt[2], shift=LEFT * 0.2), rt=0.8)
        self.at(210.1)
        moy_note = tx("(on pourrait aussi calculer k pour chaque point et faire la moyenne)", 20, GREY_B).next_to(pt, DOWN, buff=0.3)
        self.p(FadeIn(moy_note), rt=1.0)

        self.at(216.4)
        lk = mx("k", KCOL, 48)
        lit_k = row(lk, mx("=", WHITE, 48), frac(mx("A", ABSO, 48), mx("C_m", CONC, 48)), buff=0.2).move_to(LEFT * 3.5 + DOWN * 0.3)
        self.morph([(loi2, lit_k)], rt=1.8)
        self.at(219.6)
        cad_k = self.encadre(lit_k)
        self.at(228.2)
        n1 = mx(r"1{,}90", ABSO, 44)
        d1 = val(r"0{,}020", r"\mathrm{g\cdot L^{-1}}", CONC, 44)
        calc_k = row(mx("k", KCOL, 44), mx("=", WHITE, 44), frac(n1, d1), buff=0.2).move_to(RIGHT * 1.4 + DOWN * 2.2)
        self.p(FadeOut(moy_note), FadeIn(calc_k[0:2]), FadeIn(calc_k[2][1]), rt=0.6)
        self.morph([(pt[2][1], n1), (pt[1][1], d1)], rt=1.5)
        self.at(232.3)
        res_k = val("95", r"\mathrm{L\cdot g^{-1}}", RES, 44)
        eg = mx("=", WHITE, 44)
        VGroup(eg, res_k).arrange(RIGHT, buff=0.2).next_to(calc_k, RIGHT, buff=0.25)
        self.p(Write(eg), Write(res_k), rt=1.2)

        self.at(234.0)
        u_t = tx("Unités :", 22, UNIT).move_to(LEFT * 5.2 + DOWN * 3.3)
        u_eq = row(tx("A (sans unité)", 22, ABSO), mx("=", WHITE, 34),
                   mx(r"\mathrm{L\cdot g^{-1}}", KCOL, 34), mx(r"\times", WHITE, 34),
                   mx(r"\mathrm{g\cdot L^{-1}}", CONC, 34)).next_to(u_t, RIGHT, buff=0.3)
        self.p(FadeIn(u_t), Write(u_eq), rt=1.5)
        self.at(238.5)
        tr_u = self.barrer(u_eq[2], u_eq[4], rt=1.0)
        self.p(Indicate(res_k[1], color=KCOL), rt=1.0)
        self.at(245.1)
        self.p(FadeOut(VGroup(u_t, u_eq, tr_u)), rt=0.5)
        self.reponse("Le coefficient de proportionnalité vaut k = 95 L·g⁻¹.", rt=1.4)

        # ---------------- QUESTION 5 ----------------
        self.at(246.9)
        self.vider(rt=0.4)
        self.set_q("Question 5")
        self.question("5) Calculer la valeur moyenne de l'absorbance de la solution S0.")
        vals5 = VGroup(*[mx(A_S0[i], ABSO, 30) for i in range(9)]).arrange(RIGHT, buff=0.45).move_to(UP * 1.5)
        idx5 = VGroup(*[mx(f"A_{i + 1}", GREY_B, 24).next_to(vals5[i], UP, buff=0.15) for i in range(9)])
        self.p(LaggedStart(*[FadeIn(VGroup(a, b)) for a, b in zip(idx5, vals5)], lag_ratio=0.1), rt=1.5)
        self.at(256.0)
        lit5 = row(mx(r"A_{moy}", ABSO, 44), mx("=", WHITE, 44),
                   frac(mx(r"A_1 + A_2 + \dots + A_9", ABSO, 44), mx("9", WHITE, 44)), buff=0.2).move_to(DOWN * 0.1)
        self.p(Write(lit5), rt=1.5)
        self.encadre(lit5)
        self.at(261.4)
        somme = VGroup()
        for i in range(9):
            somme.add(mx(A_S0[i], ABSO, 28))
            if i < 8:
                somme.add(mx("+", WHITE, 28))
        somme.arrange(RIGHT, buff=0.1)
        calc5 = row(mx(r"A_{moy}", ABSO, 32), mx("=", WHITE, 32), frac(somme, mx("9", WHITE, 32)), buff=0.15)
        calc5.scale_to_fit_width(min(calc5.width, 12.8)).move_to(DOWN * 1.9)
        self.p(FadeIn(calc5[0:2]), FadeIn(calc5[2][1:]), rt=0.4)
        self.morph([(vals5[i], somme[2 * i]) for i in range(9)],
                   *[FadeIn(somme[2 * i + 1]) for i in range(8)], rt=1.6)
        self.at(263.6)
        res5 = row(mx(r"A_{moy}", ABSO, 40), mx("=", WHITE, 40), frac(mx(r"13{,}846", ABSO, 40), mx("9", WHITE, 40)),
                   mx("=", WHITE, 40), mx(r"1{,}54", RES, 44), buff=0.2).move_to(calc5)
        self.p(ReplacementTransform(calc5[0], res5[0]), ReplacementTransform(calc5[1], res5[1]),
               ReplacementTransform(calc5[2], res5[2]), rt=1.2)
        self.p(Write(res5[3:]), rt=0.8)
        self.at(265.6)
        self.reponse("La valeur moyenne de l'absorbance de la solution S0 est Amoy = 1,54.", rt=1.4)

        # ---------------- QUESTION 6 – méthode 1 ----------------
        self.at(271.4)
        self.vider()
        self.set_q("Question 6")
        self.question("6) Déterminer la concentration massique Cm0 d'éosine dans la solution S0.")
        self.at(277.8)
        m1 = tx("Méthode 1 : lecture graphique", 28, ABSO).to_edge(RIGHT, buff=0.6).shift(UP * 1.6)
        self.p(Write(m1), rt=1.2)
        self.at(281.9)
        ax6, deco6, pts6, droite6 = self.graphe(x_len=7.5, y_len=4.2)
        VGroup(ax6, deco6, pts6, droite6).shift(DOWN * 0.45 + LEFT * 2.2)
        self.p(Create(ax6), FadeIn(deco6), FadeIn(pts6), rt=1.4)
        self.p(Create(droite6), rt=1.0)
        cm0 = 1.54 / 95
        self.at(287.5)
        a_lab6 = mx(r"1{,}54", ABSO, 30).next_to(ax6.c2p(0, 1.54), LEFT, buff=0.15)
        h_line = DashedLine(ax6.c2p(0, 1.54), ax6.c2p(cm0, 1.54), color=ABSO, stroke_width=3)
        self.p(FadeIn(a_lab6), rt=0.5)
        self.at(290.0)
        self.p(Create(h_line), rt=1.5)
        pt6 = Dot(ax6.c2p(cm0, 1.54), radius=0.09, color=CONC)
        self.p(GrowFromCenter(pt6), rt=0.5)
        self.at(294.6)
        v_line = DashedLine(ax6.c2p(cm0, 1.54), ax6.c2p(cm0, 0), color=CONC, stroke_width=3)
        self.p(Create(v_line), rt=1.4)
        self.at(296.6)
        lu = VGroup(row(mx(r"C_{m0} \approx", CONC, 36), val(r"0{,}016", r"\mathrm{g\cdot L^{-1}}", CONC, 36)),
                    row(mx(r"C_{m0} \approx", CONC, 36), val(r"1{,}6\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 36))
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(m1, DOWN, buff=0.6)
        self.p(Write(lu[0]), Indicate(v_line, color=CONC), rt=1.5)
        self.at(298.2)
        self.p(FadeIn(lu[1], shift=DOWN * 0.2), rt=1.0)

        # ---------------- QUESTION 6 – méthode 2 ----------------
        self.at(301.8)
        self.vider(garder=[self.cur_q])
        m2 = tx("Méthode 2 : relation de Beer-Lambert", 28, KCOL).move_to(UP * 1.8)
        self.p(Write(m2), rt=1.2)
        self.at(308.9)
        loi6 = row(mx("A", ABSO, 48), mx("=", WHITE, 48), mx("k", KCOL, 48), mx(r"\times", WHITE, 48), mx(r"C_{m0}", CONC, 48), buff=0.2).move_to(LEFT * 3.5 + UP * 0.6)
        self.p(Write(loi6), rt=1.2)
        self.at(311.6)
        lit6 = row(mx(r"C_{m0}", CONC, 48), mx("=", WHITE, 48), frac(mx(r"A_{moy}", ABSO, 48), mx("k", KCOL, 48)), buff=0.2).move_to(RIGHT * 2.8 + UP * 0.6)
        fl6 = Arrow(loi6.get_right(), lit6.get_left(), color=GREY_B, buff=0.3)
        self.morph([(loi6, lit6)], GrowArrow(fl6), rt=1.6)
        self.encadre(lit6)
        self.at(322.2)
        n6 = mx(r"1{,}54", ABSO, 44)
        d6 = val("95", r"\mathrm{L\cdot g^{-1}}", KCOL, 44)
        calc6 = row(mx(r"C_{m0}", CONC, 44), mx("=", WHITE, 44), frac(n6, d6), buff=0.2).move_to(LEFT * 3.0 + DOWN * 1.6)
        self.p(FadeIn(calc6[0:2]), FadeIn(calc6[2][1]), rt=0.5)
        self.morph([(lit6[2][0], n6), (lit6[2][2], d6)], rt=1.4)
        self.at(325.0)
        res6 = row(mx("=", WHITE, 44), val(r"1{,}62\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", RES, 44), buff=0.2).next_to(calc6, RIGHT, buff=0.25)
        self.p(Write(res6), rt=1.4)
        u6 = mx(r"\frac{1}{\mathrm{L\cdot g^{-1}}} = \mathrm{g\cdot L^{-1}}", UNIT, 30).next_to(res6, DOWN, buff=0.35)
        self.p(FadeIn(u6), rt=0.8)
        self.at(329.6)
        proche = tx("→ très proche de la lecture graphique (≈ 1,6×10⁻² g·L⁻¹)", 22, RES).next_to(calc6, DOWN, buff=0.9).align_to(calc6, LEFT)
        self.p(FadeIn(proche), rt=1.0)
        self.at(331.4)
        self.reponse("La concentration massique d'éosine dans S0 est Cm0 = 1,62×10⁻² g·L⁻¹.", rt=1.5)
        self.at(337.0)
        deux = tx("À savoir faire : les DEUX méthodes", 24, ABSO).move_to(DOWN * 2.15 + RIGHT * 3.3)
        self.p(FadeOut(proche), FadeIn(deux, scale=1.2), rt=1.0)

        # ---------------- QUESTION 9 – pourcentage massique ----------------
        self.at(343.7)
        self.vider()
        self.set_q("Question 9")
        q9 = self.question("9) En déduire le pourcentage massique d'éosine dans la dosette. Détailler la démarche.")
        self.at(349.7)
        self.p(Indicate(q9, color=ABSO, scale_factor=1.05), rt=1.2)

        self.at(355.9)
        dosA = VGroup(RoundedRectangle(width=0.4, height=0.9, corner_radius=0.1, color=WHITE, fill_color=MAGENTA, fill_opacity=0.9))
        dosA.add(mx(r"V_{dos} = 2{,}00\ \mathrm{mL}", VOL, 24).next_to(dosA[0], DOWN, buff=0.12))
        dosA.add(mx(r"C_{m,dos} = \ ?", CONC, 26).next_to(dosA[1], DOWN, buff=0.1))
        fA = fiole(r"V_{fiole} = 1{,}00\ \mathrm{L}", 0.45, 0.5)
        fA.add(mx(r"C_{m1} = \ ?", CONC, 26).next_to(fA[3], DOWN, buff=0.1))
        fB = fiole(r"V_0 = 25{,}0\ \mathrm{mL}", 0.2, 0.36)
        fB.add(mx(r"C_{m0} = 1{,}62\times10^{-2}\ \mathrm{g\cdot L^{-1}}", CONC, 24).next_to(fB[3], DOWN, buff=0.1))
        sch = VGroup(dosA, fA, fB).arrange(RIGHT, buff=2.3).move_to(DOWN * 0.3)
        a1 = Arrow(dosA[0].get_right(), fA[0].get_left() + UP * 0.2, color=GREY_B, buff=0.2)
        a2 = Arrow(fA[0].get_right() + UP * 0.2, fB[0].get_left() + UP * 0.2, color=GREY_B, buff=0.2)
        a2l = mx(r"V = 10{,}0\ \mathrm{mL}", VOL, 24).next_to(a2, UP, buff=0.1)
        a1l = tx("dilution 1", 18, GREY_B).next_to(a1, UP, buff=0.1)
        sB = tx("S0", 24, CONC).next_to(fB[1], RIGHT, buff=0.2)
        self.p(FadeIn(dosA), rt=0.7)
        self.p(GrowArrow(a1), FadeIn(a1l), FadeIn(fA), rt=1.0)
        self.p(GrowArrow(a2), FadeIn(a2l), FadeIn(fB), FadeIn(sB), rt=1.0)
        self.at(370.1)
        r1 = CurvedArrow(fB[0].get_top() + UP * 1.1, fA[0].get_top() + UP * 1.1, color=ABSO, angle=TAU / 6)
        r2 = CurvedArrow(fA[0].get_top() + UP * 1.1, dosA[0].get_top() + UP * 0.5, color=ABSO, angle=TAU / 6)
        rem = tx("on remonte étape par étape", 22, ABSO).next_to(r1, UP, buff=0.1).shift(LEFT * 2)
        self.p(Create(r1), FadeIn(rem), rt=1.2)
        self.p(Create(r2), rt=1.0)

        # étape 1
        self.at(373.9)
        sch_all = VGroup(dosA, fA, fB, a1, a2, a1l, a2l, sB)
        self.p(FadeOut(r1), FadeOut(r2), FadeOut(rem), sch_all.animate.scale(0.62).to_edge(UP, buff=1.45), rt=1.2)
        et1 = tx("Étape 1 : solution de la fiole de 1,00 L", 26, ABSO).next_to(sch_all, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.p(FadeIn(et1), Circumscribe(VGroup(fA, fB), color=ABSO), rt=1.5)
        self.at(384.8)
        cons = tx("Dilution : la masse de soluté se conserve", 24, WHITE).next_to(et1, DOWN, buff=0.25).align_to(et1, LEFT)
        self.p(FadeIn(cons, shift=RIGHT * 0.2), rt=1.0)
        self.at(395.9)
        sC1 = mx("C_{m1}", CONC, 46)
        sV = mx("V", VOL, 46)
        sC0 = mx("C_{m0}", CONC, 46)
        sV0 = mx("V_0", VOL, 46)
        cons_eq = row(sC1, mx(r"\times", WHITE, 46), sV, mx("=", WHITE, 46), sC0, mx(r"\times", WHITE, 46), sV0, buff=0.18)
        cons_eq.next_to(cons, DOWN, buff=0.35).align_to(cons, LEFT).shift(RIGHT * 0.4)
        self.p(Write(cons_eq[0:3]), rt=1.2)
        self.at(402.0)
        self.p(Indicate(sV, color=VOL), Indicate(a2l, color=VOL), rt=1.0)
        self.at(406.0)
        self.p(Write(cons_eq[3:]), rt=1.5)
        self.at(414.0)
        self.p(Indicate(sV0, color=VOL), Indicate(fB[3], color=VOL), rt=1.0)
        self.at(419.3)
        lit9a = row(mx("C_{m1}", CONC, 46), mx("=", WHITE, 46),
                    frac(row(mx("C_{m0}", CONC, 46), mx(r"\times", WHITE, 46), mx("V_0", VOL, 46), buff=0.12), mx("V", VOL, 46)), buff=0.2)
        lit9a.next_to(cons_eq, RIGHT, buff=1.0)
        self.morph([(cons_eq, lit9a)], rt=1.5)
        self.encadre(lit9a, rt=1.0)
        self.at(423.0)
        nC0 = val(r"1{,}62\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 38)
        nV0 = val(r"25{,}0", r"\mathrm{mL}", VOL, 38)
        dV = val(r"10{,}0", r"\mathrm{mL}", VOL, 38)
        numA = row(nC0, mx(r"\times", WHITE, 38), nV0, buff=0.12)
        calc9a = row(mx("C_{m1}", CONC, 38), mx("=", WHITE, 38), frac(numA, dV), mx("=", WHITE, 38),
                     val(r"4{,}05\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", RES, 38), buff=0.18)
        calc9a.to_edge(DOWN, buff=0.5)
        self.p(FadeIn(calc9a[0:2]), FadeIn(calc9a[2][1]), rt=0.5)
        self.morph([(lit9a[2][0][0], nC0), (lit9a[2][0][2], nV0), (lit9a[2][2], dV)], FadeIn(numA[1]), rt=1.4)
        self.barrer(nV0[1], dV[1])
        self.p(Write(calc9a[3:]), rt=1.0)

        self.at(427.7)
        att = tx("Attention : ce n'est pas encore la dosette : la fiole de 1,00 L vient elle-même d'une dilution !", 22, RED)
        att.next_to(calc9a, UP, buff=0.35)
        self.p(FadeIn(att, shift=UP * 0.2), Circumscribe(dosA, color=RED), rt=1.5)
        self.at(436.0)
        self.p(Indicate(a1, color=RED), rt=1.0)

        # étape 2
        self.at(442.6)
        garde = [sch_all, calc9a]
        self.vider(garder=garde + [self.cur_q])
        self.p(calc9a.animate.scale(0.75).next_to(sch_all, DOWN, buff=0.25), rt=0.8)
        et2 = tx("Étape 2 : même démarche pour la dosette", 26, ABSO).next_to(calc9a, DOWN, buff=0.3).to_edge(LEFT, buff=0.6)
        self.p(FadeIn(et2), Circumscribe(VGroup(dosA, fA), color=ABSO), rt=1.4)
        cons2 = row(mx(r"C_{m,dos}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{dos}", VOL, 42), mx("=", WHITE, 42),
                    mx("C_{m1}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{fiole}", VOL, 42), buff=0.16)
        cons2.next_to(et2, DOWN, buff=0.35).align_to(et2, LEFT).shift(RIGHT * 0.3)
        self.p(Write(cons2), rt=1.6)
        self.at(447.0)
        lit9b = row(mx(r"C_{m,dos}", CONC, 42), mx("=", WHITE, 42),
                    frac(row(mx("C_{m1}", CONC, 42), mx(r"\times", WHITE, 42), mx(r"V_{fiole}", VOL, 42), buff=0.12), mx(r"V_{dos}", VOL, 42)), buff=0.2)
        lit9b.next_to(cons2, RIGHT, buff=0.8)
        self.morph([(cons2, lit9b)], rt=1.2)
        self.encadre(lit9b, rt=0.8)
        self.at(448.8)
        conv = mx(r"V_{fiole} = 1{,}00\ \mathrm{L} = 1000\ \mathrm{mL}", VOL, 30).next_to(cons2, DOWN, buff=0.3).align_to(cons2, LEFT)
        self.p(FadeIn(conv), rt=0.7)
        nC1 = val(r"4{,}05\times10^{-2}", r"\mathrm{g\cdot L^{-1}}", CONC, 38)
        nVf = val(r"1000", r"\mathrm{mL}", VOL, 38)
        dVd = val(r"2{,}00", r"\mathrm{mL}", VOL, 38)
        numB = row(nC1, mx(r"\times", WHITE, 38), nVf, buff=0.12)
        calc9b = row(mx(r"C_{m,dos}", CONC, 38), mx("=", WHITE, 38), frac(numB, dVd), mx("=", WHITE, 38),
                     val(r"20{,}2", r"\mathrm{g\cdot L^{-1}}", RES, 38), buff=0.18).to_edge(DOWN, buff=0.45)
        self.p(FadeIn(calc9b[0:2]), FadeIn(calc9b[2][1]), rt=0.4)
        self.morph([(lit9b[2][0][0], nC1), (lit9b[2][0][2], nVf), (lit9b[2][2], dVd)], FadeIn(numB[1]), rt=1.3)
        self.barrer(nVf[1], dVd[1], rt=0.5)
        self.at(451.7)
        self.p(Write(calc9b[3:]), rt=1.0)
        self.p(Circumscribe(calc9b[4], color=RES), rt=1.0)

        # étape 3
        self.at(459.1)
        self.vider(garder=[self.cur_q])
        et3 = tx("Étape 3 : pourcentage massique", 26, ABSO).to_edge(LEFT, buff=0.6).shift(UP * 1.85)
        self.p(FadeIn(et3), rt=0.8)
        defP = row(mx("P", WHITE, 44), mx("=", WHITE, 44), frac(mx(r"m_{\text{éosine}}", MASSE, 44), mx(r"m_{\text{solution}}", MASSE, 44)),
                   mx(r"\times 100", WHITE, 44), buff=0.2).next_to(et3, RIGHT, buff=0.8)
        self.p(Write(defP), rt=1.6)
        self.at(466.0)
        self.p(Indicate(defP[2][0], color=MASSE), rt=0.8)
        self.p(Indicate(defP[2][2], color=MASSE), rt=0.8)

        self.at(472.1)
        dans = tx("Dans V = 1,00 L de solution pharmaceutique :", 24, WHITE).to_edge(LEFT, buff=0.6).shift(UP * 0.4)
        self.p(FadeIn(dans), rt=0.8)
        lit_me = row(mx(r"m_{\text{éosine}}", MASSE, 38), mx("=", WHITE, 38), mx(r"C_{m,dos}", CONC, 38), mx(r"\times", WHITE, 38), mx("V", VOL, 38), buff=0.15)
        lit_me.next_to(dans, DOWN, buff=0.35).align_to(dans, LEFT)
        box_me = SurroundingRectangle(lit_me, color=BOX, buff=0.15, stroke_width=3)
        self.at(474.5)
        self.p(Write(lit_me), Create(box_me), rt=1.2)
        u_me = val(r"20{,}2", (r"\mathrm{g}", r"\cdot\mathrm{L^{-1}}"), CONC, 38)
        u_V = val(r"1{,}00", r"\mathrm{L}", VOL, 38)
        calc_me = row(mx("=", WHITE, 38), u_me, mx(r"\times", WHITE, 38), u_V, mx("=", WHITE, 38),
                      val(r"20{,}2", r"\mathrm{g}", RES, 38), buff=0.15).next_to(box_me, RIGHT, buff=0.3)
        self.at(478.0)
        self.p(FadeIn(calc_me), rt=1.0)
        tr_me = self.barrer(u_me[1][1], u_V[1])
        self.at(486.3)
        lit_ms = row(mx(r"m_{\text{solution}}", MASSE, 38), mx("=", WHITE, 38), mx(r"\rho", RHO, 38), mx(r"\times", WHITE, 38), mx("V", VOL, 38), buff=0.15)
        lit_ms.next_to(lit_me, DOWN, buff=0.55).align_to(lit_me, LEFT)
        box_ms = SurroundingRectangle(lit_ms, color=BOX, buff=0.15, stroke_width=3)
        self.p(Write(lit_ms), Create(box_ms), rt=1.2)
        self.at(489.0)
        u_r = val(r"1{,}02", (r"\mathrm{g}", r"\cdot\mathrm{mL^{-1}}"), RHO, 38)
        u_V2 = val(r"1000", r"\mathrm{mL}", VOL, 38)
        calc_ms = row(mx("=", WHITE, 38), u_r, mx(r"\times", WHITE, 38), u_V2, mx("=", WHITE, 38),
                      val(r"1020", r"\mathrm{g}", RES, 38), buff=0.15).next_to(box_ms, RIGHT, buff=0.3)
        conv2 = mx(r"(V = 1{,}00\ \mathrm{L} = 1000\ \mathrm{mL})", VOL, 26).next_to(calc_ms, DOWN, buff=0.15).align_to(calc_ms, LEFT)
        self.p(FadeIn(calc_ms), FadeIn(conv2), rt=1.2)
        tr_ms = self.barrer(u_r[1][1], u_V2[1])

        self.at(493.9)
        self.encadre(defP, rt=1.0)
        self.at(500.0)
        cent = tx("× 100 ⇒ résultat en % (sans × 100 : valeur entre 0 et 1, sans « % » !)", 20, GREY_B).next_to(defP, DOWN, buff=0.25).align_to(defP, LEFT).shift(LEFT * 0.5)
        self.p(FadeIn(cent), Indicate(defP[3], color=ABSO), rt=1.4)
        self.at(506.5)
        self.p(FadeOut(cent), rt=0.5)

        self.at(508.8)
        pn = val(r"20{,}2", r"\mathrm{g}", MASSE, 40)
        pd = val(r"1020", r"\mathrm{g}", MASSE, 40)
        calcP = row(mx("P", WHITE, 40), mx("=", WHITE, 40), frac(pn, pd), mx(r"\times 100", WHITE, 40), mx("=", WHITE, 40),
                    mx(r"1{,}98\ \%", RES, 44), buff=0.18).move_to(DOWN * 2.45)
        self.p(FadeIn(calcP[0:2]), FadeIn(calcP[2][1]), FadeIn(calcP[3]), rt=0.5)
        self.morph([(calc_me[5], pn), (calc_ms[5], pd)], rt=1.3)
        tr_p = self.barrer(pn[1], pd[1], rt=0.5)
        self.p(Write(calcP[4:]), rt=1.0)
        self.at(513.2)
        self.p(FadeOut(VGroup(dans, lit_me, box_me, calc_me, lit_ms, box_ms, calc_ms, conv2, tr_me, tr_ms)),
               VGroup(calcP, tr_p).animate.move_to(DOWN * 0.4), rt=0.8)
        self.at(514.0)
        self.reponse("Le pourcentage massique d'éosine dans la dosette commerciale est P = 1,98 % :\n"
                     "1,98 % de la masse de la solution est de l'éosine.", rt=2.0)

        # ---------------- QUESTION 10 ----------------
        self.at(522.2)
        self.vider()
        self.set_q("Question 10")
        self.question("10) Ce résultat est-il cohérent avec les informations de l'énoncé ?")
        self.at(525.0)
        donnees = VGroup(row(mx(r"P_{exp} = 1{,}98\ \%", RES, 38)), row(mx(r"P_{ref} = 2{,}0\ \%", ABSO, 38)),
                         tx("(étiquette : 2,0 % en masse)", 20, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        donnees.to_edge(LEFT, buff=0.8).shift(UP * 0.9)
        self.p(FadeIn(donnees, shift=RIGHT * 0.2), rt=1.0)
        self.at(528.8)
        lit10 = row(mx("e", WHITE, 46), mx("=", WHITE, 46),
                    frac(mx(r"\left| P_{exp} - P_{ref} \right|", WHITE, 46), mx(r"P_{ref}", ABSO, 46)), mx(r"\times 100", WHITE, 46), buff=0.2)
        lit10.move_to(RIGHT * 2.6 + UP * 0.9)
        self.p(Write(lit10), rt=1.8)
        self.encadre(lit10, rt=1.0)
        self.at(540.7)
        calc10 = row(mx("e", WHITE, 42), mx("=", WHITE, 42), frac(mx(r"\left| 1{,}98 - 2{,}0 \right|", WHITE, 42), mx(r"2{,}0", ABSO, 42)),
                     mx(r"\times 100", WHITE, 42), mx("=", WHITE, 42), mx(r"1\ \%", RES, 46), buff=0.18).move_to(DOWN * 1.3)
        self.p(Write(calc10[:4]), rt=1.5)
        self.p(Write(calc10[4:]), rt=0.8)
        self.at(543.9)
        self.reponse("L'écart relatif n'est que de 1 % : le résultat est cohérent avec l'étiquette (2,0 % en masse).", rt=1.8)
        self.at(546.5)
        self.p(Circumscribe(calc10[5], color=RES), rt=1.2)

        self.at(551.0)
        self.vider(rt=1.0)
        fin = tx("Fin de la correction", 40, WHITE)
        self.p(FadeIn(fin), rt=1.0)
        self.wait(1.5)
