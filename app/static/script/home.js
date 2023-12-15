$(document).ready(function () {
  $('#search-box').keyup(function () {
    var query = $(this).val();
    getRecipes(query)
  });
});

function getRecipes(query) {
  if (query == "") {
    query = null
  }
  $.ajax({
    url: "/search",
    method: "POST",
    data: { query: query },
    success: function (data) {
      searchDisplay = document.getElementById("search-results")
      searchDisplay.innerHTML = data
    }
  });
}
