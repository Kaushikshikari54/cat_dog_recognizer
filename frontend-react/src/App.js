import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Handle image selection and preview
  const onFileChange = (e) => {
    const selectedFile = e.target.files[0];
    setFile(selectedFile);
    setPreview(URL.createObjectURL(selectedFile));
    setResult(null); // Clear previous results
  };

  // Send image to Flask Backend
  const uploadImage = async () => {
    if (!file) return alert("Please select an image first!");

    setLoading(true);
    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
        method: "POST",
        body: formData,
      });
      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.error("Error:", error);
      setResult({ error: "Backend is offline. Run 'python app.py'" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="main-card">
        <header>
          <div className="badge">AI Powered (React)</div>
          <h1>Cat vs Dog <span className="gradient-text">Classifier</span></h1>
        </header>

        <div className="upload-container">
          <label className="drop-zone">
            📷 {file ? file.name : "Click to upload image"}
            <input type="file" onChange={onFileChange} accept="image/*" hidden />
          </label>

          {preview && (
            <div className="image-preview">
              <img src={preview} alt="Selected" />
            </div>
          )}

          <button onClick={uploadImage} disabled={loading}>
            {loading ? "Analyzing..." : "Run Classification"}
          </button>
        </div>

        {result && (
          <div className="result-display">
            {result.error ? (
              <p className="error">{result.error}</p>
            ) : (
              <>
                <div className="prediction-label">{result.prediction}</div>
                <div className="confidence-value">
                  Confidence: {(result.confidence * 100).toFixed(2)}%
                </div>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default App;