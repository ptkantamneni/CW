// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );

	$("#login-button").click(function(){
		var payload = { "username": $("#email-login").val(),
				"password": $("#password-login").val() }	

		console.log(JSON.stringify(payload));

		$.ajax({
			'url' : 'http://localhost:5000/login',
			'type' : 'POST',
			 contentType: 'application/json',
			'data' : JSON.stringify(payload),
			'success' : function(data, code, xhr) {              
			    console.log('Data: '+ data);
		            console.log("cookie: " + JSON.stringify(code));
			},
			'error' : function(request,error)
			{
			    alert("Request: "+JSON.stringify(request));
			}
		});    
	});

	$("#signup-button").click(function(){

		var payload = { "firstName":  $("#first_name").val(), 
				"lastName":   $("#last_name").val(),
				"age": $("#age").val(),
				"address": $("#address").val(),
				"email": $("#email").val(),
				"password": $("#password").val() }	


		console.log(JSON.stringify(payload));

		$.ajax({
			'url' : 'http://localhost:5000/signup',
			'type' : 'POST',
			 contentType: 'application/json',
			'data': JSON.stringify(payload),
			'success' : function(data) {              
				console.log("data" + JSON.stringify(data));
			},
			'error' : function(request,error)
			{
			    alert("Request: "+JSON.stringify(request));
			}
		});    
	});
});
