from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from werkzeug.security import generate_password_hash,check_password_hash
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email
from flask_wtf.file import FileField, FileRequired, FileAllowed
import cv2



db = SQLAlchemy()
def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255))

    @property
    def password(self):
        raise ArithmeticError('密码不可读取')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)


class LoginForm(FlaskForm):
    user_id = StringField(u'用户名', validators=[
        DataRequired(message=u'用户名不能为空'), 
        Length(1,64)])
    password = PasswordField(u'密码', validators=[DataRequired(message=u'密码不能为空')])
    submit = SubmitField(u'登录')


class UploadForm(FlaskForm):
    file = FileField(label='上传视频或图片', 
    validators=[FileRequired(u'文件已上传')]
    )
    submit = SubmitField(u'上传')



class VideoCamera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture('picture/y2mate.com - __VwoChR-3LLQ_360p.mp4')


    def __del__(self):
        self.cap.release()


    def get_frame(self):
        success, image = self.cap.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()