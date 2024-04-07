var input_search = document.getElementById("input-search");
var bodyMain = document.getElementsByTagName("body")[0];

document.getElementById("search").addEventListener("click", () => {
  toggleOfClass(input_search, "show");
});

document.getElementById("menu").addEventListener("click", () => {
  toggleOfClass(bodyMain, "show-responsive-menu");
});

document.getElementById("back-sidebar").addEventListener("click", () => {
  toggleOfClass(bodyMain, "show-responsive-menu");
});

function toggleOfClass(element, ClassName) {
  let status = element.classList.contains(ClassName);
  if (status) {
    element.classList.remove(ClassName);
  } else {
    element.classList.add(ClassName);
  }
  return status;
}
