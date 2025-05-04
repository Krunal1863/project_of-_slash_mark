// Add basic form validation and interactivity
document.getElementById('predictionForm').addEventListener('submit', function (event) {
    const bedrooms = document.getElementById('bedrooms').value;
    const bathrooms = document.getElementById('bathrooms').value;
    const sqftLiving = document.getElementById('sqft_living').value;
    const sqftLot = document.getElementById('sqft_lot').value;
    const floors = document.getElementById('floors').value;
    const yrBuilt = document.getElementById('yr_built').value;

    if (!bedrooms || !bathrooms || !sqftLiving || !sqftLot || !floors || !yrBuilt) {
        alert('Please fill out all fields.');
        event.preventDefault();
    }
});