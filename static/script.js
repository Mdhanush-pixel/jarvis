function updateData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => {
            document.getElementById('time').innerText = data.time;
            document.getElementById('temp').innerText = data.temperature;
        });
}

document.getElementById('updateBtn').addEventListener('click', updateData);

// Auto-update every 5 seconds
setInterval(updateData, 5000);
updateData(); // Run once on load
