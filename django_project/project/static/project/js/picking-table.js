// Table functionalities
document.addEventListener('DOMContentLoaded', function() {
    let tableInstances = {};

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
    function initServerTable(tableEl) {
        const tableId = tableEl.getAttribute("id")
        if (tableInstances[tableId]) {
            return;
        }

        const apiUrl = tableEl.dataset.apiUrl;
        if (!apiUrl){
            console.error(`Missing data-api url from table ${tableId}`)
            return;
        }

        // Rendering function
        // function formatDecimal(data, precision){
        //     if (data === null && data === undefined && data === '') return '';
        //     let num = parseFloat(data);
        //     if (isNaN(num)) return '';
        //     return num.toFixed(precision);
        // }

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
                    const formData = new FormData(document.getElementById('filter-form-picking'));
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
                {data: "station_code"},
                {data: "p_arrival_dt"},
                {data: "p_polarity"},
                {data: "p_onset"},
                {data: "p_arrival_dt"},
                {data: "coda_dt"}

            ]
        });
    }

    // Update table function (triggers DataTable reload with filters)
    function updateTable(tableEl){
        const tableId = tableEl.getAttribute('id')
        const tableInstance = tableInstances[tableId];
        if (tableInstance) {
            tableInstance.ajax.reload();
        } else {
            console.error(`Table instance for ${tableId} not found`);
        }
    }

    //  Handle filter form submission
    const filterForm = document.getElementById('filter-form-picking');
    if (filterForm) {
        filterForm.addEventListener('submit', async(event) => {
            event.preventDefault();

            // Show loading indicator
            const loadingSpinner = document.getElementById('loading-spinner');
            if (loadingSpinner) loadingSpinner.style.display = 'block';

            try {
                const tableEl = document.getElementById('table-picking');
                if (tableEl) {
                    updateTable(tableEl);
                }
            } finally {
                if (loadingSpinner) loadingSpinner.style.display = 'none';
            }
        });
    }

    // Handle real-time filter changes(e.g., for datetime inputs)
    const filterInputs = document.querySelectorAll('#filter-form-picking input');
    filterInputs.forEach((input) => {
        input.addEventListener(
            'input',
            debounce(async() => {

                const loadingSpinner = document.getElementById('loading-spinner');
                if (loadingSpinner) loadingSpinner.style.display = 'block';

                try {
                    const tableEl = document.getElementById('table-picking');
                    if (tableEl) {
                        updateTable(tableEl);
                    }
                } finally {
                    if (loadingSpinner) loadingSpinner.style.display = 'none';
                }
            }, 500)
        );
    });

    // Initialize DataTables for the tables in the active tab on load
    const pickingTableEl = document.getElementById('table-picking');
    if (pickingTableEl) {
        initServerTable(pickingTableEl);
    }


});