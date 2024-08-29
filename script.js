function fetchAnime() {
    const username = document.getElementById('username').value;
    if (!username) return;

    // Replace with actual API URL and method
    fetch(`https://api.example.com/get-random-anime?username=${username}`)
        .then(response => response.json())
        .then(data => {
            const animeContent = document.getElementById('anime-content');
            const animeImage = document.getElementById('anime-image');
            const animeTitle = document.getElementById('anime-title');

            if (data.image_url && data.title) {
                animeImage.src = data.image_url;
                animeImage.alt = `${data.title} cover image`;
                animeTitle.textContent = data.title;
                animeContent.style.opacity = '1'; // Fade in the content
            } else {
                animeTitle.textContent = 'No anime found';
                animeImage.src = '';
                animeContent.style.opacity = '1'; // Fade in the content
            }
        })
        .catch(error => {
            console.error('Error fetching anime:', error);
        });
}