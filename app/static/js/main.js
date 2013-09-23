$(document).ready(function() {

var noofTimes = 0;
updateDates();

function updateDates() {
	var a=noofTimes*7 +1;
	for (var i=a;i<a+7;++i) {
	var data = moment().add('days',i).format('YYYY-MM-DD');
	var year = moment().add('days',i).format('YYYY');
	var month = moment().add('days',i).format('MMM').toUpperCase();
	var date = moment().add('days',i).format('DD');
	var dayofweek = moment().add('days',i).format('ddd').toUpperCase();
	$('span.addDates').append('<button id="d'+a+'" data-daterange="'+data+'" class="DR btn btn-xs btn-danger">'+dayofweek+'<h1 class="datesec">'+date+'</h1>'+month+' '+year+'</button>');
	};
	$('button#d'+a+'').click(function() {
		var B = this;
		if ( $(B).hasClass('btn-danger') == true ) {
			$(B).addClass('btn-success').removeClass('btn-danger');
		} else {
			$(B).addClass('btn-danger').removeClass('btn-success');
		};
	});
	noofTimes = ++noofTimes;
};

$('button.PLUS').click(function() {
updateDates();
});


$("button.TR").click(function() {
	var a = this;
	if ( $(a).hasClass('btn-danger') == true ) {
		$(a).addClass('btn-success').removeClass('btn-danger');
	} else {
		$(a).addClass('btn-danger').removeClass('btn-success');
	};
});

$('button.inviteMates').click(function() {
	$('.form-horizontal').fadeOut().empty().fadeIn().append('<span class="matesEmails"><div class="form-group"><label for="mate1" class="col-lg-2 control-label">Member #1 email?</label><div class="col-lg-10"><input type="email" class="form-control" id="mate1" placeholder="Enter email.."></div></div></span><div class="addMatesbtn center"><button type="button" class="addMates btn btn-success btn-lg"><b>+</b></button></div>');
	googleLogin();
	$('span.googlelogin').empty().append('<span id="signinButton"><span class="g-signin" data-callback="signinCallback" data-clientid="875376181351.apps.googleusercontent.com" data-cookiepolicy="single_host_origin" data-requestvisibleactions="http://schemas.google.com/AddActivity" data-scope="https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/calendar.readonly"></span></span>');
	addMates();
});

var matesCount = 1;
function addMates() {
$('button.addMates').click(function() {
	matesCount = ++matesCount;
	$('.matesEmails').append('<div class="form-group"><label for="mate'+matesCount+'" class="col-lg-2 control-label">Member #'+matesCount+' email?</label><div class="col-lg-10"><input type="email" class="form-control" id="mate'+matesCount+'" placeholder="Enter email.."></div></div>');
});
};

function googleLogin() {
  (function() {
   var po = document.createElement('script'); po.type = 'text/javascript'; po.async = true;
   po.src = 'https://apis.google.com/js/client:plusone.js';
   var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(po, s);
 })();
 
 function signinCallback(authResult) {
  if (authResult['access_token']) {
    // Successfully authorized
    // Hide the sign-in button now that the user is authorized, for example:
    console.log('success');
  } else if (authResult['error']) {
    // There was an error.
    // Possible error codes:
    //   "access_denied" - User denied access to your app
    //   "immediate_failed" - Could not automatically log in the user
    // console.log('There was an error: ' + authResult['error']);
  }
};
};

});