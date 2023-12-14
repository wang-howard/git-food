function editUsername() {
    var name = prompt("Enter your new display name:", "");
    if (name !== null && name !== "") {
      document.querySelector('.username').textContent = name;


    }
  }
  
  function editAboutMe() {
    var aboutMe = prompt("Enter your new about me:", "");
    if (aboutMe !== null && aboutMe !== "") {
      document.getElementById('about-me-text').textContent = aboutMe;
    }
  }
  