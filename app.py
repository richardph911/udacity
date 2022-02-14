import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys
from sqlalchemy import MetaData, create_engine, Table, Column, ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import Session, relationship

engine = create_engine('postgresql://richardph911@localhost:5432')
session = Session(engine)
db = SQLAlchemy()

class TodoList(db.Model):
        __tablename__ = 'todolists'
        id = Column(Integer, primary_key=True)
        name = Column(String(), nullable=False)
        todos = relationship('Todo', backref='list', lazy=True)

        def __repr__(self):
            return f'<TodoList {self.id} {self.name}>'

class Todo(db.Model):
        __tablename__ = 'todos'
        id = Column(Integer, primary_key=True)
        description = Column(String(), nullable=False)
        completed = Column(Boolean, nullable=False, default=False)
        list_id = Column(Integer, ForeignKey('todolists.id'), nullable=True)

        def __repr__(self):
            return f'<Todo {self.id} {self.description}, list {self.list_id}>'
  
def create_app():
    app = Flask(__name__)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://richardph911@localhost:5432/todoAPP'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db = SQLAlchemy(app)
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all()
    #home
    @app.route('/')
    def index():
      return render_template('index.html', data = Todo.query.all())

    # #create
    # @app.route('/todos/create', methods=['POST'])
    # def create_todo():
    #     error = False
    #     body = {}
    #     try:
    #         description = request.get_json()['description']
    #         todo = Todo(description=description, completed=False)
    #         session.add(todo)
    #         session.commit()
    #         body['id'] = todo.id
    #         body['completed'] = todo.completed
    #         body['description'] = todo.description
    #     except:
    #         error = True
    #         session.rollback()
    #         print(sys.exc_info())
    #     finally:
    #         session.close()
    #     if error:
    #         abort (400)
    #     else:
    #         return jsonify(body)

    # @app.route('/todos/<todo_id>', methods=['DELETE'])
    # def delete_todo(todo_id):
    #     try:
    #         Todo.query.filter_by(id=todo_id).delete()
    #         session.commit()                
    #     except:
    #             session.rollback()
    #     finally:
    #             session.close()
    #     return jsonify({ 'success': True })
    
    # #set complete
    # @app.route('/todos/<todo_id>/set-completed', methods=['POST'])
    # def set_completed_todo(todo_id):
    #     try:
    #         completed = request.get_json()['completed']
    #         print('completed', completed)
    #         todo = Todo.query.get(todo_id)
    #         todo.completed = completed
    #         session.commit()
    #     except:
    #         session.rollback()
    #     finally:
    #         session.close()
    #     return redirect(url_for('index'))


    return app
todoapp = create_app()
