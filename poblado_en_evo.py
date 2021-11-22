import rng
import persona_definicion as pd

YEARS = 100
MEETING_BASE = 5
PRIVATE_BASE = 1

random = rng.SubtractiveRNG()
t1 = [0.2, 0.9, 0.98, 1]

def print_status(poblacion):
    print('Estado de la poblacion:')
    print('Poblacion actual : ' + str(len(poblacion)))
    if len(poblacion) == 0:
        print('Fin de la simulacion')
        return
    count1 = 0
    count2 = 0
    count3 = 0
    conocidos = 0.0
    for i in range(len(poblacion)):
        if not poblacion[i].pareja is None:
            count1 += 1

        if poblacion[i].tiempo_en_luto_restante > 0:
            count2 += 1

        if poblacion[i].tiempo_para_dar_luz > 0:
            count3 += 1

        conocidos += len(poblacion[i].conocidos)

    conocidos /= len(poblacion)
    count1 /= 2
    print('Existen ' + str(count1.__trunc__()) + ' parejas')
    print('Existen ' + str(count2) + ' personas que se separaron de sus parejas o que enviudaron recientemente')
    print('Existen ' + str(count3) + ' mujeres embarazadas')
    print('El promedio de personas conocidas por cada persona es de : ' + str(conocidos))
    print()

def random_check(table):
    r = random.random()
    for i in range(len(table)):
        if r < table[i]:
            return i
    
    return len(table)

def crear_padres_iniciales(poblacion):
    edad_categ = [[[], []] for _ in range((int)(100 / 20))]
    for persona in poblacion:
        edad_categ[(int)(persona.edad / 20 / 12)][persona.sexo].append(persona)

    emparejados = {}
    for edad_categ_i in range(len(edad_categ)):
        for sex_categ in edad_categ[edad_categ_i]:
            for persona in sex_categ:
                father_r = random_check(t1)
                if edad_categ_i + father_r < len(edad_categ):
                    f_c = edad_categ[edad_categ_i + father_r]
                    try:
                        x = random.randint(0, len(f_c[1]) - 1)
                        persona.padre = f_c[1][x]
                        for _ in range(len(f_c[1])):
                            if persona.padre.hijos_deseados > len(persona.padre.hijos):
                                persona.padre = f_c[1][(x * 2) % len(f_c[1])]
                                break

                            x = x * 2 % len(f_c[1])


                        else:
                            persona.padre = None

                        if not persona.padre is None:
                            persona.padre = f_c[1][x]
                            persona.padre.hijos.append(persona)
                            persona.conocer(persona.padre)
                    except ValueError:      # Para el molesto y poco probable caso en que la lista f_c[1] este vacia
                        pass

                    try:
                        persona.madre = emparejados[persona.padre]
                        try:
                            persona.conocer(persona.madre)
                            persona.madre.hijos.append(persona)
                        except:
                            pass

                    except KeyError:
                        pass

                mother_r = random_check(t1)
                if edad_categ_i + mother_r < len(edad_categ):
                    f_c = edad_categ[edad_categ_i + mother_r]
                    try:
                        x = random.randint(0, len(f_c[0]) - 1)
                        persona.madre = f_c[0][x]
                        for _ in range(len(f_c[0])):
                            if persona.madre.hijos_deseados > len(persona.madre.hijos):
                                persona.madre = f_c[0][(x * 2) % len(f_c[0])]
                                break

                            x = x * 2 % len(f_c[0])

                        else:
                            persona.madre = None

                        if not persona.madre is None:
                            persona.madre.hijos.append(persona)
                            persona.conocer(persona.madre)
                    except ValueError:
                        pass
                    try:
                        persona.padre = emparejados[persona.madre]
                        try:
                            persona.conocer(persona.padre)
                            persona.padre.hijos.append(persona)
                        except:
                            pass

                    except KeyError:
                        pass

                if not persona.padre is None:
                    emparejados[persona.padre] = persona.madre

                if not persona.madre is None:
                    emparejados[persona.madre] = persona.padre

                if not persona.madre is None and not persona.padre is None and random.random() > 0.1:
                    persona.madre.conocer(persona.padre)
                    persona.madre.empareja(persona.padre)

def crear_conocidos_iniciales(poblacion):
    ls = min(int(len(poblacion) / 2), 1000)
    li = 10
    for persona in poblacion:
        conocidos = random.randint(li, ls)
        for _ in range(conocidos):
            other = poblacion[random.randint(0, len(poblacion) - 1)]
            if other != persona and not other in persona.conocidos:
                persona.conocer(other)

def crear_poblacion(M, H):
    print('Generando poblacion...')
    ret = []
    for _ in range(M):
        ret.append(pd.Persona(random.randint(0, 100 * 12 - 1), sexo=0))
    for _ in range(H):
        ret.append(pd.Persona(random.randint(0, 100 * 12 - 1), sexo=1))

    crear_padres_iniciales(ret)
    crear_conocidos_iniciales(ret)
    return ret

def comenzar_simulacion_tipo1(poblacion_inicial):
    poblacion = poblacion_inicial
    poblacion_inicial = []
    for i in range(YEARS * 12 * 31):
        print_status(poblacion)
        if len(poblacion) == 0:
            return
        
        to_remove = []
        for persona_i in range(len(poblacion)):
            persona = poblacion[persona_i]
            if i % 31 == 30:
                poblacion += persona.envejece()

            if persona.muerto:
                to_remove.append(persona)
                continue
                    
            if persona.edad / 12 < 5:
                continue

            r_soc = random.random()
            for __ in range(PRIVATE_BASE):
                if r_soc < persona.indice_social:
                    try:
                        conocido = persona.conocidos[random.randint(0, len(persona.conocidos) - 1)]
                    except ValueError:
                        conocido = None

                    if conocido is None or conocido.muerto:
                        pass
                    elif not persona.pareja is None or not conocido.pareja is None:
                        pass

                    elif conocido == persona.madre:
                        pass
                    elif conocido == persona.padre:
                        pass
                    elif not persona.padre is None and conocido in persona.padre.hijos:
                        pass
                    elif not persona.madre is None and conocido in persona.madre.hijos:
                        pass
                    elif persona.sexo + conocido.sexo == 1:
                        if random.random() < persona.indice_social + conocido.indice_social - persona.indice_social * conocido.indice_social:
                            persona.intenta_emparejar(conocido)
                        else:
                            pass

                try:
                    other = poblacion[random.randint(0, len(poblacion) - 1)]
                except ValueError:
                    break
                
                if other in persona.conocidos or other.muerto:
                    continue

                if random.random() < (other.indice_social + persona.indice_social - other.indice_social * persona.indice_social):
                    persona.conocer(other)

        for fallecido in to_remove:
            poblacion.remove(fallecido)


if __name__ == "__main__":
    N = 1000
    pobl = crear_poblacion(N)
    comenzar_simulacion_tipo1(pobl)