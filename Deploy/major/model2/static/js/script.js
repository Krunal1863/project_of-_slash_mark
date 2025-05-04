document.getElementById('recommendationForm').addEventListener('submit', async function (e) {
    e.preventDefault();

    const songInput = document.getElementById('songInput').value;
    const recommendationList = document.getElementById('recommendationList');
    const recommendationsDiv = document.getElementById('recommendations');

    // Clear previous recommendations
    recommendationList.innerHTML = '';
    recommendationsDiv.style.display = 'none';

    try {
        const response = await fetch(`/recommend?song=${encodeURIComponent(songInput)}`);
        const data = await response.json();

        if (data.recommendations) {
            recommendationsDiv.style.display = 'block';
            data.recommendations.forEach(song => {
                const li = document.createElement('li');
                li.textContent = song;
                recommendationList.appendChild(li);
            });
        } else {
            alert('No recommendations found.');
        }
    } catch (error) {
        alert('An error occurred while fetching recommendations.');
        console.error(error);
    }
});