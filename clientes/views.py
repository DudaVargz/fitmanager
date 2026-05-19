from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente

@login_required
def lista_clientes(request):
    clientes = Cliente.objects.filter(ativo=True)
    return render(request, 'clientes/lista.html', {'clientes': clientes})

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()

        if not nome:
            messages.error(request, 'O nome do cliente é obrigatório.')
            return render(request, 'clientes/form.html', {'dados': request.POST})

        if not telefone:
            messages.error(request, 'O telefone do cliente é obrigatório.')
            return render(request, 'clientes/form.html', {'dados': request.POST})

        Cliente.objects.create(
            nome=nome,
            telefone=telefone,
            email=request.POST.get('email', ''),
            data_nascimento=request.POST.get('data_nascimento') or None,
            observacoes=request.POST.get('observacoes', ''),
        )
        messages.success(request, f'Cliente "{nome}" cadastrado com sucesso!')
        return redirect('lista_clientes')
    return render(request, 'clientes/form.html')

@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        nome = request.POST.get('nome', '').strip()
        telefone = request.POST.get('telefone', '').strip()

        if not nome or not telefone:
            messages.error(request, 'Nome e telefone são obrigatórios.')
            return render(request, 'clientes/form.html', {'cliente': cliente, 'dados': request.POST})

        cliente.nome = nome
        cliente.telefone = telefone
        cliente.email = request.POST.get('email', '')
        cliente.data_nascimento = request.POST.get('data_nascimento') or None
        cliente.observacoes = request.POST.get('observacoes', '')
        cliente.save()
        messages.success(request, f'Cliente "{nome}" atualizado com sucesso!')
        return redirect('lista_clientes')
    return render(request, 'clientes/form.html', {'cliente': cliente})

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    cliente.ativo = False
    cliente.save()
    messages.warning(request, f'Cliente "{cliente.nome}" removido.')
    return redirect('lista_clientes')