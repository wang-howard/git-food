$(document).ready(function () {
  $('#search-box').keyup(function () {
    var query = $(this).val();
    getRecipes(query)
  });
});

function getRecipes(query) {
  if (query != "") {
    $.ajax({
      url: "/search",
      method: "POST",
      data: { query: query },
      success: function (data) {
        $('#search-results').html(data);
      }
    });
  } else {
    $.ajax({
      url: "/search",
      method: "POST",
      data: { query: None },
      success: function (data) {
        $('#search-results').html(data);
      }
    });
  }
}
