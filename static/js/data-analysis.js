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
                tickangle: -45,
                type: 'date'
            },
            yaxis: {
                title: 'Daily Count',
                side: screenLeft,
                showgrid: true
            },
            yaxis2: {
                title: 'Cumulative Count',
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
            title: 'Phases Count by Station',
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
                title: 'Count',
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
        };
    
    };

    // 4. Wadati Profile plot
    function WadatiProfile(id, data){
        // calculate the linear regression 
        const n = data.p_travel.length;
        let sumX = 0, sumY=0, sumXY = 0, sumXX = 0;
        for (let i=0; i < n; i++) {
            sumX += data.p_travel[i];
            sumY += data.ts_tp[i];
            sumXY += data.p_travel[i] * data.ts_tp[i];
            sumXX += data.p_travel[i] * data.p_travel[i];
        }
        const slope = (n * sumXY - sumX * sumY) / (n * sumXX - sumX * sumX);
        const intercept = (sumY - slope * sumX)/n;

        // Generate points for regression line
        const xMin = Math.min(...data.p_travel);
        const xMax = Math.max(...data.p_travel);
        const regressionLine = {
            name: 'Linear Fit',
            type: 'scatter',
            mode: 'line',
            x: [xMin, xMax],
            y: [slope * xMin  + intercept, slope * xMax + intercept],
            line: {
                color: '#1F77B4',
                width: 2,
                opacity: 0.8
            }
        };


        // Scatter plot
        const ScatterWadati = {
            name: 'Data Point',
            type: 'scatter',
            mode: 'markers',
            x: data.p_travel,
            y: data.ts_tp,
            marker : {
                color: 'indianred',
                opacity: 0.8
            }
        };

        //  Equation to display
        const equation = `y = ${slope.toFixed(2)}x + ${intercept.toFixed(2)}<br> Vp/Vs: ${(1 + slope).toFixed(2)}`;

        const layout = {
            title: 'Wadati Profile',
            showlegend: true,
            template: 'plotly-white',
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
                title: 'P travel (s)',
                tickangle: 0
            },
            yaxis: {
                title: 'Ts - Tp (s)',
                rangemode: 'tozero',
                range: [0, Math.max(...data.ts_tp) * 1.1],
                anchor: 'x'
            },
            margin: {
                r:100,
                b:100
            },

            // Add annotation for the equation
            annotations: [
                {
                    x: xMin + (xMax - xMin) * 0.9,
                    y: Math.max(...data.ts_tp) * 0.2,
                    xref: 'x',
                    yref: 'y',
                    text: equation,
                    showarrow: false,
                    font: {
                        size: 12,
                        color: '#1F77B4',
                        opacity: 0.8
                    },
                    bgcolor: "rgba(255,255,255,0.5)",
                    bordercolor: '#1F77B4',
                    borderwidth: 1
                }
            ]
        };

        try {
            Plotly.newPlot(id, [ScatterWadati, regressionLine], layout);
        } catch (error) {
            console.error('Plolty.NewPlot failed:', error)
        };
    }
    

    // 5. TIme series station performance plot
    function timeSeriesStationPerformance(id, data){

        // Line plot traces
        const traces = data.stations.map(station => ({
            type: 'scatter',
            mode: 'lines',
            x: data.dates,
            y: data.dates.map(date => data.counts[date][station] || 0),
            name: station,
            line: {
                width: 1,
                opacity: 0.8
            }
        }));

        // Define layout
        const layout = {
            title: 'Event Counts per Station Over Time',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.1,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 600,
            autosize: true,
            xaxis: {
                title: 'Date',
                tickangle: -45,
                type: 'date'
            },
            yaxis: {
                title: 'Daily Counts',
                rangemode: 'tozero'
            },
            margin: {
                r: 100,
                b: 100
            }
        }
        
        // Plotly plot call
        try {
            Plotly.newPlot(id, traces, layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };
    };


    // 6. 2D hypocenters plots
    function Plot2dHypocenter(id, data) {
        // Create hover text for station
        const hoverTextStation = data.station.station_code.map((x, i) =>
            `Station: ${x}<br> Latitude: ${data.station.latitude[i]}<br> Longitude: ${data.station.longitude[i]}<br> ELev (m): ${data.station.elev[i]}`
        )

        const initHypo = {
            name: 'Initial Hypocenter',
            type: 'scatter',
            mode: 'markers',
            x: data.initial.longitude,
            y: data.initial.latitude,
            marker: {
                color: 'indianred',
                opacity: 0.8
            }
        };

        const relocHypo = {
            name: 'Relocated Hypocenter',
            type: 'scatter',
            mode: 'markers',
            x: data.reloc.longitude,
            y: data.reloc.latitude,
            marker: {
                color: '#1F77B4',
                opacity: 0.8
            }
        };

        
        const station = {
            name: 'Stations',
            type: 'scatter',
            mode: 'markers+text',
            x: data.station.longitude,
            y: data.station.latitude,
            marker: {
                color: '#FF9900',
                symbol: 'triangle-up', 
                opacity: 0.8,
                size: 14
            },
            text: data.station.station_code,
            textposition: 'top center',
            textfont:{
                size: 12,
                color: 'rgba(52, 58, 64,0.8)'
            },
            hoverinfo: 'text',
            hovertemplate: hoverTextStation
        };
        

        const layout = {
            title: '2D Hypocenter Plots',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.99,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 400,
            autosize: true,
            xaxis: {
                title: 'Longitude',
                tickangle: 0
            },
            yaxis: {
                title: 'Latitude',
                scaleanchor: "x", 
                scaleratio: 1    
            },
            margin: {
                r: 100,
                b: 100
            }
        }

        // Plotly plot call
        try {
            Plotly.newPlot(id, [initHypo, relocHypo, station], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };
    }


    // 7. Plot histogram error
    function histogramError (id, data) {

        // Initial RMS error
        const initialRms = {
            name: 'initial_rms_error',
            type: 'bar',
            x: data.bin_edges,
            y: data.init,
            marker: {
                color: 'indianred',
                opacity: 0.8
            }
        };

        // S_phase bar plot
        const relocRms = {
            name: 'reloc_rms_error',
            type: 'bar',
            x: data.bin_edges,
            y: data.reloc,
            marker: {
                color: '#1F77B4',
                opacity: 0.8
            }
        };

        // Set plot layout
        const layout = {
            title: 'Origin Time RMS error (second)',
            showlegend: true, 
            template: 'plotly_white',
            barmode: 'group',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.99,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 400,
            autosize: true,
            xaxis: {
                title: 'Second',
                tickangle: 0
            },
            yaxis: {
                title: 'Counts',
                rangemode: 'tozero',
                range: [0, Math.max(...data.init, ...data.reloc)*1.1]
            },
            margin: {
                r: 100,
                b: 100
            }
        };

        // Plotly plot call
        try {
            Plotly.newPlot(id, [initialRms, relocRms], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };

    }

    // 8. 3D plot hypocenter
    function Plot3dHypocenter(id, data) {
        // Create hover text for station
        const hoverTextStation = data.station.station_code.map((x, i) =>
            `Station: ${x}<br> Latitude: ${data.station.latitude[i]}<br> Longitude: ${data.station.longitude[i]}<br> ELev (m): ${data.station.elev[i]}`
        )

        const initHypo = {
            name: 'Initial Hypocenter',
            type: 'scatter3d',
            mode: 'markers',
            x: data.initial.longitude,
            y: data.initial.latitude,
            z: data.initial.elev,
            marker: {
                size: 5,
                color: 'indianred',
                opacity: 0.8
            }
        };

        const relocHypo = {
            name: 'Relocated Hypocenter',
            type: 'scatter3d',
            mode: 'markers',
            x: data.reloc.longitude,
            y: data.reloc.latitude,
            z: data.reloc.elev,
            marker: {
                size: 5,
                color: '#1F77B4',
                opacity: 0.8
            }
        };

        const station = {
            name: 'Stations',
            type: 'scatter3d',
            mode: 'markers+text',
            x: data.station.longitude,
            y: data.station.latitude,
            z: data.station.elev,
            marker: {
                color: '#FF9900',
                symbol: 'triangle-up', 
                opacity: 0.8,
                size: 12
            },
            text: data.station.station_code,
            textposition: 'top center',
            textfont:{
                size: 12,
                color: 'rgba(52, 58, 64,0.8)'
            },
            hoverinfo: 'text',
            hovertemplate: hoverTextStation
        };


        const layout = {
            title: '3D Hypocenter Plot',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                yanchor : "top",
                y : 0.99,
                xanchor : "right",
                x : 0.99,             
                bgcolor : "rgba(255,255,255,0.5)"
            },
            height: 650,
            autosize: true,
            scene:{
                xaxis: {
                    title: 'Longitude',
                    tickangle: 0
                },
                yaxis: {
                    title: 'Latitude',
                    scaleanchor: "x", 
                    scaleratio: 1    
                },
                zaxis: {
                    title: 'Elevation (m)',
                    zeroline: false,
                }, 
                aspectmode : 'manual',
                aspectratio: {x:1, y:1, z:0.5},
                camera:{
                    up:{x:0, y:0, z:1},
                    eye: {x:0.5, y:0.5, z:0.5}
                }

            }
        }

        // Plotly plot call
        try {
            Plotly.newPlot(id, [initHypo, relocHypo, station], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };
    }


    // 9. Magnitude histogram plot 
    function magnitudeHistogram(id, data) {
        const magHist = {
            name: 'Magnitude',
            x: data.magnitude,
            type: 'histogram',
            marker: {
                color: 'indianred',
                line: {
                    color:'white',
                    width: 0.5
                }
            }, 
            opacity: 0.8
        };

        const layout = {
            title: 'Magnitude Histogram',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                    yanchor : "top",
                    y : 0.99,
                    xanchor : "right",
                    x : 0.99,             
                    bgcolor : "rgba(255,255,255,0.5)"
                },
            height: 400,
            autosize: true,
            xaxis: {
                title: 'Magnitude',
                tickangle: 0
            },
            yaxis: {
                title: 'Counts',
                rangemode: 'tozero',
            },
            bargap: 0.1,
            margin: {
                r: 100,
                b: 100
            }

        };

        // Plotly plot call
        try {
            Plotly.newPlot(id, [magHist], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };
    }

    // 10. Gutenberg-Richter Analysis
    function gutenbergRichterAnalysis(id, data){

        // Cumulative magnitude data
        const cumulativeCounts = {
            name: 'Cumulative (N >= M)',
            type: 'scatter',
            mode: 'markers',
            x: data.cumulative.x,
            y: data.cumulative.y,
            marker: {
                color: '#1F77B4',
                size: 8,
                opacity: 0.8,
                hovertemplate: 'Magnitude: ${x:.3f}<br> Log10(Count): ${y:.3f}',
            }
        }

        // Non-cumulative magnitude data
        const nonCumulativeCounts = {
            name: 'Non-Cumulative',
            type: 'scatter',
            mode: 'markers',
            x: data.non_cumulative.x,
            y: data.non_cumulative.y,
            marker: {
                symbol: 'triangle-up',
                color: 'green',
                size : 8,
                opacity: 0.8,
                hovertemplate: 'Magnitude: ${x:.3f}<br> Log10(Count): ${y:.3f}'
            }
        }

        // Plot the fitted line
        const fittedLine = {
            name: `Fit: b_val = ${data.b_value.toFixed(3)}, a_val = ${data.a_value.toFixed(3)}, R^2 = ${data.r_value**2}`,
            type: 'scatter',
            mode: 'line',
            x: data.fitted_line.x,
            y: data.fitted_line.y,
            line: {
                color: 'indianred',
                opacity: 0.8
            }
        }

        // Plot the Magnitude Completeness
        const magnitudeCompleteness = {
            name: `Magnitude Completeness: ${data.mc[0]}`,
            type: 'scatter',
            mode: 'markers+text',
            x: [data.mc[0]],
            y: [data.mc[1]],
            marker: {
                size: 12,
                symbol: 'triangle-down',
                color:'#FF9900',
                opacity: 0.8
            },
            text: 'MC',
            textposition: 'top center',
            textfont : {
                size: 12,
                color: '#333333' 
            },
            hovertemplate: '<b>Magnitude Completeness</b><br>Log10(N >= M): %{y:.2f}<br>Magnitude: %{x:.2f}<extra></extra>'
        }

        // Plot layout
        const layout = {
            title: 'Gutenberg-Richter Analysis',
            showlegend: true,
            template: 'plotly_white',
            legend: {
                    yanchor : "top",
                    y : 0.99,
                    xanchor : "right",
                    x : 1.50,             
                    bgcolor : "rgba(255,255,255,0.5)"
                },
            height: 400,
            autosize: true,
            xaxis: {
                title: 'Magnitude',
                tickangle: 0,
                zeroline: false
            },
            yaxis: {
                title: 'Log10(Count)',
                rangemode: 'tozero',
            },
            margin: {
                r: 100,
                b: 100
            }
        }

        
        // Plotly plot call
        try {
            Plotly.newPlot(id, [cumulativeCounts, nonCumulativeCounts, fittedLine, magnitudeCompleteness], layout);
        } catch (error) {
            console.error('Plotly.newPlot failed:', error)
        };

    }
    

    // Function to update UI with fetched data
    function updateUI(data) {
        if (!data || !data.general_statistics || !data.overall_daily_intensities || !data.station_performance) {
            console.error('Invalid or missing data')
            return;
        }

        // Get data
        const gen_stats = data.general_statistics;
        const daily_intensities = data.overall_daily_intensities;
        const station_performance = data.station_performance;
        const wadati_profile =  data.wadati_profile;
        const time_series_station_performance = data.time_series_performance;
        const hypocenter = data.hypocenter;
        const rms_error = data.rms_error;
        const magnitude_hist = data.magnitude_histogram;
        const gutenberg_analysis = data.gutenberg_analysis;

        // call animateCount for each statistic
        animateCount('station-count', gen_stats.total_stations, 2000);
        animateCount('event-count', gen_stats.total_events, 2000);
        animateCount('phase-count', gen_stats.total_phases, 2000);

        // create plot for daily overall intensities
        intensitiesOverallPlot('daily-overall-intensities', daily_intensities);

        // create plot for station performance
        stationPerformanceBar('station-performance', station_performance);

        // create plot for wadati profile
        WadatiProfile('wadati-profile', wadati_profile);

        // crate plot for time series station performance
        timeSeriesStationPerformance('time-series-performance', time_series_station_performance);

        // create 2D plot hypocenter
        Plot2dHypocenter('hypocenter-plot', hypocenter);

        // create plot for rms error histogram
        histogramError('rms-error', rms_error);

        // create 3D plot hypocenter
        Plot3dHypocenter('hypocenter-plot-3d', hypocenter);

        // create magnitude histogram plot
        magnitudeHistogram('magnitude-histogram', magnitude_hist);

        // create plot for Gutenberg-Analysis
        gutenbergRichterAnalysis('gutenberg-richter-analysis', gutenberg_analysis);
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