function editUsername() {
  var name = prompt("New display name:", "");
  if (name !== null && name !== "") {
    document.querySelector('.username').textContent = name;


  }
}

function editAboutMe() {
  var aboutMe = prompt("Tell us about yourself:", "");
  if (aboutMe !== null && aboutMe !== "") {
    document.getElementById('about-me-text').textContent = aboutMe;
  }
}
