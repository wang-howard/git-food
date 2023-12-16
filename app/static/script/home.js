document.addEventListener("DOMContentLoaded", function () {
  getRecipes(null)
  const searchBox = document.getElementById("search-box")
  searchBox.addEventListener("keyup", function () {
    getRecipes(searchBox.value)
  });
})

function getRecipes(query) {
  if (query == "") {
    query = null
  }
  fetch("search", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "query": query }),
  })
    .then(response => response.json())
    .then(data => {
      if (data.status === "success") {
        const searchDisplay = document.getElementById("search-results")
        searchDisplay.innerHTML = data.data
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}