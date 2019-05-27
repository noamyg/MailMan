function addNewRow(){
    var newRow = $('<tr class="row">');
    var cols = "";
    cols += '<td class="col-1"></td>'
    cols += '<td class="col-3"><select required class="form-control" id="featuresTableFeatureOrBug"><option selected value="">Choose</option><option value="Bug">Bug</option><option value="Feature">Feature</option></select></td>';
    cols += '<td class="col-4"><input required type="text" name="featuresTableSubject" class="form-control" /></td>';
    cols += '<td class="col-4"><input type="text" name="featuresTableDescription"  class="form-control"/></td>';
    cols += '<td class="col-1"><a href="javascript:void(0);" onclick="removeRow(this)" style="color: red;"><span class="glyphicon glyphicon-remove"/></a></td>';
    newRow.append(cols);
    $("#featureRequests").append(newRow);
};

function removeRow(element){
    $(element).closest("tr").remove();
};

function sendMailToCreator(submitButton){
    var $submitButton = $(submitButton);
    $submitButton.addClass('disabled');
    $submitButton.html('<i class="fa fa-space-shuttle faa-passing animated"></i>');
    var featureRequests = $('#featureRequests').tableToJSON({
      onlyColumns: [1,2,3],
      ignoreEmptyRows: true,
      extractor: function(cellIndex, $cell) {
        return $cell.find('input,select').val();
      }
    });
    var data = JSON.stringify(
        {
            "t" : "sendMessageToCreator",
            "to" : $('#to').val(),
            "cc" : $('#cc').val(),
            "bcc" : $('#bcc').val(),
            "sp" : {
                "YourName" : $('#name').val()
            },
            "bp" : {
                "YourName" : $('#name').val(),
                "PhoneNumber" : $('#phone').val(),
                "Liked" : $('#like').val(),
                "Notes" : $('#notes').val(),
                "FeatureRequests" : featureRequests
            }
        }
    );
    $.ajax({
        url: 'sendMail',
        type: 'post',
        contentType: 'application/json; charset=utf-8',
        success: function (data){
            $submitButton.removeClass('btn-primary').addClass('btn-success');
            $submitButton.html('<i class="fa fa-check animated"></i>')
        },
        data: data
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