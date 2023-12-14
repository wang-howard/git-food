function editUsername(un) {
  var displayName = document.getElementById('display-name');
  var currentName = displayName.textContent.trim();
  var inputElem = `<input type="text" class="user-text" id="username-input" value="${currentName}" size="${currentName.length}" style="width: auto;">`;

  displayName.innerHTML = inputElem;

  // Focus on new input and select the text
  var inputField = document.getElementById('username-input');
  inputField.focus();
  inputField.select();

  // Handle when the user presses enter key to save the new name
  inputField.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var newDisplayName = inputField.value;
      updateUser(un, newDisplayName, 'display-name');

      // Set the username to the new value and remove the input box
      displayName.innerHTML = newDisplayName;
    }
  });
}

function editAboutMe(un) {
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
      updateUser(un, newAbout, 'about-me');

      // Set the username to the new value and remove the input box
      aboutElem.innerHTML = newAbout;
    }
  });
}

function updateUser(un, data, item) {
  $.ajax({
    url: `/u/${un}/edit-user`,
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
    error: function (response) {
      alert('An error occurred while making the change. ' + response.message);
    }
  });
}

function confirmDelete(un, recipeId) {
  event.stopPropagation()
  if (confirm('Are you sure you want to delete this recipe?')) {
    deleteRecipe(un, recipeId);
  }
}

function deleteRecipe(un, recipeId) {
  $.ajax({
    url: `/u/${un}/delete-recipe/${recipeId}`,
    method: 'POST',
    data: {
      recipe_id: recipeId,
    },
    success: function (response) {
      if (response.status == 'success') {
        alert('Recipe deleted.');
      }
    },
    error: function (response) {
      alert('An error occurred while making the change. ' + response.message);
    }
  });
}
