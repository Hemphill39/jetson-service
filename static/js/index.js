$(document).ready(function() {
	var selected_classifier = "";
	
	$(".thumbs-up").click(function () {
		var resultTag = this.id[this.id.length - 1];
		var document_id = $("#document-id" + resultTag).val();
		var query = $("#query-text").val();
		sendDiscoveryFeedback(10, document_id, query, resultTag);
	});
	
	$(".thumbs-down").click(function() {
		var resultTag = this.id[this.id.length - 1];
		var document_id = $("#document-id" + resultTag).val();
		var query = $("#query-text").val();
		sendDiscoveryFeedback(0, document_id, query, resultTag);
	});
	
	function collapseAccordions() {
		$('.collapse').collapse('hide');
	}
	
	function sendDiscoveryFeedback(feedback, document_id, query, resultTag) {
		data = {
			feedback : feedback,
			document_id: document_id,
			query: query
		}
	
		url = "/api/feedback"
		$.ajax({
			type:"POST",
			url: url,
			data: JSON.stringify(data),
			dataType: 'json',
			contentType: 'application/json; charset=utf-8',
			success: function(result) {
				if (result.result['response']) {
					showSnackbar("Thank you for your feedback!");
					$("#feedback-container" + resultTag).hide();
				}
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
	
	function query(queryText, category) {

		collapseAccordions();
	
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
	
				var discoveryResponse = JSON.parse(result.result);
	
				// If the Watson NLC was able to correctly classify the request, then it will just return html
				if (discoveryResponse['error'].length > 0) {
					showSnackbar(discoveryResponse['error']);
					$("#query-text").removeAttr("disabled");
				} else {
					if (discoveryResponse['articles'].length > 0) {
						$(".card").hide();
						$('#result1').html("");
						$('#result2').html("");
						$('#result3').html("");
						$('#collapseheader1').html("");
						$('#collapseheader2').html("");
						$('#collapseheader3').html("");
						for (var i = 0; i < discoveryResponse['articles'].length; i++) {
							var resultTag = '#result' + (i + 1);
							var collapseTag = '#collapseheader' + (i + 1);
							var cardTag = "#card" + (i + 1);
							var article = discoveryResponse['articles'][i]
							var rawHTML = article['html']
							var documentId = article['document_id']
							rawHTML = rawHTML.substring(4);
							var end = rawHTML.indexOf('<');
							if (end > 50){
								end = 50;
								rawHTML = rawHTML.substring(0, end);
								rawHTML = rawHTML+ "..."
							}else{
								rawHTML = rawHTML.substring(0, end);
							}
							$(collapseTag).html(rawHTML+"<br>");
							$(resultTag).html(article['html']);
							$("#document-id" + (i+1)).val(documentId);
							$("#feedback-container" + (i+1)).show();
							$(cardTag).show()
						}
						$("#response").hide();
						$("#category-dropdown-button").hide();
						$("#result0").hide();
						$("#accordion").show();
					}
					//Otherwise we need to some logic to populate and show the dropdown box
					//to let the user choose a category for their query
					else {
						$("#category-dropdown-button").show();
						$("#feedback-container").hide();
						$("#response").show();
						$("#accordion").hide();
	
						var outstring = "<p>To clarify your results, please pick a category from the box on the right.</p>"
						$("#category-dropdown").empty()
						for (var i = 0; i < discoveryResponse['categories'].length; i++) {
							category = discoveryResponse['categories'][i]
							$("#category-dropdown").append('<a class="dropdown-item" href="#">' + category + '</a>');
						}
						$("#result0").html(outstring);
						$("#result0").show();
					}
					$("#result-container").show();
					$("#query-text").removeAttr("disabled");
				}
	
	
			},
			error: function (XMLHttpRequest, textStatus, errorThrown) {
				$("#query-text").removeAttr("disabled");
				$("#result-container").hide();
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
});
