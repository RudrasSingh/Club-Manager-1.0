const inputs = ["input1", "input2", "input3", "input4"];

inputs.map((id) => {
  const input = document.getElementById(id);
  addListener(input);
});

function addListener(input) {
  input.addEventListener("keyup", () => {
    const code = parseInt(input.value);
    if (code >= 0 && code <= 9) {
      const n = input.nextElementSibling;
      if (n) n.focus();
    } else {
      input.value = "";
    }

    const key = event.key; // const {key} = event; ES6+
    if (key === "Backspace" || key === "Delete") {
      const prev = input.previousElementSibling;
      if (prev) prev.focus();
    }
  });
}

var timeleft = 30;
    var downloadTimer = setInterval(settimerrr, 1000);

    function settimerrr() {
        timeleft--;
        document.getElementById("countdowntimer").textContent = timeleft;
        if (timeleft <= 0) {
            clearInterval(downloadTimer);
            document.getElementById("resendtext").innerHTML = '<a href="#" onclick="resendOTP()">Resend Now</a>';
        }
    }

    function resendOTP() {
        timeleft = 30; 
        document.getElementById("resendtext").innerHTML = "Resend OTP in <span id='countdowntimer'>30</span> Seconds";
        downloadTimer = setInterval(settimerrr, 1000);
    }

function redirect()
{
  var input1 = document.getElementById("input1").value;
  var input2 = document.getElementById("input2").value;
  var input3 = document.getElementById("input3").value;
  var input4 = document.getElementById("input4").value;

  // Check if all input fields are filled
  if (input1 !== "" && input2 !== "" && input3 !== "" && input4 !== "") {
    window.location.href = "{{ url_for('static', forname='') }}";
  } else {
    // Alert the user to fill all input fields
    alert("Please fill all fields of the OTP.");
  }
 
}


