import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const enrollSchema = Yup.object({
  student_id: Yup.number().required("Required"),
  grade: Yup.number().min(0).max(100, "0-100").nullable(true),
});

const gradeSchema = Yup.object({
  grade: Yup.number().min(0).max(100, "0-100").required("Required"),
});

export default function CourseDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [course, setCourse] = useState(null);
  const [students, setStudents] = useState([]);
  const [editingEnrollment, setEditingEnrollment] = useState(null);

  const load = async () => {
    const c = await fetch(`/api/courses/${id}`).then(r => r.json());
    const s = await fetch(`/api/students`).then(r => r.json());
    setCourse(c);
    setStudents(s);
  };
  useEffect(() => { load(); }, [id]);

  const enroll = async (values, actions) => {
    const r = await fetch("/api/enrollments", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...values, course_id: Number(id) }),
    });
    if (r.ok) { actions.resetForm(); load(); } else { alert("Enroll failed"); }
  };

  const deleteCourse = async () => {
    if (!window.confirm("Delete this course?")) return;
    const r = await fetch(`/api/courses/${id}`, { method: "DELETE" });
    if (r.status === 204) navigate("/courses"); else alert("Delete failed");
  };

  const updateGrade = async (enrollmentId, values) => {
    const r = await fetch(`/api/enrollments/${enrollmentId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    if (!r.ok) { alert("Update failed"); return; }
    setEditingEnrollment(null);
    load();
  };

  const removeEnrollment = async (enrollmentId) => {
    if (!window.confirm("Remove this enrollment?")) return;
    const r = await fetch(`/api/enrollments/${enrollmentId}`, { method: "DELETE" });
    if (r.status === 204) load(); else alert("Delete failed");
  };

  if (!course) return <p>Loading…</p>;

  return (
    <div>
      <h2>{course.title}</h2>
      <p>
        Level: {course.level} — {course.duration}h<br />
        Instructor: {course.instructor?.name}
      </p>

      <h3>Enrolled Students</h3>
      <ul className="list">
        {course.students?.map(s => (
          <li key={s.enrollment_id} className="card">
            <div style={{display:"flex", justifyContent:"space-between", gap:12}}>
              <span>{s.name} — grade: {s.grade ?? "N/A"}</span>
              <div className="actions">
                <button className="small" onClick={()=>setEditingEnrollment(s.enrollment_id)}>Edit grade</button>
                <button className="btn-danger small" onClick={()=>removeEnrollment(s.enrollment_id)}>Remove</button>
              </div>
            </div>

            {editingEnrollment === s.enrollment_id && (
              <Formik
                initialValues={{ grade: s.grade ?? 0 }}
                validationSchema={gradeSchema}
                onSubmit={(vals)=>updateGrade(s.enrollment_id, vals)}
              >
                <Form className="inline-form">
                  <label>Grade (0–100)<Field name="grade" type="number" min="0" max="100" /></label>
                  <ErrorMessage name="grade" component="div" className="error" />
                  <div className="actions">
                    <button type="submit" className="small">Save</button>
                    <button type="button" className="btn-secondary small" onClick={()=>setEditingEnrollment(null)}>Cancel</button>
                  </div>
                </Form>
              </Formik>
            )}
          </li>
        ))}
      </ul>

      <h3>Enroll a student</h3>
      <Formik
        initialValues={{ student_id: "", grade: "" }}
        validationSchema={enrollSchema}
        onSubmit={enroll}
      >
        <Form style={{ display: "grid", gap: 8, maxWidth: 360 }}>
          <label>Student
            <Field as="select" name="student_id">
              <option value="">-- choose --</option>
              {students.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
            </Field>
          </label>
          <ErrorMessage name="student_id" component="div" className="error" />

          <label>Grade (optional)
            <Field name="grade" type="number" min="0" max="100" />
          </label>
          <ErrorMessage name="grade" component="div" className="error" />

          <button type="submit">Enroll</button>
        </Form>
      </Formik>

      <hr />
      <button onClick={deleteCourse} className="btn-danger">Delete Course</button>
    </div>
  );
}
