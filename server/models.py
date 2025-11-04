from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

# le db est déclaré ici puis initialisé dans app.py avec db.init_app(app)
db = SQLAlchemy()


# ── MODELS ────────────────────────────────────────────────────────────────────
class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    year = db.Column(db.Integer, default=1)

    enrollments = db.relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "year": self.year}


class Instructor(db.Model):
    __tablename__ = "instructors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    specialty = db.Column(db.String(120), default="")

    courses = db.relationship(
        "Course",
        back_populates="instructor",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {"id": self.id, "name": self.name, "specialty": self.specialty}


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # heures
    level = db.Column(db.String(20), default="beginner")

    instructor_id = db.Column(db.Integer, db.ForeignKey("instructors.id"), nullable=False)
    instructor = db.relationship("Instructor", back_populates="courses")

    enrollments = db.relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan",
    )

    def to_dict(self, include_instructor=False, include_students=False):
        payload = {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "level": self.level,
            "instructor_id": self.instructor_id,
        }
        if include_instructor:
            payload["instructor"] = self.instructor.to_dict() if self.instructor else None
        if include_students:
            payload["students"] = [
                {
                    "id": e.student.id,
                    "name": e.student.name,
                    "email": e.student.email,
                    "grade": e.grade,
                    "enrolled_at": e.enrolled_at.isoformat(),
                    "enrollment_id": e.id,
                }
                for e in self.enrollments
            ]
        return payload


class Enrollment(db.Model):
    __tablename__ = "enrollments"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    grade = db.Column(db.Float, nullable=True)
    enrolled_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    __table_args__ = (UniqueConstraint("student_id", "course_id", name="uq_student_course"),)

    def to_dict(self):
        return {
            "id": self.id,
            "student_id": self.student_id,
            "course_id": self.course_id,
            "grade": self.grade,
            "enrolled_at": self.enrolled_at.isoformat() if self.enrolled_at else None,
        }
