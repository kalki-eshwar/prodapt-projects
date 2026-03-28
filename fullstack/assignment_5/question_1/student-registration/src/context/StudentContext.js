import React, { createContext, useState } from 'react';

const StudentContext = createContext();

export const StudentProvider = ({ children }) => {
  const [studentDetails, setStudentDetails] = useState({
    name: '',
    email: '',
    phone: '',
  });

  const [selectedCourses, setSelectedCourses] = useState([]);
  const [isSubmitted, setIsSubmitted] = useState(false);

  const updateStudentDetails = (name, value) => {
    setStudentDetails((prev) => ({ ...prev, [name]: value }));
  };

  const toggleCourse = (course) => {
    setSelectedCourses((prev) => 
      prev.includes(course) ? prev.filter(c => c !== course) : [...prev, course]
    );
  };

  const submitRegistration = () => {
    setIsSubmitted(true);
  };

  return (
    <StudentContext.Provider value={{
      studentDetails,
      selectedCourses,
      isSubmitted,
      updateStudentDetails,
      toggleCourse,
      submitRegistration
    }}>
      {children}
    </StudentContext.Provider>
  );
};

export default StudentContext;
