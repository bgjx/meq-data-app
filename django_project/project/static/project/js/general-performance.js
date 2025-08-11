//  Maps functionality
document.addEventListener('DOMContentLoaded', function() {
    // check global variable
    if (typeof window.absUrl === 'undefined' || typeof window.mapboxToken === 'undefined') {
        console.error("Missing required global variables: absUrl");
        return;
    }

    //  setup cache for fetched data (by creating new map object) 
    let cacheData = new Map();

    //  function to fetch analysis data with filters application 
    async function fetchAnalysisData(filters = {}) {

        // Extract site slug
        const siteSlug = window.absUrl.split("/")[2];

        const cacheKey = JSON.stringify(filters);
        if (cacheData.has(cacheKey)) {
            return cacheData.get(cacheKey)
        }
        const queryString = new URLSearchParams(filters).toString();
        const url  = `/project/api/general-performance/${siteSlug}${queryString ? `?${queryString}` : ''}`;

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

    // Helper function to get CSRF token from cookies
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

    //  Function to animate counting
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

    // Function for overall plot intensities
    function intensitiesOverallPlot(id, data){

        // Create hover text array
        const hoverTextDaily = data.x_values.map((x, i) =>
            `Date: ${x}<br> Events: ${data.y_bar[i]}`
        )

        const hoverTextCumulative = data.x_values.map((x, i) =>
            `Date: ${x}<br> Events: ${data.y_cum[i]}`
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
            title: {
                text: 'Daily Intensity of Recorded Events',
                font: {
                    size: 18
                }
            },
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
                title: {
                    text: 'Date',
                    fiont: {
                        size: 14
                    }
                },
                tickangle: -45,
                type: 'date'
            },
            yaxis: {
                title: {
                    text: 'Daily Counts',
                    font: {
                        size: 14
                    }
                },
                showgrid: true
            },
            yaxis2: {
                title: {
                    text: 'Cumulative Counts',
                    font: {
                        size: 14
                    }
                },
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
            Plotly.react(id, [barData, lineData], layout);
        } catch (error) {
            console.error('Plotly.react failed:', error)
        }
        
    };

    // 2D MapBox plot 
    function Plot2dHypocenterMapbox(id, data){
        // Create hover text for station
        const hoverTextStation = data.station.station_code.map((x, i) => 
            `Station: ${x}<br> Latitude: ${data.station.latitude[i]}<br> Longitude: ${data.station.longitude[i]}<br> Elev (m): ${data.station.elev[i]}`
        )

        const initHypo = {
            name: 'Initial Hypocenter',
            type: 'scattermap',
            mode: 'markers',
            lat: data.initial.latitude,
            lon: data.initial.longitude,
            marker: {
                // color: data.initial.source_depth_m,
                size: data.norm_magnitude.map(item => item * 25),
                color: 'indianred',
                opacity: 0.9,
            },
            text : data.initial.elev.map((x, i) =>
            `Depth (m): ${-1*(x.toFixed(2))}<br>Mag: ${data.magnitude[i].toFixed(2)}<br>Lat: ${data.initial.latitude[i].toFixed(5)}<br>Lon: ${data.initial.longitude[i].toFixed(5)}`,
            ),  
            hoverinfo: 'text' 
        };

        const relocHypo = {
            name: 'Relocated Hypocenter',
            type: 'scattermap',
            mode: 'markers',
            lat: data.reloc.latitude,
            lon: data.reloc.longitude,
            marker: {
                // color: data.reloc.source_depth_m,
                size: data.norm_magnitude.map(item => item * 25),
                color: '#1F77B4',
                opacity: 0.9,
            },
            text : data.reloc.elev.map((x, i) =>
            `Depth (m): ${(-1*x.toFixed(2))}<br>Mag: ${data.magnitude[i].toFixed(2)}<br>Lat: ${data.reloc.latitude[i].toFixed(5)}<br>Lon: ${data.reloc.longitude[i].toFixed(5)}`,
            ), 
            hoverinfo: 'text'
        };

        const station = {
            name: 'Stations',
            type: 'scattermap',
            mode: 'markers+text',
            lat: data.station.latitude,
            lon: data.station.longitude,
            text: data.station.station_code,
            textposition: 'top center',
            marker: {
                symbol: 'triangle',
                color: 'black',
                opacity: 0.8,
                size: 14
            },
            textfont:{
                size: 14,
                color: 'rgba(255, 255, 255, 0.8)'
            },
            hoverinfo: 'text',
            hovertemplate: hoverTextStation
        };

        // set map layout 
        const layout = {
            title: {
                text: '2D Hypocenter Map Plots',
                font: {
                    size: 18
                },
            },
            map: {
                style: 'satellite-streets',
                center: {
                    lat: data.center_map.lat,
                    lon: data.center_map.lon,
                },
                zoom: 12,
            },
            autosize: true,
            height: 782,
            showlegend: true,
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.99,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
        }

        const config = {
            displayModeBar: true
        }

        // Plotly plot call
        try {
            Plotly.react(id, [initHypo, relocHypo, station], layout, config);
        } catch (error) {
            console.error('Plotly.react failed:', error)
        };
    };  


    // Function to update UI with fetched data
    function updateUI(data) {
        if (!data || !data.general_statistics || !data.overall_daily_intensities || !data.hypocenter) {
            console.error('Invalid or missing data')
            return;
        }

        // get data
        const gen_stats = data.general_statistics;
        const daily_intensities = data.overall_daily_intensities;
        const hypocenter = data.hypocenter;

        // call animateCount for each statistic
        animateCount('station-count', gen_stats.total_stations, 3000);
        animateCount('event-count', gen_stats.total_events, 3000);
        animateCount('phase-count', gen_stats.total_phases, 3000);

        // create plot for daily overall intensities
        intensitiesOverallPlot('daily-overall-intensities', daily_intensities);

        // create 2D plot hypocenter(Mapbox)
        Plot2dHypocenterMapbox('hypocenter-plot-2d-mapbox', hypocenter);
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
        });
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