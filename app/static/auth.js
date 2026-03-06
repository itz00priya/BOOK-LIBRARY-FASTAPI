document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const errorBox = document.getElementById('error-box');

    function showError(message) {
        errorBox.textContent = message;
        errorBox.style.display = 'block';
    }

    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;

            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            try {
                const response = await fetch('/api/v1/users/login', {
                    method: 'POST',
                    body: formData
                });

                if (response.ok) {
                    const data = await response.json();
                    localStorage.setItem('token', data.access_token);
                    localStorage.setItem('user_role', data.role);
                    localStorage.setItem('user_email', username);
                    window.location.href = '/';
                } else {
                    const error = await response.json();
                    showError(error.detail || 'Login failed. Please check your credentials.');
                }
            } catch (error) {
                console.error('Login error:', error);
                showError('Something went wrong. Please try again later.');
            }
        });
    }

    if (registerForm) {
        registerForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const full_name = document.getElementById('full_name').value;
            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;

            try {
                const response = await fetch('/api/v1/users/register', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        username,
                        full_name,
                        email,
                        password
                    })
                });

                if (response.ok) {
                    window.location.href = '/login?registered=true';
                } else {
                    const error = await response.json();
                    showError(error.detail || 'Registration failed. Please try again.');
                }
            } catch (error) {
                console.error('Registration error:', error);
                showError('Something went wrong. Please try again later.');
            }
        });
    }

    // Check if redirected after registration
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('registered') && errorBox) {
        errorBox.textContent = 'Account created successfully! Please sign in.';
        errorBox.style.display = 'block';
        errorBox.style.background = '#dcfce7';
        errorBox.style.color = '#166534';
    }
});
