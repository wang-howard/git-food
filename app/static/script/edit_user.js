function editUsername() {
  var usernameElem = document.getElementById('display-name');
  var currentName = usernameElem.innerHTML;
  var inputElem = '<input type="text" id="username-input" value="' + currentName + '">';

  usernameElem.innerHTML = inputElem;

  // Focus on new input and select the text
  var inputField = document.getElementById('username-input');
  inputField.focus();
  inputField.select();

  // Handle when the user presses enter key to save the new name
  inputField.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var newUsername = inputField.value;
      saveNewUsername(newUsername);

      // Set the username to the new value and remove the input box
      usernameElem.innerHTML = newUsername;
      var newUsernameElem = document.createElement('h1');
      newUsernameElem.id = 'display-name';
      newUsernameElem.className = 'username';
      newUsernameElem.innerText = newUsername;
      inputElem.parentNode.replaceChild(newUsernameElem, inputElem);

    }
  });
}

function saveNewUsername(newUsername) {
  $.ajax({
    url: '/edit-display-name',
    method: 'POST',
    data: {
      new_username: newUsername
    },
    success: function (response) {
      if (response.status == 'success') {
        alert('Username updated successfully to ' + response.new_username);
      }
    },
    error: function () {
      alert('An error occurred while updating the username.');
    }
  });
}

function editAboutMe() {
  var aboutMe = prompt("Tell us about yourself:", "");
  if (aboutMe !== null && aboutMe !== "") {
    document.getElementById('about-me-text').textContent = aboutMe;
  }
}
