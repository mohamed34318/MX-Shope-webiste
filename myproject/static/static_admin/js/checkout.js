$("#checkout").click(function () {
  var namecard = $("#namecard").val();
  var cardnum = $("#cardnum").val();
  var date = $("#date").val();
  var cvv = $("#cvv").val();
  if (namecard != " " || cardnum != " " || date != " " || cvv != " ") {
    swal({
      title: "Good job!",
      text: "order is submited",
      icon: "success",
      button: "ok",
    });
  } else {
    swal({
      title: "missing values",
      text: "check missing fields",
      icon: "error",
      button: "ok",
    });
  }

}
)