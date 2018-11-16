//Program a custom submit function for the form
$("form#data").submit(function (event) {

    event.preventDefault();
    
    $("#outputBox").css("display", "none");
   
	var filename = $("#file1").val();
	var extension = filename.replace(/^.*\./, '');
	
	if(extension=="doc" || extension=='docx')
	{
		$("#loader").css("display", "block");
		move();
    var formData = new FormData($(this)[0]);
    var xhttp = new XMLHttpRequest();

    xhttp.onreadystatechange = function () {

        if (this.readyState == 4 && this.status == 200) {
            console.log("Hello")
            var result1 = JSON.parse(this.responseText);
            sessionStorage.setItem("demoSess",result1.Data);
            localStorage.setItem("quentinTarantino",JSON.stringify(result1));
            result=result1.Data[0];
            //alert(result1.Data);

            console.log("Hello world!");
            console.log(result);

            if (result) {
				$('#downCheck').css("display", "block");
                $("#loader").css("display", "none");
                $("#outputBox").css("display", "block");
				 if($("#downCheck").prop('checked') == true){
				$('a.downloadXls').attr('href', "https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT%20Flask/OutputSection/AI%20Sample%20%20duration%20conflict.docx_section.csv?download=1");
			   }else{
				$('a.downloadXls').on("click", function (e) {
					e.preventDefault();
				});
				}
				$("#page_nos").text(result.page_nos);
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
	}else{
	alert("File should be only doc");
	}
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
sessionStorage.setItem("demoSess","default");
$("#outputvalue").change(function (event) {
var str = $('option:selected', this).text();

//alert(str);
var x=sessionStorage.getItem("demoSess");
y=JSON.parse(localStorage.getItem("quentinTarantino"));

//alert("y value "+y.Data.length);
for (var i = 0; i < y.Data.length; i++) {
if(y.Data[i]["Checkvalue"]==str){
    //alert(y.Data[i]["Confidence"]);
    result=y.Data[i]
    if (result) {
				$('#downCheck').css("display", "block");
                $("#loader").css("display", "none");
                $("#outputBox").css("display", "block");
				 if($("#downCheck").prop('checked') == true){
				$('a.downloadXls').attr('href', "https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT%20Flask/OutputSection/AI%20Sample%20%20duration%20conflict.docx_section.csv?download=1");
			   }else{
				$('a.downloadXls').on("click", function (e) {
					e.preventDefault();
				});
				}
                $("#gap").text(result.Gap_outcome);
                $("#requirement").text(result.Response);
                $("#feedback").text(result.Start_End);
                $("#reason").text(result.Reason);

            }
            else {
                alert("Something Went Wrong");
            }
            }

}


})



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