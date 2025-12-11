const { createApp } = Vue;

const API_BASE_URL = 'http://localhost:5000';

createApp({
    data() {
        return {
            user: null,
            currentView: 'dashboard',
            showLogin: false,
            showRegister: false,
            showAddDoctor: false,
            
            loginForm: {
                username: '',
                password: ''
            },
            
            registerForm: {
                username: '',
                email: '',
                password: '',
                full_name: '',
                contact_number: ''
            },
            
            dashboardStats: null,
            doctors: [],
            patients: [],
            appointments: [],
            specializations: [],
            treatmentHistory: [],
            selectedDoctors: []
        }
    },
    
    mounted() {
        this.checkAuth();
    },
    
    methods: {
        async checkAuth() {
            try {
                const response = await axios.get(`${API_BASE_URL}/auth/me`, {
                    withCredentials: true
                });
                this.user = response.data;
                this.loadDashboard();
            } catch (error) {
                console.log('Not authenticated');
            }
        },
        
        async login() {
            try {
                const response = await axios.post(`${API_BASE_URL}/auth/login`, this.loginForm, {
                    withCredentials: true
                });
                this.user = response.data.user;
                this.showLogin = false;
                this.loginForm = { username: '', password: '' };
                this.loadDashboard();
                alert('Login successful!');
            } catch (error) {
                alert(error.response?.data?.error || 'Login failed');
            }
        },
        
        async register() {
            try {
                await axios.post(`${API_BASE_URL}/auth/register`, this.registerForm);
                this.showRegister = false;
                alert('Registration successful! Please login.');
                this.showLogin = true;
                this.registerForm = {
                    username: '',
                    email: '',
                    password: '',
                    full_name: '',
                    contact_number: ''
                };
            } catch (error) {
                alert(error.response?.data?.error || 'Registration failed');
            }
        },
        
        async logout() {
            try {
                await axios.post(`${API_BASE_URL}/auth/logout`, {}, {
                    withCredentials: true
                });
                this.user = null;
                this.currentView = 'dashboard';
            } catch (error) {
                console.error('Logout error:', error);
            }
        },
        
        async loadDashboard() {
            try {
                let endpoint = '';
                if (this.user.role === 'admin') {
                    endpoint = '/admin/dashboard';
                } else if (this.user.role === 'doctor') {
                    endpoint = '/doctor/dashboard';
                } else if (this.user.role === 'patient') {
                    endpoint = '/patient/dashboard';
                }
                
                const response = await axios.get(`${API_BASE_URL}${endpoint}`, {
                    withCredentials: true
                });
                this.dashboardStats = response.data;
            } catch (error) {
                console.error('Dashboard load error:', error);
            }
        },
        
        async loadDoctors() {
            try {
                const response = await axios.get(`${API_BASE_URL}/admin/doctors`, {
                    withCredentials: true
                });
                this.doctors = response.data;
            } catch (error) {
                console.error('Load doctors error:', error);
            }
        },
        
        async deleteDoctor(doctorId) {
            if (!confirm('Are you sure you want to deactivate this doctor?')) return;
            
            try {
                await axios.delete(`${API_BASE_URL}/admin/doctors/${doctorId}`, {
                    withCredentials: true
                });
                alert('Doctor deactivated successfully');
                this.loadDoctors();
            } catch (error) {
                alert(error.response?.data?.error || 'Failed to deactivate doctor');
            }
        },
        
        async loadAppointments() {
            try {
                let endpoint = '';
                if (this.user.role === 'admin') {
                    endpoint = '/admin/appointments';
                } else if (this.user.role === 'doctor') {
                    endpoint = '/doctor/appointments';
                } else if (this.user.role === 'patient') {
                    endpoint = '/patient/appointments';
                }
                
                const response = await axios.get(`${API_BASE_URL}${endpoint}`, {
                    withCredentials: true
                });
                this.appointments = response.data;
            } catch (error) {
                console.error('Load appointments error:', error);
            }
        },
        
        async completeAppointment(appointmentId) {
            const diagnosis = prompt('Enter diagnosis:');
            if (!diagnosis) return;
            
            const prescription = prompt('Enter prescription:');
            const notes = prompt('Enter notes (optional):');
            
            try {
                await axios.post(
                    `${API_BASE_URL}/doctor/appointments/${appointmentId}/complete`,
                    { diagnosis, prescription, notes },
                    { withCredentials: true }
                );
                alert('Appointment completed successfully');
                this.loadAppointments();
            } catch (error) {
                alert(error.response?.data?.error || 'Failed to complete appointment');
            }
        },
        
        async cancelAppointment(appointmentId) {
            if (!confirm('Are you sure you want to cancel this appointment?')) return;
            
            try {
                let endpoint = '';
                if (this.user.role === 'doctor') {
                    endpoint = `/doctor/appointments/${appointmentId}/cancel`;
                } else if (this.user.role === 'patient') {
                    endpoint = `/patient/appointments/${appointmentId}/cancel`;
                }
                
                await axios.post(`${API_BASE_URL}${endpoint}`, {}, {
                    withCredentials: true
                });
                alert('Appointment cancelled successfully');
                this.loadAppointments();
            } catch (error) {
                alert(error.response?.data?.error || 'Failed to cancel appointment');
            }
        },
        
        async loadSpecializations() {
            try {
                const response = await axios.get(`${API_BASE_URL}/patient/specializations`, {
                    withCredentials: true
                });
                this.specializations = response.data;
            } catch (error) {
                console.error('Load specializations error:', error);
            }
        },
        
        async viewDoctors(specializationId) {
            try {
                const response = await axios.get(
                    `${API_BASE_URL}/patient/doctors?specialization_id=${specializationId}`,
                    { withCredentials: true }
                );
                this.selectedDoctors = response.data;
                // Show doctors in a modal or new view
                alert(`Found ${this.selectedDoctors.length} doctors`);
            } catch (error) {
                console.error('View doctors error:', error);
            }
        },
        
        async loadTreatmentHistory() {
            try {
                const response = await axios.get(`${API_BASE_URL}/patient/treatment-history`, {
                    withCredentials: true
                });
                this.treatmentHistory = response.data;
            } catch (error) {
                console.error('Load treatment history error:', error);
            }
        },
        
        async exportTreatments() {
            try {
                const response = await axios.post(`${API_BASE_URL}/api/export/treatments`, {}, {
                    withCredentials: true
                });
                alert(response.data.message);
            } catch (error) {
                alert(error.response?.data?.error || 'Export failed');
            }
        },
        
        formatStatLabel(key) {
            return key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
        }
    },
    
    watch: {
        currentView(newView) {
            if (newView === 'doctors' && this.user.role === 'admin') {
                this.loadDoctors();
            } else if (newView === 'appointments') {
                this.loadAppointments();
            } else if (newView === 'specializations' && this.user.role === 'patient') {
                this.loadSpecializations();
            } else if (newView === 'history' && this.user.role === 'patient') {
                this.loadTreatmentHistory();
            }
        }
    }
}).mount('#app');
