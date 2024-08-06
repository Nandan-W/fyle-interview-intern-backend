
from flask import Blueprint, request
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.assignments import Assignment
from core.models.principals import Principal
from core import db
from core.apis import decorators
# from core.models.assignments import GradeEnum, AssignmentStateEnum
from .schema import AssignmentSchema , TeacherSchema

principal_assignments_resources = Blueprint('principal_assignments_resources', __name__)


@principal_assignments_resources.route('/teachers', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_teachers(p):
    """Returns list of all teachers"""
    teachers = Teacher.query.all()
    teachers_dump = TeacherSchema().dump(teachers, many=True)  
    return APIResponse.respond(data=teachers_dump)


@principal_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_all_assignments(p):
    """Returns list of all assignments"""
    assignments = Assignment.get_all_assignments()
    assignments_dump = AssignmentSchema().dump(assignments, many=True)  
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/regrade', methods=['POST'], strict_slashes=False)
@decorators.authenticate_principal
@decorators.accept_payload
def regrade_assignment(p, incoming_payload):
    """Re-grade an assignment"""
    assignment_id = incoming_payload.get('id')
    new_grade = incoming_payload.get('grade')

    # Ensure 'grade' is valid and exists in GradeEnum
    if new_grade not in GradeEnum.__members__:
        return APIResponse.respond(error='Invalid grade', message='Grade must be one of {}'.format(list(GradeEnum.__members__.keys())), status_code=400)

    assignment = Assignment.regrade_assignment(
        _id=assignment_id,
        new_grade=new_grade,
        auth_principal=p
    )
    db.session.commit()
    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)


# from flask import Blueprint
# from core import db
# from core.apis import decorators
# from core.apis.responses import APIResponse
# from core.models.assignments import Assignment

# from .schema import AssignmentSchema, AssignmentGradeSchema
# teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


# @teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
# @decorators.authenticate_principal
# def list_assignments(p):
#     """Returns list of assignments"""
#     teachers_assignments = Assignment.get_assignments_by_teacher()
#     teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
#     return APIResponse.respond(data=teachers_assignments_dump)


# @teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
# @decorators.accept_payload
# @decorators.authenticate_principal
# def grade_assignment(p, incoming_payload):
#     """Grade an assignment"""
#     grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)

#     graded_assignment = Assignment.mark_grade(
#         _id=grade_assignment_payload.id,
#         grade=grade_assignment_payload.grade,
#         auth_principal=p
#     )
#     db.session.commit()
#     graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
#     return APIResponse.respond(data=graded_assignment_dump)
