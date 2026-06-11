
# BracketMaster

Sistema web para gerenciamento de partidas, torneios e análise de desempenho de jogadores de Magic: The Gathering.

## Sobre o Projeto

O BracketMaster é uma aplicação web desenvolvida para auxiliar jogadores e organizadores de eventos de Magic: The Gathering no gerenciamento de partidas casuais e campeonatos competitivos.

A plataforma permite registrar partidas, criar torneios, gerenciar decks, acompanhar estatísticas de desempenho e automatizar processos como pareamentos e classificação de jogadores.

## Funcionalidades

### Usuários
- Cadastro de usuários
- Login e autenticação
- Perfis personalizáveis
- Histórico de partidas

### Partidas
- Registro de partidas casuais
- Registro de resultados
- Histórico completo de confrontos
- Acompanhamento de desempenho

### Campeonatos
- Criação de torneios
- Inscrição de jogadores
- Geração automática de rodadas
- Pareamentos automáticos
- Controle de classificação
- Encerramento de campeonatos


## Requisitos do Domínio

O sistema suporta:

- Formatos de jogo:
  - Standard
  - Modern
  - Commander
  - Outros formatos

- Formatos de torneio:
  - Sistema Suíço
  - Eliminatória Simples

## Tecnologias Utilizadas

### Backend
- Python
- Django
- PostgreSQL

### Frontend
- HTML5
- CSS3
- JavaScript

### Infraestrutura
- Render (Deploy)
- Gunicorn
- WhiteNoise

## Arquitetura

O sistema foi projetado seguindo princípios de separação de responsabilidades utilizando a arquitetura MVC/MVT do Django.

Principais módulos:

```text
users/
├── autenticação
├── perfis
└── estatísticas

matches/
├── partidas
├── rodadas
├── resultados
└── pareamentos

tournaments/
├── torneios
├── inscrições
├── classificação
└── gerenciamento
````

## Instalação

### 1. Clonar o repositório

```bash
git clone https://github.com/luiz-gustavo-soares/bracketmaster.git
cd bracketmaster
```

### 2. Criar ambiente virtual

Linux:

```bash
python -m venv venv
source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env`:

```env
SECRET_KEY=sua_chave_secreta

DEBUG=True

DB_NAME=bracketmaster
DB_USER=postgres
DB_PASSWORD=senha
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=seu_email@gmail.com
EMAIL_HOST_PASSWORD=sua_senha_app
DEFAULT_FROM_EMAIL=BracketMaster <seu_email@gmail.com>
```

### 5. Executar migrações

```bash
python manage.py migrate
```

### 6. Criar superusuário

```bash
python manage.py createsuperuser
```

### 7. Iniciar servidor

```bash
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000
```


## Licença

Este projeto foi desenvolvido para fins acadêmicos na disciplina de Engenharia Web da Universidade Federal dos Vales do Jequitinhonha e Mucuri (UFVJM).

---

Desenvolvido com foco na organização de eventos e análise estratégica para jogadores de Magic: The Gathering.

