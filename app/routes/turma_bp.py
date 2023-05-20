from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from ..data_base import session, Turmas, Alunos, Estagios

turma_bp = Blueprint('Blueprint_turma', __name__)


def lista_todas_turmas():
   return session.query(Turmas).all()


def get_turma_por_id(turma_id):
   return session.query(Turmas).get(turma_id)


def extrair_numero_descricao(descricao_turma):
   return descricao_turma.split(":")[1].strip()


def criar_turma(descricao_turma):
   nova_turma = Turmas(descricao=descricao_turma)
   session.add(nova_turma)
   session.commit()


def atualizar_turma(turma, descricao_turma):
   turma.descricao = descricao_turma
   session.commit()


def deletar_turma(turma):
   alunos = session.query(Alunos).filter_by(turmaId=turma.id).all()
   for aluno in alunos:
      estagio = session.query(Estagios).filter_by(alunoId=aluno.id).first()
      if estagio:
         session.delete(estagio)
      session.delete(aluno)
   session.delete(turma)
   session.commit()

@turma_bp.route('/')
@turma_bp.route('/Turmas')
def tabela_turmas():
   turmas = lista_todas_turmas()
   return render_template('templates_turmas/turmas.html', turmas=turmas)


@turma_bp.route('/Nova_Turma', methods=["POST", "GET"])
def nova_Turma():
   if request.method == "POST":
      arr=[]
      descricao_turma = f"Turma: {request.form['turma']}"
      if not session.query(Turmas).filter_by(descricao=descricao_turma).first():
         arr.append("0")
         criar_turma(descricao_turma)
      else:
         arr.append(f"A {descricao_turma} já existe.")
      return jsonify(arr)
   turmas = lista_todas_turmas()
   return render_template('templates_turmas/nova_turma.html', turmas=turmas)


def turma_existente(descricao_turma, turma_id):
   turma = session.query(Turmas).filter_by(descricao=descricao_turma).first()
   return turma is not None and turma.id != turma_id

@turma_bp.route('/Editar_Turma/<int:turma_id>', methods=['GET', 'POST'])
def editar_turma(turma_id):
   turma = get_turma_por_id(turma_id)
   if request.method == "POST":
      arr = []
      descricao_turma = f"Turma: {request.form['turma']}"
      if not turma_existente(descricao_turma, turma_id):
         arr.append("0")
         atualizar_turma(turma, descricao_turma)
      else:
         arr.append(f"A {descricao_turma} já existe.")
      return jsonify(arr)
   numero = extrair_numero_descricao(turma.descricao)
   return render_template('templates_turmas/editar_turma.html', turma=turma, numero=numero)





@turma_bp.route('/EliminarTurma/<int:turma_id>', methods=['GET', 'POST'])
def eliminar_turma(turma_id):
   turma = get_turma_por_id(turma_id)
   if not turma:
      return redirect(url_for('Blueprint_turma.tabela_turmas'))
   deletar_turma(turma)
   return redirect(url_for('Blueprint_turma.tabela_turmas'))
