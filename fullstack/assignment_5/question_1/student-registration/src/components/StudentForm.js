import React, { useContext } from 'react';
import StudentContext from '../context/StudentContext';

const StudentForm = () => {
  const { studentDetails, updateStudentDetails } = useContext(StudentContext);

  const handleChange = (e) => {
    const { name, value } = e.target;
    updateStudentDetails(name, value);
  };

  return (
    <div>
      <h2>Student Details</h2>
      <form>
        <div>
          <label>Name:</label>
          <input type="text" name="name" value={studentDetails.name} onChange={handleChange} />
        </div>
        <div>
          <label>Email:</label>
          <input type="email" name="email" value={studentDetails.email} onChange={handleChange} />
        </div>
        <div>
          <label>Phone:</label>
          <input type="tel" name="phone" value={studentDetails.phone} onChange={handleChange} />
        </div>
      </form>
    </div>
  );
};

export default StudentForm;