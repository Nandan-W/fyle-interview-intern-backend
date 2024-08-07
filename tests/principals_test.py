import pytest
from core import db
from core.models.assignments import AssignmentStateEnum, GradeEnum, Assignment
from core.models.principals import Principal

@pytest.fixture
def existing_principal():
    # fetching an existing principal from db
    return Principal.query.first()

def test_principal_repr(existing_principal):
    principal = existing_principal
    repr_output = repr(principal)
    expected_repr = f'<Principal {principal.id!r}>'
    assert repr_output == expected_repr


def test_get_assignments(client, h_principal):
    response = client.get(
        '/principal/assignments',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['state'] in [AssignmentStateEnum.SUBMITTED, AssignmentStateEnum.GRADED]


def test_grade_assignment_draft_assignment(client, h_principal):
    """
    failure case: If an assignment is in Draft state, it cannot be graded by principal
    """

    # Creating a draft assignment (ensure id 5 exists and is in draft state)
    draft_assignment = Assignment( student_id=1, teacher_id=1, content='Draft Assignment', state=AssignmentStateEnum.DRAFT)
    db.session.add(draft_assignment)
    db.session.commit()

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': draft_assignment.id,
            'grade': GradeEnum.A.value
        },
        headers=h_principal
    )

    db.session.delete(draft_assignment)
    db.session.commit()

    assert response.status_code == 400


def test_grade_assignment(client, h_principal):

    submitted_assignment = Assignment(student_id=1, teacher_id=1, content='Existing Submitted Assignment', state=AssignmentStateEnum.SUBMITTED)
    db.session.add(submitted_assignment)
    db.session.commit()

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': submitted_assignment.id,
            'grade': GradeEnum.C.value
        },
        headers=h_principal
    )

    db.session.delete(submitted_assignment)
    db.session.commit()

    assert response.status_code == 400



def test_regrade_assignment(client, h_principal):

    graded_assignment = Assignment(student_id=1, teacher_id=1, content='Existing Graded Assignment', state=AssignmentStateEnum.GRADED)
    db.session.add(graded_assignment)
    db.session.commit()

    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': graded_assignment.id,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 200

    assert response.json['data']['state'] == AssignmentStateEnum.GRADED.value
    assert response.json['data']['grade'] == GradeEnum.B

    db.session.delete(graded_assignment)
    db.session.commit()

def test_regrade_assignment_with_unallowed_grade(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 4,
            'grade': 'E'
        },
        headers=h_principal
    )

    assert response.status_code == 400


def test_regrade_assignment_which_is_not_available(client, h_principal):
    response = client.post(
        '/principal/assignments/grade',
        json={
            'id': 450,
            'grade': GradeEnum.B.value
        },
        headers=h_principal
    )

    assert response.status_code == 404

def test_list_teachers(client, h_principal):
    """Test listing all teachers"""
    response = client.get(
        '/principal/teachers',
        headers=h_principal
    )

    assert response.status_code == 200

    data = response.json['data']
    assert isinstance(data, list)
    
    if data:
        for teacher in data:
            assert 'id' in teacher
            assert 'user_id' in teacher
            assert 'created_at' in teacher
            assert 'updated_at' in teacher

