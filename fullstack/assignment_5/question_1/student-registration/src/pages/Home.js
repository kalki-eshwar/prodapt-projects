import React, { useContext } from 'react';
import StudentForm from '../components/StudentForm';
import CourseList from '../components/CourseList';
import SelectedCourses from '../components/SelectedCourses';
import Summary from '../components/Summary';
import StudentContext from '../context/StudentContext';

const Home = () => {
  const { isSubmitted } = useContext(StudentContext);

  if (isSubmitted) {
    return <Summary />;
  }

  return (
    <div>
      <StudentForm />
      <CourseList />
      <SelectedCourses />
      <Summary />
    </div>
  );
};

export default Home;