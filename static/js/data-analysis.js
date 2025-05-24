//  Maps functionality
document.addEventListener('DOMContentLoaded', function() {
    // check global variable
    if (typeof window.absUrl == 'undefined' || typeof window.mapboxToken == 'undefined') {
        console.error("Missing required global variables: site_slug and mapbox token");
        return;
    }

    async function fetchMeqData(){
        const response = await fetch(`${window.absUrl}get-meq-data`);
        const data = await response.json();
        return data;
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

    // Tabs functionality 
    let tabs = document.querySelectorAll(".nav-tabs li button");
    let tabContent = document.querySelectorAll(".tab-contents-map .tab-content");

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            tabContent.forEach(content => {
                content.classList.remove('active')
            });
            tabs.forEach(tab =>{
                tab.classList.remove("active")
            });
            tabContent[index].classList.add("active");
            tabs[index].classList.add("active");

            // Resizing the PlotLy charts in the active tab
            let activeTabPlots = tabContent[index].querySelectorAll('.maps-meq');
            activeTabPlots.forEach(plot => {
                if (plot && typeof Plotly !== 'undefined' && plot._fullLayout) {
                    Plotly.Plots.resize(plot);
                }
            });
        });
    });
    
    //  call the function once the page is loaded
    fetchMeqData().then(data => {
        createScatterMap(data, 'scatter-map-wcc', 'meq_wcc');
        createDensityMap(data, 'density-map-wcc', 'meq_wcc');
        createScatterMap(data, 'scatter-map-nll', 'meq_nll');
        createDensityMap(data, 'density-map-nll', 'meq_nll');
    });

});