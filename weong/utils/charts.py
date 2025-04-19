meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

paleta_cores = ['#55efc4', '#81ecec', '#a29bfe', '#ffeaa7', '#fab1a0', '#ff7675', '#fd79a8']
cor_primaria, cor_sucesso, cor_vagas_abertas = '#79aec8', paleta_cores[0], paleta_cores[3]

def get_meses():
    ano = {}
    
    for mes in meses:
        ano[mes] = 0
    return ano

def gera_paleta_cores(quantidade):
    paleta = []

    i = 0
    while i < len(paleta_cores) and len(paleta) < quantidade:
        paleta.append(paleta_cores[i])
        i += 1
        if i == len(paleta_cores) and len(paleta) < quantidade:
            i = 0
    return paleta