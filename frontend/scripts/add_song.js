const apiUrl = 'http://127.0.0.1:5000/api/songs'; // For adding a song
const playlistsApiUrl = 'http://127.0.0.1:5000/api/playlists'; // For fetching playlists

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch playlists from the backend
        const response = await fetch(playlistsApiUrl);
        const data = await response.json();

        console.log(data); // Debug log to ensure correct response

        const playlistSelect = document.getElementById('playlist');

        // Populate playlists in the dropdown
        if (data.playlists && data.playlists.length > 0) {
            data.playlists.forEach((playlist) => {
                const option = document.createElement('option');
                option.value = playlist.id; // Playlist ID
                option.textContent = playlist.name; // Playlist name only
                playlistSelect.appendChild(option);
            });
        } else {
            alert('No playlists available. Please create some playlists first.');
        }
    } catch (error) {
        console.error('Error fetching playlists:', error);
        alert('Error fetching playlists. Please try again later.');
    }
});

//// Handle form submission
document.getElementById('add-song-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const songName = document.getElementById('song-name').value;
    const artist = document.getElementById('artist').value;
    const duration = document.getElementById('duration').value;
    const releaseDate = document.getElementById('release-date').value;
    const playlistId = document.getElementById('playlist').value; // Selected playlist
    const userId = "default_user"; // Default or dynamic user ID

    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                song_name: songName,
                artist: artist,
                duration: duration,
                release_date: releaseDate,
                playlist_id: playlistId,
                user_id: userId
            }),
        });

        if (response.ok) {
            alert('Song added successfully!');
            document.getElementById('add-song-form').reset();
        } else {
            const errorData = await response.json();
            alert(`Error adding song: ${errorData.error}`);
        }
    } catch (error) {
        console.error('Error adding song:', error);
        alert('Error adding song. Please try again.');
    }
});
