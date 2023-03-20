
let inputFile = document.getElementById('picture');
let fileNameField = document.getElementById('file-name');
inputFile.addEventListener('change', function(event)){
	let uploadedFileName = event.target.files.[0].name;
	fileNameField.textContent = uploadedFileName;
}