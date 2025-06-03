//  Maps functionality
document.addEventListener('DOMContentLoaded', function() {
    // check global variable
    if (typeof window.data == 'undefined') {
        console.error("Missing required global variables: data.");
        return;
    }

    // Parsed the data
    let parsedData;
    try {
        parsedData = JSON.parse(window.data)
    } catch (e) {
        console.error("Failed to parse window.data as JSON:", e);
        return;
    }

    // cache for fetched data
    const event_stats = parsedData.general_statistics;

    //  A function to animate counting
    function animateCount(id, endValue, duration = 1000) {
        const element = document.getElementById(id);
        if (!element) {
            console.error(`Element with id ${id} not found`);
            return;
        }

        const startTime = performance.now();
        const step = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const value = Math.floor(progress * endValue);

            element.textContent = value.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(step);
            }
        };

        requestAnimationFrame(step);
    }

    // call animateCount for each statistic
    animateCount('station-count', event_stats.total_stations);
    animateCount('event-count', event_stats.total_events);
    animateCount('phase-count', event_stats.total_phases);
});