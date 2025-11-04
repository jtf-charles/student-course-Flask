#!/usr/bin/env python3
from datetime import datetime
import re

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource, abort

from models import db, Student, Instructor, Course, Enrollment

# ── App config ────────────────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
COURSE_ALLOWED_FIELDS = {"title", "duration", "level", "instructor_id"}
STUDENT_ALLOWED_FIELDS = {"name", "email", "year"}
INSTR_ALLOWED_FIELDS = {"name", "specialty"}
ENROLL_ALLOWED_FIELDS = {"student_id", "course_id", "grade"}

def method_not_allowed():
    abort(405, message="method not allowed on this endpoint")

# ── Routes simples ────────────────────────────────────────────────────────────
@app.route("/")
def index():
    return "Project Server — Student Course Tracker"

# ── STUDENTS (collection) ─────────────────────────────────────────────────────
class Students(Resource):
    def get(self):
        students = [s.to_dict() for s in Student.query.order_by(Student.id).all()]
        return make_response(jsonify(students), 200)

    def post(self):
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        email = (data.get("email") or "").strip()
        year = int(data.get("year", 1))

        if not name:
            abort(400, message="name is required")
        if not EMAIL_RE.match(email):
            abort(400, message="email format invalid")

        s = Student(name=name, email=email, year=year)
        db.session.add(s)
        db.session.commit()
        return make_response(s.to_dict(), 201)

    # Pas logique sur une collection → 405
    def patch(self):  # update bulk (non supporté)
        method_not_allowed()

    def delete(self):  # delete bulk (non supporté)
        method_not_allowed()

# ── STUDENT by ID ─────────────────────────────────────────────────────────────
class StudentByID(Resource):
    def get(self, id):
        s = Student.query.get_or_404(id)
        return make_response(s.to_dict(), 200)

    def post(self, id):  # créer sur /:id non supporté
        method_not_allowed()

    def patch(self, id):
        s = Student.query.get_or_404(id)
        data = request.get_json() or {}

        for k, v in data.items():
            if k in STUDENT_ALLOWED_FIELDS:
                if k == "email" and not EMAIL_RE.match(v or ""):
                    abort(400, message="email format invalid")
                if k == "name":
                    v = (v or "").strip()
                    if not v:
                        abort(400, message="name is required")
                if k == "year":
                    v = int(v)
                setattr(s, k, v)

        db.session.commit()
        return make_response(s.to_dict(), 200)

    def delete(self, id):
        s = Student.query.get_or_404(id)
        db.session.delete(s)
        db.session.commit()
        return make_response({}, 204)

# ── INSTRUCTORS (collection) ──────────────────────────────────────────────────
class Instructors(Resource):
    def get(self):
        items = [i.to_dict() for i in Instructor.query.order_by(Instructor.id).all()]
        return make_response(jsonify(items), 200)

    def post(self):
        data = request.get_json() or {}
        name = (data.get("name") or "").strip()
        specialty = (data.get("specialty") or "").strip()
        if not name:
            abort(400, message="name is required")

        i = Instructor(name=name, specialty=specialty)
        db.session.add(i)
        db.session.commit()
        return make_response(i.to_dict(), 201)

    def patch(self):   # bulk update non supporté
        method_not_allowed()

    def delete(self):  # bulk delete non supporté
        method_not_allowed()

# ── INSTRUCTOR by ID ──────────────────────────────────────────────────────────
class InstructorByID(Resource):
    def get(self, id):
        i = Instructor.query.get_or_404(id)
        return make_response(i.to_dict(), 200)

    def post(self, id):
        method_not_allowed()

    def patch(self, id):
        i = Instructor.query.get_or_404(id)
        data = request.get_json() or {}

        for k, v in data.items():
            if k in INSTR_ALLOWED_FIELDS:
                if k == "name":
                    v = (v or "").strip()
                    if not v:
                        abort(400, message="name is required")
                setattr(i, k, v)

        db.session.commit()
        return make_response(i.to_dict(), 200)

    def delete(self, id):
        i = Instructor.query.get_or_404(id)
        db.session.delete(i)
        db.session.commit()
        return make_response({}, 204)

# ── COURSES (collection) ──────────────────────────────────────────────────────
class Courses(Resource):
    def get(self):
        q = Course.query
        level = request.args.get("level")
        instructor_id = request.args.get("instructor_id", type=int)
        if level:
            q = q.filter(Course.level == level)
        if instructor_id:
            q = q.filter(Course.instructor_id == instructor_id)
        items = [c.to_dict(include_instructor=True) for c in q.order_by(Course.id)]
        return make_response(jsonify(items), 200)

    def post(self):
        data = request.get_json() or {}
        title = (data.get("title") or "").strip()
        duration = int(data.get("duration", 0))
        level = (data.get("level") or "beginner").strip().lower()
        instructor_id = data.get("instructor_id")

        if not title:
            abort(400, message="title is required")
        if duration <= 0:
            abort(400, message="duration must be a positive integer")
        if instructor_id is None:
            abort(400, message="instructor_id is required")

        c = Course(title=title, duration=duration, level=level, instructor_id=instructor_id)
        db.session.add(c)
        db.session.commit()
        return make_response(c.to_dict(include_instructor=True), 201)

    def patch(self):
        method_not_allowed()

    def delete(self):
        method_not_allowed()

# ── COURSE by ID ──────────────────────────────────────────────────────────────
class CourseByID(Resource):
    def get(self, id):
        c = Course.query.get_or_404(id)
        return make_response(c.to_dict(include_instructor=True, include_students=True), 200)

    def post(self, id):
        method_not_allowed()

    def patch(self, id):
        c = Course.query.get_or_404(id)
        data = request.get_json() or {}

        for k, v in data.items():
            if k in COURSE_ALLOWED_FIELDS:
                if k == "duration":
                    v = int(v)
                    if v <= 0:
                        abort(400, message="duration must be positive")
                if k == "title":
                    v = (v or "").strip()
                    if not v:
                        abort(400, message="title is required")
                setattr(c, k, v)

        db.session.commit()
        return make_response(c.to_dict(include_instructor=True), 200)

    def delete(self, id):
        c = Course.query.get_or_404(id)
        db.session.delete(c)
        db.session.commit()
        return make_response({}, 204)

# ── ENROLLMENTS (collection) ──────────────────────────────────────────────────
class Enrollments(Resource):
    def get(self):
        items = [e.to_dict() for e in Enrollment.query.order_by(Enrollment.id)]
        return make_response(jsonify(items), 200)

    def post(self):
        data = request.get_json() or {}
        student_id = data.get("student_id")
        course_id = data.get("course_id")
        grade = data.get("grade", None)

        if student_id is None or course_id is None:
            abort(400, message="student_id and course_id are required")

        if grade is not None:
            try:
                grade = float(grade)
                if not (0 <= grade <= 100):
                    abort(400, message="grade must be between 0 and 100")
            except Exception:
                abort(400, message="grade must be numeric")

        e = Enrollment(student_id=student_id, course_id=course_id, grade=grade)
        db.session.add(e)
        db.session.commit()
        return make_response(e.to_dict(), 201)

    def patch(self):
        method_not_allowed()

    def delete(self):
        method_not_allowed()

# ── ENROLLMENT by ID ──────────────────────────────────────────────────────────
class EnrollmentByID(Resource):
    def get(self, id):
        e = Enrollment.query.get_or_404(id)
        return make_response(e.to_dict(), 200)

    def post(self, id):
        method_not_allowed()

    def patch(self, id):
        e = Enrollment.query.get_or_404(id)
        data = request.get_json() or {}

        for k, v in data.items():
            if k in ENROLL_ALLOWED_FIELDS:
                if k == "grade":
                    try:
                        v = float(v)
                    except Exception:
                        abort(400, message="grade must be numeric")
                    if not (0 <= v <= 100):
                        abort(400, message="grade must be between 0 and 100")
                setattr(e, k, v)

        db.session.commit()
        return make_response(e.to_dict(), 200)

    def delete(self, id):
        e = Enrollment.query.get_or_404(id)
        db.session.delete(e)
        db.session.commit()
        return make_response({}, 204)

# ── Bind resources (préfixe /api) ─────────────────────────────────────────────
api.add_resource(Students,        "/api/students")
api.add_resource(StudentByID,     "/api/students/<int:id>")

api.add_resource(Instructors,     "/api/instructors")
api.add_resource(InstructorByID,  "/api/instructors/<int:id>")

api.add_resource(Courses,         "/api/courses")
api.add_resource(CourseByID,      "/api/courses/<int:id>")

api.add_resource(Enrollments,     "/api/enrollments")
api.add_resource(EnrollmentByID,  "/api/enrollments/<int:id>")

# ── Run ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app.run(port=5555, debug=True)
