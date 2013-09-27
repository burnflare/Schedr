$(document).ready(function() {

$('#myModal').modal();

$.ajax({
		  type: "GET",
		  dataType: "json",
		  url: "/admin/"
		}).done(function(json) {
			$.each(json.event_list,function(i,el){
			  $('span.meetings').prepend('<a href="calender.html/?pid='+el.meetings_id+'"><button type="button" class="btn btn-success btn-lg btnwide">'+el.event_name+'</button></a>');
			});	
	});

});