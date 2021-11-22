EPSILON = 0.00001

def probabilidad_cond_secuencial(prob, repeticion):
    prob_acumulada = prob
    for _ in range(repeticion - 1):
        prob_acumulada += (100 - prob_acumulada) * prob /100

    return prob_acumulada

def bisection(li, ls, res, func):
    current = func((li + ls) / 2)
    while abs(current - res) > EPSILON:
        c1 = func(li)
        c2 = func(ls)
        if c1 <= current <= res:
            li = (li + ls) / 2

        elif res <= current <= c2:
            ls = (li + ls) / 2

        current = func((li + ls) / 2)

    return (li + ls) / 2, current