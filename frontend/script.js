document.addEventListener('DOMContentLoaded', () => {
    // Init map, center kl
    const map = L.map('map').setView([3.139, 101.6869], 11);
        const outletLayer = L.layerGroup().addTo(map);
    const responseContainer = document.getElementById('response-container');

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);

    // with new outlet markers
    const updateMap = (outlets) => {
                outletLayer.clearLayers(); // Clear previous markers
        const query = document.getElementById('search-input').value;

        if (outlets.length > 0) {
            responseContainer.textContent = `Found ${outlets.length} outlets matching your criteria.`;
        } else if (query) {
            responseContainer.textContent = `Sorry, no outlets were found matching your criteria.`;
        } else {
            responseContainer.textContent = '';
        }
        outlets.forEach(outlet => {
            const marker = L.marker([outlet.latitude, outlet.longitude]).addTo(outletLayer);
            L.circle([outlet.latitude, outlet.longitude], {
                color: 'red',
                fillColor: '#f03',
                fillOpacity: 0.2,
                radius: 5000
            }).addTo(outletLayer);
            marker.bindPopup(`<b>${outlet.name}</b><br>${outlet.address}<br><a href="${outlet.waze_link}" target="_blank">Open in Waze</a>`);
        });
    };

    const fetchAllOutlets = () => {
        responseContainer.textContent = '';
        fetch('http://127.0.0.1:8000/api/outlets/')
            .then(response => response.json())
            .then(updateMap)
            .catch(error => {
                console.error('Error fetching outlet data:', error);
                alert('Could not fetch outlet data. Make sure the backend API is running.');
            });
    };

    const performSearch = () => {
                responseContainer.textContent = 'Searching...';
        const query = document.getElementById('search-input').value;
        if (!query) {
            fetchAllOutlets();
            return;
        }

        fetch('http://127.0.0.1:8000/api/outlets/search/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: query }),
        })
        .then(response => response.json())
        .then(data => {
            responseContainer.textContent = data.response_text;
            updateMap(data.outlets);
        })
        .catch(error => {
            console.error('Error searching for outlets:', error);
            alert('An error occurred during the search.');
        });
    };

    document.getElementById('search-button').addEventListener('click', performSearch);
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            performSearch();
        }
    });


    // search suggestions
        const suggestions = [
        "Which outlets are open 24 hours?",
        "Show me outlets with McDelivery",
        "Show me all KFC outlets",
        "Which outlets host Birthday Parties?"
    ];
    const suggestionsContainer = document.getElementById('suggestions-container');

    suggestions.forEach(text => {
        const button = document.createElement('button');
        button.textContent = text;
        button.className = 'suggestion-button';
        button.addEventListener('click', () => {
            document.getElementById('search-input').value = text;
            performSearch();
        });
        suggestionsContainer.appendChild(button);
    });

    // Initial load
    fetchAllOutlets();
});
