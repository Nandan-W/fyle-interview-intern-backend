
from flask import Blueprint, request
from core.apis.responses import APIResponse
from core.models.teachers import Teacher
from core.models.assignments import Assignment, AssignmentStateEnum,GradeEnum
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
    assignments = Assignment.query.filter(
        Assignment.state.in_([AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED])
    ).all()
    # filter to ensure assignments in draft are not sent back
    assignments_dump = AssignmentSchema().dump(assignments, many=True)  
    return APIResponse.respond(data=assignments_dump)


@principal_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_or_regrade_assignment(p, incoming_payload):
    """Grade or re-grade an assignment"""
    assignment_id = incoming_payload.get('id')
    new_grade = incoming_payload.get('grade')


    if new_grade not in GradeEnum.__members__:
        return APIResponse.respond(error='Invalid grade', message='Grade must be one of {}'.format(list(GradeEnum.__members__.keys())), status_code=400)

    assignment = Assignment.get_by_id(assignment_id)
    if not assignment:
        return APIResponse.respond(error='Assignment not found', status_code=404)

    if assignment.state != AssignmentStateEnum.GRADED.value:
        return APIResponse.respond(error='Assignment is still in draft state and cannot be graded', status_code=400)
    
    assignment.grade = new_grade
    db.session.commit()

    assignment_dump = AssignmentSchema().dump(assignment)
    return APIResponse.respond(data=assignment_dump)

