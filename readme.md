# 🍕 Pizza Sales BI & Relatórios Automatizados

> Sistema web Full-Stack desenvolvido em **Django** integrado a pipelines de Análise de Dados em **Python (Pandas & Matplotlib)** para processar bases transacionais de vendas, extrair indicadores de desempenho (KPIs) e gerar relatórios gerenciais automatizados em PDF sob demanda.

---

## 🎯 O Problema & A Solução
* **O Desafio:** Empresas do setor alimentício acumulam grandes volumes de dados de vendas (milhares de registros históricos) sem conseguir transformá-los facilmente em insights acionáveis para a tomada de decisão gerencial.
* **A Solução:** Uma aplicação web intuitiva que automatiza o cruzamento de dados, calcula métricas de faturamento e sazonalidade, e disponibiliza relatórios executivos prontos para download em PDF com gráficos analíticos embutidos.

---

## 🛠️ Stack Tecnológica
* **Back-end:** Python 3.10+, Django 5+
* **Data Science & Analytics:** Pandas (manipulação e agregação de dados), Matplotlib (geração de gráficos analíticos)
* **Geração de Documentos:** FPDF2 (criação dinâmica de relatórios em PDF)
* **Front-end:** HTML5, Bootstrap 4 (interface responsiva)
* **Banco de Dados:** SQLite (padrão Django para desenvolvimento)

---

## 📊 Principais Funcionalidades
* **Processamento de Grandes Bases:** Análise estruturada de dados transacionais históricos por ano.
* **Indicadores Chave (KPIs):** Identificação automática de dias de pico de vendas, horários de maior movimento, sabores e tamanhos mais rentáveis.
* **Data Visualization:** Geração dinâmica de gráficos de distribuição mensal integrados aos documentos exportados.
* **Exportação Executiva:** Botão dedicado para renderização e download de relatórios gerenciais em formato PDF.

---

## ⚙️ Como Executar o Projeto Localmente

Siga os passos abaixo para clonar e rodar o projeto na sua máquina:

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/GuMouzin/seu-repositorio.git
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual:**
   ```bash
   python -m venv venv
   # No Windows:
   venv\Scripts\activate
   # No Linux/Mac:
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Aplique as migrações do banco de dados:**
   ```bash
   python manage.py migrate
   ```

5. **Inicie o servidor de desenvolvimento:**
   ```bash
   python manage.py runserver
   ```

6. **Acesse no navegador:**
   Abra `http://127.0.0.1:8000/` e interaja com o painel de relatórios.

---

## 📂 Estrutura do Projeto
```text
├── data/relatorios/        # Bases de dados transacionais divididas por ano (CSV)
├── relatorios-anuais/      # App Django principal (Views, Templates e regras de negócio)
├── big_data/               # Configurações globais do projeto Django (Settings, URLs)
├── scripts/                # Jupyter Notebooks de exploração e tratamento de dados
├── manage.py               # Utilitário de linha de comando do Django
└── requirements.txt        # Dependências do projeto
```

---
*Desenvolvido por **Gustavo Mouzin**.*