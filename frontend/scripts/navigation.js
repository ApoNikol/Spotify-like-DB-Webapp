async function loadPlaylists() {
    const playlistsContainer = document.getElementById('playlists-container');

    playlistsContainer.innerHTML = '<p>Loading playlists...</p>';

    try {
        const response = await fetch('http://127.0.0.1:5000/api/playlists');
        const data = await response.json();

        if (data.playlists && data.playlists.length > 0) {
            playlistsContainer.innerHTML = ''; // Clear loading message

            data.playlists.forEach((playlist) => {
                const playlistElement = document.createElement('div');
                playlistElement.classList.add('playlist');
                playlistElement.innerHTML = `
                    <h3>${playlist.name}</h3>
                    <button class="delete-btn" onclick="deletePlaylist(${playlist.id})">Delete Playlist</button>
                    <ul class="songs">
                        ${playlist.songs.map(song => `
                            <li class="song">
                                ${song.name} (${song.artist}) 
                                <button class="delete-song-btn" onclick="deleteSong(${song.id})">X</button>
                            </li>`).join('')}
                    </ul>
                `;
                playlistsContainer.appendChild(playlistElement);
            });
        } else {
            playlistsContainer.innerHTML = '<p>No playlists available.</p>';
        }
    } catch (error) {
        playlistsContainer.innerHTML = `<p>Error loading playlists: ${error.message}</p>`;
    }
}

async function deletePlaylist(playlistId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/playlists/${playlistId}`, { method: 'DELETE' });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to delete playlist');
        }

        const data = await response.json();
        alert(data.message);
        loadPlaylists();  // Reload playlists after deletion
    } catch (error) {
        alert(`Error deleting playlist: ${error.message}`);
    }
}

async function deleteSong(songId) {
    try {
        const response = await fetch(`http://127.0.0.1:5000/api/songs/${songId}`, { method: 'DELETE' });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to delete song');
        }

        const data = await response.json();
        alert(data.message);
        loadPlaylists();  // Reload playlists after deletion
    } catch (error) {
        alert(`Error deleting song: ${error.message}`);
    }
}

window.onload = loadPlaylists;  // Load playlists when the page loads
