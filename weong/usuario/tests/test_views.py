from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Ong
from vaga.models import Endereco

class VagaIntegrationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='ong_teste', password='senha123')
        self.endereco = Endereco.objects.create(
            logradouro='Rua Exemplo',
            numero='123',
            complemento='Sala 1',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='12345000'
        )
        self.ong = Ong.objects.create(
            usuario=self.user,
            nome_fantasia='ONG Integração',
            cnpj='12345678000199',
            telefone='11999999999',
            endereco=self.endereco,
            status='Ativa'
        )
        self.client.login(username='ong_teste', password='senha123')

    def test_criar_vaga(self):
        url = reverse('cadastro-vaga')
        data = {
            'titulo': 'Vaga de Integração',
            'descricao': 'Descrição da vaga de integração.',
            'localizacao': 'São Paulo',
            'requisitos': 'Boa comunicação.',
            'categoria': 'Educação'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)  # redirect após criar a vaga
