from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profissional

@login_required
def lista_profissionais(request):
    profissionais = Profissional.objects.filter(ativo=True)
    return render(request, 'profissionais/lista.html', {'profissionais': profissionais})

@login_required
def cadastrar_profissional(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        especialidade = request.POST.get('especialidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()

        if not nome or not especialidade or not telefone:
            messages.error(request, 'Nome, especialidade e telefone são obrigatórios.')
            return render(request, 'profissionais/form.html', {'dados': request.POST})

        Profissional.objects.create(
            nome=nome,
            especialidade=especialidade,
            telefone=telefone,
            email=request.POST.get('email', ''),
        )
        messages.success(request, f'Profissional "{nome}" cadastrado com sucesso!')
        return redirect('lista_profissionais')
    return render(request, 'profissionais/form.html')

@login_required
def editar_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        especialidade = request.POST.get('especialidade', '').strip()
        telefone = request.POST.get('telefone', '').strip()

        if not nome or not especialidade or not telefone:
            messages.error(request, 'Nome, especialidade e telefone são obrigatórios.')
            return render(request, 'profissionais/form.html', {'profissional': profissional})

        profissional.nome = nome
        profissional.especialidade = especialidade
        profissional.telefone = telefone
        profissional.email = request.POST.get('email', '')
        profissional.save()
        messages.success(request, f'Profissional "{nome}" atualizado com sucesso!')
        return redirect('lista_profissionais')
    return render(request, 'profissionais/form.html', {'profissional': profissional})

@login_required
def excluir_profissional(request, pk):
    profissional = get_object_or_404(Profissional, pk=pk)
    profissional.ativo = False
    profissional.save()
    messages.warning(request, f'Profissional "{profissional.nome}" removido.')
    return redirect('lista_profissionais')