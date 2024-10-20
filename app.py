from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, RepairRequest 
from flask import redirect, request
from flask import render_template, request, redirect, url_for

app = Flask(__name__)
from datetime import datetime
from flask_migrate import Migrate
from flask import session
# Конфигурация базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///repair_requests.db'
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация базы данных для текущего приложения
db.init_app(app)

# Flask-Migrate для управления миграциями базы данных
from flask_migrate import Migrate
migrate = Migrate(app, db)

# Инициализация Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание базы данных и таблиц
with app.app_context():
    db.create_all()

# Маршрут для отображения страницы входа
@app.route('/')
def index():
    return render_template('index.html')

# Маршрут для отображения страницы регистрации
@app.route('/register_page')
def register_page():
    return render_template('register.html')

# Маршрут для отображения страницы заявок после входа


# Загрузка пользователя
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/add_user', methods=['POST'])
def add_user():
  

    data = request.json 
    username = data.get('username')
    password = data.get('password')
    role = data.get('role', 'user') 

    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'User already exists'}), 400

    new_user = User(username=username, role=role)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


# Создание базы данных
with app.app_context():
    db.create_all()

# Регистрация пользователя
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        role = data.get('role', 'user')  # Убедитесь, что роль по умолчанию указана

        if User.query.filter_by(username=username).first():
            return jsonify({'message': 'User already exists'}), 400

        new_user = User(username=username, role=role)  # Убедитесь, что роль сохраняется
        new_user.set_password(password)  # Убедитесь, что метод set_password работает
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        return jsonify({'message': str(e)}), 500







@login_manager.unauthorized_handler
def unauthorized_callback():
    return redirect(url_for('login') + '?next=' + request.path)

def find_user_by_username(username):
    return User.query.filter_by(username=username).first()

@app.route('/requests_page')
def requests_page():
    return render_template('requests.html', user_role=session.get('user_role'))


# Вход в систему
@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()  # Найти пользователя по имени

        if user is None:
            return jsonify({'message': 'User not found'}), 404

        if user.check_password(password):  # Проверка пароля
            
            login_user(user)  # Вход пользователя
            session['user_role'] = user.role  # Установка роли в сессии
            return redirect(url_for('requests_page'))  # Перенаправление на страницу запросов
        else:
            return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'message': 'Internal server error'}), 500
@app.route('/admin_page')
def admin_page():
    if session.get('user_role') != 'admin':  # Проверка роли
        return "Access denied", 403  # Запрет доступа
    # Дальнейшая логика для админской страницы
    return render_template('admin_page.html')

@app.route('/some_protected_route')
def some_protected_route():
    if session.get('user_role') != 'admin':
        return "Access denied", 403
    # Логика для обработки запроса
    return render_template('protected_page.html')






# Выход из системы
@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200

# Создание заявки на ремонт
from datetime import datetime

@app.route('/requests', methods=['POST'])
def create_request():
    data = request.json
    date_added = datetime.strptime(data['date_added'], '%Y-%m-%dT%H:%M:%S')
    
    new_request = RepairRequest(
        request_number=data['request_number'],
        date_added=date_added, 
        equipment_type=data['equipment_type'],
        issue_type=data['issue_type'],
        description=data['description'],
        client=data['client'],
        status=data['status'],
        completed_at=None 
       
    )

    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Request added successfully'}), 201


# Получение всех заявок
@app.route('/requests', methods=['GET'])
@login_required
def get_requests():
    requests = RepairRequest.query.all()
    return jsonify([{
        'id': req.id,
        'request_number': req.request_number,
        'equipment_type': req.equipment_type,
        'issue_type': req.issue_type,
        'description': req.description,
        'client': req.client,
        'status': req.status,
        'responsible_person': req.responsible_person,
        'comments': req.comments,
        'date_added': req.date_added.isoformat() if req.date_added else None,  
        'completed_at': req.completed_at,
    } for req in requests]), 200



# Обновление заявки
@app.route('/requests/<int:id>', methods=['GET', 'PUT'])
@login_required
def get_or_update_request(id):
    if session.get('user_role') != 'admin':
        return "Access denied", 403 
    req = RepairRequest.query.get(id)
    if not req:
        return jsonify({'message': 'Request not found'}), 404

    if request.method == 'GET':
       
        return jsonify({
            'request_number': req.request_number,
           
            'description': req.description,
           
            'status': req.status,
            'responsible_person': req.responsible_person,
            'completed_at': req.completed_at
        
        })

    # Обработка метода PUT (обновление заявки)
    data = request.json

    if 'description' in data:
        req.description = data['description']
   
    if 'status' in data:
        req.status = data['status']
        if req.status == 'Выполнено' and req.completed_at is None: 
            req.completed_at = datetime.utcnow()

    if 'responsible_person' in data:
        req.responsible_person = data['responsible_person']
 
    db.session.commit()
    return jsonify({'message': 'Request updated successfully'}), 200



@app.route('/requests/<int:id>', methods=['DELETE'])
@login_required
def delete_request(id):
    req = RepairRequest.query.get(id)
    if not req:
        return jsonify({'message': 'Request not found'}), 404

    db.session.delete(req)
    db.session.commit()
    return jsonify({'message': 'Request deleted successfully'}), 200


# Получение статистики
@app.route('/statistics', methods=['GET'])
@login_required
def get_statistics():
    total_requests = RepairRequest.query.count()
    completed_requests = RepairRequest.query.filter_by(status='выполнено').count()
    
    # Вычисление среднего времени выполнения
    average_completion_time = db.session.query(
        db.func.avg(db.func.julianday(RepairRequest.completed_at) - db.func.julianday(RepairRequest.date_added))
    ).filter(RepairRequest.status == 'выполнено').scalar()

    return jsonify({
        'total_requests': total_requests,
        'completed_requests': completed_requests,
        'average_completion_time': average_completion_time if average_completion_time else 0
    }), 200








@app.route('/add-request')
def add_request_page():
    return render_template('add_request.html')

@app.route('/requests', methods=['POST'])
def add_request():
    data = request.json
    if not all(key in data for key in ['request_number', 'date_added', 'equipment_type', 'issue_type', 'description', 'client', 'status']):
        return jsonify({'message': 'Missing fields'}), 400

    # Assuming you have the necessary logic to add a new request
    new_request = RepairRequest(
        request_number=data['request_number'],
        date_added=datetime.strptime(data['date_added'], '%Y-%m-%d'),
        equipment_type=data['equipment_type'],
        issue_type=data['issue_type'],
        description=data['description'],
        client=data['client'],
        status=data['status']
    )
    db.session.add(new_request)
    db.session.commit()

    return jsonify({'message': 'Request added successfully'}), 201

if __name__ == '__main__':
    app.run(debug=True)

