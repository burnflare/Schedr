$(document).ready(function() {	
    
var event_name;
var event_venue;
var suggested_date = [];
var suggested_time;
var duration;
var split = location.search.replace('?', '').split('=');
	
	$.ajax({
		  dataType: "json", 
		  type: "GET",
		  url: "/specific_event/"+split[1]+"",
		}).done(function(json) {
			event_name = json.current_meeting.event_name;
			event_venue = json.current_meeting.event_venue;
			suggested_date = json.current_meeting.suggested_date.split(',');
			suggested_time = json.current_meeting.suggested_time.split(',');
			duration = json.duration;
			$('.meetingName').text(event_name);
			$('.meetingVenue').text(event_venue);
			$('.meetingTime').text(duration);
			
			if (json.finalized_time == null) {
			} else {
				var a = ++suggested_date.length;
				for (var i=0;i<a;++i) {
					var b= moment(suggested_date[i], "YYYY-MM-DD").format('dddd, MMMM Do YYYY');
					var c=suggested_date[i];
					$('div.row').append('<div class="col-sm-3 oneday"><h3 class="date">'+b+'</h3><span id ="d'+i+'" data-date="'+suggested_date[i]+'" class="timeslots"></span></div>');
					var timeslots = [];
					var timeslot1 = [0000,0100,0200,0300,0400,0500];
					var timeslot2 = [0600,0700,0800,0900,1000,1100];
					var timeslot3 = [1200,1300,1400,1500,1600,1700];
					var timeslot4 = [1800,1900,2000,2100,2200,2300];
					if (jQuery.inArray(1,suggested_time) >= 0) {
						$.merge(timeslots, timeslot1);
					};
					if (jQuery.inArray(2,suggested_time) >= 0) {
						$.merge(timeslots, timeslot2);
					};
					if (jQuery.inArray(3,suggested_time) >= 0) {
						$.merge(timeslots, timeslot3);
					};
					if (jQuery.inArray(4,suggested_time) >= 0) {
						$.merge(timeslots, timeslot4);
					};
					var k = ++timeslots.length;
					for (var z=0;z<k;++z) {
					$('span#d'+i+'').append('<button id="t'+timeslots[z]+'_'+c+'" class="timeslot btn btn-default center"><h1 class="glyping glyphicon glyphicon-remove"></h1><b class="timetext">'+timeslots[z]+'</b></button>');
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
			selectedTimeslots.push($(A).attr('id'));
		} else {
			$(A).find('h1.glyping').addClass('glyphicon-remove').removeClass('glyphicon-ok');
			selectedTimeslots = jQuery.grep(selectedTimeslots, function(value) {
			  return value != $(A).attr('id');
			});
		};
	});
};
	
});