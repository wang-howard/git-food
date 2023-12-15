function confirmRestoreVersion(username, recipeId) {
    var confirmRestore = confirm("Are you sure you want to restore this version? This will delete all newer versions.");
    if (confirmRestore) {
      fetch(`/u/${username}/${recipeId}/restore`, {
        method: 'POST',
        body: JSON.stringify({ 'recipe_id': recipeId }),
      })
      .then(response => response.json())
      .then(data => {
        if (data.status === 'success') {
          window.location.href = `/u/${username}`;  // Redirect to profile or updated recipe view
        } else {
          alert(data.message);  // Show error message from server
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
    }
  }