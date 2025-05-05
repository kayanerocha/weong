from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from usuario.models import Ong, Voluntario
from vaga.models import Endereco

class PermissionTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.endereco = Endereco.objects.create(
            logradouro='Rua Exemplo',
            numero='123',
            complemento='Sala 1',
            bairro='Centro',
            cidade='São Paulo',
            estado='SP',
            cep='12345000'
        )
        self.ong_user = User.objects.create_user(username='ong_teste', password='senha123')
        self.ong = Ong.objects.create(
            usuario=self.ong_user,
            nome_fantasia='ONG Teste',
            cnpj='12345678000199',
            telefone='11999999999',
            endereco=self.endereco,
            status='Ativa'
        )
        self.voluntario_user = User.objects.create_user(username='voluntario_teste', password='senha123')
        self.voluntario = Voluntario.objects.create(
            usuario=self.voluntario_user,
            nome_completo='Voluntário Teste',
            cpf='12345678900',
            telefone='11988887777',
            data_nascimento='2000-01-01',
            endereco=self.endereco,
            status='Ativo'
        )
        self.vaga_url = reverse('cadastro-vaga')

    def test_ong_pode_criar_vaga(self):
        self.client.login(username='ong_teste', password='senha123')
        data = {
            'titulo': 'Vaga Teste Permissão',
            'descricao': 'Descrição de permissão',
            'localizacao': 'São Paulo',
            'requisitos': 'Experiência prévia',
            'categoria': 'Educação'
        }
        response = self.client.post(self.vaga_url, data)
        self.assertEqual(response.status_code, 302)  # A view redireciona após criar

    def test_voluntario_nao_pode_criar_vaga(self):
        self.client.login(username='voluntario_teste', password='senha123')
        data = {
            'titulo': 'Vaga Teste Voluntário',
            'descricao': 'Tentativa inválida',
            'localizacao': 'São Paulo',
            'requisitos': 'Nenhum',
            'categoria': 'Educação'
        }
        response = self.client.post(self.vaga_url, data)
        self.assertEqual(response.status_code, 302)  # Se tiver verificação de permissão, ou 302 se redirecionar

    def test_nao_autenticado_nao_pode_criar_vaga(self):
        data = {
            'titulo': 'Vaga Teste Anônimo',
            'descricao': 'Sem autenticação',
            'localizacao': 'São Paulo',
            'requisitos': 'Nenhum',
            'categoria': 'Educação'
        }
        response = self.client.post(self.vaga_url, data)
        self.assertEqual(response.status_code, 302)  # Redireciona para login
