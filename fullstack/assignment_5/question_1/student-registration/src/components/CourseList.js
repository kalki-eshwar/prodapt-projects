import React, { useContext } from 'react';
import StudentContext from '../context/StudentContext';

const availableCourses = ['React', 'Python', 'Data Science'];

const CourseList = () => {
  const { selectedCourses, toggleCourse } = useContext(StudentContext);

  const handleCheckboxChange = (course) => {
    toggleCourse(course);
  };

  return (
    <div>
      <h2>Select Courses</h2>
      <ul>
        {availableCourses.map(course => (
          <li key={course}>
            <label>
              <input
                type="checkbox"
                checked={selectedCourses.includes(course)}
                onChange={() => handleCheckboxChange(course)}
              />
              {course}
            </label>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CourseList;