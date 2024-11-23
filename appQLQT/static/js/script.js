// appQLQT/static/appQLQT/js/scripts.js
document.addEventListener('DOMContentLoaded', function() {
    console.log('JavaScript loaded successfully!');
});
document.addEventListener('DOMContentLoaded', function() {
    // Example: Alert when the search button is clicked
    const searchButton = document.querySelector('.input-group button');
    
    if (searchButton) {
        searchButton.addEventListener('click', function() {
            const searchInput = document.querySelector('.input-group input');
            alert(`You searched for: ${searchInput.value}`);
        });
    }

    // Example: Adding smooth scroll to sections if you have anchors
    const scrollLinks = document.querySelectorAll('a[href^="#"]');
    scrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
});

// Get the video
var video = document.getElementById("myVideo");

// Get the button
var btn = document.getElementById("myBtn");

// Pause and play the video, and change the button text
function myFunction() {
  if (video.paused) {
    video.play();
    btn.innerHTML = "Pause";
  } else {
    video.pause();
    btn.innerHTML = "Play";
  }
}