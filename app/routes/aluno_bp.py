from flask import Blueprint, jsonify, render_template, redirect, url_for, request
from ..data_base import *


aluno_bp = Blueprint('Blueprint_aluno', __name__)

def get_todos_alunos():
   return session.query(Alunos).all()

def get_todas_turmas():
   return session.query(Turmas).all()

@aluno_bp.route('/Alunos', methods=["POST", "GET"])
def tabela_alunos():
   try:
      alunos = get_todos_alunos()
      turmas = get_todas_turmas()
      return render_template('templates_alunos/alunos.html', alunos=alunos, turmas=turmas)

   except:
      session.rollback()
      raise


def obter_nome_abreviado(nome_completo):
   partes_nome = nome_completo.split()
   primeiro_nome = partes_nome[0]
   ultimo_sobrenome = partes_nome[-1]
   nome_abreviado = f"{primeiro_nome} {ultimo_sobrenome}"
   return nome_abreviado

@aluno_bp.route('/get_alunos', methods=["POST", "GET"])
def get_alunos():
   try:
      alunos = []
      turma = session.query(Turmas).first()
      if request.method == "POST" and request.json.get("selected_value"):
         selected_value = request.json.get("selected_value")
         turma = session.query(Turmas).filter_by(descricao=selected_value).first()
         alunos = session.query(Alunos).filter_by(turmaId=turma.id).all()

         alunos_json = []
         for aluno in alunos:
            nome_abreviado = obter_nome_abreviado(aluno.nome)
            aluno_dict = {
                  'id': aluno.id,
                  'turmaId': aluno.turmaId,
                  'nr': aluno.nr,
                  'nome': aluno.nome,
                  'nome_abreviado': nome_abreviado,
                  'morada': aluno.morada,
                  'cod_postal': aluno.cod_postal,
                  'cartao_cidadao': aluno.cartao_cidadao,
                  'validade_cc': aluno.validade_cc,
                  'nif': aluno.nif
            }
            alunos_json.append(aluno_dict)

         return jsonify(alunos_json)
      
      # Retornar uma resposta vazia ou uma mensagem de erro caso a condição não seja atendida
      return jsonify([])  # ou return jsonify({'error': 'Mensagem de erro'})

   except:
      session.rollback()
      raise




@aluno_bp.route('/Novo_Aluno', methods=["POST", "GET"])
def novo_aluno():
   try:
      if request.method == 'POST':
         arr = []
         turmas = request.form['turmas']
         numero = f"L{request.form['numero']}"
         Nome = request.form['Nome']
         morada = request.form['morada']
         codigo_postal = request.form['codigo_postal']
         localidade = request.form['localidade']
         cartao_cidadao = request.form['cartao_cidadao']
         validade_cc = request.form['validade_cc']
         nif = request.form['nif']
         codigo_postal = codigo_postal + " " + localidade
         aluno_existente = session.query(Alunos).filter(
            (Alunos.cartao_cidadao == cartao_cidadao) | 
            (Alunos.nif == nif) | 
            (Alunos.nr == numero)
         ).first()
         
         if aluno_existente:
            if aluno_existente.cartao_cidadao == cartao_cidadao:
               arr.append(f'O cartão de cidadão {cartao_cidadao}, já existe')
            elif aluno_existente.nif == nif:
               arr.append(f'O NIF {nif}, já existe')
            elif aluno_existente.nr == numero:
               arr.append(f'O aluno número {numero}, já existe')
         else:
            arr.append("0")
            novo_aluno = Alunos(
               nr=numero,
               nome=Nome,
               morada=morada,
               cod_postal=codigo_postal,
               cartao_cidadao=cartao_cidadao,
               validade_cc=validade_cc,
               nif=nif)
            turma = session.query(Turmas).filter_by(descricao=turmas).first()
            novo_aluno.turmaId = turma.id
            session.add(novo_aluno)
            session.commit()
         return jsonify(arr)
      turmas = (session.query(Turmas).all())
      return render_template('templates_alunos/novo_aluno.html', turmas=turmas)

   except:
      session.rollback()
      raise



@aluno_bp.route('/Editar_Aluno/<int:aluno_id>', methods=["POST", "GET"])
def editar_alunos(aluno_id):
   try:
      aluno = session.query(Alunos).get(aluno_id)
      if request.method == 'POST':
         arr=[]
         turmas = request.form['turmas']
         numero = f"L{request.form['numero']}"
         cartao_cidadao = request.form['cartao_cidadao']
         nif = request.form['nif']
         codigo_postal = request.form['codigo_postal']
         localidade = request.form['localidade']
         codigo_postal = codigo_postal + " " + localidade

         aluno_existe = session.query(Alunos).filter(
            (Alunos.id != aluno_id),
            (Alunos.cartao_cidadao == cartao_cidadao) |
            (Alunos.nif == nif) |
            (Alunos.nr == numero)
         ).first()

         if aluno_existe:
            if aluno_existe.cartao_cidadao == cartao_cidadao:
               arr.append(f'O cartão de cidadão {cartao_cidadao}, já existe')
            elif aluno_existe.nif == nif:
               arr.append(f'O NIF {nif}, já existe')
            else:
               arr.append(f'O aluno número {numero}, já existe')
            turmas = session.query(Turmas).all()
            turmaEdit = session.query(Turmas).filter_by(
               id=aluno.turmaId).first().descricao
         else:
            arr.append("0")
            aluno.nr = numero
            aluno.nome = request.form['Nome']
            aluno.morada = request.form['morada']
            aluno.cod_postal = codigo_postal
            aluno.cartao_cidadao = cartao_cidadao
            aluno.validade_cc = request.form['validade_cc']
            aluno.nif = nif
            turma = session.query(Turmas).filter_by(descricao=turmas).first()
            aluno.turmaId = turma.id
            session.commit()
         return jsonify(arr)
      turmas = session.query(Turmas).all()
      turmaEdit = session.query(Turmas).filter_by(
         id=aluno.turmaId).first().descricao
      localidade = aluno.cod_postal[9:]
      codigoPostal = aluno.cod_postal[:8]
      return render_template('templates_alunos/editar_aluno.html', turmas=turmas, aluno=aluno, numero=aluno.nr[1:], turmaEdit=turmaEdit, localidade=localidade, codigoPostal=codigoPostal)

   except:
      session.rollback()
      raise


@aluno_bp.route('/EliminarAluno/<int:aluno_id>', methods=['GET', 'POST'])
def eliminar_aluno(aluno_id):
   try:
      aluno = session.query(Alunos).get(aluno_id)
      estagio = session.query(Estagios).filter_by(alunoId=aluno.id).first()
      if estagio:
         session.delete(estagio)
      session.delete(aluno)
      session.commit()
      return redirect(url_for('Blueprint_aluno.tabela_alunos'))

   except:
      session.rollback()
      raise

