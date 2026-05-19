from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento
from clientes.models import Cliente
from profissionais.models import Profissional
from servicos.models import Servico
from datetime import date
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.db.models import Count
from django.db.models.functions import TruncDate, TruncMonth
import json
from django.http import HttpResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

@login_required
def dashboard(request):
    hoje = date.today()
    agendamentos = Agendamento.objects.filter(
        data_hora__date=hoje
    ).exclude(status='cancelado')
    context = {
        'agendamentos': agendamentos,
        'total_clientes': Cliente.objects.filter(ativo=True).count(),
        'total_profissionais': Profissional.objects.filter(ativo=True).count(),
        'total_servicos': Servico.objects.filter(ativo=True).count(),
    }
    return render(request, 'agendamentos/dashboard.html', context)

@login_required
def lista_agendamentos(request):
    agendamentos = Agendamento.objects.all().order_by('-data_hora')

    # Filtros
    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')
    profissional_id = request.GET.get('profissional', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    if busca:
        agendamentos = agendamentos.filter(
            cliente__nome__icontains=busca
        )

    if status:
        agendamentos = agendamentos.filter(status=status)

    if profissional_id:
        agendamentos = agendamentos.filter(profissional_id=profissional_id)

    if data_inicio:
        agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)

    if data_fim:
        agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

    context = {
        'agendamentos': agendamentos,
        'profissionais': Profissional.objects.filter(ativo=True),
        'busca': busca,
        'status': status,
        'profissional_id': profissional_id,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total': agendamentos.count(),
    }
    return render(request, 'agendamentos/lista.html', context)

@login_required
def cadastrar_agendamento(request):
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        profissional_id = request.POST.get('profissional')
        servico_id = request.POST.get('servico')
        data_hora = request.POST.get('data_hora')

        if not all([cliente_id, profissional_id, servico_id, data_hora]):
            messages.error(request, 'Todos os campos são obrigatórios.')
        else:
            # Verificar conflito de horário
            conflito = Agendamento.objects.filter(
                profissional_id=profissional_id,
                data_hora=data_hora,
            ).exclude(status='cancelado').exists()

            if conflito:
                messages.error(request, 'Este profissional já tem um agendamento neste horário.')
            else:
                Agendamento.objects.create(
                    cliente_id=cliente_id,
                    profissional_id=profissional_id,
                    servico_id=servico_id,
                    data_hora=data_hora,
                    observacoes=request.POST.get('observacoes', ''),
                )
                messages.success(request, 'Agendamento criado com sucesso!')
                return redirect('dashboard')

    context = {
        'clientes': Cliente.objects.filter(ativo=True),
        'profissionais': Profissional.objects.filter(ativo=True),
        'servicos': Servico.objects.filter(ativo=True),
    }
    return render(request, 'agendamentos/form.html', context)

@login_required
def editar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    if request.method == 'POST':
        data_hora = request.POST.get('data_hora')
        profissional_id = request.POST.get('profissional')

        # Verificar conflito de horário (excluindo o próprio agendamento)
        conflito = Agendamento.objects.filter(
            profissional_id=profissional_id,
            data_hora=data_hora,
        ).exclude(status='cancelado').exclude(pk=pk).exists()

        if conflito:
            messages.error(request, 'Este profissional já tem um agendamento neste horário.')
        else:
            agendamento.cliente_id = request.POST.get('cliente')
            agendamento.profissional_id = profissional_id
            agendamento.servico_id = request.POST.get('servico')
            agendamento.data_hora = data_hora
            agendamento.status = request.POST.get('status')
            agendamento.observacoes = request.POST.get('observacoes', '')
            agendamento.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('dashboard')

    context = {
        'agendamento': agendamento,
        'clientes': Cliente.objects.filter(ativo=True),
        'profissionais': Profissional.objects.filter(ativo=True),
        'servicos': Servico.objects.filter(ativo=True),
    }
    return render(request, 'agendamentos/form.html', context)

@login_required
def cancelar_agendamento(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    agendamento.status = 'cancelado'
    agendamento.save()
    messages.warning(request, f'Agendamento de "{agendamento.cliente}" cancelado.')
    return redirect('dashboard')

@login_required
def perfil(request):
    if request.method == 'POST':
        acao = request.POST.get('acao')

        if acao == 'atualizar_nome':
            request.user.first_name = request.POST.get('first_name', '').strip()
            request.user.last_name = request.POST.get('last_name', '').strip()
            request.user.email = request.POST.get('email', '').strip()
            request.user.save()
            messages.success(request, 'Perfil atualizado com sucesso!')

        elif acao == 'trocar_senha':
            senha_atual = request.POST.get('senha_atual')
            nova_senha = request.POST.get('nova_senha')
            confirmar_senha = request.POST.get('confirmar_senha')

            if not request.user.check_password(senha_atual):
                messages.error(request, 'Senha atual incorreta.')
            elif nova_senha != confirmar_senha:
                messages.error(request, 'As novas senhas não coincidem.')
            elif len(nova_senha) < 6:
                messages.error(request, 'A nova senha deve ter pelo menos 6 caracteres.')
            else:
                request.user.set_password(nova_senha)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Senha alterada com sucesso!')

        return redirect('perfil')

    context = {
        'total_agendamentos': Agendamento.objects.count(),
        'agendamentos_confirmados': Agendamento.objects.filter(status='confirmado').count(),
        'agendamentos_concluidos': Agendamento.objects.filter(status='concluido').count(),
        'agendamentos_cancelados': Agendamento.objects.filter(status='cancelado').count(),
    }
    return render(request, 'agendamentos/perfil.html', context)

@login_required
def relatorios(request):
    # Período padrão: últimos 30 dias
    from datetime import timedelta
    hoje = date.today()
    data_inicio = request.GET.get('data_inicio', str(hoje - timedelta(days=30)))
    data_fim = request.GET.get('data_fim', str(hoje))

    agendamentos = Agendamento.objects.filter(
        data_hora__date__gte=data_inicio,
        data_hora__date__lte=data_fim,
    )

    # Agendamentos por dia
    por_dia = (
        agendamentos
        .annotate(dia=TruncDate('data_hora'))
        .values('dia')
        .annotate(total=Count('id'))
        .order_by('dia')
    )

    # Agendamentos por status
    por_status = (
        agendamentos
        .values('status')
        .annotate(total=Count('id'))
    )

    # Agendamentos por profissional
    por_profissional = (
        agendamentos
        .values('profissional__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )

    # Agendamentos por serviço
    por_servico = (
        agendamentos
        .values('servico__nome')
        .annotate(total=Count('id'))
        .order_by('-total')[:8]
    )

    # Serializar para JSON
    labels_dia = [item['dia'].strftime('%d/%m') for item in por_dia]
    dados_dia = [item['total'] for item in por_dia]

    status_map = {
        'agendado': 'Agendado',
        'confirmado': 'Confirmado',
        'concluido': 'Concluído',
        'cancelado': 'Cancelado',
    }
    labels_status = [status_map.get(item['status'], item['status']) for item in por_status]
    dados_status = [item['total'] for item in por_status]

    labels_profissional = [item['profissional__nome'] for item in por_profissional]
    dados_profissional = [item['total'] for item in por_profissional]

    labels_servico = [item['servico__nome'] for item in por_servico]
    dados_servico = [item['total'] for item in por_servico]

    context = {
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'total': agendamentos.count(),
        'total_confirmados': agendamentos.filter(status='confirmado').count(),
        'total_concluidos': agendamentos.filter(status='concluido').count(),
        'total_cancelados': agendamentos.filter(status='cancelado').count(),
        'labels_dia': json.dumps(labels_dia),
        'dados_dia': json.dumps(dados_dia),
        'labels_status': json.dumps(labels_status),
        'dados_status': json.dumps(dados_status),
        'labels_profissional': json.dumps(labels_profissional),
        'dados_profissional': json.dumps(dados_profissional),
        'labels_servico': json.dumps(labels_servico),
        'dados_servico': json.dumps(dados_servico),
    }
    return render(request, 'agendamentos/relatorios.html', context)

@login_required
def exportar_pdf(request):
    # Pega os mesmos filtros da lista
    busca = request.GET.get('busca', '')
    status = request.GET.get('status', '')
    profissional_id = request.GET.get('profissional', '')
    data_inicio = request.GET.get('data_inicio', '')
    data_fim = request.GET.get('data_fim', '')

    agendamentos = Agendamento.objects.all().order_by('-data_hora')

    if busca:
        agendamentos = agendamentos.filter(cliente__nome__icontains=busca)
    if status:
        agendamentos = agendamentos.filter(status=status)
    if profissional_id:
        agendamentos = agendamentos.filter(profissional_id=profissional_id)
    if data_inicio:
        agendamentos = agendamentos.filter(data_hora__date__gte=data_inicio)
    if data_fim:
        agendamentos = agendamentos.filter(data_hora__date__lte=data_fim)

    # Configurar resposta HTTP como PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="agendamentos.pdf"'

    doc = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=2*cm,
        bottomMargin=2*cm,
    )

    elementos = []
    styles = getSampleStyleSheet()

    # Estilo do título
    estilo_titulo = ParagraphStyle(
        'titulo',
        parent=styles['Title'],
        fontSize=18,
        textColor=colors.HexColor('#F5E642'),
        spaceAfter=4,
        fontName='Helvetica-Bold',
    )

    estilo_subtitulo = ParagraphStyle(
        'subtitulo',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#a0a0a0'),
        spaceAfter=20,
    )

    estilo_rodape = ParagraphStyle(
        'rodape',
        parent=styles['Normal'],
        fontSize=8,
        textColor=colors.HexColor('#a0a0a0'),
        alignment=TA_CENTER,
    )

    # Cabeçalho
    elementos.append(Paragraph('⚡ FitManager', estilo_titulo))
    elementos.append(Paragraph(f'Relatório de Agendamentos — gerado em {date.today().strftime("%d/%m/%Y")}', estilo_subtitulo))

    # Filtros aplicados
    filtros_texto = []
    if busca:
        filtros_texto.append(f'Cliente: {busca}')
    if status:
        filtros_texto.append(f'Status: {status}')
    if data_inicio:
        filtros_texto.append(f'De: {data_inicio}')
    if data_fim:
        filtros_texto.append(f'Até: {data_fim}')

    if filtros_texto:
        estilo_filtro = ParagraphStyle(
            'filtro',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.HexColor('#F5E642'),
            spaceAfter=12,
        )
        elementos.append(Paragraph('Filtros: ' + ' | '.join(filtros_texto), estilo_filtro))

    elementos.append(Spacer(1, 0.3*cm))

    # Tabela de agendamentos
    cabecalho = ['Data/Hora', 'Cliente', 'Profissional', 'Serviço', 'Status']
    dados = [cabecalho]

    status_map = {
        'agendado': 'Agendado',
        'confirmado': 'Confirmado',
        'concluido': 'Concluído',
        'cancelado': 'Cancelado',
    }

    for ag in agendamentos:
        dados.append([
            ag.data_hora.strftime('%d/%m/%Y %H:%M'),
            ag.cliente.nome,
            ag.profissional.nome,
            ag.servico.nome,
            status_map.get(ag.status, ag.status),
        ])

    if len(dados) == 1:
        dados.append(['Nenhum agendamento encontrado', '', '', '', ''])

    tabela = Table(dados, colWidths=[3.5*cm, 4.5*cm, 4.5*cm, 4*cm, 2.5*cm])
    tabela.setStyle(TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a1a1a')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#F5E642')),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),
        ('TOPPADDING', (0, 0), (-1, 0), 10),

        # Linhas
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor('#111111')),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.HexColor('#d0d0d0')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('TOPPADDING', (0, 1), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 1), (-1, -1), 8),

        # Linhas alternadas
        *[('BACKGROUND', (0, i), (-1, i), colors.HexColor('#161616'))
          for i in range(2, len(dados), 2)],

        # Bordas
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#2e2e2e')),
        ('ROWBACKGROUNDS', (0, 0), (-1, 0), [colors.HexColor('#1a1a1a')]),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elementos.append(tabela)
    elementos.append(Spacer(1, 0.8*cm))

    # Totais
    estilo_total = ParagraphStyle(
        'total',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#a0a0a0'),
    )
    elementos.append(Paragraph(f'Total de registros: {agendamentos.count()}', estilo_total))
    elementos.append(Spacer(1, 1*cm))
    elementos.append(Paragraph('FitManager — Sistema de Agendamentos para Personal Trainer', estilo_rodape))

    doc.build(elementos)
    return response