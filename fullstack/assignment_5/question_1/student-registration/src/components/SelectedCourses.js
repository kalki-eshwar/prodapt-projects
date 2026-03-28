import React, { useContext } from 'react';
import StudentContext from '../context/StudentContext';

const SelectedCourses = () => {
  const { selectedCourses, toggleCourse } = useContext(StudentContext);

  if (selectedCourses.length === 0) return <div>No courses selected.</div>;

  return (
    <div>
      <h2>Selected Courses</h2>
      <ul>
        {selectedCourses.map(course => (
          <li key={course}>
            {course} <button onClick={() => toggleCourse(course)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SelectedCourses;