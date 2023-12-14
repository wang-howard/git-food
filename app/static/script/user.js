function editUsername() {
  var usernameElem = document.getElementById('display-name');
  var currentName = usernameElem.textContent.trim();
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
      updateUser(newUsername, 'display-name');

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

function editAboutMe() {
  var aboutElem = document.getElementById('about-me-text');
  var currentAbout = aboutElem.textContent.trim();
  var inputElem = '<input type="text" id="about-input" style="height:auto; width:100%; text-align:left;" value="' + currentAbout + '">';

  aboutElem.innerHTML = inputElem;

  // Focus on new input and select the text
  var inputField = document.getElementById('about-input');
  inputField.focus();
  inputField.select();

  // Handle when the user presses enter key to save the new name
  inputField.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var newAbout = inputField.value;
      updateUser(newAbout, 'about-me');

      // Set the username to the new value and remove the input box
      aboutElem.innerHTML = newAbout;
      var newAboutElem = document.createElement('div');
      newUsernameElem.id = 'about-me-text';
      newUsernameElem.innerText = newAbout;
      inputElem.parentNode.replaceChild(newAboutElem, inputElem);
    }
  });
}

function updateUser(data, item) {
  $.ajax({
    url: '/edit-user',
    method: 'POST',
    data: {
      new_data: data,
      item_changed: item,
    },
    success: function (response) {
      if (response.status == 'success') {
        alert('Update successful.');
      }
    },
    error: function () {
      alert('An error occurred while making the change. ' + response.message);
    }
  });
}

function confirmDelete(recipeId) {
  event.stopPropagation();
  if (confirm('Are you sure you want to delete this recipe?')) {
    deleteRecipe(recipeId);
  }
}

function deleteRecipe(recipeId) {
  fetch(`/u/${current_user.username}/delete_recipe/${recipeId}`, {
    method: 'POST',
    credentials: 'include' // Necessary for including session cookie in request
  })
  .then(response => {
    if (!response.ok) { throw response; }
    return response.json();
  })
  .then(data => {
    if (data.status === 'success') {
      // Remove the recipe element from the DOM or refresh the page
      location.reload();
    } else {
      alert('Error deleting recipe: ' + data.message);
    }
  })
  .catch((error) => {
    // If the response is not OK and it's not a JSON, it'll fail here
    alert('An error occurred while attempting to delete the recipe.');
  });
}
