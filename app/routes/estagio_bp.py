from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from ..data_base import session, Estagios, Entidade, Turmas, Alunos


estagio_bp = Blueprint('Blueprint_estagio', __name__)


@estagio_bp.route('/')
@estagio_bp.route('/Estagios')
def tabela_estagios():
   # TODO: caso uma entidade ou um aluno seja apagado deve apagar tbm os estagios que ele esta
   estagios = session.query(Estagios).all()
   entidade = session.query(Entidade).all()
   turmas = session.query(Turmas).all()
   alunos = session.query(Alunos).all()
   for estagio in estagios:
      aluno = session.query(Alunos).filter_by(id=estagio.alunoId).first()
      estagio.nome_aluno = aluno.nome
   for estagio in estagios:
      entidade = session.query(Entidade).filter_by(id=estagio.entidadeId).first()
      estagio.nome_entidade = entidade.nome
   return render_template('templates_estagios/estagios.html', estagios=estagios, entidade=entidade, turmas=turmas, alunos=alunos)

@estagio_bp.route('/get_estagios', methods=["POST", "GET"])
def get_alunos():
   turma = session.query(Turmas).first()
   estagios = None
   if request.method == "POST" and request.json.get("selected_value"):
      selected_value = request.json.get("selected_value")
      if selected_value == "todos":
         estagios = session.query(Estagios).all()
      else:
         turma = session.query(Turmas).filter_by(
               descricao=selected_value).first()
         id_turma = turma.id
         alunos = session.query(Alunos).filter_by(turmaId=id_turma).all()
         alunos_ids = [aluno.id for aluno in alunos]
         estagios = session.query(Estagios).filter(Estagios.alunoId.in_(alunos_ids)).all()
   estagios_json = []
   if estagios != None:
      for estagio in estagios:
         aluno = session.query(Alunos).filter_by(id=estagio.alunoId).first()
         entidade = session.query(Entidade).filter_by(id=estagio.entidadeId).first()
         estagios_json.append({'id': estagio.id, 'aluno': aluno.nome, 'entidade': entidade.nome, 'data_inicio': str(estagio.data_inicio.strftime('%d-%m-%Y')), 'data_fim': str(estagio.data_fim.strftime('%d-%m-%Y'))})
   return jsonify(estagios_json)



@estagio_bp.route('/Novo_Estagio', methods=["POST", "GET"])
def novo_estagios():
   turmas = session.query(Turmas).all()
   entidade = session.query(Entidade).all()
   alunos = session.query(Alunos).all()
   if request.method == 'POST':
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
      entidades_selecionada = session.query(Entidade).filter_by(nome=entidades_selecionada).first()
      entidadeId = entidades_selecionada.id
      if selected_aluno != 'nenhum':
         p = Estagios(alunoId=selected_aluno, entidadeId=entidadeId, data_inicio=data_inicio, data_fim=data_fim,
                     morada=morada, cod_postal=cod_postal, tutor=tutor, email_tutor=email_tutor, orientador=orientador)
         session.add(p)
         session.commit()
         return redirect(url_for('Blueprint_estagio.tabela_estagios'))
   return render_template('templates_estagios/novo_estagio.html', turmas=turmas, entidade=entidade, alunos=alunos)

@estagio_bp.route('/get_options', methods=['GET', "POST"])
def get_options():
   turma = session.query(Turmas).first()
   if request.method == "POST" and request.json.get("selected_value"):
      selected_value = request.json.get("selected_value")
      if selected_value == "todos":
         alunos = session.query(Estagios).all()
      else:
         turma = session.query(Turmas).filter_by(
               descricao=selected_value).first()
         id_turma = turma.id
         alunos = session.query(Alunos).filter_by(turmaId=id_turma).all()
   return jsonify([{'id': aluno.id, 'nome': aluno.nome_abreviado} for aluno in alunos])

@estagio_bp.route('/get_info_entidade', methods=['GET', 'POST'])
def get_info_entidade():
   if request.method == "POST" and request.json.get("nome_entidade"):
      nome_entidade = request.json.get("nome_entidade")

      entidade = session.query(Entidade).filter_by(nome=nome_entidade).first()
      codigo_postal, localidade = entidade.cod_postal.split(" ")
   return jsonify({'morada': str(entidade.morada), 'cod_postal': str(codigo_postal), 'localidade': str(localidade)})


@estagio_bp.route('/Editar_Estagio/<int:estagio_id>', methods=["POST", "GET"])
def editar_estagios(estagio_id):
   estagio = session.query(Estagios).get(estagio_id)
   if request.method == 'POST':
      estagio.data_inicio = request.form['data_inicio']
      estagio.data_fim = request.form['data_fim']
      estagio.morada = request.form['morada']
      cod_postal = request.form['cod_postal']
      localidade = request.form['localidade']
      estagio.cod_postal = cod_postal + " " + localidade
      estagio.tutor = request.form['Tutor']
      estagio.email_tutor = request.form['EmailTutor']
      estagio.orientador = request.form['Orintador']
      alunos = request.form['alunos']
      estagio.alunoId = alunos
      entidades = request.form['entidades']
      entidade = session.query(Entidade).filter_by(nome=entidades).first()
      estagio.entidadeId = entidade.id
      session.commit()
      return redirect(url_for('Blueprint_estagio.tabela_estagios'))
   localidade = estagio.cod_postal[9:]
   codigoPostal = estagio.cod_postal[:8]
   turmas = session.query(Turmas).all()
   entidade = session.query(Entidade).all()
   alunos = session.query(Alunos).all()
   return render_template('templates_estagios/editar_estagio.html', estagio=estagio, turmas=turmas, entidade=entidade, id_entidade=estagio.entidadeId, alunos=alunos, id_alunos=estagio.alunoId,  localidade=localidade, codigoPostal=codigoPostal)


@estagio_bp.route('/Eliminar_Estagio/<int:estagio_id>', methods=["POST", "GET"])
def eliminar_estagios(estagio_id):
   estagio = session.query(Estagios).get(estagio_id)
   session.delete(estagio)
   session.commit()
   return redirect(url_for('Blueprint_estagio.tabela_estagios'))
