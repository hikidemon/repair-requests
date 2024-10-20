from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, request
from datetime import datetime
# Инициализация базы данных (экземпляр создается один раз)
db = SQLAlchemy()



# Модель заявки на ремонт
class RepairRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    request_number = db.Column(db.String(50), unique=True, nullable=False)
    equipment_type = db.Column(db.String(100), nullable=False)
    issue_type = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    client = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='в ожидании')
    responsible_person = db.Column(db.String(100))
    comments = db.Column(db.String(200))
    date_added = db.Column(db.DateTime, default=db.func.current_timestamp())
    completed_at = db.Column(db.DateTime, nullable=True)  

    def __repr__(self):
        return f'<RepairRequest {self.request_number}>'



# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False)  # Роль (администратор или пользователь)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Удаление старой базы данных (если необходимо)
if os.path.exists('repair_requests.db'):
    os.remove('repair_requests.db')

# Создание новой базы данных и таблиц
def create_database(app):
    with app.app_context():
        db.create_all()  # Создает все таблицы для ваших моделей
        print("База данных и таблицы успешно созданы!")
