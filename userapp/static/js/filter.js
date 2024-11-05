$(document).ready(function() {
    var table1 = $('#example2').DataTable();
    $('#id_company_type').change(function() {
        var keyword1 = $("#id_company_type").val().join(' ')
        console.log(keyword1)
        table1.column(2).search(keyword1).draw();
    });
    $('#id_product').change(function() {
        var keyword1 = $("#id_product").val().join(' ')
        console.log(keyword1)
        table1.column(7).search(keyword1).draw();
    });
    $('#id_trader').change(function() {
        var keyword1 = $("#id_trader").val()
        console.log(keyword1)
        table1.column(3).search(keyword1).draw();
    });
    $('#id_payment').change(function() {
        var keyword1 = $("#id_payment").val().join(' ')
        console.log(keyword1)
        table1.column(8).search(keyword1).draw();
    });
    $('#id_issuing_bank').change(function() {
        var keyword1 = $("#id_issuing_bank").val().join(' ')
        console.log(keyword1)
        table1.column(9).search(keyword1).draw();
    });
    $('#id_receiving_bank').change(function() {
        var keyword1 = $("#id_receiving_bank").val().join(' ')
        console.log(keyword1)
        table1.column(10).search(keyword1).draw();
    });
    $('#id_tt_bank').change(function() {
        var keyword1 = $("#id_tt_bank").val().join(' ')
        console.log(keyword1)
        table1.column(11).search(keyword1).draw();
    });
    $('#id_country').change(function() {
        var keyword1 = $("#id_country").val()
        console.log(keyword1)
        table1.column(14).search(keyword1).draw();
    });

});

function showinvi() {
  var x = document.getElementById("invisiblediv");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}