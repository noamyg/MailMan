function sendMailToCreator(){
    var $submitButton = $('#submit');
    $submitButton.addClass('disabled');
    $submitButton.html('<i class="fa fa-space-shuttle faa-passing animated"></i>')
    $.ajax({
        url: 'sendMail',
        type: 'post',
        contentType: 'application/json; charset=utf-8',
        success: function (data){
            $submitButton.removeClass('btn-primary').addClass('btn-success');
            $submitButton.html('<i class="fa fa-check animated"></i>')
        },
        data: JSON.stringify(
            {
                "t" : "sendMessageToCreator",
                "to" : $('#to').val(),
                "cc" : $('#cc').val(),
                "bcc" : $('#bcc').val(),
                "sp" : {},
                "bp" : {
                    "YourName" : $('#name').val(),
                    "PhoneNumber" : $('#phone').val(),
                    "Liked" : $('#like').val(),
                    "Notes" : $('#notes').val()
                }
            }
        )
    });
};

function uploadTemplate(){
    var form = $('form')[0];
    var formData = new FormData(form);
    $.ajax({
        url: 'templateUploader',
        type: 'post',
        processData: false,
        contentType: false,
        data: formData
    })
    .success(function (data) {
        toastr.success("Template successfully uploaded");
        location.reload();
    })
    .fail(function (error) {
        toastr.clear();
        toastr.error("Error occurred: " + error.responseText);
    });
    return false;
};