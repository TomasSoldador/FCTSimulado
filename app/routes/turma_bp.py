from flask import Blueprint, render_template, redirect, url_for, request
from ..data_base import *
from re import search

turma_bp = Blueprint('Blueprint_turma', __name__)


@turma_bp.route('/Turmas')
def tabela_turmas():
   turmas = session.query(Turmas).all()
   return render_template('templates_turmas/turmas.html', turmas=turmas)


@turma_bp.route('/Nova_Turma', methods=["POST", "GET"])
def nova_Turma():
   mensagem = None
   if request.method == "POST":
      turma = f"Turma: {request.form['turma']}"
      if not session.query(Turmas).filter_by(descricao=turma).first():
         p = Turmas(
               descricao=turma)
         session.add(p)
         session.commit()
         return redirect(url_for('Blueprint_turma.tabela_turmas'))
      else:
         turmas = session.query(Turmas).all()
         mensagem = f"A {turma} já existe."
         return render_template('templates_turmas/nova_turma.html', turmas=turmas, mensagem=mensagem)
   return render_template('templates_turmas/nova_turma.html')


@turma_bp.route('/Editar_Turma/<int:turma_id>', methods=['GET', 'POST'])
def editar_turma(turma_id):
   turma = session.query(Turmas).get(turma_id)
   if request.method == 'POST':
      nova_turma = f"Turma: {request.form['turma']}"
      if not session.query(Turmas).filter(Turmas.id != turma_id, Turmas.descricao == nova_turma).first():
         turma.descricao = nova_turma
         session.commit()
         return redirect(url_for('Blueprint_turma.tabela_turmas'))
      else:
         numero = search(r'\d+', turma.descricao).group()
         mensagem = f"A {nova_turma} já existe."
         return render_template('templates_turmas/editar_turma.html', turma=turma, numero=numero, mensagem=mensagem)

   numero = search(r'\d+', turma.descricao).group()
   return render_template('templates_turmas/editar_turma.html', turma=turma, numero=numero)


@turma_bp.route('/EliminarTurma/<int:turma_id>', methods=['GET', 'POST'])
def eliminar_turma(turma_id):
   #TODO: pergunta se temos a certeza se queremos eliminar e os riscos de tal
   alunos = session.query(Alunos).filter_by(turmaId=turma_id).all()
   for aluno in alunos:
      estagio = session.query(Estagios).filter_by(alunoId=aluno.id).first()
      if estagio:
         session.delete(estagio)
      session.delete(aluno)
   turma = session.query(Turmas).get(turma_id)
   session.delete(turma)
   session.commit()
   return redirect(url_for('Blueprint_turma.tabela_turmas'))
