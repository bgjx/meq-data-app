//  Maps functionality
document.addEventListener('DOMContentLoaded', function() {
    // check global variable
    if (typeof window.absUrl == 'undefined' || typeof window.mapboxToken == 'undefined') {
        console.error("Missing required global variables: site_slug and mapbox token");
        return;
    }

    // cache for fetched data
    let cacheData = null;
    
    //  function to fetch MEQ data
    async function fetchMeqData(){
        if (cacheData) {
            return cacheData;
        }
        try {
            const response = await fetch(`${window.absUrl}get-meq-data`);
            if (!response.ok) {
                throw new Error(`Http error! status: ${response.status}`);
            }
            cacheData = await response.json();
            return cacheData;
        } catch (error) {
            console.error("Error fetching MEQ data:", error);
            return null;
        }
    }

    // function for scatter map
    function createScatterMap(data, elementId, datasetKey){
        const scatterData = {
            type : 'scattermapbox',
            lat: data[datasetKey].map(item => item.lat),
            lon: data[datasetKey].map(item => item.lon),
            mode: 'markers',
            marker :{
                color: data[datasetKey].map(item => item.depth_m),
                size : data[datasetKey].map(item => item.norm_mw * 10),
                colorscale: 'IceFire',
                opacity: 0.9,
                colorbar: {
                    title: 'Depth (m)',
                    tickvals: [8000, 6000, 4000, 2000, 0, -2000],
                    ticktext: ['8000', '6000', '4000', '2000', '0', '-2000'], 
                },
            },
            text : data[datasetKey].map(item => `Depth: ${item.depth_m}<br>Mag: ${item.mw_mag}`),
            hoverinfo: 'text' 
        };

        const stationData = {
            type: 'scattermapbox',
            mode: 'markers+text',
            lat: data.station.map(item => item.lat),
            lon: data.station.map(item => item.lon),
            text : data.station.map(item => item.sta),
            textposition: 'top center',
            marker: {
                symbol: 'triangle',
                size : 14,
                color: 'red',
                angleref: 'previous',
            },
            hoverinfo: 'text',
        };

        const layout = {
            title: ' MEQ Scatter Map',
            mapbox: {
                style: 'outdoors',
                center: {lat: data.center_map.lat, lon: data.center_map.lon}, 
                zoom: 12,
                accesstoken: `${window.mapboxToken}`
            },
            showlegend: false,
            height: 782,
            autosize: true, 
        };
        const config = {
            displayModeBar: false,
        };
        Plotly.newPlot(elementId, [scatterData, stationData], layout, config);
    }

    // Function for density map
    function createDensityMap(data, elementId, datasetKey) {
        const densityData = {
            type : 'densitymapbox',
            lat: data[datasetKey].map(item => item.lat),
            lon: data[datasetKey].map(item => item.lon),
            radius: 10,
            colorscale : 'Viridis',
            colorbar:{
                title: 'Density',
            },
        };

        const stationData = {
            type: 'scattermapbox',
            mode: 'markers+text',
            lat: data.station.map(item => item.lat),
            lon: data.station.map(item => item.lon),
            text : data.station.map(item => item.sta),
            textposition: 'top center',
            marker: {
                symbol: 'triangle',
                size : 14,
                color: 'red',
                angleref: 'previous',
            },
            hoverinfo: 'text',
        };

        const layout = {
            title: 'MEQ Density Map',
            mapbox :{
                style: 'outdoors',
                center: {lat: data.center_map.lat, lon: data.center_map.lon},
                zoom: 12,
                accesstoken: `${window.mapboxToken}`,
            },
            showlegend: false,
            height: 782,
            autosize: true,
        };

        const config = {
            displayModeBar : false,
        };

        Plotly.newPlot(elementId, [densityData, stationData], layout, config);
    }

    // Initialized tabs to prevent re-rendering
    const InitializedTabs = {
        'scatter-map-wcc': false,
        'density-map-wcc': false,
        'scatter-map-nll': false,
        'density-map-nll': false
    };

    // Tabs functionality 
    let tabs = document.querySelectorAll(".nav-tabs li button");
    let tabContent = document.querySelectorAll(".tab-contents-map .tab-content");

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", async () => {
            //  Update active tab and content
            tabContent.forEach(content => content.classList.remove('active'));
            tabs.forEach(tab => tab.classList.remove("active"));
            tabContent[index].classList.add("active");
            tabs[index].classList.add("active");

            // Get the map elements in the active tab
            const activeTabPlots = tabContent[index].querySelectorAll('.maps-meq');
            const mapIds = Array.from(activeTabPlots).map(plot => plot.id)

            // Fetch data and create maps for uninitialized tabs
            for (const mapId of mapIds) {
                if (!InitializedTabs[mapId]) {
                    const data = await fetchMeqData();
                    if (!data) {
                        console.error(`Failed to fetch data for map ${mapId}`)
                        continue;
                    }

                    if (mapId.includes('scatter')) {
                        createScatterMap(data, mapId, mapId.includes('wcc') ? 'meq_wcc' : 'meq_nll');
                    } else if (mapId.includes('density')) {
                        createDensityMap(data, mapId, mapId.includes('wcc') ? 'meq_wcc': 'meq_nll');
                    }
                    InitializedTabs[mapId] = true;
                }
            }

            // Resize Plotly charts in the active tab
            activeTabPlots.forEach(plot => {
                if (plot && typeof Plotly !== 'undefined' && plot._fullLayout) {
                    Plotly.Plots.resize(plot);
                }
            });
        });
    });
    
    //  Optionally trigger the first tab click to load the initial map
    if (tabs.length > 0) {
        tabs[0].click();
    }
});