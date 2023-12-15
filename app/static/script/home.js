$(document).ready(function () {
  $('#search-box').keyup(function () {
    var query = $(this).val();
    if (query != '') {
      $.ajax({
        url: "/search",
        method: "POST",
        data: { query: query },
        success: function (data) {
          $('#results').html(data);
        }
      });
    } else {
      $('#results').html('');
    }
  });
});
