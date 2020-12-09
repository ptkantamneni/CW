// A $( document ).ready() block.
$( document ).ready(function() {
    console.log( "ready!" );

	$("#login-button").click(function(){
		$.ajax({
			'url' : 'http://localhost:5000/login',
			'type' : 'POST',
			'data' : {
			    'numberOfWords' : 10
			},
			'success' : function(data) {              
			    alert('Data: '+data);
			},
			'error' : function(request,error)
			{
			    alert("Request: "+JSON.stringify(request));
			}
		});    
	});

	$("#signup-button").click(function(){
		$.ajax({
			'url' : 'http://localhost:5000/signup',
			'type' : 'POST',
			'data' : {
			    'numberOfWords' : 10
			},
			'success' : function(data) {              
			    alert('Data: '+data);
			},
			'error' : function(request,error)
			{
			    alert("Request: "+JSON.stringify(request));
			}
		});    
	});
});
