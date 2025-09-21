const configForm = document.getElementById('config-form');
const teaConfigs = document.getElementById('tea-configs');

// Fetch config and populate the form
fetch('http://localhost:8000/api/config')
    .then(response => response.json())
    .then(data => {
        const teas = data.teas;
        for (const key of ['tea1', 'tea2', 'tea3']) {
            const div = document.createElement('div');
            div.innerHTML = `
                <label for="${key}">${key}:</label>
                <input type="text" id="${key}" name="${key}" value="${teas[key]}">
            `;
            teaConfigs.appendChild(div);
        }
    });

// Handle form submission
configForm.addEventListener('submit', (event) => {
    event.preventDefault();
    const formData = new FormData(configForm);
    const newConfig = { teas: {} };
    for (const [key, value] of formData.entries()) {
        newConfig.teas[key] = value;
    }

    // Placeholder for saving the config
    console.log('Saving new config:', newConfig);

    fetch('http://localhost:8000/api/config', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(newConfig)
    });
});
