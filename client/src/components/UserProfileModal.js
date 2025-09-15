import React, { useState } from 'react';

const UserProfileModal = ({ isOpen, onSubmit, onClose }) => {
  const [profile, setProfile] = useState({
    user_type: '',
    age_group: '',
    work_hours: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (profile.user_type && profile.age_group && profile.work_hours) {
      onSubmit(profile);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <h2>Welcome to the Longevity Research Study</h2>
        <p>Please answer a few quick questions to help us with our research:</p>
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Are you a founder or employee?</label>
            <select 
              value={profile.user_type} 
              onChange={(e) => setProfile({...profile, user_type: e.target.value})}
              required
            >
              <option value="">Select...</option>
              <option value="founder">Founder</option>
              <option value="employee">Employee</option>
            </select>
          </div>

          <div className="form-group">
            <label>Age group:</label>
            <select 
              value={profile.age_group} 
              onChange={(e) => setProfile({...profile, age_group: e.target.value})}
              required
            >
              <option value="">Select...</option>
              <option value="18-25">18-25</option>
              <option value="26-35">26-35</option>
              <option value="36-45">36-45</option>
              <option value="46-55">46-55</option>
              <option value="56+">56+</option>
            </select>
          </div>

          <div className="form-group">
            <label>How many hours per week do you work?</label>
            <select 
              value={profile.work_hours} 
              onChange={(e) => setProfile({...profile, work_hours: e.target.value})}
              required
            >
              <option value="">Select...</option>
              <option value="20-30">20-30 hours</option>
              <option value="31-40">31-40 hours</option>
              <option value="41-50">41-50 hours</option>
              <option value="51-60">51-60 hours</option>
              <option value="60+">60+ hours</option>
            </select>
          </div>

          <div className="modal-buttons">
            <button type="submit" className="submit-btn">
              Start Chatting
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UserProfileModal;