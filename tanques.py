class Tank:
    def __init__(self, nombre, color, n_minas, n_parabolico, posicion):
        self.ins = None
        self.nombre = nombre
        self.color = color
        self.n_minas = n_minas
        self.n_parabolico = n_parabolico
        self.vida = 100
        self.aun_vivo = True
        self.posicion = posicion
        self.dx = 0
        self.colisiono = False
        self.mina_colisionada = 5

    def set_dx(self, dx):
        self.dx = dx

    def reducir_vida(self, danio):
        self.vida -= danio
        if self.vida > 0:
            self.aun_vivo = True
        else:
            self.vida = 0
            self.aun_vivo = False

    def estoy_vivo(self):
        return self.aun_vivo

    def get_y(self):
        return self.posicion[1]

    def get_x(self):
        return self.posicion[0]

    def set_ins(self, ins):
        self.ins = ins

    def get_tam_ins(self):
        return len(self.ins)

    def get_ins(self):
        return self.ins