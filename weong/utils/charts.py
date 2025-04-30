from vaga.models import Vaga

meses = [
    'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
    'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
]

paleta_cores = ['#55efc4', '#81ecec', '#a29bfe', '#ffeaa7', '#fab1a0', '#ff7675', '#fd79a8']
cor_primaria, cor_sucesso, cor_vagas_abertas, cor_ongs, cor_voluntarios = '#79aec8', paleta_cores[0], paleta_cores[3], paleta_cores[1], paleta_cores[4]
cores_areas = ['#3A59D1', '#3D90D7', '#7AC6D2', '#B5FCCD', '#9FB3DF', '#9EC6F3', '#BDDDE4', '#FFF1D5', '#F6F1DE', '#3E3F5B', '#8AB2A6', '#8AB2A6', '#ACD3A8', '#94B4C1']

def get_meses():
    ano = {}
    
    for mes in meses:
        ano[mes] = 0
    return ano

def get_areas():
    areas_dict = {}
    for area in Vaga.AREAS:
        areas_dict[area[0]] = 0
    return areas_dict

def get_cores_areas():
    areas = get_areas()
    for i, area in enumerate(Vaga.AREAS):
        areas[area[0]] = cores_areas[i]
    return areas

def gera_paleta_cores(quantidade):
    paleta = []

    i = 0
    while i < len(paleta_cores) and len(paleta) < quantidade:
        paleta.append(paleta_cores[i])
        i += 1
        if i == len(paleta_cores) and len(paleta) < quantidade:
            i = 0
    return paleta