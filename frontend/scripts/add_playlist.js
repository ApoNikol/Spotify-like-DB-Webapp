const apiUrl = 'http://127.0.0.1:5000/api/playlists';

document.getElementById('add-playlist-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const playlistName = document.getElementById('playlist-name').value;

    if (!playlistName) {
        alert('Please provide a playlist name.');
        return;
    }

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ name: playlistName }),
        });

        if (response.ok) {
            alert('Playlist created successfully!');
            document.getElementById('add-playlist-form').reset();
        } else {
            const errorData = await response.json();
            alert('Error creating playlist: ' + errorData.error);
        }
    } catch (error) {
        console.error('Fetch error:', error);
        alert('An error occurred while connecting to the server.');
    }
});
