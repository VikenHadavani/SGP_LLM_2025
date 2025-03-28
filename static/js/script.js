// Sidebar toggle functionality
const menuToggle = document.getElementById('menu-toggle');
const sidebar = document.getElementById('sidebar');
const mainContent = document.getElementById('main-content');

menuToggle.addEventListener('click', () => {
    sidebar.classList.toggle('collapsed');
    mainContent.classList.toggle('expanded');
});

// File upload preview functionality
const fileInput = document.getElementById('image');
const fileName = document.getElementById('filename');
const imagePreviewContainer = document.getElementById('image-preview-container');
const imagePreview = document.getElementById('image-preview');
const removeImageButton = document.getElementById('remove-image');

fileInput.addEventListener('change', (event) => {
    const file = event.target.files[0];
    if (file) {
        fileName.textContent = file.name;
        const reader = new FileReader();
        reader.onload = (e) => {
            imagePreview.src = e.target.result;
            imagePreviewContainer.classList.add('active');
        };
        reader.readAsDataURL(file);
    }
});

removeImageButton.addEventListener('click', () => {
    fileInput.value = '';
    fileName.textContent = 'No file chosen';
    imagePreviewContainer.classList.remove('active');
    imagePreview.src = '';
});

// Login modal functionality
const loginButton = document.getElementById('login-btn');
const modalOverlay = document.getElementById('login-modal');
const modalClose = document.getElementById('modal-close');
const cancelLogin = document.getElementById('cancel-login');

loginButton.addEventListener('click', () => {
    modalOverlay.classList.add('active');
});

modalClose.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
});

cancelLogin.addEventListener('click', () => {
    modalOverlay.classList.remove('active');
});

// Toast notification functionality
const toast = document.getElementById('toast');
const toastClose = document.getElementById('toast-close');

function showToast(message) {
    const toastMessage = document.getElementById('toast-message');
    toastMessage.textContent = message;
    toast.style.opacity = '1';
    toast.style.visibility = 'visible';

    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.visibility = 'hidden';
    }, 3000); // Hide after 3 seconds
}

toastClose.addEventListener('click', () => {
    toast.style.opacity = '0';
    toast.style.visibility = 'hidden';
});

// Form submission loading spinner
const analysisForm = document.getElementById('analysis-form');
const submitButton = document.getElementById('submit-btn');
const loadingSpinner = document.getElementById('loading-spinner');

analysisForm.addEventListener('submit', (event) => {
    event.preventDefault(); // Prevent default form submission
    submitButton.disabled = true;
    loadingSpinner.style.display = 'inline-block';

    // Simulate form submission delay
    setTimeout(() => {
        submitButton.disabled = false;
        loadingSpinner.style.display = 'none';
        showToast('Image analysis submitted successfully!');
    }, 2000); // Simulate a 2-second delay
});