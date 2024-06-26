import re
from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..data_base import session, Estagios, Entidade, Turmas, Alunos

estagio_bp = Blueprint('Blueprint_estagio', __name__)


def obter_nome_abreviado(nome_completo):
   partes_nome = nome_completo.split()
   primeiro_nome = partes_nome[0]
   ultimo_sobrenome = partes_nome[-1]
   nome_abreviado = f"{primeiro_nome} {ultimo_sobrenome}"
   return nome_abreviado

# Função de verificação de email
def verificar_email(email):
   pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
   return re.match(pattern, email) is not None

@estagio_bp.route('/')
@estagio_bp.route('/Estagios')
def tabela_estagios():
   try:
      estagios = session.query(Estagios).all()
      entidades = session.query(Entidade).all()
      turmas = session.query(Turmas).all()
      alunos = session.query(Alunos).all()
      for estagio in estagios:
         aluno = session.query(Alunos).filter_by(id=estagio.alunoId).first()
         estagio.nome_aluno = aluno.nome
      for estagio in estagios:
         entidade = session.query(Entidade).filter_by(id=estagio.entidadeId).first()
         estagio.nome_entidade = entidade.nome
      return render_template('templates_estagios/estagios.html', estagios=estagios, entidades=entidades, turmas=turmas, alunos=alunos)
   except:
      session.rollback()
      raise

@estagio_bp.route('/get_estagios', methods=["POST", "GET"])
def get_alunos():
   try:
      turma = session.query(Turmas).first()
      estagios = None
      if request.method == "POST" and request.json.get("selected_value"):
         selected_value = request.json.get("selected_value")
         turma = session.query(Turmas).filter_by(
               descricao=selected_value).first()
         alunos = session.query(Alunos).filter_by(turmaId=turma.id).all()
         alunos_ids = [aluno.id for aluno in alunos]
         estagios = session.query(Estagios).filter(Estagios.alunoId.in_(alunos_ids)).all()
      estagios_json = []
      if estagios != None:
         for estagio in estagios:
            aluno = session.query(Alunos).filter_by(id=estagio.alunoId).first()
            entidade = session.query(Entidade).filter_by(id=estagio.entidadeId).first()
            estagios_json.append({'id': estagio.id, 'nome_abreviado': obter_nome_abreviado(aluno.nome), 'entidade': entidade.nome, 'data_inicio': str(estagio.data_inicio.strftime('%d-%m-%Y')), 'data_fim': str(estagio.data_fim.strftime('%d-%m-%Y'))})
      return jsonify(estagios_json)

   except:
      session.rollback()
      raise

@estagio_bp.route('/get_options', methods=['GET', "POST"])
def get_options():
   try:
      turma = session.query(Turmas).first()
      if request.method == "POST" and request.json.get("selected_value"):
         selected_value = request.json.get("selected_value")
         if selected_value == "nenhum":
            alunos = session.query(Alunos).all()
         else:
            turma = session.query(Turmas).filter_by(
                  descricao=selected_value).first()
            id_turma = turma.id
            alunos = session.query(Alunos).filter_by(turmaId=id_turma).all()
      return jsonify([{'id': aluno.id, 'nome': obter_nome_abreviado(aluno.nome)} for aluno in alunos])

   except:
      session.rollback()
      raise



@estagio_bp.route('/get_info_entidade', methods=['GET', 'POST'])
def get_info_entidade():
   try:
      if request.method == "POST" and request.json.get("nome_entidade"):
         nome_entidade = request.json.get("nome_entidade")
         entidade = session.query(Entidade).filter_by(nome=nome_entidade).first()
         codigo_postal, localidade = entidade.cod_postal.split(" ")
      return jsonify({'morada': str(entidade.morada), 'cod_postal': str(codigo_postal), 'localidade': str(localidade)})

   except:
      session.rollback()
      raise

@estagio_bp.route('/Novo_Estagio', methods=["POST", "GET"])
def novo_estagios():
   try:
      turmas = session.query(Turmas).all()
      entidade = session.query(Entidade).all()
      alunos = session.query(Alunos).all()
      if request.method == 'POST':
         arr=[]
         selected_aluno = request.form['alunos']
         entidades_selecionada = request.form['entidades']
         data_inicio = request.form['data_inicio']
         data_fim = request.form['data_fim']
         morada = request.form['morada']
         cod_postal = request.form['cod_postal']
         localidade = request.form['localidade']
         cod_postal = cod_postal + " " + localidade
         tutor = request.form['Tutor']
         email_tutor = request.form['EmailTutor']
         orientador = request.form['Orintador']

         

         estagio_existente = session.query(Estagios).filter(Estagios.alunoId == selected_aluno).first()

         if estagio_existente or selected_aluno == "nenhum" or entidades_selecionada == "nada":
            if selected_aluno == "nenhum":
               arr.append(f'Selecione um aluno')
            elif estagio_existente:
               name = session.query(Alunos).filter_by(id=selected_aluno).first()
               arr.append(f'O aluno: {name.nome_abreviado}, já está em um estágio')
            elif entidades_selecionada == "nada":
               arr.append(f'Selecione uma entidade')
         elif not verificar_email(email_tutor):  # Verificar o email do tutor
            arr.append("Email do tutor inválido")
         else:
            arr.append("0")
            entidades_selecionada = session.query(Entidade).filter_by(nome=entidades_selecionada).first()
            p = Estagios(
               alunoId=selected_aluno,
               entidadeId=entidades_selecionada.id,
               data_inicio=data_inicio,
               data_fim=data_fim,
               morada=morada,
               cod_postal=cod_postal,
               tutor=tutor,
               email_tutor=email_tutor,
               orientador=orientador
            )

            session.add(p)
            session.commit()
         return jsonify(arr)
      return render_template('templates_estagios/novo_estagio.html', turmas=turmas, entidade=entidade, alunos=alunos)

   except:
      session.rollback()
      raise




@estagio_bp.route('/Editar_Estagio/<int:estagio_id>', methods=["POST", "GET"])
def editar_estagios(estagio_id):
   try:
      turmas = session.query(Turmas).all()
      entidade = session.query(Entidade).all()
      alunos = session.query(Alunos).all()
      estagio = session.query(Estagios).get(estagio_id)
      if request.method == 'POST':
         arr = []
         alunoId = request.form['alunos']
         entidades = request.form['entidades']

         estagio_existente = session.query(Estagios).filter(
               (Estagios.id != estagio_id) &
               (
                  (Estagios.alunoId == alunoId)
               )
         ).first()

         if estagio_existente or alunoId == "nenhum" or entidades == "nada":
               if alunoId == "nenhum":
                  arr.append(f'Selecione um aluno')
               elif estagio_existente:
                  name = session.query(Alunos).filter_by(id=alunoId).first()
                  arr.append(f'O aluno: {name.nome_abreviado}, já está em um estágio')
               elif entidades == "nada":
                  arr.append(f'Selecione uma entidade')

         else:
               arr.append("0")
               estagio.alunoId = alunoId
               estagio.data_inicio = request.form['data_inicio']
               estagio.data_fim = request.form['data_fim']
               estagio.morada = request.form['morada']
               cod_postal = request.form['cod_postal']
               localidade = request.form['localidade']
               estagio.cod_postal = cod_postal + " " + localidade
               estagio.tutor = request.form['Tutor']
               estagio.email_tutor = request.form['EmailTutor']
               estagio.orientador = request.form['Orintador']

               # Verificação do email do tutor
               email_tutor = request.form['EmailTutor']
               if not verificar_email(email_tutor):
                  arr.append(f'O email do tutor é inválido.')

               entidade = session.query(Entidade).filter_by(nome=entidades).first()
               estagio.entidadeId = entidade.id
               session.commit()
         return jsonify(arr)

      localidade = estagio.cod_postal[9:]
      codigoPostal = estagio.cod_postal[:8]
      return render_template('templates_estagios/editar_estagio.html', estagio=estagio, turmas=turmas,
                              entidade=entidade, id_entidade=estagio.entidadeId, alunos=alunos,
                              id_alunos=estagio.alunoId, localidade=localidade, codigoPostal=codigoPostal)

   except:
      session.rollback()
      raise

@estagio_bp.route('/Eliminar_Estagio/<int:estagio_id>', methods=["POST", "GET"])
def eliminar_estagios(estagio_id):
   try:
      estagio = session.query(Estagios).get(estagio_id)
      session.delete(estagio)
      session.commit()
      return redirect(url_for('Blueprint_estagio.tabela_estagios'))

   except:
      session.rollback()
      raise
