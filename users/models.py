from flask import Flask, jsonify, request, session
from app import mongo, bcrypt, profile, cover, post, resource, resume
from datetime import datetime
from bson.objectid import ObjectId
import os
from werkzeug.utils import secure_filename
from PIL import Image, ImageOps


class User:

    def start_session(self, user):
        del user['password']
        del user['_id']
        session['logged_in'] = True
        session['user'] = user
        return jsonify(user), 200

    def login(self):
        user = mongo.db.user.find_one({"$or": [{"email": request.form.get(
            'email-username')}, {"username": request.form.get('email-username')}]})

        if not user:
            return jsonify({'error': 'No such email or username exists'}), 403

        if not bcrypt.check_password_hash(user.get('password'), request.form.get('password')):
            return jsonify({'error': 'Incorrect password'}), 403

        return self.start_session(user)

    def signup(self):

        if mongo.db.user.find_one({"$or": [{"email":  request.form.get('email')}, {"username": request.form.get('username')}]}):
            return jsonify({'error': 'Email or Username already exists'}), 409

        if(request.form.get('password') != request.form.get('confirm-password')):
            return jsonify({'error': 'Password doesn\'t match'}), 422

        user = {
            'firstname':  request.form.get('firstname'),
            'lastname': request.form.get('lastname'),
            'email': request.form.get('email'),
            'username': request.form.get('username'),
            'password': bcrypt.generate_password_hash(request.form.get('password')).decode('UTF-8'),
            'school': request.form.get('school-option'),
            'branch': request.form.get('branch'),
            'graduation_year': request.form.get('graduation-year'),
            'programme_duration': request.form.get('programme-duration'),
            'about': request.form.get('about')
        }

        if mongo.db.user.insert_one(user):
            return self.start_session(user)

        return jsonify({'error': 'Signup failed'}), 501

    def getUser(self, username=None):
        if not username:
            username = session.get('user').get('username')

        user = mongo.db.user.find_one({'username': username}, {
                                      'password': 0, '_id': 0})
        return user

    def updateProfile(self):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        baseDir = os.getcwd()

        file = request.files.get('file')
        if file:
            file.filename = f"{user.get('username')}_profile.webp"
            try:
                file_path = profile.path(file.filename)
                os.remove(file_path)
            except FileNotFoundError:
                pass
            finally:
                try:
                    profileDir = os.path.join(
                        baseDir, os.path.join('uploads', 'profile'))
                    im = Image.open(file).convert('RGB')
                    im = ImageOps.exif_transpose(im)
                    im.save(
                        f"{os.path.join(profileDir, file.filename)}", "WEBP")
                except:
                    return jsonify({'error': 'Failed to upload profile photo'}), 501

        coverfile = request.files.get('coverfile')
        if coverfile:
            coverfile.filename = f"{user.get('username')}_cover.webp"
            try:
                file_path = cover.path(coverfile.filename)
                os.remove(file_path)
            except FileNotFoundError:
                pass
            finally:
                try:
                    coverDir = os.path.join(
                        baseDir, os.path.join('uploads', 'cover'))
                    im = Image.open(coverfile).convert('RGB')
                    im = ImageOps.exif_transpose(im)
                    im.save(
                        f"{os.path.join(coverDir, coverfile.filename)}", "WEBP")
                except:
                    return jsonify({'error': 'Failed to upload cover photo'}), 501

        resumefile = request.files.get('resume')
        if resumefile:
            file_ext = os.path.splitext(resumefile.filename)[1]
            resumefile.filename = f"{user.get('username')}_resume{file_ext}"
            try:
                file_path = resume.path(resumefile.filename)
                os.remove(file_path)
            except FileNotFoundError:
                pass
            finally:
                if not resume.save(resumefile):
                    return jsonify({'error': 'Failed to upload resume'}), 501

        user_update = {
            'firstname':  request.form.get('firstname'),
            'lastname': request.form.get('lastname'),
            'about': request.form.get('description'),
            'linkedin': request.form.get('linkedin'),
            'twitter': request.form.get('twitter'),
            'instagram': request.form.get('instagram'),
            'github': request.form.get('github'),
            'facebook': request.form.get('facebook'),
            'skills': request.form.get('skills').split(','),
            'profile': user.get('profile') if file.filename == '' else file.filename,
            'cover': user.get('cover') if coverfile.filename == '' else coverfile.filename,
            'resume': user.get('resume') if resumefile.filename == '' else resumefile.filename
        }
        print(user_update.get('skills'))

        if mongo.db.user.update_one(user, {'$set': user_update}, upsert=False).acknowledged:
            user.update(user_update)
            session['user'] = user
            return jsonify(user), 201

        return jsonify({'error': 'Failed updating the profile'}), 501


class WorkExperience:

    def getWorkExp(self, user=None):
        if not user:
            user = session.get('user')

        work_exp = mongo.db.work_exp.find({'user': user.get('username')})
        return list(work_exp)

    def saveWorkExp(self):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        joining_date = datetime.strptime(
            str(request.form.get('joindate')), '%Y-%m-%d')
        ending_date = datetime.strptime(
            str(request.form.get('enddate')), '%Y-%m-%d')
        if ending_date <= joining_date:
            return jsonify({'error': 'Date mismatch'}), 401

        experience_details = {
            'user': user.get('username'),
            'role': request.form.get('role'),
            'type': request.form.get('type'),
            'company': request.form.get('company'),
            'location': request.form.get('location'),
            'joining_date': joining_date,
            'ending_date': ending_date,
            'description': request.form.get('description'),
            'upload_time': datetime.now()
        }

        if mongo.db.work_exp.insert_one(experience_details):
            del experience_details['_id']
            return jsonify(experience_details), 201

        return jsonify({'error': 'Failed adding your work experience'}), 501

    def deleteWorkExp(self, id):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        result = mongo.db.work_exp.find_one_and_delete({'_id': ObjectId(id)})
        if "_id" in result:
            print("deleted")
            return jsonify({'message': "Work experience deleted successfully"}), 204
        return jsonify({'message': "Failed to delete work experience"}), 501


class Resource:

    def getFileInfo(self, file):
        file_ext = os.path.splitext(file.filename)[1]
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        filename = file.filename
        return filename, file_ext, file_length

    def getResources(self):
        resources = mongo.db.resource.find()
        return list(resources)

    def getUserResources(self, user=None):
        if not user:
            user = session.get('user')

        resources = mongo.db.resource.find(
            {'author.username': user.get('username')})
        return list(resources)

    def saveResource(self):

        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        user = {
            'email': user.get('email'),
            'firstname':  user.get('firstname'),
            'lastname': user.get('lastname'),
            'username': user.get('username')
        }

        file = request.files.get('file')
        filename, file_ext, file_size = self.getFileInfo(file)
        if not file:
            return jsonify({'error': 'No file found to be uploaded'}), 401

        totalUploads = mongo.db.resource.count()
        file.filename = f"{user.get('username')}{totalUploads}{filename}"
        if not resource.save(file):
            return jsonify({'error': 'File failed to be uploaded'}), 501

        resource_details = {
            'author': user,
            'resource_name': filename,
            'tags': request.form.get('tags-input').split(','),
            'location': file.filename,
            'description': request.form.get('description'),
            'filesize': file_size,
            'file_ext': file_ext,
            'upload_time': datetime.now()
        }

        if mongo.db.resource.insert_one(resource_details):
            del resource_details['_id']
            return jsonify(resource_details), 201

        return jsonify({'error': 'Failed creating the resource'}), 501

    def editResource(self):
        pass

    def deleteResource(self, id):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        result = mongo.db.resource.find_one_and_delete({'_id': ObjectId(id)})
        print(result)
        if "_id" in result:
            print("deleted")
            return jsonify({'message': "Resource deleted successfully"}), 204
        return jsonify({'message': "Failed to delete resource"}), 501


class Review:

    def getReviews(self):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        reviews = mongo.db.review.find(
            {'to.username': user.get('username'), 'status': 'reviewed'})
        return list(reviews)

    def getRequests(self):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        requests = mongo.db.review.find(
            {'from': user.get('username'), 'status': 'pending'})
        return list(requests)

    def sendRequest(self, fromUser, requestFor):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        toUser = {
            'email': user.get('email'),
            'firstname':  user.get('firstname'),
            'lastname': user.get('lastname'),
            'username': user.get('username'),
            'profile': user.get('profile')
        }

        review = {
            'from': fromUser,
            'to': toUser,
            'type': requestFor,
            'doc_link': f"{user.get('resume') if requestFor=='resume' else user.get('linkedin')}",
            'status': 'pending',
            'request_time': datetime.now()
        }

        if mongo.db.review.insert_one(review):
            return jsonify({'message': "Request sent successfully"}), 201

    def sendReview(self, id):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        user = {
            'email': user.get('email'),
            'firstname':  user.get('firstname'),
            'lastname': user.get('lastname'),
            'username': user.get('username'),
            'profile': user.get('profile')
        }

        review_update = {
            'from': user,
            'description': request.form.get('review'),
            'status': 'reviewed',
            'reviewed_time': datetime.now()
        }

        if mongo.db.review.update_one({'_id': ObjectId(id)}, {'$set': review_update}, upsert=False).acknowledged:
            return jsonify({'message': "Review sent successfully"}), 201
        return jsonify({'error': "Failed sending the review "}), 500


class Opportunity:

    def getOpportunities(self):
        opportunities = mongo.db.opportunity.find()
        return list(opportunities)

    def getUserOpportunities(self, user=None):
        if not user:
            user = session.get('user')
        opportunities = mongo.db.opportunity.find(
            {'author.username': user.get('username')})
        return list(opportunities)

    def addOpportunity(self):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        user = {
            'email': user.get('email'),
            'firstname':  user.get('firstname'),
            'lastname': user.get('lastname'),
            'username': user.get('username'),
            'profile': user.get('profile')
        }

        opportunity_details = {
            'author': user,
            'role': request.form.get('role'),
            'tags': request.form.get('tags-input').split(','),
            'location': request.form.get('location'),
            'company': request.form.get('company'),
            'role_type': request.form.get('type'),
            'description': request.form.get('description'),
            'application_link': request.form.get('applink'),
            'added_time': datetime.now()
        }

        if mongo.db.opportunity.insert_one(opportunity_details):
            del opportunity_details['_id']
            return jsonify(opportunity_details), 201

        return jsonify({'error': 'Failed creating the opportunity'}), 501

    def deleteOpportunity(self, id):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        result = mongo.db.opportunity.find_one_and_delete({'_id': ObjectId(id)})
        print(result)
        if "_id" in result:
            print("deleted")
            return jsonify({'message': "Opportunity deleted successfully"}), 204
        return jsonify({'message': "Failed to delete opportunity"}), 501


class Post:

    def getFileInfo(self, file):
        file_ext = os.path.splitext(file.filename)[1]
        file.seek(0, os.SEEK_END)
        file_length = file.tell()
        file.seek(0)
        filename = file.filename
        return filename, file_ext, file_length

    def getPosts(self):
        posts = mongo.db.post.find()
        return list(posts)

    def getUserPosts(self, user=None):
        if not user:
            user = session.get('user')

        posts = mongo.db.post.find({'author.username': user.get('username')})
        return list(posts)

    def addPost(self):

        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401
        del user['about']
        del user['branch']
        del user['graduation_year']
        del user['programme_duration']
        del user['school']

        files = request.files.getlist('file')
        location = []
        filename, file_ext, file_size = self.getFileInfo(files[0])

        uploads = list(mongo.db.post.find(
            {'author.username': user.get('username')}, {'location': 1, '_id': 0}))
        totalUploads = 0
        for upload in uploads:
            totalUploads += len(upload['location'])

        baseDir = os.getcwd()
        for file in files:
            if not file:
                return jsonify({'error': 'No file found to be uploaded'}), 401
            file.filename = secure_filename(file.filename)
            file.filename = f"{user.get('username')}{totalUploads}{file.filename.split('.')[0]}.webp"
            totalUploads += 1
            try:
                postDir = os.path.join(
                    baseDir, os.path.join('uploads', 'post'))
                im = Image.open(file).convert('RGB')
                im = ImageOps.exif_transpose(im)
                im.save(
                    f"{os.path.join(postDir, file.filename)}", "WEBP")
                location.append(file.filename)
            except:
                return jsonify({'error': 'Failed to create new post'}), 501

        user = {
            'email': user.get('email'),
            'firstname':  user.get('firstname'),
            'lastname': user.get('lastname'),
            'username': user.get('username'),
            'profile': user.get('profile')
        }

        post_details = {
            'author': user,
            'location': location,
            'description': request.form.get('description'),
            'added_time': datetime.now()
        }

        if mongo.db.post.insert_one(post_details):
            del post_details['_id']
            return jsonify(post_details), 201

        return jsonify({'error': 'Failed creating the post'}), 501

    def deletePost(self, id):
        user = session.get('user')
        if not user:
            return jsonify({'error': 'Unauthorized access'}), 401

        result = mongo.db.post.find_one_and_delete({'_id': ObjectId(id)})
        print(result)
        if "_id" in result:
            print("deleted")
            return jsonify({'message': "Post deleted successfully"}), 204
        return jsonify({'message': "Failed to delete post"}), 501
