from validate_docbr import CNPJ

def cnpj_valido(cnpj: str) -> bool:
    cnpj_valido = CNPJ()
    if not cnpj_valido.validate(cnpj):
        return False
    return True