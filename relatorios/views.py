from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from datetime import datetime
import locale
import os

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

def index(request):
    relatorios_dir = os.path.join(settings.MEDIA_ROOT, 'relatorios')
    anos = []

    if os.path.exists(relatorios_dir):
        for filename in os.listdir(relatorios_dir):
            if filename.startswith('relatorio_') and filename.endswith('.csv'):
                try:
                    ano = int(filename[len('relatorio_'):-len('.csv')])
                    anos.append(ano)
                except ValueError:
                    continue

    anos.sort()
    return render(request, 'relatorios/index.html', {'anos': anos})

def gerar_relatorio_pdf(request, ano):
    
    relatorios_dir = os.path.join(settings.MEDIA_ROOT, 'relatorios')
    dadoscertos = pd.read_csv(relatorios_dir + f'/relatorio_{ano}.csv')
    dadoscertos['order_date'] = pd.to_datetime(dadoscertos['order_date'], format='%d-%m-%Y')

    dia_mais_vendido = dadoscertos['order_date'].value_counts().idxmax()
    qtd_vendas = dadoscertos['order_date'].value_counts().max()

    #Análise do horário que mais vendeu
    dadoscertos['order_time'] = pd.to_datetime(dadoscertos['order_time'], format='%H:%M:%S')
    dadoscertos['hour_interval'] = dadoscertos['order_time'].dt.hour // 1
    vendas_por_horario = dadoscertos.groupby('hour_interval').size()

    horario_mais_vendido = vendas_por_horario[vendas_por_horario == vendas_por_horario.max()].index.to_list()


    #Análise do sabor que mais vendeu

    sabor_mais_vendido = dadoscertos['pizza_name'].value_counts().idxmax()
    qtd_sabor = dadoscertos['pizza_name'].value_counts().max()


    #Análise do tamanho que mais vendeu

    tamanho_mais_vendido = dadoscertos['pizza_size'].value_counts().idxmax()
    qtd_tamanho = dadoscertos['pizza_size'].value_counts().max()


    #Análise de receita gerada por cada sabor

    receita_por_sabor = dadoscertos.groupby('pizza_name')['total_price'].sum()

    receita_por_sabor = receita_por_sabor.sort_values(ascending=False)


    #Análise do mês que mais vendeu

    dadoscertos['order_date'] = pd.to_datetime(dadoscertos['order_date'], format = '%d-%m-%Y')
    dadoscertos['month'] = dadoscertos['order_date'].dt.month

    vendas_por_mes = dadoscertos['month'].value_counts()

    mes_mais_vendido = vendas_por_mes.idxmax()
    qtd_mes = vendas_por_mes.max()


    #Analise de top5 sabores mais vendidos

    vendas_por_sabor = dadoscertos['pizza_name'].value_counts()

    top5 = vendas_por_sabor.head(5)
    topmenos5 = vendas_por_sabor.tail(5)


    # Análise do mês que mais vendeu
    dadoscertos['order_date'] = pd.to_datetime(dadoscertos['order_date'], format='%d-%m-%Y')
    dadoscertos['month'] = dadoscertos['order_date'].dt.month

    vendas_por_mes = dadoscertos['month'].value_counts()

    mes_mais_vendido = vendas_por_mes.idxmax()
    qtd_mes = vendas_por_mes.max()

    # Gerando o gráfico
    plt.figure(figsize=(10, 6))
    barplot = vendas_por_mes.sort_index().plot(kind='bar', color='skyblue')

    # Adicionando os valores nas barras
    for index, value in enumerate(vendas_por_mes.sort_index()):
        barplot.text(index, value + 10, str(value), ha='center', va='bottom', fontsize=9)

    plt.title('Quantidade de vendas por mês')
    plt.xlabel('Mês')
    plt.ylabel('Quantidade de vendas')
    # plt.yticks(range(0, vendas_por_mes.max() + 20000, 20000))
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig('vendas_por_mes.png')


    # Criando a instância do PDF

    class PDF(FPDF):
        def header(self):
            if self.page_no() == 1:  # Adiciona o cabeçalho apenas na primeira página
                # Define a fonte e tamanho do cabeçalho
                self.set_font('Arial', 'B', 26)
                # Adiciona o cabeçalho com a frase "Relatório de vendas" seguido pelo ano específico
                self.cell(0, 10, f'Relatório de vendas ({self.ano})', 0, 1, 'C')

        def footer(self):
            # Define a fonte do rodapé
            self.set_y(-15)
            self.set_font('Arial', 'I', 8)
            # Adiciona a data de geração no rodapé
            self.cell(0, 10, f'Data de geração: {datetime.now().strftime("%d/%m/%Y %H:%M")}', 0, 0, 'C')

    # Cria uma instância da classe PDF
    pdf = PDF()
    # Define o ano no objeto PDF
    pdf.ano = ano

    # Definindo as propriedades do PDF
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Variável para controlar a altura restante na página atual
    altura_restante = pdf.h - pdf.y

    # Adiciona um espaço entre o título e a primeira seção de informações
    pdf.ln()

    # Seção: Receita por sabor
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Receita por sabor de pizza', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    receita_total = 0
    for pizza, receita in receita_por_sabor.items():
        receita_formatada = locale.currency(receita, grouping=True, symbol=None)
        receita_total += receita
        pdf.cell(200, 10, txt=f"{pizza}: R$ {receita_formatada}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Receita total: R$ {locale.currency(receita_total, grouping=True, symbol=None)}", ln=True, align='L') 
    
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)  # Reinicia a posição Y para evitar conflitos com o cabeçalho
        altura_restante = pdf.h - pdf.y
    
    pdf.ln(5)

    # Seção: Dia que mais vendeu
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Dia que mais vendeu', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, txt=f"Dia que mais vendeu: {datetime.strftime(dia_mais_vendido, '%d/%m/%Y')}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Quantidade de vendas nesse dia: {qtd_vendas}", ln=True, align='L')

    # Se a seção não couber na página atual, adiciona uma nova página
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)  # Reinicia a posição Y para evitar conflitos com o cabeçalho
        altura_restante = pdf.h - pdf.y

    pdf.ln(5)

    # Seção: Horário que mais vendeu
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Horário que mais vendeu', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, txt="Horários que mais venderam:", ln=True, align='L')
    for horario in horario_mais_vendido:
        pdf.cell(200, 10, txt=f"Entre as {horario}:00 e as {horario + 1}:00", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Quantidade de vendas nesses horários: {vendas_por_horario.max()}", ln=True, align='L')

    # Se a seção não couber na página atual, adiciona uma nova página
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)  # Reinicia a posição Y para evitar conflitos com o cabeçalho
        altura_restante = pdf.h - pdf.y

    pdf.ln(5)

    # Seção: Sabor que mais vendeu
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Sabor que mais vendeu', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, txt=f"Sabor que mais vendeu: {sabor_mais_vendido}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Quantidade vendida desse sabor: {qtd_sabor}", ln=True, align='L')
    
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)  # Reinicia a posição Y para evitar conflitos com o cabeçalho
        altura_restante = pdf.h - pdf.y


    pdf.ln(5)
    
    
    # Seção: Tamanho que mais vendeu    
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Tamanho que mais vendeu', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, txt=f"Tamanho que mais vendeu: {tamanho_mais_vendido}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Quantidade desse tamanho vendidas: {qtd_tamanho}", ln=True, align='L')
    
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)
        altura_restante = pdf.h - pdf.y

    pdf.ln(5)

    # Seção: Mês que mais vendeu
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Mês que mais vendeu', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.cell(200, 10, txt=f"Mês que mais vendeu: {mes_mais_vendido}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Quantidade vendida nesse mês: {qtd_mes}", ln=True, align='L')
        
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)
        altura_restante = pdf.h - pdf.y

    pdf.ln(5)

    # Seção: Top 5 sabores mais vendidos
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Top 5 sabores mais vendidos', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    for sabor, quantidade in top5.items():
        pdf.cell(200, 10, txt=f"{sabor}: {quantidade}", ln=True, align='L')
        
    if pdf.get_y() + 10 > altura_restante:
        pdf.add_page()
        pdf.set_y(20)
        altura_restante = pdf.h - pdf.y

    pdf.ln(5)

    # Adicionando o gráfico ao PDF
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, txt='Gráfico de vendas em relação aos meses', ln=True, align='C')

    pdf.set_font('Arial', '', 10)
    pdf.image('vendas_por_mes.png', x = None, y = None, w = 200, h = 100, type = '', link = '')
    
    pdf_bytes = bytes(pdf.output(dest='S'))

    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="relatorio_{ano}.pdf"'
    
    
    return response

