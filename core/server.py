from flask import jsonify
from marshmallow.exceptions import ValidationError
from core import app
from core.apis.assignments import student_assignments_resources, teacher_assignments_resources,principal_assignments_resources
from core.libs import helpers
from core import db
from core.models.users import User
from core.apis.decorators import authenticate_principal
from core.libs.exceptions import FyleError
from werkzeug.exceptions import HTTPException, Forbidden

from sqlalchemy.exc import IntegrityError

app.register_blueprint(student_assignments_resources, url_prefix='/student')
app.register_blueprint(teacher_assignments_resources, url_prefix='/teacher')
app.register_blueprint(principal_assignments_resources, url_prefix='/principal')


@app.route('/')
def ready():
    response = jsonify({
        'status': 'ready',
        'time': helpers.get_utc_now()
    })

    return response


@app.route('/trigger-integrity-error')
def trigger_integrity_error():
    raise IntegrityError('mock params', 'mock statement', 'mock orig')


@app.route('/trigger-http-exception')
def trigger_http_exception():
    raise Forbidden(description='mock HTTPException')


@app.route('/trigger-unhandled-exception')
def trigger_unhandled_exception():
    raise ValueError("This is a generic exception")


@app.errorhandler(Exception)
def handle_error(err):
    if isinstance(err, FyleError):
        return jsonify(
            error=err.__class__.__name__, message=err.message
        ), err.status_code
    elif isinstance(err, ValidationError):
        return jsonify(
            error=err.__class__.__name__, message=err.messages
        ), 400
    elif isinstance(err, IntegrityError):
        return jsonify(
            error=err.__class__.__name__, message=str(err.orig)
        ), 400
    elif isinstance(err, HTTPException):
        return jsonify(
            error=err.__class__.__name__, message=str(err)
        ), err.code 
    return jsonify(
            error='InternalServerError', message='An unexpected error occurred.'
        ), 500

@app.errorhandler(404)
def page_not_found(e):
    return jsonify(
        error='NotFoundError', message='No such api'
    ), 404
