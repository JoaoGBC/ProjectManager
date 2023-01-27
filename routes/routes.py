from app import app, login_manager
from flask import render_template, redirect, request
from Models.Models import Users, Projects
from flask_login import login_user, logout_user, login_required, current_user
from Database.database import scoped_session, sessionLocal
from copy import deepcopy

# @login_manager.user_loader
# def load_user(user_id):
#     return Users.query.filter_by(Id= user_id).first()

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    email = request.form['Email']
    senha = request.form['Senha']
    usuario = Users.query.filter(Users.Email == email).first()
    if(not usuario or not usuario.Verifica_senha(senha)):
        #TODO: inserir flash usuario ou senha incorreta
        return redirect('/')
    else:
        login_user(usuario)
        return redirect('/userView')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')


@app.route('/userView')
@login_required
def userView():
    db = sessionLocal()
    projects = Projects.query.filter(Projects.Dono == current_user.get_id()).all()
    return render_template('userView.html', projects = projects)

@app.route('/createNewProject', methods=['GET', 'POST'])
@login_required
def createNewProject():
    if(request.method == 'GET'):
        return render_template('newProject.html')
    if(request.method == 'POST'):
        project = Projects(request.form['NomeProjeto'],
                           request.form['Descricao'],
                           current_user.get_id())
        if(Projects.validate_project(project)):
            db = sessionLocal()
            db.add(project)
            db.commit()
            db.close()
            return redirect('/userView')

@app.route('/editProject/<int:ProjectId>')
@login_required
def editProject(ProjectId):
    if(current_user.NivelAcesso == 0):
        project = Projects.query.filter(Projects.Id == ProjectId).first()
        user = Users.query.filter(Users.Id == project.Dono).first()
        return render_template('adminReview.html', project = project, user = user)
    else:
        return render_template('userReview.html')



@app.route('/userRegistration', methods = ['GET', 'POST'])
@login_required
def userRegistration():
    user = current_user
    if(request.method == 'GET' ): #and not user.NivelAcesso
        return render_template('userRegistration.html')

    if(request.method == 'POST' ): #and not user.NivelAcesso
            userForRegistration = Users(request.form['Nome'],
                                        request.form['Sobrenome'],
                                        request.form['Email'],
                                        request.form['AreaAtuacao'],
                                        request.form['Supervisor'],
                                        request.form['Cargo'],
                                        int(request.form['NivelAcesso']),
                                        request.form['Senha'])

            if(Users.validate_user(userForRegistration)): #and not user.NivelAcesso
                db = sessionLocal()
                db.add(userForRegistration)
                db.commit()
                db.close()
                return redirect('/')
            
            else:
                print('usuario invalido')
                return redirect('/userRegistration')

@app.route('/projectUpdate/<int:ProjectId>', methods = ['PUT', 'POST'])
@login_required
def projectUpdate(ProjectId):
    projectUpdate = Projects(request.form['NomeProjeto'],
                       request.form['Descricao'],
                       request.form['Dono'],
                       request.form['Prioridade'])
    
    db = sessionLocal()
    projeto = db.query(Projects).filter(Projects.Id == ProjectId).first()
    projeto.NomeProjeto = request.form['NomeProjeto']
    projeto.Descricao = request.form['Descricao']
    projeto.Prioridade = request.form['Prioridade']
    projeto.Dono = request.form['Dono']
    db.commit()
    db.close()
    return redirect('/userView')


@app.route('/delete/<int:ProjectId>')
@login_required
def delete(ProjectId):
    db = sessionLocal()
    db.query(Projects).filter(Projects.Id == ProjectId).delete()
    db.commit()
    db.close()
    return redirect('/userView')