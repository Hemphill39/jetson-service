var selected_classifier = "";

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

			// If the Watson NLC was able to correctly classify the request, then it will just return html
			if (wrapper_object['error'].length > 0) {
				showSnackbar(wrapper_object['error']);
			} else {
				if (wrapper_object['html'].length > 0) {
					for (var i = 1; i < wrapper_object['html'].length + 1; i++) {
						var s = '#result' + i;
						$(s).html(wrapper_object['html'][i - 1]);
					}
					//$("#result1").html(wrapper_object['html']);
					$("#category-dropdown-button").hide();
					$("#response").hide();
					$(" #accordion").show();
				}
				//Otherwise we need to some logic to populate and show the dropdown box
				//to let the user choose a category for their query
				else {
					$("#category-dropdown-button").show();
					$("#response").show();
					$("#accordion").hide();

					var outstring = "<p>To clarify your results, please pick a category from the box on the right.</p>"
					$("#category-dropdown").empty()
					for (var i = 0; i < wrapper_object['categories'].length; i++) {
						category = wrapper_object['categories'][i]
						$("#category-dropdown").append('<a class="dropdown-item" href="#">' + category + '</a>');
					}
					$("#result0").html(outstring);
				}
			}

			$("#result-container").show();
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
	$("#response").hide();
	$("#submit-search").click(function () {
		console.log('Search Sent with classifier ' + selected_classifier);

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
