from flask import Blueprint
from core import db
from core.apis import decorators
from core.apis.responses import APIResponse
from core.models.assignments import Assignment

from .schema import AssignmentSchema, AssignmentGradeSchema
teacher_assignments_resources = Blueprint('teacher_assignments_resources', __name__)


@teacher_assignments_resources.route('/assignments', methods=['GET'], strict_slashes=False)
@decorators.authenticate_principal
def list_assignments(p):
    """Returns list of assignments"""
    teacher_id = p.teacher_id

    teachers_assignments = Assignment.get_assignments_by_teacher(teacher_id)
    teachers_assignments_dump = AssignmentSchema().dump(teachers_assignments, many=True)
    return APIResponse.respond(data=teachers_assignments_dump)


@teacher_assignments_resources.route('/assignments/grade', methods=['POST'], strict_slashes=False)
@decorators.accept_payload
@decorators.authenticate_principal
def grade_assignment(p, incoming_payload):
    """Grade an assignment"""
    grade_assignment_payload = AssignmentGradeSchema().load(incoming_payload)
    teacher_id = p.teacher_id

    # Validate the assignment
    assignment = Assignment.query.filter_by(id=grade_assignment_payload.id).first()
    if not assignment:
        return APIResponse.respond(error='FyleError',message="Assignment not found", status_code=404)
    if assignment.teacher_id != teacher_id:
        return APIResponse.respond(error='FyleError',message="Assignment does not belong to this teacher", status_code=400)
    if assignment.state not in ['SUBMITTED']:
        return APIResponse.respond(error='FyleError',message="Assignment must be in 'SUBMITTED' state to be graded", status_code=400)

    graded_assignment = Assignment.mark_grade(
        _id=grade_assignment_payload.id,
        grade=grade_assignment_payload.grade,
        auth_principal=p
    )
    db.session.commit()
    graded_assignment_dump = AssignmentSchema().dump(graded_assignment)
    return APIResponse.respond(data=graded_assignment_dump)
