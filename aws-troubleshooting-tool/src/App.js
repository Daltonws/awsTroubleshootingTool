import React, { useState } from 'react';

function TroubleshootForm() {
    const [formData, setFormData] = useState({
        platform: '',
        service: '',
        error_code: '',
        runtime: '',
        error_description: ''
    });
    const [response, setResponse] = useState('');
    const [submitStatus, setSubmitStatus] = useState({ submitted: false, success: false, message: '' });

    // Handles changes in form fields
    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    // Handles form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        setSubmitStatus({ submitted: false, success: false, message: '' });

        try {
            const dataToSend = {
                ...formData,
                service: formData.service.split(',').map(s => s.trim())
            };

            const response = await fetch('http://localhost:5000/troubleshoot', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(dataToSend)
            });

            if (response.ok) {
                const data = await response.text();
                setResponse(data);
                setSubmitStatus({ submitted: true, success: true, message: 'Form submitted successfully!' });
            } else {
                setResponse('');
                setSubmitStatus({ submitted: true, success: false, message: 'Error: Failed to fetch response.' });
            }
        } catch (error) {
            setResponse('');
            setSubmitStatus({ submitted: true, success: false, message: `Network error: ${error.message}` });
        }
    };

    // Style definitions
    const formContainerStyle = {
        background: 'linear-gradient(to top, #e6f9ff 0%, #ffffff 100%)',
        padding: '20px',
        borderRadius: '10px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
        maxWidth: '500px',
        margin: 'auto',
        marginTop: '50px'
    };

    const titleStyle = {
        textAlign: 'center',
        color: '#333',
        marginBottom: '20px'
    };

    const formStyle = {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        margin: '20px'
    };

    const inputStyle = {
        margin: '10px',
        padding: '10px',
        width: '300px',
        borderRadius: '5px',
        border: '1px solid #ddd'
    };

    const buttonStyle = {
        padding: '10px 20px',
        margin: '10px',
        borderRadius: '5px',
        border: 'none',
        backgroundColor: '#4CAF50',
        color: 'white',
        fontSize: '16px',
        cursor: 'pointer'
    };

    const requiredStyle = {
        color: '#ff0000',
        display: 'block',
        marginBottom: '5px'
    };

    return (
        <div style={formContainerStyle}>
            <h2 style={titleStyle}>AWS Troubleshooting Tool</h2>
            <form onSubmit={handleSubmit} style={formStyle}>
                <label style={requiredStyle}>
                    Platform*:
                    <input
                        type="text"
                        name="platform"
                        style={inputStyle}
                        value={formData.platform}
                        onChange={handleChange}
                        placeholder="e.g., AWS, GCP, Azure"
                        required
                    />
                </label>
                <label style={requiredStyle}>
                    Services*:
                    <input
                        type="text"
                        name="service"
                        style={inputStyle}
                        value={formData.service}
                        onChange={handleChange}
                        placeholder="e.g., Lambda, S3"
                        required
                    />
                </label>
                <label>
                    Error Code:
                    <input
                        type="text"
                        name="error_code"
                        style={inputStyle}
                        value={formData.error_code}
                        onChange={handleChange}
                        placeholder="e.g., 404 (optional)"
                    />
                </label>
                <label>
                    Runtime:
                    <input
                        type="text"
                        name="runtime"
                        style={inputStyle}
                        value={formData.runtime}
                        onChange={handleChange}
                        placeholder="e.g., Node.js 12.x, python (optional)"
                    />
                </label>
                <div style={{ marginBottom: '10px' }}>
                    <label style={requiredStyle}>
                        Error Description*:
                    </label>
                    <textarea
                        name="error_description"
                        style={{ ...inputStyle, height: '100px' }}
                        value={formData.error_description}
                        onChange={handleChange}
                        placeholder="Describe the issue, error logs"
                        required
                    />
                </div>
                <button type="submit" style={buttonStyle}>Submit</button>
            </form>
            {submitStatus.submitted && (
                <div style={{ color: submitStatus.success ? 'green' : 'red', marginTop: '10px' }}>
                    {submitStatus.message}
                </div>
            )}
            {response && <div dangerouslySetInnerHTML={{ __html: response }} />}
        </div>
    );
}

export default TroubleshootForm;
