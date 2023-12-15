// Get the modal
var modal = document.getElementById("collaboratorModal");

// Get the button that opens the modal
var btn = document.getElementById("add-collaborator-button");

// Get the elements that close the modal
var span = document.getElementsByClassName("close")[0];
var cancelInvite = document.getElementById("cancelInvite");

// When the user clicks on the button, open the modal 
btn.onclick = function() {
  modal.style.display = "block";
}

// When the user clicks on <span> (x), close the modal
span.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks on "No, Cancel", close the modal
cancelInvite.onclick = function() {
  modal.style.display = "none";
}

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == modal) {
    modal.style.display = "none";
  }
}