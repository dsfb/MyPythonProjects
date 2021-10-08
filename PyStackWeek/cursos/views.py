from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Aulas, Cursos


def home(request):
    if request.session.get('usuario'):
        cursos = Cursos.objects.all()
        request_usuario = request.session.get('usuario')
        return render(request, 'home.html', {'cursos': cursos, 'request_usuario': request_usuario})
    else:
        return redirect('/auth/login/?status=2')

def curso(request, id):
    if request.session.get('usuario'):
        aulas = Aulas.objects.filter(curso = id)
        request_usuario = request.session.get('usuario')
        return render(request, 'curso.html', {'aulas': aulas, 'request_usuario': request_usuario})
    else:
        return redirect('/auth/login/?status=2')

def aula(request, id):
    if request.session.get('usuario'):
        aula = Aulas.objects.get(id = id)
        usuario_id = request.session['usuario']
        comentarios = Comentarios.objects.filter(aula = aula).order_by('-data')

        request_usuario = request.session.get('usuario')
        usuario_avaliou = NotasAulas.objects.filter(aula_id = id).filter(usuario_id = request_usuario)
        avaliacoes = NotasAulas.objects.filter(aula_id = id)



        return render(request, 'aula.html', {'aula': aula,
                                            'usuario_id': usuario_id,
                                            'comentarios': comentarios,
                                            'request_usuario': request_usuario,
                                            'usuario_avaliou': usuario_avaliou,
                                            'avaliacoes': avaliacoes})
    else:
        return redirect('/auth/login/?status=2')

def comentarios(request):
    usuario_id = int(request.POST.get('usuario_id'))
    comentario = request.POST.get('comentario')
    aula_id = int(request.POST.get('aula_id'))

    comentario_instancia = Comentarios(usuario_id = usuario_id,
                                       comentario = comentario,
                                       aula_id = aula_id)
    comentario_instancia.save()

    comentarios = Comentarios.objects.filter(aula = aula_id).order_by('-data')
    somente_nomes = [i.usuario.nome for i in comentarios]
    somente_comentarios = [i.comentario for i in comentarios]
    comentarios = list(zip(somente_nomes, somente_comentarios))

    return HttpResponse(json.dumps({'status': '1', 'comentarios': comentarios }))

def processa_avaliacao(request):
    if request.session.get('usuario'):

        avaliacao = request.POST.get('avaliacao')
        aula_id = request.POST.get('aula_id')
        
        usuario_id = request.session.get('usuario')

        usuario_avaliou = NotasAulas.objects.filter(aula_id = aula_id).filter(usuario_id = usuario_id)

        if not usuario_avaliou:
            nota_aulas = NotasAulas(aula_id = aula_id,
                                    nota = avaliacao,
                                    usuario_id = usuario_id,
                                    )
            nota_aulas.save()
            return redirect(f'/home/aula/{aula_id}')
        else:
            return redirect('/auth/login/')

    else:
        return redirect('/auth/login/')
