import threading
import os                                                          
from multiprocessing import Pool


def inicia_programa(nome_arquivo):
    os.system('py -3.8 {}'.format(nome_arquivo))

if __name__ == "__main__":

    arquivos = ['CrawlerAtualizacaoEstoqueTarkett.py','Saldos_roca.py','saldos_incepa.py']

    processos = []
    for arquivo in arquivos:
        processos.append(threading.Thread(target=inicia_programa, args=(arquivo,)))

    for processo in processos:
        processo.start()
#'muse.py','ajuste_bobinex_saldo.py',