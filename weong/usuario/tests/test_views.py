from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Ong
from vaga.models import Endereco

class VagaIntegrationTest(APITestCase):
    def setUp(self):
        # Criação do usuário ONG
        self.user = User.objects.create_user(username='ong_teste', password='senha123')
        # Criação do endereço
        self.endereco = Endereco.objects.create(
            logradouro='Rua Exemplo',
            numero='123',
            complemento='Sala 1',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='12345000'
        )
        # Associação do usuário à ONG
        self.ong = Ong.objects.create(
            usuario=self.user,
            nome_fantasia='ONG Integração',
            cnpj='12345678000199',
            telefone='11999999999',
            endereco=self.endereco,
            status='Ativa'
        )
        # Autentica a ONG no client
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_criar_vaga(self):
        url = reverse('vaga-create')  # Verifica a sua URL name no urls.py
        data = {
            'titulo': 'Vaga de Integração',
            'descricao': 'Descrição da vaga de integração.',
            'localizacao': 'São Paulo',
            'requisitos': 'Boa comunicação.',
            'categoria': 'Educação'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['titulo'], 'Vaga de Integração')
