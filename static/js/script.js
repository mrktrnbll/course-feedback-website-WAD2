
// let inputFile = document.getElementById('picture');
// let fileNameField = document.getElementById('file-name');
// inputFile.addEventListener('change', function(event)){
// 	let uploadedFileName = event.target.files.[0].name;
// 	fileNameField.textContent = uploadedFileName;
// }

$(document).ready(function() {
	$('#like_btn').click(function() {
		var catecategoryIdVar;
		catecategoryIdVar = $(this).attr('data-categoryid');
		$.get('/rango/like_category/',
			{'category_id': catecategoryIdVar},
			function(data) {
				$('#like_count').html(data);
				$('#like_btn').hide();
			})
	});
});

