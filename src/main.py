import utils
import constants


def main():
    print(constants.mensaje_inicio)
    utils.espera()
    print(constants.mensaje_inicio_2)
    utils.espera()
    print(constants.instrucciones)
    utils.espera(5)
    utils.turnos()

main()