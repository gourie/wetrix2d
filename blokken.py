class Blok(object):

    def __init__(self, color, positions_list):
        self.kleur = color
        self.posities = positions_list
        self.aantal_eenheden = len(self.posities)

class Bodem(Blok):

    def __init__(self, color='grey'):
        Blok.__init__(self, color)

class Proefbuis(Blok):

    def __init__(self, max_level, color='white'):
        Blok.__init__(self, color)
        self.max_level = max_level
        self.current_level = 0

class Upper(Blok):

    def __init__(self, color='green'):
        Blok.__init__(self, color)

class Downer(Blok):

    def __init__(self, color='red'):
        Blok.__init__(self, color)

class Water(Blok):

    def __init__(self, color='blue'):
        Blok.__init__(self, color)

class Vuur(Blok):

    def __init__(self, color='yellow'):
        Blok.__init__(self, color)