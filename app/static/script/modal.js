var modal = document.getElementById("collaboratorModal");
var btn = document.getElementById("collaborator-button");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function () {
  modal.style.display = "block";
}

span.onclick = function () {
  modal.style.display = "none";
}

window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

function confirmCollab(elem) {
  var confirmation = confirm("Confirm collaborator? This will replace/remove the current collaborator on the recipe.");
  if (confirmation) {
    return true;
  } else {
    return false;
  }
}