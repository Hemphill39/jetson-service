var selected_classifier = "";

$("#thumbs-up-btn").click(function () {
	document_id = $("#document-id").val();
	query = $("query-text").val();
	sendDiscoveryFeedback(4, document_id, query);
})

$("#thumbs-down-btn").click(function() {
	document_id = $("#document-id").val();
	query = $("query-text").val();
	sendDiscoveryFeedback(0, document_id, query);
})

function sendDiscoveryFeedback(feedback, document_id, query) {
	data = { 
		feedback : feedback,
		document_id: document_id,
		query: query
	}

	url = "/api/feedback"
	$.ajax({
		type:"POST",
		url: url,
		data: data,
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function(result) {
			showSnackbar("Thank you for your feedback!");
			$("#feedback-container").hide();
		}, error: function(err) {
			showSnackbar("Error sending your feedback");
		}
	});
}

function showSnackbar(message) {
	// Get the snackbar DIV
	var snackbar = document.getElementById("snackbar")

	// Add the "show" class to DIV
	snackbar.className = "show";
	snackbar.textContent = message

	// After 3 seconds, remove the show class from DIV
	setTimeout(function () { snackbar.className = snackbar.className.replace("show", ""); }, 5000);
}

var query = function (queryText, category) {
	var package = {}
	package['queryText'] = queryText;
	package['category'] = category;

	var url = "/api/query";

	$.ajax({
		type: "POST",
		url: url,
		data: JSON.stringify(package),
		dataType: 'json',
		contentType: 'application/json; charset=utf-8',
		success: function (result) {

			var wrapper_object = JSON.parse(result.result);

			if (wrapper_object['error'].length > 0) {
				showSnackbar(wrapper_object['error']);
			} else {
				// If the Watson NLC was able to correctly classify the request, then it will just return html
				if (wrapper_object['html'].length > 0) {
					$("#result").html(wrapper_object['html']);
					$("#category-dropdown-button").hide();
					$("#feedback-container").show();
					$("#document-id").val(wrapper_object['document-id']);
				}

				//Otherwise we need to some logic to populate and show the dropdown box
				//to let the user choose a category for their query
				else {
					$("#category-dropdown-button").show();

					var outstring = "<p>To clarify your results, please pick a category from the box on the right.</p>"
					$("#category-dropdown").empty()
					for (var i = 0; i < wrapper_object['categories'].length; i++) {
						category = wrapper_object['categories'][i]
						$("#category-dropdown").append('<a class="dropdown-item" href="#">' + category + '</a>');
					}
					$("#result").html(outstring);
				}

				$("#result-container").show();
			}
			$("#query-text").removeAttr("disabled");
		},
		error: function (XMLHttpRequest, textStatus, errorThrown) {
			$("#query-text").removeAttr("disabled");
			showSnackbar('Error while searching for request');
		}
	});
}

$(document).ready(function () {

	$("#category-dropdown-button").hide();

	$("#submit-search").click(function () {
		var queryText = $('#query-text').val();
		var category = selected_classifier;

		$("#query-text").attr("disabled", "disabled");

		query(queryText, category);

	});

	$('#query-text').keypress(function (e) {
		if (e.which == 13) {//Enter key pressed
			$('#submit-search').click();//Trigger search button click event
		}
	});

	//Need to set this super basic function to track which value of the dropdown was last selected
	//this will let the parent of the list objects (really <a> elements) delegate the function
	//which we need since the <a>'s are dynamically generated.
	$("#category-dropdown").on('click', 'a', function (event) {
		selected_classifier = $(this).text();
		var queryText = $("#query-text").val();
		query(queryText, selected_classifier);
		selected_classifier = "";
	});

});
