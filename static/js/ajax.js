$(document).ready(function() {
	$('#like_btn').click(function() {
		console.log("Button pressede")
		var catecategoryIdVar;
		catecategoryIdVar = $(this).attr('review-id');
		console.log(catecategoryIdVar)
		$.get('/like_review/',
			{'review_id': catecategoryIdVar},
			function(data) {
				$('#reviews').html(data);
				$('#like_btn').hide();
			})
	});
});