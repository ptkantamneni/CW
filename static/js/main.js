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

  $("#reset-values-relationship-modal").click(function(){
    console.log("reset relationship called.");
    $("#relationship-email-in-modal").val('');
    $("#relationship-type-in-modal").val('');
  });

  	setInterval(function() {
		 $.ajax({
			'url' : 'http://localhost:5000/user_info',
			'type' : 'GET',
			 contentType: 'application/json',
			'success' : function(data, code, xhr) {              
			    console.log('User Info Data: '+ JSON.stringify(data));
			    var msg = data["message"]
			    var name = msg["name"]
			    $("#user-name").text("Name: " + name);
			    $("#user-age").text("Age: " + msg["age"]);
			    $("#user-email").text("Email: " + msg["email"]);
			    
			    var score = msg["riskScore"];
			    var severityRank = "";
			    if(score == 5){
			    	severityRank = "Covid positive"
			    }
			    else if(score >=4){
			    	severityRank = "High risk"
			    }
			    else if(score >=3){
			    	severityRank = "Moderate risk"
			    }
			    else if(score >=2){
			    	severityRank = "Low risk"
			    }
			    else{
			    	severityRank = "Very low risk"
			    }

		    	$("#user-risk-score").text("Risk Score: " + msg["riskScore"] + ": " + severityRank);
			    if( msg["testResult"] !== null){
			    	$("#user-test-result").text("Test Result: " + msg["testResult"]);
			    	$("#user-test-date").text("Test Date: " + msg["testDate"]);
			    }
			    
			},
			'error' : function(request,error)
			{
			    console.log("User Info Request: "+JSON.stringify(request));
			}
			}); 
	}, 2000);

	setInterval(function() {
		 $.ajax({
			'url' : 'http://localhost:5000/event/get_event',
			'type' : 'GET',
			 contentType: 'application/json',
			'success' : function(data, code, xhr) {              
			    console.log('User Event Data: '+ JSON.stringify(data));
		    	$("#user-events").empty();
			    $.each(data, function(i, event){
			    	// $("#user-events").append('<li>Event: ' + event["placeName"] + '<br>' + "\n Risk Score: " + event["riskScore"] + '</li>');

			    	$("#user-events").append('<li>Event: ' + event["placeName"] + '<br>');
			    	$("#user-events").append('Risk Score: ' + event["riskScore"] + '<br>');
			    	$("#user-events").append('Address: ' + event["address"] + '<br>');
			    	$("#user-events").append('Confirmed Cases: ' + event["confirmedCases"] + '<br>');
			    	$("#user-events").append('Open Space: ' + event["openSpace"] + '<br>');
			    	$("#user-events").append('Number of people rating: ' + event["numPeople"] + '<br>')
			    	$("#user-events").append('Social Distance Rating: ' + event["socialDistancing"] + '<br>');
			    	$("#user-events").append('Mask Compliance Rating: ' + event["maskComplianceRating"] + '<br>');
			    	$("#user-events").append('Check In Date: ' + event["checkInDate"] + '<br>');
			    	$("#user-events").append('Check Out Date: ' + event["checkOutDate"] + '<br>');
			    	$("#user-events").append('<b>');
			    	$("#user-events").append('<b>');
			    	$("#user-events").append('</li>');

			    	// $("#user-events").append("Event Name: " + event["placeName"] + "\n");
			    });
			},
			'error' : function(request,error)
			{
			    console.log("User Info Request: "+JSON.stringify(request));
			}
			}); 
	}, 2000);


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
				location.reload(true)
				console.log("data" + JSON.stringify(data));
			},
			'error' : function(request,error)
			{
			    alert("Request: "+JSON.stringify(request));
			}
		});
	});

  $("#save-relationship-btn").click(function(){
    var payload = { "friendEmail":  $("#relationship-email-in-modal").val(),
        "relationshipType":   $("#relationship-type-in-modal").val()}

    console.log(JSON.stringify(payload));

    $.ajax({
      'url' : 'http://localhost:5000/relationship/addRelationship',
      'type' : 'POST',
       contentType: 'application/json',
      'data': JSON.stringify(payload),
      'success' : function(data) {
        console.log("data" + JSON.stringify(data));
        window.location.replace("http://localhost:5000/render-home");
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
				location.reload(true)
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
