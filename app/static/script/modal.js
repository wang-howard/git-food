var modal = document.getElementById("collaboratorModal");
var btn = document.getElementById("add-collaborator-button");
var span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
  modal.style.display = "block";
}

span.onclick = function() {
  modal.style.display = "none";
}

window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}

var searchBtn = document.getElementById("searchCollaborator");
searchBtn.onclick = function() {
  var username = document.getElementById("collaboratorUsername").value;
  console.log("Searching for user:", username);
  // Add your AJAX call or form submission logic here
}
