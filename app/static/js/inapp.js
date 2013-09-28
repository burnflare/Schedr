var startendDate = [];
var suggested_date = [];

$(document).ready(function() {	
    
var event_name;
var event_venue;
var suggested_time;
var duration;
var meeting_id;
var split = location.search.replace('?', '').split('=');
	
	$.ajax({
		  dataType: "json", 
		  type: "GET",
		  url: "/specific_event/"+split[1]+"",
		}).done(function(json) {
			console.log('in done');
			event_name = json.current_meeting.event_name;
			event_venue = json.current_meeting.event_venue;
			meeting_id = json.current_meeting.meetings_id;
			console.log(meeting_id);
			suggested_date = json.current_meeting.suggested_date.split(',');
			var a = suggested_date.length;
			startendDate = [suggested_date[0],suggested_date[a-1]];
			suggested_time = json.current_meeting.suggested_time.split(',');
			duration = json.duration;
			$('.meetingName').text(event_name);
			$('.meetingVenue').text(event_venue);
			$('.meetingTime').text(duration);
			if (json.current_meeting.finalized_time != "") {
			} else {
				for (var i=0;i<a;++i) {
					var b= moment(suggested_date[i], "YYYY-MM-DD").format('dddd, MMMM Do YYYY');
					var c=suggested_date[i];
					$('div.row').append('<div class="col-sm-3 oneday"><h3 class="date">'+b+'</h3><span id ="d'+i+'" data-date="'+suggested_date[i]+'" class="timeslots"></span></div>');
					var timeslots = [];
					var timeslot1 = ["00","01","02","03","04","05"];
					var timeslot2 = ["06","07","08","09","10","11"];
					var timeslot3 = ["12","13","14","15","16","17"];
					var timeslot4 = ["18","19","20","21","22","23"];
					console.log(suggested_time);
					if (jQuery.inArray("1",suggested_time) >= 0) {
						$.merge(timeslots, timeslot1);
					};
					if (jQuery.inArray("2",suggested_time) >= 0) {
						$.merge(timeslots, timeslot2);
					};
					if (jQuery.inArray("3",suggested_time) >= 0) {
						$.merge(timeslots, timeslot3);
					};
					if (jQuery.inArray("4",suggested_time) >= 0) {
						$.merge(timeslots, timeslot4);
					};
					console.log(timeslots);
					var k = timeslots.length;
					for (var z=0;z<k;++z) {
					$('span#d'+i+'').append('<button id="d'+timeslots[z]+'00_'+c+'" class="timeslot btn btn-default center"><h1 class="glyping glyphicon glyphicon-remove"></h1><b class="timetext">'+timeslots[z]+'</b></button>');
					};
				};
			functionClicks();
			};
	});

var selectedTimeslots = [];

function functionClicks() {
	$('button.timeslot').click(function() {
		var A = this;
		if ($(A).find('h1.glyping').hasClass('glyphicon-remove') == true) {
			$(A).find('h1.glyping').addClass('glyphicon-ok').removeClass('glyphicon-remove');
			var B = $(A).attr('id').substring(1);
			selectedTimeslots.push(B);
		} else {
			$(A).find('h1.glyping').addClass('glyphicon-remove').removeClass('glyphicon-ok');
			var B = $(A).attr('id').substring(1);
			selectedTimeslots = jQuery.grep(selectedTimeslots, function(value) {
			  return value != B;
			});
		};
	});
};

$('button.submit').click(function() {
	$.ajax({
			  data: JSON.stringify({selected_timings:selectedTimeslots}),
			  contentType: 'application/json', 
			  type: "POST",
			  url: "/schedule/"+meeting_id+"",
		  }).done(function() {
			   $('div.row').empty();
			   $('div.foot').empty();
			   $('span.ty').fadeOut().empty().append("<h1>Thank you</h1><h4>Schedr will generate the best meeting time when all members have indicated theirs and deliver it to your email inbox.<br/>Have a nice day!</h4>").fadeIn();
	});
});
	
});