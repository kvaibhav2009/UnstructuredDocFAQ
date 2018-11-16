//Program a custom submit function for the form
$("form#data").submit(function (event) {

    event.preventDefault();

    $("#outputBox").css("display", "none");

	var filename = $("#file1").val();
	var extension = filename.replace(/^.*\./, '');

	if(extension=='docx'|| extension=="DOCX" || extension=="doc" || extension=="DOC")
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
				$('#downCheck').css("display", "inline-block");
                $("#loader").css("display", "none");
                $("#outputBox").css("display", "block");
				 if($("#downCheck").prop('checked') == true){
				$('a.downloadXls').attr('href',encodeURI (result1.Path));
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
                html="";
                for(i=0;i<result.Clause.length;i++)
                {
                    //alert("Clause length");
                    //alert(result.Clause.length);
                    //alert("Clause ");
                    //alert(result.Clause[i])
                    if(result.Clause[i].page_no=='--')
                    {
                        passage=result.Clause[i].passage;
                        substring=result.Clause[i].Entity_Substring;
                        var Entity=result.Clause[i].Entity;
                        //alert(str(result.Checkvalue))
                        //var formatted_passage= boldStringduplex(passage,substring);
                        if(result.Checkvalue=="Benchmarking")
                        {
                            var formatted_passage= boldString(passage,substring);
                        }
                        else
                        {
                            var formatted_passage= boldStringduplex(passage,substring);
                        }

                        html+="<span> <b><span> For "+Entity+" </b> </span> </span><br/> </br><span> "+formatted_passage+"</span><br><br>"
                    }
                    else
                    {
                        passage=result.Clause[i].passage
                        substring=result.Clause[i].Entity_Substring
                        //alert(result.Clause[i].Entity)
                        var Entity=result.Clause[i].Entity
                        var page_no=result.Clause[i].page_no
                        var section_no=result.Clause[i].section_no
                        //alert('Clause ')
                        //alert(str(result.Checkvalue))
                        //var formatted_passage= (boldStringduplex(passage,substring))
                        //var formatted_passage= boldString(passage,substring);
                        if(result.Checkvalue=="Benchmarking")
                        {

                        var formatted_passage= (boldString(passage,substring))
                        }
                        else
                        {
                        var formatted_passage= (boldStringduplex(passage,substring))
                        }


                        //alert("formatted_passage "+formatted_passage);
                        html+="<span> <b><span> For "+Entity+", Page "+page_no+" & Section "+section_no+"</span> of SOW states that:</b></span> <br/></br><span > "+formatted_passage+"</span><br><br>";
                    }

                }
                 $("#pageresponse").html(html);

            }
            else {
                alert("Something Went Wrong");
            }

        }
    };
    xhttp.open("POST", 'http://127.0.0.1:4998/router', true);
    xhttp.send(formData);
	}else{
	alert("File should be only docx");
	}
});

function boldString(str, find){
    var arr=find.split('ooo')
    //alert("Splited array ")
    //alert((arr))
    //for(i=0;i<arr.length;i++)
    {
    find=arr[0]
    //alert("Find "+find)
    var re = new RegExp(find, 'g');
    if(find != '')
    str=str.replace(find, ' <b><u>'+find+'</u></b> ');

    //alert(str)
    }
    return str;


}


function boldString1(str, find)
{
    var arr=find.split('ooo')
    for(i=0;i<arr.length;i++)
    {
    find=arr[i]
    find='12) month'
    alert('Find '+find)
    str='Each partys liability  whether in contract  tort  or any other theory of liability  arising out of \r or in connection with this Agreement  shall not exceed the lesser of: (a) 300 % of the total \r amount paid and/or payable to Supplier by XYZ under this Agreement during the twelve \r (12) month preceding the event giving rise to the claim  or (b) ($total contract value).  \r "\r "Each partys liability  whether in contract  tort  or any other theory of liability  arising out of or in connection with this Agreement  shall not exceed the lesser of: (a) 300 % of the total amount paid and/or payable to Supplier by XYZ under this Agreement during the twelve (12) month preceding the event giving rise to the claim  or (b) ($total contract value)..'
    alert('str '+str)
    //var re = new RegExp(find, 'g');
    str=str.replace(find, ' <b><u>'+find+'</u></b> ');
    alert(str)
    }
    return str;


}


function boldStringduplex(str, find){

    var arr=find.split('ooo')
    //alert("passage"+str);
    //alert("find"+find);
    //alert("Array");
    //alert(arr);
    var textdec='textdec'

    for(j=0;j<arr.length;j++)
    {
    //if(arr[i]!='')
        {
        //alert(arr[j]);
        //var re = new RegExp("18) month", 'g');
        str=str.replace(arr[j],' <b><u>'+arr[j]+'</u></b> ');// '<span class='''+textdec+''' >'+arr[i]+'</span>');
        //str=str.replace(arr[i], "<span class='textdec' >'+arr[i]+'</span>");
        //alert(j+"  "+str);
        }

    }
    //alert("last"+str);
    return str;
}

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
				$('#downCheck').css("display", "inline-block");
                $("#loader").css("display", "none");
                $("#outputBox").css("display", "block");
				 if($("#downCheck").prop('checked') == true){
				$('a.downloadXls').attr('href', "https://13.232.229.71/user/vaibhav.vijay.kotwal/files/CDAT_Flask/OutputSection/AI%20Sample%20%20duration%20conflict.docx_section.csv?download=1");
			   }else{
				$('a.downloadXls').on("click", function (e) {
					e.preventDefault();
				});
				}
                $("#gap").text(result.Gap_outcome);
                $("#requirement").text(result.Response);
                $("#feedback").text(result.Start_End);
                $("#reason").text(result.Reason);

                html="";
                for(i=0;i<result.Clause.length;i++)
                {
                    if(result.Clause[i].page_no=='--' || result.Clause[i].section_no=='--')
                    {
                        passage=result.Clause[i].passage;
                        substring=result.Clause[i].Entity_Substring;
                        var Entity=result.Clause[i].Entity;

                        if(result.Checkvalue=="Benchmarking")
                        {

                        var formatted_passage= (boldString(passage,substring))
                        }
                        else
                        {
                        var formatted_passage= (boldStringduplex(passage,substring))
                        }


                        //alert("formatted_passage "+formatted_passage);

                        html+="<span> <b><span> For "+Entity+" </b> </span> </span><br/> </br><span> "+formatted_passage+"</span><br><br>"
                    }
                    else
                    {
                        passage=result.Clause[i].passage;
                        substring=result.Clause[i].Entity_Substring;
                        //alert(result.Clause[i].Entity)
                        var Entity=result.Clause[i].Entity;
                        var page_no=result.Clause[i].page_no;
                        var section_no=result.Clause[i].section_no;

                        if(result.Checkvalue=="Benchmarking")
                        {

                        var formatted_passage= (boldString(passage,substring))
                        }
                        else
                        {
                        var formatted_passage= (boldStringduplex(passage,substring))
                        }


                        //alert("formatted_passage "+formatted_passage);

                        html+="<span> <b><span> For "+Entity+", Page "+page_no+" & Section "+section_no+"</span> of SOW states that:</b></span> <br/></br><span > "+formatted_passage+"</span><br><br>";
                   }

                }
                 $("#pageresponse").html(html);


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


$(document).ready(function () {
    $('#downCheck').click(function () {
        if (this.checked){
            $('#downloadbtn').css("display","block");
        }
        else
            $('#downloadbtn').css("display","none");
        });
    });