from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Servico

@login_required
def lista_servicos(request):
    servicos = Servico.objects.filter(ativo=True)
    return render(request, 'servicos/lista.html', {'servicos': servicos})

@login_required
def cadastrar_servico(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        preco = request.POST.get('preco', '').strip()
        duracao = request.POST.get('duracao_minutos', '').strip()

        if not nome or not preco or not duracao:
            messages.error(request, 'Nome, duração e preço são obrigatórios.')
            return render(request, 'servicos/form.html', {'dados': request.POST})

        Servico.objects.create(
            nome=nome,
            descricao=request.POST.get('descricao', ''),
            duracao_minutos=duracao,
            preco=preco,
        )
        messages.success(request, f'Serviço "{nome}" cadastrado com sucesso!')
        return redirect('lista_servicos')
    return render(request, 'servicos/form.html')

@login_required
def editar_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        preco = request.POST.get('preco', '').strip()
        duracao = request.POST.get('duracao_minutos', '').strip()

        if not nome or not preco or not duracao:
            messages.error(request, 'Nome, duração e preço são obrigatórios.')
            return render(request, 'servicos/form.html', {'servico': servico})

        servico.nome = nome
        servico.descricao = request.POST.get('descricao', '')
        servico.duracao_minutos = duracao
        servico.preco = preco
        servico.save()
        messages.success(request, f'Serviço "{nome}" atualizado com sucesso!')
        return redirect('lista_servicos')
    return render(request, 'servicos/form.html', {'servico': servico})

@login_required
def excluir_servico(request, pk):
    servico = get_object_or_404(Servico, pk=pk)
    servico.ativo = False
    servico.save()
    messages.warning(request, f'Serviço "{servico.nome}" removido.')
    return redirect('lista_servicos')