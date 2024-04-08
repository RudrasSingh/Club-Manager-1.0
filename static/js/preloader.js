var preloader = document.querySelector('.loading');
var body = document.querySelector('body');

preloader.style.display = 'flex'; // Display the preloader
body.classList.add('loading'); // Add the loading class to body to prevent scrolling

setTimeout(function() {
  preloader.style.display = 'none'; // Hide the preloader
  body.classList.remove('loading'); // Remove the loading class to enable scrolling
}, 2000); //2sec preloader time
