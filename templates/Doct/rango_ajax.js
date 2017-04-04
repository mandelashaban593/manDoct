



$(document).ready(function() {

function get_contact(){

       $("#test").submit(function(event){
            $.ajax({
                 type:"POST",
                 url:"/Doct/test/",
                 data: {
                        'fname': $('#fname').val(), // from form
                        'lname': $('#lname').val() // from form

                        },
                 success: function(data){
                     $('#message').html("<h2> Your first Name:</h2>") 

                     setTimeout(function(){get_contact();}, 10000);

                 }
            });
            return false; //<---- move it here
       });


}








function get_contact(){
    var feedback = $.ajax({
        type: "POST",
        url:"/Doct/test/",
        data: {
            'fname': $('#fname').val(), // from form
            'lname': $('#lname').val() // from form

            },
        async: false
    }).success(function(){
        setTimeout(function(){get_contact();}, 10000);
    }).responseText;

    $('div.feedback-box').html(feedback);
}


get_contact();




       $("#converse").submit(function(event){
            $.ajax({
                 type:"POST",
                 url:"/Doct/sendrep/",
                 data: {
                        'telno': $('#telno').val(), // from form
                        'dtelno': $('#dtelno').val(), // from form
                        'dmsg': $('#dmsg').val() // from form

                        },
                 success: function(data){
                     /*$('#message').html("<h2>Contact Form Submitted!</h2>") */
                      $( '#mainsection').html(data);
                 }
            });
            return false; //<---- move it here
       });


  





});