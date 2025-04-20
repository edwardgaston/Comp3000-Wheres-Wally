import React, { useState } from 'react';
import axios from 'axios';

const UploadForm = ({ onResult }) => {
  const [image, setImage] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
    setPreview(URL.createObjectURL(file));
  };

  const handleUpload = async () => {
    if (!image) return;
    setLoading(true);

    const formData = new FormData();
    formData.append('image', image);

    try {
      const res = await axios.post('http://localhost:5000/api/detect', formData);
      onResult(res.data);  // bounding boxes or annotated image URL
    } catch (err) {
      console.error(err);
      alert("Detection failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-form">
      <input type="file" accept="image/*" onChange={handleChange} />
      {preview && <img src={preview} alt="preview" style={{ width: '300px' }} />}
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Detecting..." : "Find Wally!"}
      </button>
    </div>
  );
};

export default UploadForm;
