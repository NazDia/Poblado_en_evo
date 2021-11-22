from persona_definicion import *
from rng import SubtractiveRNG

random = SubtractiveRNG()
categorias = { x * 5 + 12 : [] for x in range(int(123 / 5))}
bebes = [0.7, 0.86, 0.94, 0.98, 1]
YEARS = 100

def print_status(pob, parejas, embarazadas):
    pop = 0
    for i in pob:
        pop += len(pob[i])

    par = 0
    for i in parejas:
        for j in parejas[i]:
            par += parejas[i][j]

    em = 0
    for i in embarazadas:
        em += sum(embarazadas[i])

    print('Poblacion actual : ' + str(int(pop)))
    print('Cantidad de parejas : ' + str(int(par)))
    print('Cantidad de embarazadas : ' + str(int(em)))


def check_add(value, dic, to_add):
    for i in dic.keys():
        if value <= i:
            dic[i].append(to_add)
            return

    dic[i].append(to_add)

def get(value, dic):
    for i in dic.keys():
        if value <= i:
            return dic[i]

    return dic[i]
    
def multi_len_2(tabla, index):
    ret = 0
    for i in tabla:
        ret += len(tabla[i][index])

    return ret

def multi_len_1(tabla, index):
    ret = 0
    tabla = tabla[index]
    for i in tabla:
        ret += i

    return ret

def categ_pobl(poblacion):
    for i in poblacion:
        check_add(i[0], categorias, i)

    return categorias

def union(params):
    ret = 0
    temp = var(params, 0 , len(params))
    temp = [x for x in temp if len(x) > 0]
    for i in range(len(temp)):
        t = 1
        for num in temp[i]:
            t *= num

        ret += (-1) ** (len(temp[i]) + 1) * t

    return ret

def var(params, i, l):
    if i == l - 1:
        return [[params[i]], []]

    temp = var(params, i + 1, l)
    ret = [[params[i]] + l for l in temp] + [l for l in temp]
    return ret

def males(poblacion):
    return {key : [ x for x in poblacion[key] if x[1] == 1] for key in poblacion}

def females(poblacion):
    return {key : [ x for x in poblacion[key] if x[1] == 0] for key in poblacion}

def calculate_pop(pob, tabla_embarazadas, tabla_prob_muerte_m, tabla_prob_muerte_h):
    em = 0
    for i in tabla_embarazadas.keys():
        em += tabla_embarazadas[i][1] + tabla_embarazadas[i][0] * 3 / 4
        tabla_embarazadas[i][1] = tabla_embarazadas[i][0] / 4
        tabla_embarazadas[i][0] *= 3 / 4

    new = 0
    for i in range(int(em)):
        cr = random.random()
        for j in range(len(bebes)):
            if bebes[j] > cr:
                new += j
                break


    pob[12] += [ (0, random.randint(0, 1)) for i in range(new) ]
    changes = { x : 0 for x in pob.keys()}
    for key in pob.keys():
        prob_1 = get(key, tabla_prob_muerte_m)
        prob_2 = get(key, tabla_prob_muerte_h)
        to_remove = []
        for i in range(len(pob[key])):
            cr = random.random()
            if cr < prob_1 and pob[key][i][1] == 1:
                to_remove.append(pob[key][i])

            elif cr < prob_2 and pob[key][i][1] == 0:
                to_remove.append(pob[key][i])

            elif pob[key][i][0] >= 125:
                to_remove.append(i)

        try:
            changes[key] = len(to_remove) / len(pob[key])
        except:
            pass
        for i in to_remove:
            pob[key].remove(i)

    return changes
        

def simulacion(pob_categ):
    parejas = { key : {key2 : 0 for key2 in pob_categ.keys()} for key in pob_categ.keys() }
    prob_pareja = { x : get(x, tabla_querer_pareja) for x in pob_categ.keys()}
    prob_muerte = { x : get(x, tabla_de_fallecimiento_1) for x in pob_categ.keys()}
    prob_muerte_f = { x : get(x, tabla_de_fallecimiento_1_f) for x in pob_categ.keys()}
    luto = [{ x : 0 for x in pob_categ.keys()} for __ in range(2)]
    prob_embarazo = { x : get(x, tabla_de_prob_embarazo) for x in pob_categ.keys()}
    embarazadas = {key : [0 for i in range(2)] for key in pob_categ.keys()}
    for_next_f = 0
    for_next_m = 0
    for year in range(YEARS + 1):
        if year == 0:
            continue
        changes = { x : 0 for x in pob_categ.keys() }
        for key in pob_categ.keys():
            to_remove_f = 0
            to_remove_m = 0
            for i in range(len(pob_categ[key])):
                pob_categ[key][i] = (pob_categ[key][i][0] + 1, pob_categ[key][i][1]) if year % 12 == 11 else (pob_categ[key][i][0], pob_categ[key][i][1])
                if pob_categ[key][i][0] >= key + 5 or pob_categ[key][i][0] > 125:
                    if pob_categ[key][i][1] == 0:
                        to_remove_f += 1
                    else:
                        to_remove_m += 1
                    try:
                        pob_categ[key + 5].append(pob_categ[key][i])
                    except KeyError:
                        pass

            for i in range(to_remove_f):
                pob_categ[key].remove((key + 5, 0))

            for i in range(to_remove_m):
                pob_categ[key].remove((key + 5, 1))

            to_remove = to_remove_m + to_remove_f
            try:
                changes[key] += to_remove / len(pob_categ[key])
            except:
                changes[key] = 0

            try:
                changes[key + 5] -= to_remove / len(pob_categ[key + 5])

            except:
                pass

        changes2 = calculate_pop(pob_categ, embarazadas, prob_muerte, prob_muerte_f)
        for key in embarazadas.keys():
            for l in range(len(embarazadas[key])):
                try:
                    embarazadas[key][l + 1] += embarazadas[key][l] - embarazadas[key][l] * (changes[key] + changes2[key] - changes[key] * changes2[key])
                    embarazadas[key + 5][l + 1] = embarazadas[key][l] * changes[key]

                except:
                    pass

            for i in parejas[key].keys():
                embarazadas[key][0] += parejas[key][i] * prob_embarazo[key]

        hombres = males(pob_categ)
        mujeres = females(pob_categ)
        sexo = luto[0]
        for key in sexo.keys():
            to_next = 0
            sexo[key] -= sexo[key] * union([changes[key], changes2[key]])
            s = 0
            for key2 in parejas.keys():
                s += parejas[key][key2] * union([union([probabilidad_de_separacion_1, changes[key], changes[key2], changes2[key]]), union([probabilidad_de_separacion_1, changes[key], changes[key2], changes2[key2]])])
            sexo[key] += s
            l = 1 / get(key, tabla_lambdas_luto)
            if year - 1 >= l / 12:
                sexo[key] *= l / 12 - for_next_f
                if sexo[key] < 0:
                    sexo[key] = 0
                for_next_f = sexo[key]
            sexo[key] += to_next
            to_next += sexo[key] * changes[key]

        sexo = luto[1]
        for key in sexo.keys():
            to_next = 0
            sexo[key] -= sexo[key] * union([changes[key], changes2[key]])
            s = 0
            for key2 in parejas.keys():
                s += parejas[key2][key] * union([union([probabilidad_de_separacion_1, changes[key], changes[key2], changes2[key]]), union([probabilidad_de_separacion_1, changes[key], changes[key2], changes2[key2]])])
            sexo[key] += s
            l = 1 / get(key, tabla_lambdas_luto)
            if year - 1 >= l / 12:
                sexo[key] *= l / 12 - for_next_m
                if sexo[key] < 0:
                    sexo[key] = 0
                for_next_m = sexo[key]
            sexo[key] += to_next
            to_next += sexo[key] * changes[key]


        for key in parejas.keys():
            l = 0
            for i in parejas[key].keys():
                l += parejas[key][i]
            for key2 in parejas[key].keys():
                parejas[key][key2] -= parejas[key][key2] * union([probabilidad_de_separacion_1, changes[key], changes[key2], changes2[key], changes2[key2]])  
                l2 = 0
                for i in parejas.keys():
                    l2 += parejas[i][key2]
                men = (len(hombres[key2]) - luto[1][key2] - l2) * min(year, 1 / get(key2, tabla_lambdas_luto))
                men = men if men > 0 else 0
                women = (len(mujeres[key]) - luto[0][key] - l) * min(year, 1 / get(key, tabla_lambdas_luto))
                women = women if women > 0 else 0
                x = min(men, women) * prob_pareja[key2] * prob_pareja[key] * get(abs(key - key2), tabla_establecer_pareja)
                parejas[key][key2] += x
                try:
                    parejas[key + 5][key2] += parejas[key][key2] * changes[key]
                except KeyError:
                    pass
                try:
                    parejas[key][key2 + 5] += parejas[key][key2] * changes[key2]
                except KeyError:
                    pass
                try:
                    parejas[key + 5][key2 + 5] += parejas[key][key2] * changes[key] * changes2[key]
                except KeyError:
                    pass
                if parejas[key][key2] > min(len(hombres[key2]), len(mujeres[key])):
                    parejas[key][key2] = min(len(hombres[key2]), len(mujeres[key]))

                if parejas[key][key2] < 0:
                    parejas[key][key2] = 0

        print_status(pob_categ, parejas, embarazadas)


            