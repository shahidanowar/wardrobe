// File Preview
function previewImage(input) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function(e) {
            document.getElementById('imagePreview').src = e.target.result;
            document.getElementById('imagePreview').style.display = 'block';
        };
        reader.readAsDataURL(input.files[0]);
    }
}

// Outfit Recommendation
async function getOutfitRecommendation(occasion) {
    try {
        const response = await fetch(`/wardrobe/recommend_outfit?occasion=${occasion}`);
        const data = await response.json();
        
        if (data.error) {
            showAlert('error', data.error);
            return;
        }
        
        displayOutfit(data.outfit);
    } catch (error) {
        showAlert('error', 'Failed to get outfit recommendation');
    }
}

function displayOutfit(outfit) {
    const container = document.getElementById('outfitRecommendation');
    container.innerHTML = '';
    
    outfit.forEach(item => {
        const itemElement = document.createElement('div');
        itemElement.className = 'col-md-4 mb-3';
        itemElement.innerHTML = `
            <div class="card">
                <img src="/static/uploads/${item.image_url}" class="card-img-top" alt="${item.name}">
                <div class="card-body">
                    <h5 class="card-title">${item.name}</h5>
                    <p class="card-text">${item.category}</p>
                </div>
            </div>
        `;
        container.appendChild(itemElement);
    });
}

// Flash Messages
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.role = 'alert';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
