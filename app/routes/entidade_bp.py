from flask import Blueprint, render_template, redirect, url_for, request
from ..data_base import *

entidade_bp = Blueprint('Blueprint_entidade', __name__)


@entidade_bp.route('/Entidades')
def tabela_entidades():
   #listar as todas as entidades na pagina principal das entidades
   entidades = session.query(Entidade).all()
   return render_template('templates_entidades/entidades.html', entidades=entidades)


@entidade_bp.route('/Nova_Entidade', methods=["POST", "GET"])
def nova_entidade():
   if request.method == "POST":
      nome = request.form['Nome']
      morada = request.form['morada']
      cod_postal = request.form['cod_postal']
      localidade = request.form['localidade']
      nif = request.form['nif']
      pessoa_responsavel = request.form['pessoa_responsavel']
      cargo_pessoa_responsavel = request.form['cargo_pessoa_responsavel']
      cod_postal = cod_postal + " " + localidade

      entidade_existe = session.query(Entidade).filter(
         (
            (Entidade.nome == nome) |
            (Entidade.morada == morada) |
            (Entidade.cod_postal == cod_postal) |
            (Entidade.nif == nif)
         )
      ).first()

      if entidade_existe:
         if entidade_existe.morada == morada:
               mensagem = f'A morada {morada}, já existe'
         elif entidade_existe.nif == nif:
               mensagem = f'O NIF {nif}, já existe'
         elif entidade_existe.nome == nome:
               mensagem = f'Esse nome da entidade: {nome}, ja esta registado'
         elif entidade_existe.cod_postal == cod_postal:
               mensagem = f'O {cod_postal} ja existe'

         return render_template('templates_entidades/nova_entidade.html', mensagem=mensagem)
      
      p = Entidade(
         nome=nome, 
         morada=morada, 
         cod_postal=cod_postal, 
         nif=nif,
         pessoa_responsavel=pessoa_responsavel, 
         cargo_pessoa_responsavel=cargo_pessoa_responsavel
      )

      session.add(p)
      session.commit()
      return redirect(url_for('Blueprint_entidade.tabela_entidades'))
   
   return render_template('templates_entidades/nova_entidade.html')



@entidade_bp.route('/Editar_Entidade/<int:entidades_id>', methods=["POST", "GET"])
def editar_entidade(entidades_id):
   entidade = session.query(Entidade).get(entidades_id)
   if request.method == 'POST':
      nome = request.form['Nome']
      morada = request.form['morada']
      cod_postal = request.form['cod_postal']
      localidade = request.form['localidade']
      nif = request.form['nif']
      pessoa_responsavel = request.form['pessoa_responsavel']
      cargo_pessoa_responsavel = request.form['cargo_pessoa_responsavel']

      entidade_existe = session.query(Entidade).filter(
         (Entidade.id != entidades_id) &
         (
            (Entidade.nome == nome) |
            (Entidade.morada == morada) |
            (Entidade.cod_postal == cod_postal) |
            (Entidade.nif == nif)
         )
      ).first()

      if entidade_existe:
         mensagem = "os seguintes atributos ja existem: "
         if entidade_existe.nome == nome:
            mensagem = f'O nif {nome}, já existe'
         if entidade_existe.morada == morada:
            mensagem = f'O nif {morada}, já existe'
         if entidade_existe.cod_postal == cod_postal:
            mensagem = f'O nif {cod_postal}, já existe'
         if entidade_existe.nif == nif:
            mensagem = f'O nif {nif}, já existe'

         localidade = entidade.cod_postal[9:]
         codigoPostal = entidade.cod_postal[:8]
         
         return render_template('templates_entidades/editar_entidade.html', entidade=entidade, localidade=localidade, codigoPostal=codigoPostal, mensagem=mensagem)
      
      entidade.nome = nome
      entidade.morada = morada
      entidade.cod_postal = cod_postal + " " + localidade
      entidade.nif = nif
      entidade.pessoa_responsavel = pessoa_responsavel
      entidade.cargo_pessoa_responsavel = cargo_pessoa_responsavel

      session.commit()
      return redirect(url_for('Blueprint_entidade.tabela_entidades'))

   localidade = entidade.cod_postal[9:]
   codigoPostal = entidade.cod_postal[:8]
   print(localidade)
   return render_template('templates_entidades/editar_entidade.html', entidade=entidade, localidade=localidade, codigoPostal=codigoPostal)



@entidade_bp.route('/EliminarEntidade/<int:entidades_id>', methods=['GET', 'POST'])
def eliminar_entidade(entidades_id):
   entidades = session.query(Entidade).get(entidades_id)
   estagios = session.query(Estagios).filter_by(entidadeId=entidades_id).all()
   for estagio in estagios:
      session.delete(estagio)
   session.delete(entidades)
   session.commit()
   return redirect(url_for('Blueprint_entidade.tabela_entidades'))
