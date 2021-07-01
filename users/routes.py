from flask import render_template, Blueprint, request, redirect, url_for, Response, make_response, jsonify, session
from functools import wraps
from users.models import User, Resource, Review, Opportunity, Post, WorkExperience
from app import mongo
import os

users_bp = Blueprint('user', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' in session and session['logged_in']:
            return f(*args, **kwargs)
        return redirect(url_for('authentication', c=request.url))
    return decorated_function


@users_bp.route('/login/', methods=['POST'])
def login():
    return User().login()


@users_bp.route('/signup/', methods=['POST'])
def signup():
    return User().signup()


@users_bp.route('/home/', methods=['GET'])
@users_bp.route('/', methods=['GET'])
@login_required
def home():
    posts = Post().getPosts()
    return render_template('home.html', posts=posts)


@users_bp.route('/resources/', methods=['GET'])
@login_required
def resources():
    resources = Resource().getResources()
    return render_template('resources.html', resources=resources)


@users_bp.route('/opportunities/', methods=['GET'])
@login_required
def opportunities():
    opportunities = Opportunity().getOpportunities()
    return render_template('opportunities.html', opportunities=opportunities)


@users_bp.route('/reviews/', methods=['GET'])
@login_required
def reviews():
    reviews = Review().getReviews()
    return render_template('review_reviews.html', reviews=reviews)


@users_bp.route('/requests/', methods=['GET'])
@login_required
def requests():
    review_requests = Review().getRequests()
    return render_template('review_requests.html', requests=review_requests)


# @users_bp.route('/profile/', methods=['GET'])
# @users_bp.route('/profile/timeline/', methods=['GET'])
# @login_required
# def profile():
#     user = User().getUser()
#     posts = Post().getUserPosts(user)
#     return render_template('profile_posts.html', user=user, posts=posts)
# 
#
# @users_bp.route('/profile/about/', methods=['GET'])
# @login_required
# def profileAbout():
#     user = User().getUser()
#     try:
#         user.get('skills').remove('')
#     except:
#         pass
#     social_link = user.get('twitter') or user.get('facebook') or user.get(
#         'github') or user.get('instagram') or user.get('linkedin')
#     work_exp = WorkExperience().getWorkExp()
#     posts = len(Post().getUserPosts())
#     resources = len(Resource().getUserResources())
#     opportunities = len(Opportunity().getUserOpportunities())
#     return render_template('profile_about.html', user=user, work_exp=work_exp, social_link=social_link, posts=posts, resources=resources, opportunities=opportunities)


@users_bp.route('/profile/about/edit', methods=['POST'])
@login_required
def editprofileAbout():
    return User().updateProfile()


# @users_bp.route('/profile/resources/', methods=['GET'])
# @login_required
# def profileResource():
#     user = User().getUser()
#     resources = Resource().getUserResources()
#     return render_template('profile_resources.html', user=user, resources=resources)


# @users_bp.route('/profile/opportunities/', methods=['GET'])
# @login_required
# def profileOpportunities():
#     user = User().getUser()
#     opportunities = Opportunity().getUserOpportunities()
#     return render_template('profile_opportunities.html', user=user, opportunities=opportunities)


@users_bp.route('/profile/<user>/', methods=['GET'])
@users_bp.route('/profile/<user>/timeline/', methods=['GET'])
@login_required
def userProfileTimeline(user):
    user = User().getUser(user)
    if user is None:
        return render_template('404.html')
    posts = Post().getUserPosts(user)
    other = not user == User().getUser()
    return render_template('profile_posts.html', other=other, user=user, posts=posts)


@users_bp.route('/profile/<user>/about/', methods=['GET'])
@login_required
def userProfileAbout(user):
    user = User().getUser(user)
    if user is None:
        return render_template('404.html')
    social_link = user.get('twitter') or user.get('facebook') or user.get(
        'github') or user.get('instagram') or user.get('linkedin')
    try:
        user.get('skills').remove('')
    except:
        pass
    work_exp = WorkExperience().getWorkExp(user)
    posts = len(Post().getUserPosts(user))
    resources = len(Resource().getUserResources(user))
    opportunities = len(Opportunity().getUserOpportunities(user))
    other = not user == User().getUser()
    return render_template('profile_about.html', other=other, user=user, work_exp=work_exp, posts=posts, resources=resources, opportunities=opportunities, social_link=social_link)


@users_bp.route('/profile/<user>/resources/', methods=['GET'])
@login_required
def userProfileResource(user):
    user = User().getUser(user)
    if user is None:
        return render_template('404.html')
    resources = Resource().getUserResources(user)
    other = not user == User().getUser()
    return render_template('profile_resources.html', other=other, user=user, resources=resources)


@users_bp.route('/profile/<user>/opportunities/', methods=['GET'])
@login_required
def userProfileOpportunities(user):
    user = User().getUser(user)
    if user is None:
        return render_template('404.html')
    opportunities = Opportunity().getUserOpportunities(user)
    other = not user.get('username') == session.get('user').get('username')
    return render_template('profile_opportunities.html', other=other, user=user, opportunities=opportunities)


@users_bp.route('/add-post/', methods=['POST'])
@login_required
def addPost():
    return Post().addPost()


@users_bp.route('/post/delete/<id>', methods=['DELETE'])
@login_required
def deletePost(id):
    return Post().deletePost(id)


@users_bp.route('/add-resource/', methods=['POST'])
@login_required
def addResource():
    return Resource().saveResource()


@users_bp.route('/resource/delete/<id>', methods=['DELETE'])
@login_required
def deleteResource(id):
    return Resource().deleteResource(id)


@users_bp.route('/add-opportunity/', methods=['POST'])
@login_required
def addOpportunity():
    return Opportunity().addOpportunity()


@users_bp.route('/opportunity/delete/<id>', methods=['DELETE'])
@login_required
def deleteOpportunity(id):
    return Opportunity().deleteOpportunity(id)


@users_bp.route('/edit-profile/', methods=['POST'])
@login_required
def editProfile():
    return User().updateProfile()


@users_bp.route('/add-work-exp/', methods=['POST'])
@login_required
def addWorkExp():
    return WorkExperience().saveWorkExp()


@users_bp.route('/work-exp/delete/<id>', methods=['DELETE'])
@login_required
def deleteWorkExp(id):
    return WorkExperience().deleteWorkExp(id)


@users_bp.route('/send-review/<id>', methods=['POST'])
@login_required
def sendReview(id):
    return Review().sendReview(id)


@users_bp.route('/send-request/<fromUser>/<requestFor>', methods=['POST'])
@login_required
def sendRequest(fromUser, requestFor):
    return Review().sendRequest(fromUser, requestFor)


@users_bp.route('/logout/', methods=['POST'])
@login_required
def logoutUser():
    if 'logged_in' in session:
        session.clear()
        return jsonify({'message': 'Logged out successfully'})
    return jsonify({'error': 'Log out unsuccessful'})
