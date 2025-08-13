// Table functionalities
document.addEventListener('DOMContentLoaded', function() {
    // check global variable 
    if (typeof window.absUrl === 'undefined'){
        console.error("Missing global variable: absUrl");
        return;
    }

    // setup cache for fetched data (by creating new map object)
    let cacheData = new Map();

    // function to fetch analysis data with filters application
    async function fetchData(filters = {}){
        // Extract site slug
        const siteSlug = window.absUrl.split("/")[2];

        const cacheKey = JSON.stringify(filters);
        if (cacheData.has(cacheKey)) {
            return cacheData.get(cacheKey)
        }

        const queryString = new URLSearchParams(filters).toString();
        const url = `/project/api/hypocenter-table-data/${siteSlug}/${catalogType}${queryString ? `?${queryString}` : ''}`;

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
            console.error('Error fetching hypocenter table data:', error)
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
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))

                }
            }
        }
        return cookieValue;
    }

    // Function to update table
    function updateTable(data){
        if (!data.data){
            console.error('Invalid or missing data')
            return;
        }
    }


    // Debounce function to limit frequent API calls
    function debounce(func, wait){
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    //  Handle filter form submission
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        filterForm.addEventListener('submit', async(event) => {
            event.preventDefault();
            const formData = new FormData(filterForm);
            const filters = Object.fromEntries(formData);

            // Show loading indicator
            const loadingSpinner = document.getElementById('loading-spinner');
            if (loadingSpinner) loadingSpinner.style.display = 'block';
            try{
                const data = await fetchData(filters);
                updateTable(data);
            } finally {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
            }
        });
    }

    // Handle real-time filter changes(e.g., for slider or inputs)
    const filterInputs = document.querySelectorAll('#filter-form input');
    filterInputs.forEach((input) => {
        input.addEventListener(
            'input',
            debounce(async() => {
                const formData = new FormData(filterForm);
                const filters = Object.fromEntries(formData);

                const loadingSpinner = document.getElementById('laoding-spinner');

                if (loadingSpinner) loadingSpinner.style.display = 'block';

                try {
                    const data = await fetchData(filters);
                    updateTable(data);
                } finally {
                    if (loadingSpinner) loadingSpinner.style.display = 'none';
                }
            }, 500)
        );
    });

    // Initial data fetch (no filters)
    (async () =>  {
        const data = await fetchData();
        updateTable(data);
    })();



    const tabs = document.querySelectorAll(".nav-tabs li button");
    const tabContent = document.querySelectorAll(".tab-contents-tab .tab-content");
    let tableInstances = {};

    // Function to initialize a DataTable with server-side mode
    function initServerTable(tableEl, catalogType, siteSlug) {
        const tableId = tableEl.getAttribute("id")
        
        // Avoid re-initializing if already done
        if (tableInstances[tableId]) {
            return;
        }

        tableInstances[tableId] = new DataTable(tableEl, {
            processing: true,
            serverSide: true,
            ajax: {
                url: `api/hypocenter-table-data/${siteSlug}/${catalogType}`,
                data: function (d) {
                    return d;
                }
            },
            columns: [
                {data: "source_id"},
                {data: "source_lat"},
                {data: "source_lon"},
                {data: "source_depth_m"},
                {data: "source_origin_dt"},
                {data: "source_err_rms_s"},
                {data: "magnitude"},
                {data: "remarks"}

            ]
        });
    }


    // Initialize DataTables for the tables in the active tab on load
    const activeTab = document.querySelector(".nav-tabs li button.active");
    if (activeTab) {
        const activeIndex = Array.from(tabs).indexOf(activeTab);
        if (tabContent[activeIndex]) {
            const activeTables = tabContent[activeIndex].querySelectorAll(".table-container table");
            activeTables.forEach(function(table) {
                // Pass catalogType and siteSlug based on your context
                const catalogType = table.dataset.catalogType;
                const siteSlug = table.dataset.siteSlug;
                initServerTable(table, catalogType, siteSlug);
            });
        }
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            tabContent.forEach(content => content.classList.remove('active'));
            tabs.forEach(t => t.classList.remove("active"));

            if (tabContent[index]) {
                tabContent[index].classList.add("active");
                tabs[index].classList.add("active");

                const activeTables = tabContent[index].querySelectorAll(".table-container table");
                activeTables.forEach(function(table) {
                    const catalogType = table.dataset.catalogType;
                    const siteSlug = table.dataset.siteSlug;
                    initServerTable(table, catalogType, siteSlug);
                });
            }
        });
    });

    // For picking table
    let picking_table = new DataTable('#picking-table');

    // For station table
    let station_table = new DataTable('#station-table');

    // For upload preview table
    let preview_table = new DataTable('#preview-table');

});