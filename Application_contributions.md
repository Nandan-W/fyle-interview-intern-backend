# Application Contributions

This document outlines the contributions made to increase statement coverage and implement necessary functionalities in the project. The focus has been on improving code coverage through various tests and adding essential features. Below is a detailed account of the modifications and enhancements made to different parts of the application.

## Increasing Statement Coverage

### 1. `core/api/decorators.py`
- **Initial Coverage**: 91%
- **Enhancements**:
  - Added principal functions in `core/models/assignments.py`
  - Referenced these in `core/api/assignments/principal.py`
  - Updated `server.py` to include `principal.py`

### 2. `core/api/assignments/principals.py`
- **Initial Coverage**: 65%
- **Enhancements**:
  - Filled with content from previous step.
  - Added `TeacherSchema`, `StudentSchema`, etc., in `schema.py`
  - Updated routes and test cases for full coverage

### 3. `core/models/assignments.py`
- **Initial Coverage**: 93%
- **Enhancements**:
  - Added functions in `student.py` and `student_tests.py`
  - Implemented `repr` logging for assignments

### 4. `core/models/principal.py`
- **Initial Coverage**: 90%
- **Enhancements**:
  - Added `repr` logging function for `Principal` user entity

### 5. `core/models/student.py`
- **Initial Coverage**: 90%
- **Enhancements**:
  - Added `repr` logging function for `Student` user

### 6. `core/models/teacher.py`
- **Initial Coverage**: 90%
- **Enhancements**:
  - Added `repr` logging function for `Teacher` user

### 7. `core/libs/assertions.py`
- **Initial Coverage**: 80%
- **Enhancements**:
  - Created `assertions_test.py` with necessary assertion tests

### 8. `core/libs/exceptions.py`
- **Initial Coverage**: 70%
- **Enhancements**:
  - Created `exceptions_test.py` with necessary exception tests

### 9. `core/models/users.py`
- **Initial Coverage**: 76%
- **Enhancements**:
  - Added required test functions

### 10. `core/apis/assignments/student.py`
- **Enhancements**:
  - Added/corrected functions to view, create, edit drafts, and submit assignments
  - Added relevant test cases

### 11. `core/apis/assignments/teacher.py`
- **Enhancements**:
  - Added/corrected functions to view and grade assignments
  - Included relevant test cases

### 12. `core/server.py`
- **Initial Coverage**: 84%
- **Enhancements**:
  - Created `server_test.py` to test:
    - Route `/`
    - Error handlers for `HTTPException`, `IntegrityError`
    - 404 handler for unknown routes
    - Unhandled exceptions

## Test Cases Summary

### 1. `assertions_tests.py`
- **Tests**:
  - `test_assert_auth_raises_fyle_error`
  - `test_assert_true_raises_fyle_error`
  - `test_assert_valid_raises_fyle_error`
  - `test_assert_found_raises_fyle_error`

### 2. `exceptions_test.py`
- **Tests**:
  - `test_fyle_error_to_dict`

### 3. `principals_test.py`
- **Tests**:
  - `test_principal_repr`
  - `test_get_assignments`
  - `test_grade_assignment_draft_assignment`
  - `test_regrade_assignment`
  - `test_list_teachers`

### 4. `server_test.py`
- **Tests**:
  - `test_ready_route`
  - `test_page_not_found`
  - `test_integrity_error_handling`
  - `test_http_exception_handling`
  - `test_unhandled_exception_handling`

### 5. `student_test.py`
- **Tests**:
  - `test_student_repr`
  - `test_get_assignments_student_1`
  - `test_post_assignment_null_content`
  - `test_submit_assignment_student_1`
  - `test_assignment_resubmit_error`

### 6. `teachers_test.py`
- **Tests**:
  - `test_teacher_repr`
  - `test_get_assignments_teacher_1`
  - `test_grade_assignment_cross`
  - `test_grade_assignment_valid`

### 7. `users_test.py`
- **Tests**:
  - `test_user_repr`
  - `test_user_filter`
  - `test_get_by_id`
  - `test_get_by_email`
