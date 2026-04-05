// Configuration for the StreamAI Frontend
// Replace this with your actual Render backend URL after deployment
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000'
        : 'https://cp-project-1-tpw5.onrender.com' // Updated with actual Render backend URL
};

export default CONFIG;
