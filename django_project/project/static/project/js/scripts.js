document.addEventListener('DOMContentLoaded', function() {
    // Sidebar expander
    const hamburger = document.querySelector("#toggle-btn");
    if (hamburger) {
        hamburger.addEventListener("click", function() {
            const sidebar = document.querySelector("#sidebar");
            const mainContent = document.querySelector("#side-main");
            if (sidebar && mainContent) {
                sidebar.classList.toggle("expand");
                mainContent.classList.toggle("expand");
            } else {
                console.log('Sidebar or main content not found!');
            }
        });
    } else {
        console.log('Hamburger button not found!');
    }

    // Toggle collapsible
    const filterCollapse = document.getElementById('filterCollapse');
    if (filterCollapse) {
        const chevronIcon = document.querySelector('.bi-chevron-down, .bi-chevron-up');
        if (chevronIcon) {
            filterCollapse.addEventListener('show.bs.collapse', function() {
                if (chevronIcon.classList.contains('bi-chevron-up')) {
                    chevronIcon.classList.replace('bi-chevron-up', 'bi-chevron-down');
                }
            });
            filterCollapse.addEventListener('hide.bs.collapse', function() {
                if (chevronIcon.classList.contains('bi-chevron-down')) {
                    chevronIcon.classList.replace('bi-chevron-down', 'bi-chevron-up');
                }
            });
        } else {
            console.log('Chevron icon not found!');
        }
    } else {
        console.log('Filter collapse element not found!');
    }

    // Table functionalities
    const tabs = document.querySelectorAll(".nav-tabs li button");
    const tabContent = document.querySelectorAll(".tab-contents-tab .tab-content");

    // Initialize DataTables for the tables in the active tab on load
    const activeTab = document.querySelector(".nav-tabs li button.active");
    if (activeTab) {
        const activeIndex = Array.from(tabs).indexOf(activeTab);
        if (tabContent[activeIndex]) {
            const activeTables = tabContent[activeIndex].querySelectorAll(".table-container table");
            activeTables.forEach(function(table) {
                new DataTable(table);
            });
        }
    }

    tabs.forEach((tab, index) => {
        tab.addEventListener("click", () => {
            tabContent.forEach(content => {
                content.classList.remove('active');
            });
            tabs.forEach(t => {
                t.classList.remove("active");
            });
            if (tabContent[index]) {
                tabContent[index].classList.add("active");
                tabs[index].classList.add("active");

                // Restyling the tables
                const activeTables = tabContent[index].querySelectorAll(".table-container table");
                activeTables.forEach(function(table) {
                    new DataTable(table);
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