import React, { useContext, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProductList from '../components/ProductList';
import { AuthContext } from '../context/AuthContext';


const Dashboard = () => {
    const { user } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!user) {
            navigate('/login');
        }
    }, [user, navigate]);

    if (!user) return null;

    return (
        <div className="dashboard-container">
            <header className="dashboard-header">
                <h1>Welcome, {user.name}</h1>
                <p>Enjoy our exclusive products!</p>
            </header>
            <main>
                <h2>Products:</h2>
                <ProductList />
            </main>
        </div>
    );
};

export default Dashboard;
