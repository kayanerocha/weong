from unidecode import unidecode

def remover_acentos(texto: str) -> str:
    return unidecode(str(texto))

def string_simples(texto: str) -> str:
    return remover_acentos(texto).strip().lower()