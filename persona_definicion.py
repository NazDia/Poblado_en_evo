import rng
from biseccion_de_prob_condicional import bisection, probabilidad_cond_secuencial

random = rng.SubtractiveRNG()

lambda_prob = lambda x : probabilidad_cond_secuencial(x, 12)

tabla_de_fallecimiento_1 = {12 : 0.25, 45 : 0.1, 76 : 0.3, 125 : 0.7}

# Un aproximado de la probabilidad por mes asumiendo que la probabilidad
# de la tabla anterior sea por año
tabla_de_fallecimiento_2 = { x : bisection(0, 1, tabla_de_fallecimiento_1[x], lambda_prob)[0] for x in tabla_de_fallecimiento_1.keys()}

tabla_de_fallecimiento_1_f = {12: 0.25, 45 : 0.15, 76 : 0.35, 125 : 0.65}
tabla_de_fallecimiento_2_f = { x : bisection(0, 1, tabla_de_fallecimiento_1_f[x], lambda_prob)[0] for x in tabla_de_fallecimiento_1_f.keys()}

probabilidad_de_separacion_1 = 0.2

# Un aproximado de la probabilidad por mes asumiendo que la probabilidad
# de separacion sea por año
probabilidad_de_separacion_2 = bisection(0, 1, probabilidad_de_separacion_1, lambda_prob)[0]

tabla_lambdas_luto = { 15 : 1 / 3, 35 : 1 / 6, 45 : 1 / 12, 60 : 1 / 24, 125 : 1 / 48}
tabla_de_prob_embarazo = { 12 : 0, 15 : 0.2, 21 : 0.45, 35 : 0.8, 45 : 0.4, 60 : 0.2, 125 : 0.05}
tabla_querer_pareja = { 12 : 0, 15 : 0.6, 21 : 0.65, 35 : 0.8, 45 : 0.6, 60 : 0.5, 125 : 0.2}
tabla_establecer_pareja = { 5 : 0.45, 10 : 0.4, 15 : 0.35, 20 : 0.25, 125 : 0.15}
tabla_de_hijos_deseados = [0.6, 0.75, 0.35, 0.2, 0.1, 0.05]
tabla_de_numero_de_hijos = [0.7, 0.86, 0.94, 0.98, 1]           # En este caso se suman para mayor facilidad de revision de los numeros aleatorios


def r_check(value, table, default=False):
    for i in table.keys():
        if value < i:
            return random.random() <= table[i]

    else:
        return default

class Persona:
    def __init__(self, edad=0, sexo=-1, pareja=None, madre=None, padre=None):
        self.edad = edad                                            # La edad se representara en meses, para saber 
                                                                    # la edad en años se divide entre 12
        self.sexo = random.randint(0, 1) if sexo == -1 else sexo    # 0 -> Mujer, 1 -> Hombre
        self.pareja = None                                          # Referencia al objeto Persona que representa su pareja
        self.tiempo_en_luto_restante = 0                            # Tiempo de espera restante tras la separacion o muerte de su anterior pareja
                                                                    # Es -1 si no esta de luto
        self.tiempo_para_dar_luz = 0                                # Tiempo que falta para que de a luz
                                                                    # Es -1 si no esta embarazada
        self.hijos_deseados = self.hallar_hijos_deseados()
        self.madre = madre
        self.padre = padre
        self.hijos = []
        self.indice_social = random.random()
        self.conocidos = [madre, padre]
        self.conocidos = [x for x in self.conocidos if not x is None]
        self.muerto = False


    def envejece(self):
        ret = []
        self.edad += 1                             # Aumenta la edad, en la simulacion todos envececeran a la vez
        if self.tiempo_en_luto_restante > 0:       # Revision para modificacion de parametros si esta en luto
            self.tiempo_en_luto_restante -= 1

        if self.tiempo_para_dar_luz > 0:           # Revision para modificacion de parametros si esta embarazada
            self.tiempo_para_dar_luz -= 1
            if self.tiempo_para_dar_luz == 0:
                ret = self.da_a_luz()

        edad = self.edad / 12
        for i in tabla_de_fallecimiento_2.keys():
            if edad < i:
                prob = tabla_de_fallecimiento_2[i]
                break

        else:
            self.muere()
            return []

        if random.random() < prob:
            self.muere()
            return []

        if not self.pareja is None and random.random() <= probabilidad_de_separacion_2:
            self.separacion()

        if not self.pareja is None and r_check(self.edad / 12, tabla_de_prob_embarazo):
            self.embarazarse()

        return ret

    def hallar_luto(self):
        edad = self.edad / 12
        for key in tabla_lambdas_luto.keys():
            if edad < key:
                self.tiempo_en_luto_restante = random.exp_random(tabla_lambdas_luto[key])
                return


    def muere(self):
        self.muerto = True
        # Se eliminan de todas las referencias posibles para
        # que el recolector de basura lo elimine eventualmente
        # y que la memoria no se sobrecargue con datos que no se
        # usaran mas.
        if not self.pareja is None:
            self.pareja.hallar_luto()
            self.pareja.pareja = None               # Se modifica el estado de su pareja
            

        # Se elimina la referencia en ambos padres
        # si no fueron borrados (murieron) ya
        if not self.padre is None:
            try:
                self.padre.hijos.remove(self)
            except:
                pass
        
        if not self.madre is None:
            try:
                self.madre.hijos.remove(self)
            except:
                pass


        # Se elimina la referencia en los hijos y en los conocidos
        for i in self.hijos:
            if self.sexo == 0:
                i.madre = None

            else:
                i.padre = None

        for i in self.conocidos:
            try:
                i.conocidos.remove(self)
            except:
                pass

    #
    # Ser pareja es una relacion simetrica
    #
    def empareja(self, x):
        self.pareja = x
        x.pareja = self
        return True

    def separacion(self):
        self.pareja.pareja = None
        self.pareja = None
        self.hallar_luto()

    def da_a_luz(self):
        rand = random.random()
        for i in range(len(tabla_de_numero_de_hijos)):
            if rand < tabla_de_numero_de_hijos[i]:
                hijos = i + 1

        ret = [Persona() for i in range(hijos)] # Se crea cada persona nueva con sexo distribuyendo uniformemente (ver constructor de la clase)
        self.hijos += ret
        return ret

    def hallar_hijos_deseados(self):
        for i in range(len(tabla_de_hijos_deseados)):
            if random.random() < tabla_de_hijos_deseados[i]:
                return i + 1

        while i < 10:
            if random.random() < tabla_de_hijos_deseados[-1]:
                return i + 1

            i += 1

        return i

    def conocer(self, other):
        other.conocidos.append(self)
        self.conocidos.append(other)

    def embarazarse(self):
        self.tiempo_para_dar_luz = 9

    def intenta_emparejar(self, other):
        if not r_check(self.edad / 12, tabla_querer_pareja):
            return False

        if not r_check(other.edad / 12, tabla_querer_pareja):
            return False

        if not r_check(abs(self.edad - other.edad) / 12, tabla_establecer_pareja):
            return False

        return self.empareja(other)
