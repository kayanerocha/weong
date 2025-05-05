from django.test import TestCase
from django.contrib.auth.models import User
from vaga.models import Endereco
from usuario.models import Ong

class OngModelTest(TestCase):
    def setUp(self):
        # Cria um usuário para associar à ONG
        self.user = User.objects.create_user(
            username='usuario_teste',
            password='senha123'
        )
        # Cria um endereço para associar à ONG (usando os campos corretos)
        self.endereco = Endereco.objects.create(
            logradouro='Rua Exemplo',
            numero='123',
            complemento='Sala 1',
            bairro='Bairro Teste',
            cidade='São Paulo',
            estado='SP',
            cep='12345000'
        )

    def test_criar_ong(self):
        ong = Ong.objects.create(
            usuario=self.user,
            nome_fantasia="ONG Teste",
            razao_social="Organização Não Governamental Teste",
            cnpj="12345678000199",
            telefone="11999999999",
            site="https://www.ongteste.com.br",
            status="Ativa",
            endereco=self.endereco
        )
        # Validações básicas
        self.assertEqual(ong.nome_fantasia, "ONG Teste")
        self.assertEqual(ong.status, "Ativa")
        self.assertEqual(ong.endereco.cidade, "São Paulo")