import numpy as np
from vpython import *
import random

# config
PROEFBUIS_LENGTE = 5
PROEFBUIS_MAXLEVEL = 10


class Wetrix2D(object):

    def __init__(self, title="Wetrix2d", width=1200, height=600, bg_color=color.black):
        self.scene = canvas(title=title, width=width, height=height,
                            center=vector(0, 0, 0) + vector(width, height, 0) / 2.0, background=bg_color)
        self.box_eenheid = 10
        self.bodem_hoogtes = [0] * int(self.scene.width / self.box_eenheid)
        self.water_niveaus = [0] * int(self.scene.width / self.box_eenheid)
        self.blokken = [L1upper(), L1downer(), L2upper(), L2downer()]
        self.proefbuis = Proefbuis(PROEFBUIS_MAXLEVEL)
        self.snelheid_in_eenheden_per_seconde = 5
        self.key_shift = 0

    def main_loop(self):

        self.toon_start_scherm()

        # initialize startblok
        start_blok = self.random_kies_blok()
        box_list = self.toon_blok(start_blok, (self.scene.width / 2, self.scene.height))

        # initializeer positioneringsblok
        positionerings_blok = BalkPlat(kleur=color.yellow, breedte=start_blok.breedte, hoogte=1)
        box_list_positionerings_blok = self.toon_blok(positionerings_blok, (np.min([box_i.pos.x for box_i in box_list]), -1 * self.box_eenheid))

        self.scene.bind('keydown', self.key_input)

        while not self.proefbuis.is_vol():
            rate(self.snelheid_in_eenheden_per_seconde)

            # beweeg startblok naar beneden
            for box_item in box_list:
                box_item.pos = box_item.pos - vector(self.key_shift * self.box_eenheid, self.box_eenheid, 0)
            for box_item_pos_blok in box_list_positionerings_blok:
                box_item_pos_blok.pos = box_item_pos_blok.pos - vector(self.key_shift * self.box_eenheid, 0, 0)
            blok_raakt_bodem_list = self.blok_raakt_bodem(box_list)
            if len(blok_raakt_bodem_list) != 0:
                # update bodemhoogtes
                for x_pos in blok_raakt_bodem_list:
                    self.bodem_hoogtes[int(x_pos[0] / self.box_eenheid)] += int(start_blok.hoogtes_voor_elke_x_pos[x_pos[1]])
                # plaats nieuw startblok
                start_blok = self.random_kies_blok()
                box_list = self.toon_blok(start_blok, (self.scene.width / 2, self.scene.height))
                for box_item_pos_blok in box_list_positionerings_blok:
                    box_item_pos_blok.visible = False
                    del box_item_pos_blok
                positionerings_blok = BalkPlat(kleur=color.yellow, breedte=start_blok.breedte, hoogte=1)
                box_list_positionerings_blok = self.toon_blok(positionerings_blok, (
                np.min([box_i.pos.x for box_i in box_list]), -1 * self.box_eenheid))

            self.key_shift = 0

    def key_input(self, evt):
        if evt.key == "right":
            self.key_shift = -1
            print("right key clicked")
        elif evt.key == "left":
            self.key_shift = 1
            print("left key clicked")

    def blok_raakt_bodem(self, blok_box_list):
        res = []
        for index, box_item in enumerate(blok_box_list):
            if box_item.pos.y / self.box_eenheid == self.bodem_hoogtes[int(box_item.pos.x / self.box_eenheid)]:
                res.append((box_item.pos.x, index))
        return res

    def toon_start_scherm(self):
        # bodem
        for i in range(len(self.bodem_hoogtes)):
            box(pos=vector(i * self.box_eenheid, 0, 0), length=self.box_eenheid, height=self.box_eenheid, width=1,
                    color=color.gray(0.5))
        self.bodem_hoogtes = [1] * len(self.bodem_hoogtes)

        # proefbuis
        for i in range(PROEFBUIS_LENGTE):
            box(pos=vector(i * self.box_eenheid, self.scene.height, 0), length=self.box_eenheid,
                height=self.box_eenheid, width=1,
                color=color.white)

    def toon_blok(self, blok_object, scherm_positie):
        # assert 0 <= scherm_positie[0] <= self.scene.width and -1 <= scherm_positie[1] <= self.scene.height
        x_shift, y_shift = self.bereken_verplaatsing(scherm_positie, blok_object)
        box_list = []
        for pos in blok_object.posities:
            box_list.append(box(pos=vector(pos[0] * self.box_eenheid + scherm_positie[0] - x_shift,
                                           pos[1] * self.box_eenheid + scherm_positie[1] - y_shift, 0),
                                length=self.box_eenheid, height=self.box_eenheid, width=1, color=blok_object.kleur))
        blok_object.print_name()
        return box_list

    def toon_positioneringshulp(self, vallende_blok_box_list):
        pass

    def random_kies_blok(self):
        return random.choice(self.blokken)

    def bereken_verplaatsing(self, scherm_positie, blok_object):
        return max((scherm_positie[0] + blok_object.breedte * self.box_eenheid) - self.scene.width, 0), max(
            (scherm_positie[1] + blok_object.hoogte * self.box_eenheid) - self.scene.height, 0)


class Proefbuis(object):

    def __init__(self, max_level):
        self.max_level = max_level
        self._current_level = 0

    def is_vol(self):
        return self._current_level >= self.max_level

    @property
    def current_level(self):
        return self._current_level

    # @current_level.setter
    # def current_level(self, value):
    #     assert isinstance(value, int)
    #     self._current_level = value

    def update_current_level(self, incremental_value):
        assert isinstance(incremental_value, int) and incremental_value > 0
        self._current_level += incremental_value


class Blok(object):
    """ Blok met gegeven kleur, breedte, hoogte en dikte

    - posities: list, relatieve posities van de bouwblokjes (vierkantjes)
    """

    def __init__(self, kleur, breedte, hoogte, dikte=1):
        self.posities = None
        self.kleur = kleur
        self.breedte = breedte
        self.hoogte = hoogte
        self.dikte = dikte
        self.hoogtes_voor_elke_x_pos = None

    def bereken_hoogtes_voor_elke_x_pos(self):
        self.hoogtes_voor_elke_x_pos = [np.sum(np.array(self.posities)[..., 0] == x_pos) for x_pos in
                                        np.unique(np.array(self.posities)[..., 0])]

    def print_name(self):
        return self._print_name()


class BalkPlat(Blok):
    """
    Platte balk
    """

    def __init__(self, kleur, breedte=3, hoogte=1):
        Blok.__init__(self, kleur, breedte, hoogte)
        self.posities = []
        self.posities.extend([(i, j) for i in range(breedte) for j in range(self.dikte)])
        self.posities.extend([(i, j) for i in range(self.dikte) for j in range(self.dikte, hoogte)])
        self.bereken_hoogtes_voor_elke_x_pos()

    def _print_name(self):
        print("Platte balk")


class L1(Blok):
    """
    Letter L rechtopstaand
    """

    def __init__(self, kleur, breedte=3, hoogte=5):
        Blok.__init__(self, kleur, breedte, hoogte)
        self.posities = []
        self.posities.extend([(i, j) for i in range(breedte) for j in range(self.dikte)])
        self.posities.extend([(i, j) for i in range(self.dikte) for j in range(self.dikte, hoogte)])
        self.bereken_hoogtes_voor_elke_x_pos()

    def _print_name(self):
        print("Letter L rechtopstaand")


class L1upper(L1):
    """
    Letter L rechtopstaand, upper = groen
    """

    def __init__(self, kleur=color.green):
        L1.__init__(self, kleur)


class L1downer(L1):
    """
    Letter L rechtopstaand, downer = rood
    """

    def __init__(self, kleur=color.red):
        L1.__init__(self, kleur)


class L2(Blok):
    """
    Letter L omgevallen naar links
    """

    def __init__(self, kleur, breedte=3, hoogte=5):
        Blok.__init__(self, kleur, hoogte, breedte)
        self.posities = []
        self.posities.extend([(i, j) for i in range(hoogte) for j in range(self.dikte)])
        self.posities.extend([(i, j) for i in range(hoogte - self.dikte, hoogte) for j in range(self.dikte, breedte)])
        self.bereken_hoogtes_voor_elke_x_pos()

    def _print_name(self):
        print("Letter L omgevallen naar links")


class L2upper(L2):
    """
    Letter L omgevallen naar links, upper = groen
    """

    def __init__(self, kleur=color.green):
        L2.__init__(self, kleur)


class L2downer(L2):
    """
    Letter L omgevallen naar links, downer = rood
    """

    def __init__(self, kleur=color.red):
        L2.__init__(self, kleur)


# class Blok(object):
#
#     def __init__(self, kleur, posities_list):
#         self.kleur = kleur
#         self.posities = posities_list
#         self.aantal_eenheden = len(self.posities)
#
#
# class Upper(Blok):
#
#     def __init__(self, kleur='green'):
#         Blok.__init__(self, kleur)
#
#
# class Downer(Blok):
#
#     def __init__(self, kleur='red'):
#         Blok.__init__(self, kleur)
#
#
# class Water(Blok):
#
#     def __init__(self, kleur='blue'):
#         Blok.__init__(self, kleur)
#
#
# class Vuur(Blok):
#
#     def __init__(self, kleur='yellow'):
#         Blok.__init__(self, kleur)


wetrix2d = Wetrix2D()
wetrix2d.main_loop()