from flask import *
from flask_login import LoginManager, current_user, login_required, login_user
from APP.models import User, LoginForm, UploadForm, VideoCamera
from werkzeug import secure_filename
# from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

blue = Blueprint('first_blue', __name__)
def init_blue(app):
    app.register_blueprint(blueprint=blue)

login_manage = LoginManager()
def init_login(app):
    login_manage.login_view = 'first_blue.login'
    login_manage.login_message_category = 'info'
    login_manage.login_message = 'Access denied.'
    login_manage.init_app(app)


@login_manage.user_loader
def load_user(user_id):
    user = User.query.get(int(user_id))
    return user 


@login_manage.request_loader
def request_loader(request):
    pass

@blue.route('/')
@blue.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        user = User.query.filter_by(user_id=user_id).first()
        if user is not None and user.check_password_hash(password):
            login_user(user)
            flash('Login success')
            return redirect(url_for('first_blue.detection'))
        flash('Invalid username or password.')
        
    
    return render_template('login.html',form=form)


@blue.route('/index')
def index():
    return render_template('index.html')


@blue.route('/detection',methods=['GET', 'POST'])
@login_required
def detection():
    form = UploadForm()
    if form.validate_on_submit():
        filename = secure_filename(form.file.data.filename)
        print(filename)
        form.file.data.save('picture/' + filename)
        flash('上传成功')
        return redirect('/detection')

    return render_template('detection.html', form=form)



@blue.route('/video')
def video():
    return render_template('video.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@blue.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()), 
    mimetype='multipart/x-mixed-replace; boundary=frame')