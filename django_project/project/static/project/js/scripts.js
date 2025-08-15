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

    // For station table
    let station_table = new DataTable('#station-table');

    // For upload preview table
    let preview_table = new DataTable('#preview-table');


    // Pop up messages
    const toastElList = [].slice.call(document.querySelectorAll('.toast'))
    toastElList.map(function (toastEl) {
        const toast = new bootstrap.Toast(toastEl)
        toast.show()
    })
});