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
        const hoverTextDaily = data.x_values.map((x, i) =>
            `Date: ${x}<br> Events: ${data.y_bar[i]}`
        )

        const hoverTextCumulative = data.x_values.map((x, i) =>
            `Date: ${x}<br> Events: ${data.y_bar[i]}`
        )

        // bar plot
        const barData = {
            name: 'Daily Intensities',
            type: 'bar',
            x: data.x_values,
            y: data.y_bar,
            marker: {
                    color: 'indianred',
                    opacity: 0.8
                },
            text: hoverTextDaily,
            hoverinfo: 'text',
            yaxis: 'y'
        };

        // line plot
        const lineData = {
            name: 'Cumulative Intensities',
            type: 'line',
            x: data.x_values,
            y: data.y_cum,
            marker : {
                color: '#FF9900',
                opacity: 0.8
            },
            text: hoverTextCumulative,
            hoverinfo: 'text',
            yaxis: 'y2'
        }

        // set plot layout
        const layout = {
            title: 'Daily Intensity of Recorded Events',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.20,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 600,
            autosize:true,
            xaxis : {
                title: 'Date',
                tickangle: -45
            },
            yaxis: {
                title: 'Daily Counts',
                side: screenLeft,
                showgrid: true
            },
            yaxis2: {
                title: 'Cumulative Counts',
                side: 'right',
                overlaying: 'y',
                showgrid:false,
                rangemode: 'tozero', 
                range: [0, Math.max(...data.y_cum) * 1.1], 
                anchor: 'x'
            },
            margin: {
                r: 100,
                b: 100
            }
        };

        // Plotly plot call
        try {
            Plotly.newPlot(id, [barData, lineData], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        }
        
    };

    // 3. Function for station performances (Bar plots)
    function stationPerformanceBar(id, data){
        // get the list of stations and the phases
        const stations = Object.keys(data);
        const p_phase =  stations.map(station => data[station].p_phase);
        const s_phase =  stations.map(station => data[station].s_phase);

        // Data validation
        if (stations.length === 0 || p_phase.length !== stations.length || s_phase.length !== stations.length) {
            console.log('Invalid data: stations, p_phase, and s_phase must have valid lengths', {stations, p_phase, s_phase});
            return;
        }

        // Create hovertext for each phases
        const hoverTextP = stations.map((station, i) =>
            `Station: ${station}<br>P_phase: ${p_phase[i]}` 
        );

        const hoverTextS = stations.map((station, i) =>
            `Station: ${station}<br>S_phase: ${s_phase[i]}`
        );

        // P_phase bar plot
        const pPhaseData = {
            name: 'P_phase',
            type: 'bar',
            x: stations,
            y: p_phase,
            marker: {
                color: 'indianred',
                opacity: 0.8
            },
            text: hoverTextP,
            hoverinfo: 'text'
        };

        // S_phase bar plot
        const sPhaseData = {
            name: 'S_phase',
            type: 'bar',
            x: stations,
            y: s_phase,
            marker: {
                color: '#1F77B4',
                opacity: 0.8
            },
            text: hoverTextS,
            hoverinfo: 'text'
        };

        // Set plot layout
        const layout = {
            title: 'Phases Counts by Station',
            showlegend: true, 
            template: 'plotly_white',
            barmode: 'group',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.25,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 400,
            autosize: true,
            xaxis: {
                title: 'Station',
                tickangle: -45
            },
            yaxis: {
                title: 'Counts',
                rangemode: 'tozero',
                range: [0, Math.max(...p_phase, ...s_phase)*1.1]
            },
            margin: {
                r: 100,
                b: 100
            }
        };

        // Plotly plot call
        try {
            Plotly.newPlot(id, [pPhaseData, sPhaseData], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        }
    
    };

    // Function to update UI with fetched data
    function updateUI(data) {
        if (!data || !data.general_statistics || !data.overall_daily_intensities || !data.station_performance) {
            console.error('Invalid or missing data')
            return;
        }

        const gen_stats = data.general_statistics;
        const daily_intensities = data.overall_daily_intensities;
        const station_performance = data.station_performance;

        // call animateCount for each statistic
        animateCount('station-count', gen_stats.total_stations, 2000);
        animateCount('event-count', gen_stats.total_events, 2000);
        animateCount('phase-count', gen_stats.total_phases, 2000);

        // create plot for daily overall intensities
        intensitiesOverallPlot('daily-overall-intensities', daily_intensities);

        // create plot for station performance
        stationPerformanceBar('station-performance', station_performance);
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