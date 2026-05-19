document.addEventListener('DOMContentLoaded', () => {
    const doctorGrid = document.getElementById('doctorGrid');
    const doctorForm = document.getElementById('doctorForm');
    const modal = document.getElementById('doctorModal');
    const modalTitle = document.getElementById('modalTitle');
    const addBtn = document.getElementById('addDoctorBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const statsCount = document.getElementById('totalDoctors');

    // Auth Elements
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const loginModal = document.getElementById('loginModal');
    const loginForm = document.getElementById('loginForm');
    const cancelLoginBtn = document.getElementById('cancelLoginBtn');
    const userStatus = document.getElementById('userStatus');

    let isEditing = false;
    let currentEditId = null;

    // --- Authentication Logic ---
    const checkAuth = () => {
        const token = localStorage.getItem('doctorToken');
        if (token) {
            loginBtn.style.display = 'none';
            logoutBtn.style.display = 'block';
            addBtn.style.display = 'flex';
            userStatus.textContent = 'Authorized Admin';
            document.querySelectorAll('.card-actions').forEach(el => el.style.display = 'flex');
        } else {
            loginBtn.style.display = 'block';
            logoutBtn.style.display = 'none';
            addBtn.style.display = 'none';
            userStatus.textContent = 'Guest Mode (View Only)';
            document.querySelectorAll('.card-actions').forEach(el => el.style.display = 'none');
        }
    };

    loginBtn.addEventListener('click', () => loginModal.classList.add('active'));
    cancelLoginBtn.addEventListener('click', () => loginModal.classList.remove('active'));

    loginForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const formData = new FormData(loginForm);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/api-token-auth/', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                const result = await response.json();
                localStorage.setItem('doctorToken', result.token);
                loginModal.classList.remove('active');
                loginForm.reset();
                checkAuth();
                fetchDoctors(); // Refresh to show action buttons
            } else {
                alert('Invalid credentials. Access denied.');
            }
        } catch (error) {
            console.error('Login error:', error);
        }
    });

    logoutBtn.addEventListener('click', () => {
        localStorage.removeItem('doctorToken');
        checkAuth();
        fetchDoctors(); // Refresh to hide action buttons
    });

    // --- CRUD Operations ---
    const fetchDoctors = async () => {
        try {
            const response = await fetch('/api/doctors/');
            const doctors = await response.json();
            renderDoctors(doctors);
            updateStats(doctors.length);
            checkAuth(); // Update UI after cards are rendered
        } catch (error) {
            console.error('Error fetching doctors:', error);
        }
    };

    const renderDoctors = (doctors) => {
        const hasToken = !!localStorage.getItem('doctorToken');
        doctorGrid.innerHTML = doctors.map(doctor => `
            <div class="doctor-card" data-id="${doctor.id}">
                <div class="doctor-avatar">👨‍⚕️</div>
                <h3 class="doctor-name">Dr. ${doctor.first_name} ${doctor.last_name}</h3>
                <p class="doctor-specialty">${doctor.specialization}</p>
                <div class="doctor-info">
                    <div class="info-item">
                        <span>Experience</span>
                        <p>${doctor.experience} Years</p>
                    </div>
                    <div class="info-item">
                        <span>Contact</span>
                        <p>${doctor.contact_number}</p>
                    </div>
                </div>
                <div class="card-actions" style="display: ${hasToken ? 'flex' : 'none'}">
                    <button class="btn-icon btn-edit" onclick="editDoctor(${doctor.id})">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"></path><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"></path></svg>
                    </button>
                    <button class="btn-icon btn-delete" onclick="deleteDoctor(${doctor.id})">
                        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="3 6 5 6 21 6"></polyline><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"></path><line x1="10" y1="11" x2="10" y2="17"></line><line x1="14" y1="11" x2="14" y2="17"></line></svg>
                    </button>
                </div>
            </div>
        `).join('');
    };

    const updateStats = (count) => {
        statsCount.textContent = count;
    };

    // Modal Control
    const openModal = (editMode = false) => {
        isEditing = editMode;
        modalTitle.textContent = editMode ? 'Edit Doctor Profile' : 'Add New Doctor';
        modal.classList.add('active');
    };

    const closeModal = () => {
        modal.classList.remove('active');
        doctorForm.reset();
        currentEditId = null;
    };

    addBtn.addEventListener('click', () => openModal(false));
    cancelBtn.addEventListener('click', closeModal);

    doctorForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const token = localStorage.getItem('doctorToken');
        if (!token) return alert('Session expired. Please log in again.');

        const formData = new FormData(doctorForm);
        const data = Object.fromEntries(formData.entries());

        const url = isEditing ? `/api/doctors/${currentEditId}/` : '/api/doctors/';
        const method = isEditing ? 'PUT' : 'POST';

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Token ${token}`,
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify(data)
            });

            if (response.ok) {
                closeModal();
                fetchDoctors();
            } else if (response.status === 401) {
                alert('Session expired. Please log in.');
                localStorage.removeItem('doctorToken');
                checkAuth();
            } else {
                const errData = await response.json();
                alert('Error: ' + JSON.stringify(errData));
            }
        } catch (error) {
            console.error('Error saving doctor:', error);
        }
    });

    window.editDoctor = async (id) => {
        try {
            const response = await fetch(`/api/doctors/${id}/`);
            const doctor = await response.json();
            
            document.getElementById('first_name').value = doctor.first_name;
            document.getElementById('last_name').value = doctor.last_name;
            document.getElementById('specialization').value = doctor.specialization;
            document.getElementById('experience').value = doctor.experience;
            document.getElementById('contact_number').value = doctor.contact_number;
            document.getElementById('email').value = doctor.email;

            currentEditId = id;
            openModal(true);
        } catch (error) {
            console.error('Error fetching doctor details:', error);
        }
    };

    window.deleteDoctor = async (id) => {
        if (!confirm('Are you sure you want to remove this doctor profile?')) return;
        const token = localStorage.getItem('doctorToken');

        try {
            const response = await fetch(`/api/doctors/${id}/`, {
                method: 'DELETE',
                headers: {
                    'Authorization': `Token ${token}`,
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            if (response.ok) {
                fetchDoctors();
            }
        } catch (error) {
            console.error('Error deleting doctor:', error);
        }
    };

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    fetchDoctors();
});
