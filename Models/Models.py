from sqlalchemy import Column, Integer, String, ForeignKey
from Database.database import Base
from flask_login import UserMixin
from app import login_manager
from werkzeug.security import generate_password_hash, check_password_hash


@login_manager.user_loader
def load_user(user_id):
    return Users.query.filter_by(Id= user_id).first()


class Users(Base, UserMixin):
    __tablename__ = "Users"

    Id = Column('Id', Integer, primary_key = True)
    Nome = Column("Nome", String, nullable=False)
    Sobrenome = Column("Sobrenome", String, nullable=False)
    Email = Column("Email", String(255), unique=True, nullable=False)
    AreaAtuacao = Column("AreaAtuacao", String, nullable=False)
    Supervisor = Column("SupervisorImediato", String, nullable=False)
    Cargo = Column("Cargo", String, nullable=False)
    Senha = Column("Senha", String, nullable= False)
    NivelAcesso = Column("NivelAcesso", Integer, nullable = False)

    def __init__(self, nome, sobrenome, email, areaatuacao, supervisor, cargo, nivelacesso,senha):
        self.Nome = nome
        self.Sobrenome = sobrenome
        self.Email = email
        self.AreaAtuacao = areaatuacao
        self.Supervisor = supervisor
        self.Cargo = cargo
        self.Senha = generate_password_hash(senha) #TODO: inserir hash da senha
        self.NivelAcesso = nivelacesso

    def Verifica_senha(self, senha):
        return check_password_hash(self.Senha, senha)

    def __repr__(self):
        return f"|{self.Id}|{self.Nome}|{self.Sobrenome}|{self.Email}|{self.AreaAtuacao}|{self.Supervisor}|{self.Cargo}\n"

    def get_id(self):
           return (self.Id)


    #TODO: criar uma função de validação do usuario. Olhar pacote schema

    # Atual versão: isinstance(user.Campo, str) verifica se User.Campo é uma string
    #               e user.Campo.strip() retira os espaços iniciais e finais do campo em questão
    #               caso o campo seja vazio ou contenha apenas espaços, retorna None, falhando na verificação
    #               e retornando false na validação do usuario
    def validate_user(user):
        if not isinstance(user, Users):
            print('falha de instancia')
            return False
        if not isinstance(user.Nome, str) or not user.Nome.strip():
            print('falha nome')
            return False
        if not isinstance(user.Sobrenome, str) or not user.Sobrenome.strip():
            print('falha sobrenome')
            return False   
        if not isinstance(user.Email, str) or not user.Email.strip():
            print('falha email')
            return False
        if not isinstance(user.AreaAtuacao, str) or not user.AreaAtuacao.strip():
            print('falha areatuacao')
            return False 
        if not isinstance(user.Supervisor, str) or not user.Supervisor.strip():
            print('falha supervisor')
            return False 
        if not isinstance(user.Senha, str) or not user.Senha.strip():
            print('falha senha')
            return False
        if not isinstance(user.NivelAcesso, int) or not (0 <= user.NivelAcesso):
            print('falha nivel acesso')
            print(user.NivelAcesso)
            return False  
        
        else:
            return True

class Projects(Base):
    __tablename__ = "Projects"

    Id = Column('Id', Integer, primary_key = True)
    NomeProjeto = Column("NomeProjeto   ", String, nullable=False)
    Descricao = Column("Descricao", String, nullable=False)
    Dono = Column("Dono", Integer, ForeignKey("Users.Id"), nullable=False)
    Prioridade = Column("Prioridade", String, nullable = True)

    def __init__(self, nomeprojeto, descricao, dono, prioridade = 'Aguardando classificação'):
        self.NomeProjeto = nomeprojeto
        self.Descricao = descricao
        self.Dono = dono
        self.Prioridade = prioridade

    def __repr__(self):
            return f"|{self.Id}|{self.NomeProjeto}|{self.Dono}||{self.Prioridade}\n"

    def validate_project(project):
        if not isinstance(project, Projects):
            return False
        if not isinstance(project.NomeProjeto, str) or not project.NomeProjeto.strip():
            return False
        if not isinstance(project.Descricao, str) or not project.Descricao.strip():
            return False
        if not isinstance(project.Dono, int) or not (0 <= project.Dono):
            return False 
        if not isinstance(project.Prioridade, str) or not project.Prioridade.strip():
            return False
        else:
            return True