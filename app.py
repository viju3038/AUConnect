import os
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, url_for, session)
from functools import wraps
from flask_bcrypt import Bcrypt
from flask_pymongo import PyMongo
from flask_uploads import ALL, DEFAULTS, IMAGES, UploadSet, configure_uploads
from werkzeug.utils import secure_filename
import timeago
import datetime
import pytz
from dateutil import relativedelta

mongo = None
bcrypt = None
profile = UploadSet('profile', IMAGES)
cover = UploadSet('cover', IMAGES)
post = UploadSet('post', IMAGES)
resource = UploadSet('resource', ALL)
resume = UploadSet('resume', DEFAULTS)
tz = pytz.timezone('Asia/Kolkata')


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MONGO_URI'] = os.environ.get('MONGODB_URI')
    app.config['UPLOADED_PROFILE_DEST'] = os.path.join('uploads', 'profile')
    app.config['UPLOADED_COVER_DEST'] = os.path.join('uploads', 'cover')
    app.config['UPLOADED_POST_DEST'] = os.path.join('uploads', 'post')
    app.config['UPLOADED_RESOURCE_DEST'] = os.path.join('uploads', 'resource')
    app.config['UPLOADED_RESUME_DEST'] = os.path.join('uploads', 'resume')

    global mongo, bcrypt
    mongo = PyMongo(app)
    bcrypt = Bcrypt(app)
    configure_uploads(app, [profile, cover, post, resource, resume])

    # ? Blueprints for maintaining the modules
    from users import routes
    app.register_blueprint(routes.users_bp, url_prefix='')

    @app.template_filter('timeperiod')
    def format_datetime_timeperiod(datetime_obj):
        now = datetime.datetime.now(tz=tz)
        datetime_obj = datetime_obj.replace(tzinfo=tz)
        return timeago.format(datetime_obj, now)

    @app.template_filter('duration')
    def calculate_duration(enddate, joindate):
        diff = relativedelta.relativedelta(enddate, joindate)
        duration = ""
        duration += f"{diff.years} years " if diff.years > 0 else ""
        duration += f"{diff.months} months " if diff.months > 0 else ""
        duration += f"{diff.days} days" if diff.days > 0 else ""
        return duration

    def ifLoggedIn(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'logged_in' in session and not session['logged_in']:
                return redirect(url_for('user.home'))
            return f(*args, **kwargs)
        return decorated_function

    # ? Root URL request handling
    @app.route('/authentication/')
    @ifLoggedIn
    def authentication():
        return render_template('authentication.html')

    # ? Root URLs request handling for sending uploaded files
    @app.route('/uploads/profile/<filename>')
    def getProfile(filename):
        try:
            return send_from_directory(app.config['UPLOADED_PROFILE_DEST'], secure_filename(filename))
        except:
            return send_from_directory(app.config['UPLOADED_PROFILE_DEST'], secure_filename('default_profile_picture_placeholder_oiUSBDcoauysdvcapiucbayspdbpiaiusdyga.png'))

    @app.route('/uploads/cover/<filename>')
    def getCover(filename):
        try:
            return send_from_directory(app.config['UPLOADED_COVER_DEST'], filename=secure_filename(filename))
        except:
            return send_from_directory(app.config['UPLOADED_COVER_DEST'], filename=secure_filename('default_cover_placeholder_djincapidfuybvpaidfubvcpacsdpjcnapbydcnas.jpg'))

    @app.route('/uploads/post/<filename>')
    def getPost(filename):
        try:
            return send_from_directory(app.config['UPLOADED_POST_DEST'], filename=secure_filename(filename))
        except:
            return send_from_directory(app.config['UPLOADED_POST_DEST'], filename=secure_filename('placeholder-post-image.jpg'))

    @app.route('/uploads/resource/<filename>')
    def getResource(filename):
        return send_from_directory(app.config['UPLOADED_RESOURCE_DEST'], secure_filename(filename))

    @app.route('/uploads/resume/<filename>')
    def getResume(filename):
        return send_from_directory(app.config['UPLOADED_RESUME_DEST'], secure_filename(filename))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
