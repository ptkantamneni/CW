// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );


	$("#reset-values-event-modal").click(function(){
		console.log("reset called.");
		$("#event-name").val('');
		$("#event-address").val('');
		$("#event-attendee-count").val('');
		$("#social-distance-rating").val('');
		$("#mask-compliance-rating").val('');
		$("#check-in-date").val('');
		$("#check-out-date").val('');
		$("#open-space").val('');
		$("#update-date").val('');

	});				

	$("#reset-values-test-result-modal").click(function(){
		console.log("reset2` called.");
		$("#test-result-in-modal").val('');
		$("#test-date-in-modal").val('');
	});



	$("#save-event-btn").click(function(){
		var payload = { "placeName" : $("#event-name").val(),
		                "address" : $("#event-address").val(),
		                "checkInDate" : $("#event-attendee-count").val(),
		                "checkOutDate": $("#social-distance-rating").val(),
		                "maskComplianceRating":   $("#mask-compliance-rating").val(),
				"socialDistanceRating": $("#social-distance-rating").val(),
				"checkInDate": $("#check-in-date").val(),
				"checkOutDate": $("#check-out-date").val(),
				"openSpace": $("#open-space").val(),
                                "numPeople": $("#event-attendee-count").val(),
				"updatedDate": $("#updated-date").val() }				


		console.log(JSON.stringify(payload));

		$.ajax({
			'url' : 'http://localhost:5000/event/create_event',
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


	$("#save-test-result-btn").click(function(){
		var payload = { "testResult":  $("#test-result-in-modal").val(), 
				"testDate":   $("#test-date-in-modal").val()}

		console.log(JSON.stringify(payload));

		$.ajax({
			'url' : 'http://localhost:5000/user/addTestResult',
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
			    console.log('Log in Data: '+ data);
		            console.log("Log in cookie: " + JSON.stringify(code));
				 $.ajax({
				'url' : 'http://localhost:5000/user_info',
				'type' : 'GET',
				 contentType: 'application/json',
				'data' : JSON.stringify(payload),
				'success' : function(data, code, xhr) {              
				    console.log('User Info Data: '+ JSON.stringify(data));
				    window.location.replace("http://localhost:5000/render-home");	
				},
				'error' : function(request,error)
				{
				    console.log("User Info Request: "+JSON.stringify(request));
				}
				});    
			},
			'error' : function(request,error)
			{
			    alert("Log in Request: "+JSON.stringify(request));
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
