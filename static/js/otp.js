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
const submit = document.getElementById("submit");

submit.addEventListener('click', () => {
    container.classList.add("active");
});

submit.addEventListener('click', () => {
    container.classList.remove("active");
});

// OTP Timer
var timeleft = 30; 
var downloadTimer = setInterval(function(){
    timeleft--;
    document.getElementById("countdowntimer").textContent = timeleft;
    if(timeleft <= 0) {
        clearInterval(downloadTimer);
        document.getElementById("resendtext").innerHTML = '<a href="#" onclick="resendOTP()">Resend Now</a>';
    }
}, 1000);


//incase u require
// function resendOTP() {
//     reload the page for resend option
//     location.reload();
// }