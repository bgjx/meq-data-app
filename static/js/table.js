document.addEventListener('DOMContentLoaded', function() {
    if (typeof window.absUrl === 'undefined' || typeof window.siteSlug === 'undefined') {
        console.error("Missing required global variables: absURL and siteSlug");
        return;
    }

    //  Fetching data
    async function fetchTabData(catalogType){
        try {
            const response = await fetch(`${window.absUrl}${window.siteSlug}/?catalog_type=${catalogType}`);
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`)
            }
            const data = await response.json()
            return data.data;
        } catch (error) {
            console.error("Error fetching tab data:", error);
            return [];
        }
    }



}

)