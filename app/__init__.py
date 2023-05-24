from flask import Flask
from .routes.turma_bp import turma_bp
from .routes.entidade_bp import entidade_bp
from .routes.aluno_bp import aluno_bp
from .routes.estagio_bp import estagio_bp
from .routes.docs_bp import docs_bp



app = Flask(__name__)
app.register_blueprint(turma_bp)
app.register_blueprint(aluno_bp)
app.register_blueprint(entidade_bp)
app.register_blueprint(estagio_bp)
app.register_blueprint(docs_bp)



app.debug = True
if __name__ == '__main__':
   app.run()



   # TODO: tirar o nome abreviado da base de dados e fazer com que apareça na tabela sem ir buscar a base de dados indo buscar ao nome completo