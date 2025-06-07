//  Maps functionality
document.addEventListener('DOMContentLoaded', function() {
    // check global variable
    if (typeof window.absUrl === 'undefined') {
        console.error("Missing required global variables: absUrl");
        return;
    }


    //  setup cache for fetched data (by creating new map object) 
    let cacheData = new Map();

    //  function to fetch analysis data with filters application 
    async function fetchAnalysisData(filters = {}) {
        const cacheKey = JSON.stringify(filters);
        if (cacheData.has(cacheKey)) {
            return cacheData.get(cacheKey)
        }

        const queryString = new URLSearchParams(filters).toString();
        const url  = `${window.absUrl}get-analysis-data${queryString ? `?${queryString}` : ''}`

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken'),
                },
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            cacheData.set(cacheKey, data);
            return data;
        } catch (error) {
            console.error('Error fetching analysis data:', error)
            return null;
        }
    }

    // Helper function to get CSRF token from cookies (if needed)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(':');
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

    // List of functions for plots and animation

    //  1. Function to animate counting
    function animateCount(id, endValue, duration=1000) {
        const element = document.getElementById(id);
        if (!element) {
            console.error(`Element with id ${id} not found`);
            return;
        }

        const startTime = performance.now()
        const step = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed/duration, 1);
            const value = Math.floor(progress * endValue);

            element.textContent = value.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    }

    // 2. Function for overall plot intensities
    function intensitiesOverallPlot(id, data){

        // Create hover text array
        const hoverText = data.x_values.map((x, i) =>
            `Date: ${x}<br> Events: ${data.y_bar[i]}`
        )

        const barData = {
            name: 'Daily Intensities',
            type: 'bar',
            x: data.x_values,
            y: data.y_bar,
            marker: {
                    color: 'indianred'
                },
            text: hoverText,
            hoverinfo: 'text',
        };

        // set plot layout
        const layout = {
            title: 'Daily Intensity of Recorded Events',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.99,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 600,
            autosize:true,
            xaxis : {
                tickangle: -45
            }
        };

        // Plotly plot call
        Plotly.newPlot(id, [barData], layout);
    }


    // Function to update UI with fetched data
    function updateUI(data) {
        if (!data || !data.general_statistics || !data.overall_daily_intensities) {
            console.error('Invalid or missing data')
            return;
        }

        const gen_stats = data.general_statistics;
        const daily_intensities = data.overall_daily_intensities;

        // call animateCount for each statistic
        animateCount('station-count', gen_stats.total_stations, 2000);
        animateCount('event-count', gen_stats.total_events, 2000);
        animateCount('phase-count', gen_stats.total_phases, 2000);

        // create plot for daily overall intensities
        intensitiesOverallPlot('daily-overall-intensities', daily_intensities)
    }

    // Debounce function to limit frequent API calls
    function debounce(func, wait){
        let timeout;
        return function (...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    //  Handle filter form submission
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const formData = new FormData(filterForm);
            const filters = Object.fromEntries(formData);

            // Show loading indicator 
            const loadingSpinner = document.getElementById('loading-spinner');
            if (loadingSpinner) loadingSpinner.style.display = 'block';

            try {
                const data = await fetchAnalysisData(filters);
                updateUI(data);
            } finally {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
            }
        } );
    }

    // Handle real-time filter changes (e.g., for sliders or inputs)
    const filterInputs = document.querySelectorAll('#filter-form input');
    filterInputs.forEach((input) => {
        input.addEventListener(
            'input',
            debounce(async () => {
                const formData = new FormData(filterForm);
                const filters = Object.fromEntries(formData);

                const loadingSpinner = document.getElementById('loading-spinner');

                if (loadingSpinner) loadingSpinner.style.display = 'block';

                try {
                    const data = await fetchAnalysisData(filters);
                    updateUI(data);
                } finally {
                    if (loadingSpinner) loadingSpinner.style.display = 'none';
                }
            }, 500)
        );
    });


    //  Initial data fetch (no filters)
    (async () => {
        const data = await fetchAnalysisData();
        updateUI(data);
    })();

});