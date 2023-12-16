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
  var inputElem = `<textarea id="about-input" name="about-input" style="height:auto; width:100%; text-align:left; rows="10">${currentAbout}</textarea>`
  aboutElem.innerHTML = inputElem;

  var inputField = document.getElementById('about-input');
  inputField.focus();
  inputField.select();

  inputField.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      var newAbout = inputField.value;
      updateUser(un, newAbout, 'about-me');

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

function confirmDelete(obj, un, recipeId) {
  event.stopPropagation()
  if (confirm('Are you sure you want to delete this recipe?')) {
    deleteRecipe(un, recipeId);
    var recipeNode = obj.parentNode.parentNode
    var container = document.getElementById("recipes-list")
    container.removeChild(recipeNode)
    if (container.children.length === 0) {
      para = '<p class="no-recipes">No current recipes.</p>'
      container.innerHTML = para
    }
  }
}

function deleteRecipe(un, recipeId) {
  $.ajax({
    url: `/u/${un}/${recipeId}/delete-recipe`,
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
