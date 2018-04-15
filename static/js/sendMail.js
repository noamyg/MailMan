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