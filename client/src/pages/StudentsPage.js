import { useEffect, useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const schema = Yup.object({
  name: Yup.string().required("Required"),
  email: Yup.string().email("Invalid email").required("Required"),
  year: Yup.number().min(1).max(4).required("Required"),
});

export default function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [editingId, setEditingId] = useState(null);

  const load = async () => {
    const r = await fetch("/api/students");
    setStudents(await r.json());
  };
  useEffect(() => { load(); }, []);

  const createStudent = async (values, actions) => {
    const r = await fetch("/api/students", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    if (r.ok) { actions.resetForm(); load(); } else { alert("Create failed"); }
  };

  const deleteStudent = async (id) => {
    if (!window.confirm("Delete this student?")) return;
    const r = await fetch(`/api/students/${id}`, { method: "DELETE" });
    if (r.status === 204) load(); else alert("Delete failed");
  };

  const submitEdit = async (id, values) => {
    const r = await fetch(`/api/students/${id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });
    if (!r.ok) { alert("Update failed"); return; }
    setEditingId(null);
    load();
  };

  const EditForm = ({ s }) => (
    <Formik
      initialValues={{ name: s.name, email: s.email, year: s.year }}
      validationSchema={schema}
      onSubmit={(vals)=>submitEdit(s.id, vals)}
    >
      <Form className="inline-form">
        <label>Name<Field name="name" /></label>
        <ErrorMessage name="name" component="div" className="error" />
        <label>Email<Field name="email" /></label>
        <ErrorMessage name="email" component="div" className="error" />
        <label>Year<Field name="year" type="number" min="1" max="4" /></label>
        <ErrorMessage name="year" component="div" className="error" />
        <div className="actions">
          <button type="submit" className="small">Save</button>
          <button type="button" className="btn-secondary small" onClick={()=>setEditingId(null)}>Cancel</button>
        </div>
      </Form>
    </Formik>
  );

  return (
    <div>
      <h2>Students</h2>
      <ul className="list">
        {students.map(s => (
          <li key={s.id} className="card">
            <div>{s.name} — {s.email} (Year {s.year})</div>
            {editingId === s.id ? (
              <EditForm s={s} />
            ) : (
              <div className="actions" style={{marginTop:8}}>
                <button className="small" onClick={()=>setEditingId(s.id)}>Edit</button>
                <button className="btn-danger small" onClick={()=>deleteStudent(s.id)}>Delete</button>
              </div>
            )}
          </li>
        ))}
      </ul>

      <h3>Add Student</h3>
      <Formik
        initialValues={{ name: "", email: "", year: 1 }}
        validationSchema={schema}
        onSubmit={createStudent}
      >
        <Form style={{ display: "grid", gap: 8, maxWidth: 360 }}>
          <label>Name<Field name="name" /></label>
          <ErrorMessage name="name" component="div" className="error" />
          <label>Email<Field name="email" /></label>
          <ErrorMessage name="email" component="div" className="error" />
          <label>Year<Field name="year" type="number" min="1" max="4" /></label>
          <ErrorMessage name="year" component="div" className="error" />
          <button type="submit">Create</button>
        </Form>
      </Formik>
    </div>
  );
}
