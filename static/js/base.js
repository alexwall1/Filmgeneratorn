$("#like").click(function() {
	$.post('/filmgeneratorn/like');
	$("#like").prop('disabled',true);
});
