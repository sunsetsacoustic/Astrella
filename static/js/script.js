document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('birth-data-form');
    const resultsSection = document.getElementById('results-section');
    const loadingSpinner = document.querySelector('.loading-spinner');
    const chartDisplay = document.getElementById('chart-display');
    const readingDisplay = document.getElementById('reading-display');
    const readingContent = document.getElementById('reading-content');

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Show loading state
        resultsSection.classList.remove('hidden');
        loadingSpinner.classList.remove('hidden');
        chartDisplay.classList.add('hidden');
        readingDisplay.classList.add('hidden');

        // Get form data
        const formData = {
            birthDate: document.getElementById('birthDate').value,
            birthTime: document.getElementById('birthTime').value,
            birthLocation: document.getElementById('birthLocation').value
        };

        try {
            const response = await fetch('/get-reading', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(formData)
            });

            if (!response.ok) {
                throw new Error('Failed to get reading');
            }

            const data = await response.json();

            // Display chart data
            document.getElementById('sun-sign').textContent = data.chart.sun;
            document.getElementById('moon-sign').textContent = data.chart.moon;
            document.getElementById('asc-sign').textContent = data.chart.ascendant;

            // Display reading
            readingContent.textContent = data.reading;

            // Show results
            loadingSpinner.classList.add('hidden');
            chartDisplay.classList.remove('hidden');
            readingDisplay.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            loadingSpinner.classList.add('hidden');
            alert('Sorry, there was an error generating your reading. Please try again.');
        }
    });
}); 