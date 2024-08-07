import pytest
from core import db
from core.models.assignments import Assignment, AssignmentStateEnum
from core.models.students import Student  
from core.models.teachers import Teacher  
from core.models.teachers import Teacher

@pytest.fixture
def existing_teacher():
    return Teacher.query.first()


def test_teacher_repr(existing_teacher):
    teacher = existing_teacher
    repr_output = repr(teacher)
    expected_repr = f'<Teacher {teacher.id!r}>'
    assert repr_output == expected_repr
    
    
def test_get_assignments_teacher_1(client, h_teacher_1):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 1
        assert assignment['state'] in ['SUBMITTED', 'GRADED']

def test_get_assignments_teacher_2(client, h_teacher_2):
    response = client.get(
        '/teacher/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['teacher_id'] == 2
        assert assignment['state'] in ['SUBMITTED', 'GRADED']


def test_grade_assignment_cross(client, h_teacher_2):
    """
    failure case: assignment 1 was submitted to teacher 1 and not teacher 2
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_2,
        json={
            "id": 1,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'



def create_test_assignment(student_id: int, teacher_id: int = None):
    """
    Create and insert a new assignment into the database.
    
    Args:
        student_id (int): ID of the student who created the assignment.
        teacher_id (int, optional): ID of the teacher to whom the assignment is submitted. Defaults to None.
    
    Returns:
        Assignment: The created assignment object.
    """
    # Create a new assignment
    assignment = Assignment(
        student_id=student_id,
        teacher_id=teacher_id,
        content="This is a test assignment.",
        state=AssignmentStateEnum.SUBMITTED  
    )
    
    db.session.add(assignment)
    db.session.commit()
    
    return assignment


def test_grade_assignment_valid(client, h_teacher_1):
    # Create a test assignment
    test_assignment = create_test_assignment(student_id=1, teacher_id=1)  

    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": test_assignment.id,
            "grade": "A"
        }
    )

    assert response.status_code == 200
    data = response.json

    db.session.delete(test_assignment)
    db.session.commit()


def test_grade_assignment_bad_grade(client, h_teacher_1):
    """
    failure case: API should allow only grades available in enum
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 1,
            "grade": "AB"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'ValidationError'


def test_grade_assignment_bad_assignment(client, h_teacher_1):
    """
    failure case: If an assignment does not exists check and throw 404
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1,
        json={
            "id": 100000,
            "grade": "A"
        }
    )

    assert response.status_code == 404
    data = response.json

    assert data['error'] == 'FyleError'


def test_grade_assignment_draft_assignment(client, h_teacher_1):
    """
    failure case: only a submitted assignment can be graded
    """
    response = client.post(
        '/teacher/assignments/grade',
        headers=h_teacher_1
        , json={
            "id": 2,
            "grade": "A"
        }
    )

    assert response.status_code == 400
    data = response.json

    assert data['error'] == 'FyleError'
