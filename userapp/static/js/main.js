$(document).ready(function() {
    console.log('yolo')
    $('#id_product').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%',
    });
    $('#id_company_type').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%'
    });
    $('#id_payment').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%'
    });
    $('#id_issuing_bank').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%',
        onChange: function(option, checked) {
            var selectID = $(option).parent().attr('id');
        }
    });
    $('#id_receiving_bank').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%'
    });
    $('#id_tt_bank').multiselect({
        includeSelectAllOption: true,
        buttonWidth: '100%'
    });

    $('#id_product').prop("required", false);
    $('#id_company_type').prop("required", false);
    $('#id_payment').prop("required", false);
    $('#id_issuing_bank').prop("required", false);
    $('#id_receiving_bank').prop("required", false);
    $('#id_tt_bank').prop("required", false);


    $('#example').DataTable();

});

function confirm_delete_file(){
    var r = confirm("Do you really want to delete?");
    if (r == true) {
        window.location = this.event.target.dataset.href;
    }
}

function confirm_delete_user(){
    var r = confirm("Do you really want to delete this user?");
    if (r == true) {
        window.location = this.event.target.dataset.href;
    }
}

function confirm_delete_company(){
    var r = confirm("Do you really want to delete this record?");
    if (r == true) {
        window.location = this.event.target.dataset.href;
    }
}

function check_disabled(){
    console.log('I did working oo')
    document.getElementById("id_counterparty_onboard_status").disabled = false;
    document.getElementById("id_serenity_onboard_status").disabled = false;
    console.log('I have done and everything work!!')
}


