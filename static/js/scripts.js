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