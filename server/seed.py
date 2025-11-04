#!/usr/bin/env python3
import random
from datetime import datetime, timedelta

from faker import Faker

# importe l'app Flask et les modèles
from app import app
from models import db, Student, Instructor, Course, Enrollment

fake = Faker()


def reset_tables():
    """Efface les données existantes sans drop_all() (préserve les migrations)."""
    Enrollment.query.delete()
    Course.query.delete()
    Student.query.delete()
    Instructor.query.delete()
    db.session.commit()


def seed_instructors():
    specialties = ["Mathematics", "Physics", "Biology", "Computer Science", "Economics"]
    instructors = []
    for spec in specialties:
        inst = Instructor(name=fake.name(), specialty=spec)
        db.session.add(inst)
        instructors.append(inst)
    db.session.commit()
    return instructors


def seed_courses(instructors):
    courses = []
    # 2 cours par instructeur
    levels = ["beginner", "intermediate", "advanced"]
    for inst in instructors:
        for _ in range(2):
            c = Course(
                title=fake.job(),
                duration=random.randint(12, 60),   # heures
                level=random.choice(levels),
                instructor_id=inst.id,
            )
            db.session.add(c)
            courses.append(c)
    db.session.commit()
    return courses


def seed_students(n=16):
    students = []
    for _ in range(n):
        s = Student(
            name=fake.name(),
            email=fake.unique.email(),
            year=random.randint(1, 4),
        )
        db.session.add(s)
        students.append(s)
    db.session.commit()
    return students


def seed_enrollments(students, courses):
    created = 0
    for s in students:
        # chaque étudiant prend 2 à 5 cours distincts
        chosen = random.sample(courses, k=random.randint(2, min(5, len(courses))))
        for c in chosen:
            # respect du UniqueConstraint (student_id, course_id)
            exists = (
                Enrollment.query.filter_by(student_id=s.id, course_id=c.id).first()
                is not None
            )
            if exists:
                continue

            # grade optionnel (70% des cas)
            grade = round(random.uniform(50, 100), 2) if random.random() < 0.7 else None
            enrolled_at = datetime.utcnow() - timedelta(days=random.randint(0, 180))

            e = Enrollment(
                student_id=s.id,
                course_id=c.id,
                grade=grade,
                enrolled_at=enrolled_at,
            )
            db.session.add(e)
            created += 1
    db.session.commit()
    return created


def run():
    with app.app_context():
        print("Seeding database…")
        reset_tables()

        instructors = seed_instructors()
        print(f"  → {len(instructors)} instructors")

        courses = seed_courses(instructors)
        print(f"  → {len(courses)} courses")

        students = seed_students(n=18)
        print(f"  → {len(students)} students")

        n_enroll = seed_enrollments(students, courses)
        print(f"  → {n_enroll} enrollments")

        print("Seed complete ✅")


if __name__ == "__main__":
    run()
