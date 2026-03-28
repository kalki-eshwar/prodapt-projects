import React, { useContext } from 'react';
import StudentContext from '../context/StudentContext';

const Summary = () => {
  const { studentDetails, selectedCourses, isSubmitted, submitRegistration } = useContext(StudentContext);

  if (isSubmitted) {
    return (
      <div className="summary">
        <h2>Registration Summary</h2>
        <p>Name: {studentDetails.name}</p>
        <p>Email: {studentDetails.email}</p>
        <p>Phone: {studentDetails.phone}</p>
        <h3>Courses Enrolled:</h3>
        <ul>
          {selectedCourses.map(course => <li key={course}>- {course}</li>)}
        </ul>
        <p>Status: Registration Successful ✅</p>
      </div>
    );
  }

  const isFormComplete = studentDetails.name && studentDetails.email && studentDetails.phone && selectedCourses.length > 0;

  return (
    <div>
      <button onClick={submitRegistration} disabled={!isFormComplete}>
        Submit Registration
      </button>
    </div>
  );
};

export default Summary;