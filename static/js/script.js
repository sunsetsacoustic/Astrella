// Astrella App Main JS
// -------------------
// - Handles multi-step form navigation, validation, AJAX requests, and sharing
// - Refactored for clarity and maintainability

// Wait for DOM to load
document.addEventListener('DOMContentLoaded', function() {
    // ========== Initialize Enhanced Inputs ========== //

    // Date picker (Flatpickr)
    flatpickr('.date-picker', {
        dateFormat: 'Y-m-d',
        maxDate: 'today',
        disableMobile: true
    });

    // Time picker (Flatpickr)
    flatpickr('.time-picker', {
        enableTime: true,
        noCalendar: true,
        dateFormat: 'H:i',
        time_24hr: true,
        disableMobile: true
    });

    // Location select (Select2 with AJAX, fallback to input)
    try {
        $('#birthLocation').select2({
            placeholder: 'Search for your birth city...',
            allowClear: true,
            minimumInputLength: 2,
            ajax: {
                url: '/api/search-location',
                dataType: 'json',
                delay: 250,
                data: function(params) {
                    return { query: params.term };
                },
                processResults: function(data) {
                    return {
                        results: data.map(function(item) {
                            return { id: item.id, text: item.name };
                        })
                    };
                },
                cache: true
            }
        }).on('select2:error', function(e) {
            // Fallback to basic input if Select2 fails
            $(this).select2('destroy');
            $(this).replaceWith('<input type="text" id="birthLocation" name="birthLocation" class="location-input" placeholder="Enter your birth city..." required>');
        });
    } catch (error) {
        // Fallback to basic input if Select2 fails
        $('#birthLocation').replaceWith('<input type="text" id="birthLocation" name="birthLocation" class="location-input" placeholder="Enter your birth city..." required>');
    }

    // ========== Multi-Step Form Logic ========== //
    const form = document.getElementById('birth-data-form');
    const steps = form.querySelectorAll('.form-step');
    const progressSteps = document.querySelectorAll('.progress-step');
    const nextButtons = form.querySelectorAll('.next-btn');
    const prevButtons = form.querySelectorAll('.prev-btn');

    // Show the given step and update progress bar
    function showStep(stepNumber) {
        steps.forEach(step => {
            step.classList.remove('active');
            if (step.dataset.step === stepNumber.toString()) {
                step.classList.add('active');
            }
        });
        progressSteps.forEach(step => {
            step.classList.remove('active');
            if (parseInt(step.dataset.step) <= parseInt(stepNumber)) {
                step.classList.add('active');
            }
        });
    }

    // Validate all required fields in the current step
    function validateStep(stepNumber) {
        const currentStep = form.querySelector(`.form-step[data-step="${stepNumber}"]`);
        const inputs = currentStep.querySelectorAll('input, select');
        let isValid = true;
        inputs.forEach(input => {
            if (input.hasAttribute('required') && !input.value) {
                isValid = false;
                input.classList.add('error');
            } else {
                input.classList.remove('error');
            }
        });
        return isValid;
    }

    // Update the review step with entered data
    function updateReviewSummary() {
        const date = document.getElementById('birthDate').value;
        const time = document.getElementById('birthTime').value;
        // Use Select2 if available, otherwise fallback to input value
        let location = '';
        if ($('#birthLocation').data('select2')) {
            location = $('#birthLocation').select2('data')[0]?.text || '';
        } else {
            location = document.getElementById('birthLocation').value;
        }
        document.getElementById('review-date').textContent = date;
        document.getElementById('review-time').textContent = time;
        document.getElementById('review-location').textContent = location;
    }

    // Next step button logic
    nextButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = this.closest('.form-step');
            const currentStepNumber = parseInt(currentStep.dataset.step);
            if (validateStep(currentStepNumber)) {
                if (currentStepNumber === 2) {
                    updateReviewSummary();
                }
                showStep(currentStepNumber + 1);
            }
        });
    });

    // Previous step button logic
    prevButtons.forEach(button => {
        button.addEventListener('click', function() {
            const currentStep = this.closest('.form-step');
            const currentStepNumber = parseInt(currentStep.dataset.step);
            showStep(currentStepNumber - 1);
        });
    });

    // ========== Form Submission & Results ========== //
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        if (!validateStep(3)) return;
        // Use Select2 if available, otherwise fallback to input value
        let location = '';
        if ($('#birthLocation').data('select2')) {
            location = $('#birthLocation').val();
        } else {
            location = document.getElementById('birthLocation').value;
        }
        const formData = {
            birthDate: document.getElementById('birthDate').value,
            birthTime: document.getElementById('birthTime').value,
            birthLocation: location
        };
        try {
            const response = await fetch('/get-reading', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            if (!response.ok) throw new Error('Failed to generate reading');
            const data = await response.json();
            displayResults(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to generate reading. Please try again.');
        }
    });

    // Display results in the results section
    function displayResults(data) {
        document.getElementById('input-section').classList.add('hidden');
        document.getElementById('results-section').classList.remove('hidden');
        // Update chart display
        document.getElementById('sun-sign').textContent = data.chart.sun;
        document.getElementById('moon-sign').textContent = data.chart.moon;
        document.getElementById('asc-sign').textContent = data.chart.ascendant;
        // Update reading content
        document.getElementById('reading-content').innerHTML = data.reading;
        // Show results
        document.getElementById('chart-display').classList.remove('hidden');
        document.getElementById('reading-display').classList.remove('hidden');
    }

    // ========== Share Button (Screenshot) ========== //
    document.getElementById('share-btn').addEventListener('click', async function() {
        const resultsSection = document.getElementById('results-section');
        try {
            const canvas = await html2canvas(resultsSection);
            const image = canvas.toDataURL('image/png');
            // Create download link
            const link = document.createElement('a');
            link.download = 'my-astrological-reading.png';
            link.href = image;
            link.click();
        } catch (error) {
            console.error('Error generating image:', error);
            alert('Failed to generate image. Please try again.');
        }
    });
}); 