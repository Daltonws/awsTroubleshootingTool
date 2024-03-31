import React, { useState } from 'react';
import './TroubleshootForm.css';

function TroubleshootForm() {
    const [formData, setFormData] = useState({
        platform: '',
        service: '',
        error_code: '',
        runtime: '',
        error_description: ''
    });
    const [response, setResponse] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleChange = (e) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
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
            } else {
                setResponse('Error: Failed to fetch response.');
            }
        } catch (error) {
            setResponse(`Network error: ${error.message}`);
        }
        setIsLoading(false);
    };

    return (
        <div className="formContainer">
            <h2 className="title">Cloud Troubleshooting Tool</h2>
            <form onSubmit={handleSubmit} className="form">
                <label className="required">
                    Platform*:
                    <input
                        type="text"
                        name="platform"
                        className="input"
                        value={formData.platform}
                        onChange={handleChange}
                        placeholder="e.g., AWS, GCP, Azure"
                        required
                    />
                </label>
                <label className="required">
                    Services*:
                    <input
                        type="text"
                        name="service"
                        className="input"
                        value={formData.service}
                        onChange={handleChange}
                        placeholder="e.g., Lambda, GCP Functions"
                        required
                    />
                </label>
                <label>
                    Error Code:
                    <input
                        type="text"
                        name="error_code"
                        className="input"
                        value={formData.error_code}
                        onChange={handleChange}
                        placeholder="e.g., 404, 502 (optional)"
                    />
                </label>
                <div className="flexColumn">
                    <label>
                        Runtime:
                        <input
                            type="text"
                            name="runtime"
                            className="input"
                            value={formData.runtime}
                            onChange={handleChange}
                            placeholder="e.g., Node.js 12.x, python (optional)"
                        />
                    </label>
                    <label className="required">
                        Error Description*:
                        <textarea
                            name="error_description"
                            className="textarea"
                            value={formData.error_description}
                            onChange={handleChange}
                            placeholder="Describe the issue or provide error logs"
                            required
                        />
                    </label>
                </div>
                <button type="submit" className="button" disabled={isLoading}>
                    {isLoading ? (
                        <>
                            Loading...
                        </>
                    ) : (
                        'Submit'
                    )}
                </button>
            </form>
            {response && (
                <div dangerouslySetInnerHTML={{ __html: response }} className="response" />
            )}
        </div>
    );
}

export default TroubleshootForm;