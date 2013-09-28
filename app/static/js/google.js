//Reverse Geolocation API

function locateMe(){
	if (navigator.geolocation) {
	    navigator.geolocation.getCurrentPosition(showPosition);
	} else {
		alert("Geolocation is not supported by this browser.");
	}
}

function showPosition(position) {
	geocoder = new google.maps.Geocoder();
	var latlng = new google.maps.LatLng(position.coords.latitude, position.coords.longitude);
	geocoder.geocode({'latLng':  latlng}, function(results, status) {
	    if (status == google.maps.GeocoderStatus.OK) {
			console.log(results);
			$('input#inputLocation').val(results[0].formatted_address);
	    } else {
	      alert('Geocoder failed due to: ' + status);
	    }
	  });
}

//User info APIs

function getUserInfo(accessToken, callback) {
	var output = {};
	$.ajax({
		data: {
			access_token: accessToken
		},
		type: "GET",
		async: false,
		url: "https://www.googleapis.com/plus/v1/people/me",
		success: function(data) {
			output['fname'] = data['name']['givenName'];
			output['lname'] = data['name']['familyName'];
			$.ajax({
				data: {
					access_token: accessToken
				},
				type: "GET",
				async: false,
				url: "https://www.googleapis.com/userinfo/v2/me",
				success: function(data) {
					output['email'] = data['email'];
				}
			});
		}
	});
	callback(output);
}

//Calendar APIs

function ISODateTimeString(d) {
	function pad(n) {
		return n < 10 ? '0' + n : n
	}
	return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes()) + ':' + pad(d.getUTCSeconds()) + 'Z'
}

function ISODateString(d) {
	function pad(n) {
		return n < 10 ? '0' + n : n
	}
	return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate());
}

function dateDifference(dateEarlier, dateLater) {
    var one_day=1000*60*60*24
    return (Math.round((dateLater.getTime()-dateEarlier.getTime())/one_day));
}

function getCalendarEvents(accessToken, startDate, endDate, callback) {
	var startD = new Date(startDate);
	var endD = new Date(endDate);
	var numberOfDays = dateDifference(startD, endD) + 1;
	getPrimaryCalendar(accessToken, startD, numberOfDays, callback);
}

function getPrimaryCalendar(accessToken, startDate, numberOfDays, callback) {
	$.ajax({
		data: {
			access_token: accessToken
		},
		type: "GET",
		url: "https://www.googleapis.com/calendar/v3/users/me/calendarList",
		async: false,
		success: function(data) {
			$.each(data['items'], function(index, item) {
				if (item['primary'] == true) {
					getEvents(accessToken, item['id'], startDate, numberOfDays, callback);
				}
			});
		}
	});
}

function getEvents(accessToken, calendarId, startDate, numberOfDays, callback) {
	var futureDate = new Date();
	futureDate.setDate(startDate.getDate() + numberOfDays);
	$.ajax({
		data: {
			access_token: accessToken,
			singleEvents: true,
			timeMin: ISODateTimeString(startDate),
			timeMax: ISODateTimeString(futureDate)
		},
		type: "GET",
		url: "https://www.googleapis.com/calendar/v3/calendars/" + calendarId + "/events",
		async: false,
		success: function(data) {
			var output = [];
			$.each(data['items'], function(index, item) {
				output.push(new Date(item['start']['dateTime']));
			});
			generateOutputJSON(output, startDate, numberOfDays, callback);
		}
	});
}

function generateOutputJSON(events, startDate, numberOfDays, callback) {
	var output = [];
	for (var i = 0; i < numberOfDays; i++) {
		var d = new Date();
		d.setDate(startDate.getDate() + i);
		d.setMinutes(0);
		d.setSeconds(0);
		var time = [];
		for (var t = 0; t < 24; t++) {
			d.setHours(t);
			
			var val = 0;
			for (var u = 0; u < events.length; u++) {
				var diff = events[u].getTime() - d.getTime();
				if (diff < 3599143 && diff > -3599143) {
					val = 1;
				}
			}
			if (val == 0) {
				if (t<10) {
					output.push("0" + t + "00_" + ISODateString(d));
				} else {
					output.push(t + "00_" + ISODateString(d));
				}	
			}
		}
		// output["d" + ISODateString(d)] = time;
	}
	callback(output);
}