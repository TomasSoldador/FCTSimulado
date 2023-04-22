from flask import Blueprint, redirect, url_for
from ..data_base import *
from docx import Document
from docx.table import Table
from re import search

docs_bp = Blueprint('Blueprint_docs', __name__)

# TODO: meter as datas no documentos

def replace_text(doc, repor):
   for paragrafo in doc.paragraphs:
      for antigo, novo in repor.items():
         if antigo in paragrafo.text:
               paragrafo.text = paragrafo.text.replace(antigo, novo)
   
   for tabela in doc.tables:
      for linha in tabela.rows:
         for celula in linha.cells:
               for antigo, novo in repor.items():
                  if antigo in celula.text:
                     celula.text = celula.text.replace(antigo, novo)

@docs_bp.route('/Baixar/<int:estagio_id>', methods=["POST", "GET"])
def baixar(estagio_id):
   estagio = session.query(Estagios).filter_by(id=estagio_id).first()
   aluno = session.query(Alunos).filter_by(id=estagio.alunoId).first()
   turma = session.query(Turmas).filter_by(id=aluno.turmaId).first()
   entidade = session.query(Entidade).filter_by(id=estagio.entidadeId).first()
   numero = search(r'\d+', turma.descricao).group()

   repor = {
      '[nome_aluno]': aluno.nome,
      '[turma]': numero,
      '[nr_aluno]': aluno.nr,
      '[orientador]': estagio.orientador,
      '[tutor]': estagio.tutor,
      '[Nome da Entidade/Empresa]': entidade.nome,
      '[Número de Contribuinte Entidade]': entidade.nif,
      '[Morada Entidade]': entidade.morada,
      '[Nome Completo]': entidade.pessoa_responsavel,
      '[Cargo/Função]': entidade.cargo_pessoa_responsavel,
      '[Nome Completo do Aluno]': aluno.nome,
      '[Número do CC]': aluno.cartao_cidadao,
      '[dd/mm/aaaa]': aluno.validade_cc.strftime("%d/%m/%Y"),
      '[Número de Contribuinte Aluno]': aluno.nif,
      '[Morada Aluno]': aluno.morada,
      '[nome]': aluno.nome,
   }

   doc1 = Document('app/docs/Folha de Presencas e Registo de Atividades Semanal.docx')
   replace_text(doc1, repor)
   doc1.save(f'Folha de Presencas e Registo de Atividades Semanal - {aluno.nome}.docx')

   doc2 = Document('app/docs/Plano de FCT.docx')
   replace_text(doc2, repor)
   doc2.save(f'Plano de FCT - {aluno.nome}.docx')

   doc3 = Document('app/docs/Grelha de Avaliacao da FCT.docx')
   replace_text(doc3, repor)
   doc3.save(f'Grelha de Avaliacao da FCT - {aluno.nome}.docx')

   doc4 = Document('app/docs/Protocolo de FCT.docx')
   replace_text(doc4, repor)
   doc4.save(f'Protocolo de FCT - {aluno.nome}.docx')

   doc5 = Document('app/docs/Plano Individual de FCT.docx')
   replace_text(doc5, repor)
   doc5.save(f'Plano Individual de FCT - {aluno.nome}.docx')

   return redirect(url_for('Blueprint_estagio.tabela_estagios'))
