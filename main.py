import argparse
import poblado_en_evo
import evo_tipo_1
from rng import SubtractiveRNG

if __name__ == "__main__":
    random = SubtractiveRNG()
    parser = argparse.ArgumentParser(description='Configura la poblacion inicial y el tipo de simulacion a usar.')
    parser.add_argument('M', metavar='M',type=int, help='Cantidad inicial de mujeres en la poblacion')
    parser.add_argument('H', metavar='H',type=int, help='Cantidad inicial de hombres en la poblacion')
    parser.add_argument('-d', action='store_true', dest='type', help='Elige el tipo de simulacion a realizar, insertar flag para hacer una simulacion a profundidad (no recomendado con poblaciones grandes)')
    args = parser.parse_args()
    if args.type:
        poblado = poblado_en_evo.crear_poblacion(args.M, args.H)
        poblado_en_evo.comenzar_simulacion_tipo1(poblado)
    else:
        poblado = evo_tipo_1.categ_pobl([(random.randint(0, 100), 0) for _ in range(args.M)] + [(random.randint(0, 100), 1) for _ in range(args.H)])
        evo_tipo_1.simulacion(poblado)
