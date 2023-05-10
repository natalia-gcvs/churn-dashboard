from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap
import secrets
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

# Cross-Site Request Forgery Protection
csrf = CSRFProtect(app)

# Bootstrap
bootstrap = Bootstrap(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# postgres://customer_data_ew3h_user:RYa4u5SB947QlTxcdInbziDk2MguQnLn@dpg-chdqfsrhp8u3v73m50f0-a.oregon-postgres.render.com/customer_data_ew3h

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

from application import routes