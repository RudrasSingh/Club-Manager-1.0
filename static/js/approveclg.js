
(function() {
    $(document).ready(function() {
      var clickable;
      clickable = false;
      $(document).on('mouseover', '.confirm', function(e) {
        return setTimeout(function() {
          return clickable = true;
        }, 1000);
      });
      $(document).on('mouseleave', '.confirm', function(e) {
        return clickable = false;
      });
      return $(document).on('click', '.confirm', function(e) {
        if (!clickable) {
          console.log('Wait...');
          return e.preventDefault();
        } else {
          return alert('Bummer. Bye bye item...');
        }
      });
    });
  
  }).call(this);