$("#submit-search").click(function(){
    console.log('Search Sent');
    var queryText = $('#query-text').val();
    var url = "/api/query/" + queryText;
    $.ajax({url: url, success: function(result){
        $("#result").html(result.result);
    }});
});