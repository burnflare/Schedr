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
				}
			});
		}
	});
	return JSON.stringify(output);
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

function dateDiff(dateEarlier, dateLater) {
    var one_day=1000*60*60*24
    return (Math.round((dateLater.getTime()-dateEarlier.getTime())/one_day));
}

function getCalendarEvents(accessToken, startDate, endDate) {
	var startD = new Date(startDate);
	var endD = new Date(endDate);
	var numberOfDays = dateDiff(startD, endD) + 1;
	getPrimaryCalendar(accessToken, startD, numberOfDays);
}

function getPrimaryCalendar(accessToken, startDate, numberOfDays) {
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
					getEvents(accessToken, item['id'], startDate, numberOfDays);
				}
			});
		}
	});
}

function getEvents(accessToken, calendarId, startDate, numberOfDays) {
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
			generateOutputJSON(output, startDate, numberOfDays);
		}
	});
}

function generateOutputJSON(events, startDate, numberOfDays) {
	var output = {};
	for (var i = 0; i < numberOfDays; i++) {
		var d = new Date();
		d.setDate(startDate.getDate() + i);
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