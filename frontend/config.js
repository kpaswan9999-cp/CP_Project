// Configuration for the StreamAI Frontend
// Replace this with your actual Render backend URL after deployment
const CONFIG = {
    API_BASE_URL: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://127.0.0.1:5000'
        : 'https://cp-project-backend.onrender.com' // <-- UPDATE THIS after deploying to Render
};

export default CONFIG;
