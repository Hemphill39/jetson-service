var selected_classifier = ""

$( document ).ready(function() {

	$( "#category-dropdown-button" ).hide();

	$("#submit-search").click(function(){
	    console.log('Search Sent with classifier ' + selected_classifier);

	    var package_to_send = {}
	    package_to_send['queryText'] = $('#query-text').val();
	    package_to_send['category'] = selected_classifier;

	    var url = "/api/query/" + JSON.stringify(package_to_send);
	    $("#query-text").attr("disabled", "disabled");
	    $.ajax({url: url, success: function(result){

	    	var wrapper_object = JSON.parse(result.result);

	    	// If the Watson NLC was able to correctly classify the request, then it will just return html
	    	if (wrapper_object['html'].length > 0){
		    	$("#result").html(wrapper_object['html']);
		    	$( "#category-dropdown-button" ).hide();
	    	}

	    	//Otherwise we need to some logic to populate and show the dropdown box
	    	//to let the user choose a category for their query
	    	else{
	    		$( "#category-dropdown-button" ).show();

	    		var outstring = "<p>To clarify your results, please pick a category from the box on the right.</p>"
	    		$( "#category-dropdown" ).empty()
	    		for (var i = 0; i < wrapper_object['categories'].length; i++){
	    			category = wrapper_object['categories'][i]
	    			$( "#category-dropdown" ).append( '<a class="dropdown-item" href="#">' + category + '</a>');
	    		}
	    		$("#result").html(outstring);
	    	}




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

	//Need to set this super basic function to track which value of the dropdown was last selected
	//this will let the parent of the list objects (really <a> elements) delegate the function
	//which we need since the <a>'s are dynamically generated.
	$("#category-dropdown").on('click', 'a', function(event) {
	    selected_classifier = $(this).text();
	    console.log(selected_classifier)
	    console.log("yo")
	});

});
