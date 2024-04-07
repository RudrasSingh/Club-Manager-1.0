document.addEventListener('DOMContentLoaded', function() {
  // Get reference to all 'Next' buttons
  var nextButtons = document.querySelectorAll('.js-btn-next');

  // Add click event listener to each 'Next' button
  nextButtons.forEach(function(button) {
      button.addEventListener('click', function() {
          // Find the next panel to display
          var currentPanel = this.closest('.multisteps-form__panel');
          var nextPanel = currentPanel.nextElementSibling;

          // Hide current panel and show next panel
          currentPanel.classList.remove('js-active');
          nextPanel.classList.add('js-active');

          // Update progress bar (optional)
          updateProgressBar();
      });
  });

  // Function to update progress bar (optional)
  function updateProgressBar() {
      var progressButtons = document.querySelectorAll('.multisteps-form__progress-btn');

      // Find the current active step and activate the next step in the progress bar
      progressButtons.forEach(function(button) {
          if (!button.classList.contains('js-active')) {
              button.classList.add('js-active');
              return;
          }
      });
  }
});
