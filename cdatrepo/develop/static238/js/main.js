//Program a custom submit function for the form
$("form#data").submit(function (event) {

    event.preventDefault();
    $("#loader").css("display", "block");
    $("#outputBox").css("display", "none");
    move();

    var formData = new FormData($(this)[0]);
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {

        if (this.readyState == 4 && this.status == 200) {

            var result = JSON.parse(this.responseText);

            if (result) {
                $("#loader").css("display", "none");
                $("#outputBox").css("display", "block");
                $("#gap").text(result.Gap_outcome);
                $("#requirement").text(result.Response);
                $("#feedback").text(result.Start_End);
                $("#reason").text(result.Reason);
            }
            else {
                alert("Something Went Wrong");
            }

        }
    };
    xhttp.open("POST", 'http://127.0.0.1:5000/router', true);
    xhttp.send(formData);
});

function move() {
    var elem = document.getElementById("myBar");
    var width = 1;
    var id = setInterval(frame, 10);
    function frame() {
        if (width >= 100) {
            clearInterval(id);
        } else {
            width++;
            elem.style.width = width + '%';
        }
    }
};

$(document).ready(function () {

    $("#loader").css("display", "none");

    $('.dropdown-menu input[type="checkbox"]').on('click', function () {
        var title = $(this).closest('.dropdown-menu').find('input[type="checkbox"]').val(),
            title = $(this).val() + ",";
        if ($(this).is(':checked')) {
            var str = $('#btntxt').text();
            var res = str.replace("Please select from the list", "");
            $('#btntxt').text(res);
            $('.multiSel').append(title);
            $(".hida").hide();
        } else {
			if ($(".dropdown-menu input:checkbox:checked").length > 0)
					{
						$('.dropdown-menu input:checked').each(function() {
						   $('#btntxt').text(this.value);
						});
						
					}
					else{
					$('#btntxt').text("Please select from the list");
					}
            
        }
    });
});