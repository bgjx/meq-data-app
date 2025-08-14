// Table functionalities
document.addEventListener('DOMContentLoaded', function() {
    // check global variable 
    if (typeof window.absUrl === 'undefined'){
        console.error("Missing global variable: absUrl");
        return;
    }

    let tableInstances = {};
    const tabs = document.querySelectorAll(".nav-tabs li button");
    const tabContent = document.querySelectorAll(".tab-contents-tab .tab-content");
    
    // setup cache for fetched data (by creating new map object)
    let cacheData = new Map();

    // function to fetch analysis data with filters application
    async function fetchData(filters = {}, catalogType, siteSlug){
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
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
                    break

                }
            }
        }
        return cookieValue;
    }

    // Debounce function to limit frequent API calls
    function debounce(func, wait){
        let timeout;
        return function(...args) {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }

    // Function to initialize a DataTable with server-side mode
    function initServerTable(tableEl, catalogType, siteSlug) {
        const tableId = tableEl.getAttribute("id")
        
        // Avoid re-initializing if already done
        if (tableInstances[tableId]) {
            return;
        }

        const apiUrl = `/project/api/hypocenter-table-data/${siteSlug}/${catalogType}`;
        tableInstances[tableId] = new DataTable(tableEl, {
            processing: true,
            serverSide: true,
            searching: true,
            ordering: true,
            pageLength: 10,
            ajax: {
                url: apiUrl,
                type: 'GET',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken'),
                },
                data: function (d) {
                    // Add extra filter params from your filter form
                    const formData = new FormData(document.getElementById('filter-form'));
                    const filters = Object.fromEntries(formData);
                    // console.log('AJAX params:', { ...d, ...filters });
                    Object.assign(d, filters);
                },
                error: function(xhr, error, thrown){
                    console.error('DataTables AJAX error:', {
                        status: xhr.status,
                        url:apiUrl,
                        response:xhr.responseText,
                        error, 
                        thrown
                    });
                },
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

    // Update table function (triggers DataTable reload with filters)
    function updateTable(catalogType, siteSlug){
        const tableId = `table-${catalogType}`;
        const tableInstance = tableInstances[tableId];
        if (tableInstance) {
            tableInstance.ajax.reload();
        } else {
            console.error(`Table instance for ${tableId} not found`);
        }
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
                // Extract catalogType and siteSlug from context (e.g., active tab or table dataset)
                const activeTab = document.querySelector(".nav-tabs li button.active");
                const activeIndex = Array.from(tabs).indexOf(activeTab);
                const activeTable = tabContent[activeIndex]?.querySelector(".table-container table");
                const catalogType = activeTable?.dataset.catalogType;
                const siteSlug = activeTable?.dataset.siteSlug;

                if (catalogType && siteSlug) {
                    const data = await fetchData(filters, catalogType, siteSlug);
                    updateTable(catalogType, siteSlug);
                }
            } finally {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
            }
        });
    }

    // Handle real-time filter changes(e.g., for datetime inputs)
    const filterInputs = document.querySelectorAll('#filter-form input');
    filterInputs.forEach((input) => {
        input.addEventListener(
            'input',
            debounce(async() => {
                const formData = new FormData(filterForm);
                const filters = Object.fromEntries(formData);

                const loadingSpinner = document.getElementById('loading-spinner');
                if (loadingSpinner) loadingSpinner.style.display = 'block';

                try {
                    const activeTab = document.querySelector(".nav-tabs li button.active");
                    const activeIndex = Array.from(tabs).indexOf(activeTab);
                    const activeTable = tabContent[activeIndex]?.querySelector(".table-container table");
                    const catalogType = activeTable?.dataset.catalogType;
                    const siteSlug = activeTable?.dataset.siteSlug;

                    if (catalogType && siteSlug) {
                        const data = await fetchData(filters, catalogType, siteSlug);
                        updateTable(catalogType, siteSlug);
                    }
                } finally {
                    if (loadingSpinner) loadingSpinner.style.display = 'none';
                }
            }, 500)
        );
    });

    // // Initial data fetch (no filters)
    // (async () =>  {
    //     const data = await fetchData();
    //     updateTable(data);
    // })();

    // Initialize DataTables for the tables in the active tab on load    
    const activeTab = document.querySelector(".nav-tabs li button.active");
    if (activeTab) {
        const activeIndex = Array.from(tabs).indexOf(activeTab);
        if (tabContent[activeIndex]) {
            const activeTables = tabContent[activeIndex].querySelectorAll(".table-container table");
            activeTables.forEach(function(table) {
                const catalogType = table.dataset.catalogType;
                const siteSlug = table.dataset.siteSlug;
                table.setAttribute('id', `table-${catalogType}`);
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
                    table.setAttribute('id', `table-${catalogType}`)
                    initServerTable(table, catalogType, siteSlug)
                });
            }
        });
    });

});