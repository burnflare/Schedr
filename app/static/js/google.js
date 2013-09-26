//User info APIs

function getUserInfo(accessToken) {
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
					console.log(output);
				}
			});
		}
	});
	return output;
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

function getCalendarEvents(accessToken, numberOfDays) {
	getPrimaryCalendar(accessToken, numberOfDays);
}

function getPrimaryCalendar(accessToken, numberOfDays) {
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
					getEvents(accessToken, item['id'], numberOfDays);
				}
			});
		}
	});
}

function getEvents(accessToken, calendarId, numberOfDays) {
	var yesterday = new Date();
	yesterday.setDate(yesterday.getDate() - 1);
	var futureDate = new Date();
	futureDate.setDate(futureDate.getDate() + numberOfDays);
	$.ajax({
		data: {
			access_token: accessToken,
			singleEvents: true,
			timeMin: ISODateTimeString(yesterday),
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
			generateOutputJSON(output, numberOfDays);
		}
	});
}

function generateOutputJSON(events, numberOfDays) {
	var output = {};
	for (var i = 0; i < numberOfDays; i++) {
		var d = new Date();
		d.setDate(d.getDate() - 1 + i);
		// d.setTime(d.getTime() + d.getTimezoneOffset() * 60000)
		d.setMinutes(0);
		d.setSeconds(0);
		var time = {};
		for (var t = 0; t < 24; t++) {
			d.setHours(t);
			
			var val = false;
			for (var u = 0; u < events.length; u++) {
				var diff = events[u].getTime() - d.getTime();
				if (diff < 3599143 && diff > -3599143) {
					// console.log(diff);
					val = true;
				}
			}
			
			if (t<10) {
				time["0" + t + "00"] = val;	
			} else {
				time[t + "00"] = val;
			}
		}
		output[ISODateString(d)] = time;
	}
	console.log(output);
}