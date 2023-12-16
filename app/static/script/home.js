document.addEventListener('DOMContentLoaded', getRecipes(null));

const searchBox = document.getElementById("search-box")
searchBox.addEventListener("keyup", getRecipes(searchBox.val()))

function getRecipes(query) {
  if (query == "") {
    query = null
  }
  fetch("search", {
    method: 'POST',
    body: JSON.stringify({ "query": query }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === 'success') {
        const searchDisplay = document.getElementById("search-results")
        searchDisplay.innerHTML = data
      } else {
        alert(data.message);  // Show error message from server
      }
    })
    .catch((error) => {
      console.error('Error:', error);
    });
}