import React from 'react';
import Detect from '../components/Detect';
import Result from '../components/Result';

const Dashboard = () => {
  return (
    <div className="dashboard-page">
      <h1>Dashboard</h1>
      <Detect />
      <Result />
    </div>
  );
};

export default Dashboard;
