//  Sidebar expander
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector("#toggle-btn");

    if (hamburger) {
        hamburger.addEventListener("click", function() {
            const sidebar = document.querySelector("#sidebar");
            const mainContent = document.querySelector("#side-main");

            if (sidebar && mainContent) {
                sidebar.classList.toggle("expand");
                mainContent.classList.toggle("expand");
            }
        });
    } else {
        console.log('Hamburger button not found!');
    }
});

// // Table functionality
// document.addEventListener('DOMContentLoaded', function(){
//     let tables = document.querySelectorAll(".table-container table")
//     tables.forEach(function(table) {
//         $(table).DataTable();
//     });
// });

document.addEventListener('DOMContentLoaded', function(){
    // Tabs functionality 
    let tabs = document.querySelectorAll(".nav-tabs li button");
    let tabContent = document.querySelectorAll(".tab-contents-tab .tab-content");

    // Initialize DataTables for the tables in the active tab on load
    let activeTab = document.querySelector(".nav-tabs li button.active");
    if (activeTab) {
        let activeIndex = Array.from(tabs).indexOf(activeTab);
        let activeTables = tabContent[activeIndex].querySelectorAll(".table-container table");
        activeTables.forEach(function (table) {
            new DataTable(table);
        });
    }

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

            //  Restyling the tables
            let activeTables = tabContent[index].querySelectorAll(".table-container table")
            activeTables.forEach(function(table) {
                new DataTable(table);
            });
        });
    });

});


