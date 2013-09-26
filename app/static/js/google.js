//User info APIs

function getUserInfo(accessToken) {
	var output = [];
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

function ISODateString(d) {
	function pad(n) {
		return n < 10 ? '0' + n : n
	}
	return d.getUTCFullYear() + '-' + pad(d.getUTCMonth() + 1) + '-' + pad(d.getUTCDate()) + 'T' + pad(d.getUTCHours()) + ':' + pad(d.getUTCMinutes()) + ':' + pad(d.getUTCSeconds()) + 'Z'
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
			timeMin: ISODateString(yesterday),
			timeMax: ISODateString(futureDate)
		},
		type: "GET",
		url: "https://www.googleapis.com/calendar/v3/calendars/" + calendarId + "/events",
		async: false,
		success: function(data) {
			$.each(data['items'], function(index, item) {
				console.log(item['start']['dateTime']);
			});
		}
	});
}

function generateOutputJSON() {
	var output = [];
	for (var i = 0; i < 10; i++) {
		output[i]['date'] =
		     output[i]['date'][i] || [];
			 
		var d = new Date();
		d.setDate(d.getDate() - 1 + i);
		output[i][date] = ISODateString(d);
		output[i][time] = false;
	}
	return output;
}