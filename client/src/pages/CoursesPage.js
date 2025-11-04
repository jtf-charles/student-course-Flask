import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  title: Yup.string().required("Required"),
  duration: Yup.number().positive("Must be > 0").required("Required"),
  level: Yup.string().oneOf(["beginner", "intermediate", "advanced"]).required(),
  instructor_id: Yup.number().required("Required"),
});

export default function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [instructors, setInstructors] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    const [c, i] = await Promise.all([
      fetch("/api/courses").then(r => r.json()),
      fetch("/api/instructors").then(r => r.json()),
    ]);
    setCourses(c);
    setInstructors(i);
  };
  useEffect(() => { load(); }, []);

  const createCourse = async (values, actions) => {
    const r = await fetch("/api/courses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    if (r.ok) { actions.resetForm(); load(); } else { alert("Create failed"); }
  };

  const startEdit = (course) => setEditingId(course.id);
  const cancelEdit = () => setEditingId(null);

  const submitEdit = async (id, values) => {
    const r = await fetch(`/api/courses/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    if (!r.ok) { alert("Update failed"); return; }
    setEditingId(null);
    load();
  };

  const deleteCourse = async (id) => {
    if (!window.confirm("Delete this course?")) return;
    const r = await fetch(`/api/courses/${id}`, { method: "DELETE" });
    if (r.status === 204) load(); else alert("Delete failed");
  };

  const EditForm = ({ course }) => (
    <Formik
      initialValues={{
        title: course.title,
        duration: course.duration,
        level: course.level,
        instructor_id: course.instructor_id,
      }}
      validationSchema={schema}
      onSubmit={(vals)=>submitEdit(course.id, vals)}
    >
      <Form className="inline-form">
        <label>Title<Field name="title" /></label>
        <ErrorMessage name="title" component="div" className="error" />

        <label>Duration (hours)<Field name="duration" type="number" min="1" /></label>
        <ErrorMessage name="duration" component="div" className="error" />

        <label>Level
          <Field as="select" name="level">
            <option value="beginner">beginner</option>
            <option value="intermediate">intermediate</option>
            <option value="advanced">advanced</option>
          </Field>
        </label>

        <label>Instructor
          <Field as="select" name="instructor_id">
            <option value="">-- choose --</option>
            {instructors.map(i => (
              <option key={i.id} value={i.id}>{i.name}</option>
            ))}
          </Field>
        </label>

        <div className="actions">
          <button type="submit" className="small">Save</button>
          <button type="button" className="btn-secondary small" onClick={cancelEdit}>Cancel</button>
        </div>
      </Form>
    </Formik>
  );

  return (
    <div>
      <h2>Courses</h2>
      <ul className="list">
        {courses.map(c => (
          <li key={c.id} className="card">
            <div>
              <Link to={`/courses/${c.id}`}>{c.title}</Link> — {c.level} — {c.duration}h
              {!!c.instructor && <> (by {c.instructor.name})</>}
            </div>

            {editingId === c.id ? (
              <EditForm course={c} />
            ) : (
              <div className="actions" style={{marginTop:8}}>
                <button className="small" onClick={()=>startEdit(c)}>Edit</button>
                <button className="btn-danger small" onClick={()=>deleteCourse(c.id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>

      <h3>Add Course</h3>
      <Formik
        initialValues={{ title: "", duration: 10, level: "beginner", instructor_id: "" }}
        validationSchema={schema}
        onSubmit={createCourse}
      >
        <Form style={{ display: "grid", gap: 8, maxWidth: 420 }}>
          <label>Title<Field name="title" /></label>
          <ErrorMessage name="title" component="div" className="error" />

          <label>Duration (hours)<Field name="duration" type="number" min="1" /></label>
          <ErrorMessage name="duration" component="div" className="error" />

          <label>Level
            <Field as="select" name="level">
              <option value="beginner">beginner</option>
              <option value="intermediate">intermediate</option>
              <option value="advanced">advanced</option>
            </Field>
          </label>

          <label>Instructor
            <Field as="select" name="instructor_id">
              <option value="">-- choose --</option>
              {instructors.map(i => (
                <option key={i.id} value={i.id}>{i.name}</option>
              ))}
            </Field>
          </label>
          <ErrorMessage name="instructor_id" component="div" className="error" />

          <button type="submit">Create</button>
        </Form>
      </Formik>
    </div>
  );
}
