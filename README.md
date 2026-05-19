<div align="center">

# ⚡ FitManager

### Sistema de Agendamentos para Personal Trainer

![Python](https://img.shields.io/badge/Python-3.14-FFD43B?style=for-the-badge&logo=python&logoColor=black)
![Django](https://img.shields.io/badge/Django-5.x-092E20?style=for-the-badge&logo=django&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![Status](https://img.shields.io/badge/Status-Em%20Produção-E8D87A?style=for-the-badge)

[🚀 Acessar Demo](#) • [📸 Screenshots](#screenshots) • [⚙️ Como Rodar](#como-rodar)

</div>

---

## 📌 Sobre o Projeto

O **FitManager** é um sistema web completo para gestão de agendamentos de personal trainers e academias. Desenvolvido com Django e MySQL, oferece uma interface moderna com dark/light mode, relatórios visuais e exportação de dados.

> Projeto desenvolvido para resolver um problema real: a dificuldade de pequenos negócios fitness em gerenciar seus agendamentos de forma organizada e profissional.

---

## ✨ Funcionalidades

- 🔐 **Autenticação segura** — login, logout e troca de senha
- 📅 **Gestão de agendamentos** — criação, edição, cancelamento e validação de conflitos de horário
- 👥 **Cadastro de clientes** — histórico, observações e restrições físicas
- 🏋️ **Cadastro de profissionais** — personal trainers e especialidades
- 📋 **Cadastro de serviços** — tipos de treino, duração e preço
- 🔍 **Busca e filtros avançados** — por cliente, status, profissional e período
- 📊 **Relatórios com gráficos** — agendamentos por dia, status, profissional e serviço
- 📄 **Exportação para PDF** — relatórios filtrados em PDF estilizado
- 👤 **Perfil do usuário** — edição de dados pessoais e senha
- 🌗 **Dark / Light mode** — preferência salva no navegador

---

## 🖼️ Screenshots

> _Adicione prints do sistema aqui_

| Dashboard | Agendamentos | Relatórios |
|-----------|-------------|------------|
| ![dashboard](#) | ![agendamentos](#) | ![relatorios](#) |

---

## 🛠️ Tecnologias

| Tecnologia | Uso |
|-----------|-----|
| Python 3.14 | Linguagem principal |
| Django 5.x | Framework web |
| MySQL 8.0 | Banco de dados |
| Bootstrap 5 | Interface responsiva |
| Chart.js | Gráficos interativos |
| ReportLab | Geração de PDF |
| WhiteNoise | Arquivos estáticos em produção |
| Gunicorn | Servidor WSGI |
| Railway | Deploy em nuvem |

---

## ⚙️ Como Rodar Localmente

### Pré-requisitos
- Python 3.10+
- MySQL 8.0+
- Git

### Passo a passo

```bash
# 1. Clone o repositório
git clone https://github.com/seu-usuario/fitmanager.git
cd fitmanager

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
# Crie um arquivo .env na raiz com:
SECRET_KEY=sua_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DB_NAME=academia
DB_USER=root
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=3306

# 5. Crie o banco de dados no MySQL
# Execute no MySQL: CREATE DATABASE academia CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 6. Rode as migrations
python manage.py migrate

# 7. Crie um superusuário
python manage.py createsuperuser

# 8. Inicie o servidor
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000`

---

## 📁 Estrutura

```
fitmanager/
├── meu_projeto/       # Configurações Django
├── clientes/          # App de clientes
├── profissionais/     # App de profissionais
├── servicos/          # App de serviços
├── agendamentos/      # Dashboard, agenda, relatórios, PDF
├── templates/
│   ├── base.html
│   ├── auth/
│   ├── agendamentos/
│   ├── clientes/
│   ├── profissionais/
│   └── servicos/
├── build.sh
├── requirements.txt
└── manage.py
```

## 🚀 Deploy

O projeto está hospedado no **Railway** com banco de dados MySQL em nuvem.

🔗 **Link:** [fitmanager.railway.app](https://fitmanager-erzl.onrender.com)

---

## 👩‍💻 Autora

Feito com 💛 por **Duda**

[![GitHub](https://img.shields.io/badge/GitHub-seu--usuario-181717?style=flat-square&logo=github)](https://github.com/DudaVargz)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-seu--perfil-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/eduarda-vargas-born-ab11b93aa)
