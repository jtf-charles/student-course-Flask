# 🎓 Student Course Tracker

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-API-green?logo=flask)
![React](https://img.shields.io/badge/React-Frontend-61dafb?logo=react)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

> Une application **Full Stack Flask + React** pour la gestion des **étudiants, cours et inscriptions**, avec un design moderne et des fonctionnalités CRUD complètes.

---

## 🧭 Sommaire
- [🎯 Objectif du projet](#-objectif-du-projet)
- [⚙️ Fonctionnalités principales](#️-fonctionnalités-principales)
- [🧩 Architecture du projet](#-architecture-du-projet)
- [🗄️ Backend – Flask API](#️-backend--flask-api)
- [💻 Frontend – React](#-frontend--react)
- [📦 Installation & Lancement](#-installation--lancement)
- [🧱 Structure des dossiers](#-structure-des-dossiers)
- [🧪 Tests et validations](#-tests-et-validations)
- [🚀 Améliorations futures](#-améliorations-futures)
- [👥 Auteurs](#-auteurs)
- [📝 Licence](#-licence)

---

## 🎯 Objectif du projet

Ce projet a été conçu dans le cadre d’un exercice complet de **développement web Full Stack**, combinant :
- Un **backend Flask RESTful** avec base de données relationnelle (SQLite),
- Un **frontend React moderne**, utilisant des formulaires validés avec **Formik + Yup**,
- Une **architecture claire et modulaire** conforme aux bonnes pratiques du développement professionnel.

L’application permet de gérer :
- Les **étudiants** 👨‍🎓  
- Les **cours** 📘  
- Les **inscriptions et notes** 🤝

---

## ⚙️ Fonctionnalités principales

### 🎓 Étudiants
- Création, modification et suppression d’un étudiant  
- Validation d’email et d’année d’étude  
- Affichage dynamique de la liste complète des étudiants

### 📘 Cours
- CRUD complet sur les cours  
- Attribution à un **instructeur**  
- Filtrage par niveau (`beginner`, `intermediate`, `advanced`)  
- Vue détaillée d’un cours avec liste des étudiants inscrits  

### 🤝 Inscriptions
- Enregistrement d’un étudiant à un cours  
- Attribution d’une **note (grade)**  
- Édition et suppression d’inscriptions  

### 💅 Interface moderne
- Thème sombre élégant  
- Navigation fluide via **React Router v6**  
- Validation en temps réel avec **Formik + Yup**  
- Appels API asynchrones via `fetch()`  

---

## 🧩 Architecture du projet

```bash
student-course-tracker/
│
├── server/                    # Backend Flask API
│   ├── app.py                 # Application principale Flask
│   ├── models.py              # Modèles SQLAlchemy
│   ├── seed.py                # Données initiales
│   ├── migrations/            # Migrations Flask-Migrate
│   └── instance/app.db        # Base SQLite
│
├── client/                    # Frontend React
│   ├── src/
│   │   ├── components/        # Composants communs (Navbar, App)
│   │   ├── pages/             # Pages principales
│   │   │   ├── CoursesPage.js
│   │   │   ├── CourseDetailPage.js
│   │   │   └── StudentsPage.js
│   │   ├── index.css          # Styles globaux (thème sombre)
│   │   └── index.js           # Point d'entrée React
│   ├── package.json
│   └── public/
│
├── Pipfile                    # Dépendances Python
├── README.md                  # Documentation
└── LICENSE.md                 # Licence MIT



## 🗄️ Backend – Flask API

### ⚙️ Technologies utilisées
- **Flask**
- **Flask-RESTful**
- **Flask-Migrate**
- **SQLAlchemy ORM**
- **SQLite** (par défaut, mais facilement extensible vers PostgreSQL)

---

### 🔗 Endpoints principaux

| Ressource | Méthode | URL | Description |
|------------|----------|-----|-------------|
| **Courses** | `GET` | `/api/courses` | Liste de tous les cours |
| **Courses** | `POST` | `/api/courses` | Créer un nouveau cours |
| **Courses** | `PATCH` | `/api/courses/<id>` | Modifier un cours existant |
| **Courses** | `DELETE` | `/api/courses/<id>` | Supprimer un cours |
| **Students** | `GET` | `/api/students` | Liste de tous les étudiants |
| **Students** | `POST` | `/api/students` | Ajouter un nouvel étudiant |
| **Students** | `PATCH` | `/api/students/<id>` | Modifier un étudiant |
| **Students** | `DELETE` | `/api/students/<id>` | Supprimer un étudiant |
| **Enrollments** | `POST` | `/api/enrollments` | Inscrire un étudiant à un cours |
| **Enrollments** | `PATCH` | `/api/enrollments/<id>` | Modifier une note |
| **Enrollments** | `DELETE` | `/api/enrollments/<id>` | Supprimer une inscription |

---

### 💾 Exemple de modèle SQLAlchemy

```python
class Course(db.Model):
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    level = db.Column(db.String(50), nullable=False)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructors.id'))

    instructor = db.relationship('Instructor', back_populates='courses')
    enrollments = db.relationship('Enrollment', back_populates='course')

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "duration": self.duration,
            "level": self.level,
            "instructor": self.instructor.name if self.instructor else None
        }








## 🚀 Installation & Lancement du projet

Cette section décrit pas à pas comment installer et exécuter le projet **Student Course Tracker** en local.  
Le projet combine un **backend Flask (API)** et un **frontend React** interconnectés.

---

### 💼 Prérequis

Avant de commencer, assurez-vous d’avoir installé :

- 🐍 **Python ≥ 3.10**
- ⚙️ **Node.js ≥ 18**
- 📦 **Pipenv** ou **virtualenv**
- 🌐 **npm** (installé automatiquement avec Node.js)

---

### 1️⃣ Cloner le projet

Ouvrez votre terminal et exécutez :

```bash
git clone https://github.com/jtf-charles/student-course-flask.git
cd student-course-flask



### 🧪 Exemple complet d’exécution

```bash
# Étape 1 - Backend
cd server
pipenv install
pipenv shell
flask db upgrade
python seed.py
flask run

# Étape 2 - Frontend
cd ../client
npm install
npm start
