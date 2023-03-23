$(document).ready(function() {
	$('.like_btn').click(function() {
		let catecategoryIdVar = $(this).attr('review-id');
		$.get('/like_review/',
			{'review_id': catecategoryIdVar},
			function(data) {
				$('#reviews').html(data);
				$('#like_btn').hide();
			})
		location.reload();
	});
});