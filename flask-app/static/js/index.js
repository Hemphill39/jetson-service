$( document ).ready(function() {
	$("#submit-search").click(function(){
	    console.log('Search Sent');
	    var queryText = $('#query-text').val();
	    var url = "/api/query/" + queryText;
	    $("#query-text").attr("disabled", "disabled");
	    $.ajax({url: url, success: function(result){
	        $("#result").html(result.result);
	        $("#result-container").show();
	        $("#query-text").removeAttr("disabled"); 
	    },
	      	error: function(XMLHttpRequest, textStatus, errorThrown) { 
        		alert("Status: " + textStatus); alert("Error: " + errorThrown); 
        		$("#query-text").removeAttr("disabled"); 
    	}});
	});

	$('#query-text').keypress(function(e){
	    if(e.which == 13){//Enter key pressed
	        $('#submit-search').click();//Trigger search button click event
	    }
	});
});