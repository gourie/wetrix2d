from vpython import *

# config
PROEFBUIS_LENGTE = 5
PROEFBUIS_MAXLEVEL = 10

class Wetrix(object):

    def __init__(self, title = "Wetrix2d", width=1200, height=600, bg_color=color.black):
        self.scene = canvas(title=title, width=width, height=height,
                            center=vector(0, 0, 0) + vector(width, height, 0) / 2.0, background=bg_color)
        self.box_eenheid = 10
        self.bodem_hoogtes = [0] * int(self.scene.width / self.box_eenheid)
        self.water_niveaus = [0] * int(self.scene.width / self.box_eenheid)
        self.blokken = []
        self.proefbuis = Proefbuis(PROEFBUIS_MAXLEVEL)

    def toon_start_scherm(self):
        # bodem
        for i in range(len(self.bodem_hoogtes)):
            box(pos=vector(i * self.box_eenheid, 0, 0), length=self.box_eenheid, height=self.box_eenheid, width=1,
                color=color.gray(0.5))
        self.bodem_hoogtes = [1] * len(self.bodem_hoogtes)

        # proefbuis
        for i in range(PROEFBUIS_LENGTE):
            box(pos=vector(i * self.box_eenheid, self.scene.height, 0), length=self.box_eenheid, height=self.box_eenheid, width=1,
                color=color.orange)

        # start-blok > alpha (just show one unit)
        self.toon_blok(Blok(color.blue, [(self.scene.width / 2.0, self.scene.height)]))

    def toon_blok(self, blok_object):
        for pos in blok_object.posities:
            box(pos=vector(pos[0], pos[1], 0), length=self.box_eenheid, height=self.box_eenheid,
                width=1, color=blok_object.kleur)
        self.blokken.append(blok_object)


class Proefbuis(object):

    def __init__(self, max_level):
        self.max_level = max_level
        self.current_level = 0


class Blok(object):

    def __init__(self, kleur, posities_list):
        self.kleur = kleur
        self.posities = posities_list
        self.aantal_eenheden = len(self.posities)


class Upper(Blok):

    def __init__(self, kleur='green'):
        Blok.__init__(self, kleur)


class Downer(Blok):

    def __init__(self, kleur='red'):
        Blok.__init__(self, kleur)


class Water(Blok):

    def __init__(self, kleur='blue'):
        Blok.__init__(self, kleur)


class Vuur(Blok):

    def __init__(self, kleur='yellow'):
        Blok.__init__(self, kleur)



wetrix2d = Wetrix()
wetrix2d.toon_start_scherm()