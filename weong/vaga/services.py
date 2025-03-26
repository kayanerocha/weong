from .models import Candidatura, Vaga

def candidatos_selecionados(id_vaga: int) -> bool:
    candidatos_aceitos = Candidatura.objects.filter(vaga_id=id_vaga, status='Aceito').count()
    if candidatos_aceitos == Vaga.objects.filter(id=id_vaga).get().quantidade_vagas:
        return True
    return False

def candidatura_existe(vaga_id: int, voluntario_id: int):
    candidatura = Candidatura.objects.filter(vaga_id=vaga_id, voluntario_id=voluntario_id).first()
    if candidatura:
        return True
    return False

def possui_candidatura(vaga_id: int) -> bool:
    candidaturas = Candidatura.objects.filter(vaga_id=vaga_id).count()
    if candidaturas > 0:
        return True
    return False