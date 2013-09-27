var TR = [];
var meetingName;
var meetingVenue;
var datesSelected = [];
var matesCount = 1;var matesEmails = [];
 function signinCallback(authResult) {
  if (authResult['access_token']) {
	  getUserInfo(authResult['access_token'], function(data){
		  $.ajax({
			  data: JSON.stringify(data),
			  dataType: "json",
			  contentType: 'application/json', 
			  type: "POST",
			  url: "/login/",
		  }).done(function() {
			  console.log("Login success");
		  });
	  });
    $.ajax({
		  data: JSON.stringify({recipients:matesEmails,name:meetingName,venue:meetingVenue,date:datesSelected,timeslot:TR}), 
		  contentType: 'application/json', 
		  type: "POST",
		  url: "/event/",
		  beforeSend : function (){
               for (var i=0;i<=matesCount;++i) {
					matesEmails.push($('input#mate'+i+'').val());
			   };
          },
		}).done(function() {
			console.log('inside done');
		  window.location = "almostthere.html";
	});
    console.log('success');
  } else if (authResult['error']) {
	$('.form-horizontal').empty().append('There was an error, refresh the page and try again!');
  }
};

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
		console.log(datesSelected);
		var B = this;
		if ( $(B).hasClass('btn-danger') == true ) {
			$(B).addClass('btn-success').removeClass('btn-danger');
			datesSelected.push($(B).attr('data-daterange'));
		} else {
			$(B).addClass('btn-danger').removeClass('btn-success');
			datesSelected = jQuery.grep(datesSelected, function(value) {
				return value != $(this).attr('data-daterange');
			});
		};
	});
	noofTimes = ++noofTimes;
};

$('button.PLUS').click(function() {
updateDates();
});

$('a.PP').click(function() {
	$('#ppModal').modal();
	$('#pp').append('<p>This Privacy Policy describes how users’ personal information is handled in order to engage in the services available in our application. It applies generally to web pages where this policy appears in the footer. By accepting the Privacy Policy, you express consent to our collection, storage, use and disclosure of your personal information as described in this Privacy Policy. This Privacy Policy is effective upon acceptance for new users and is otherwise effective on August 12, 2013.</p><h4>Definitions</h4><ol><li>References to ”Our”, ”We”, ”Us” and "Schedulr" shall be references to Schedulr.</li><li>References to ”You”, ”Users” and ”Your” shall mean references to user(s) using this app, as the context requires.</li></ol><h4>Information Collection</h4><p>We collect but do not store some of your personal information. The personal information collected includes but isnt restricted to the following:</p><ol><li>Your name (as it appears on Facebook).</li><li>Additional information which we may ask for if we believe site policies are violated.</li></ol><p>We do collect and store any information you explicitly enter into the application, including but not limited to the following:</p><ol><li>The items you create listings for.</li><li>The city and country you choose in such item listings.</li><li>Any comments you enter on a listing.</li></ol><p>In addition, we also collect and store a number that is uniquely associated with your Facebook account.</p><h4>Information Usage</h4><p>The primary purpose in collecting information is to provide users with a smooth and customized experience.</p><p>We will use the information collected for the following purposes:</p><ol><li>To provide our intended services.</li><li>To resolve disputes, and troubleshoot problems and errors.</li><li>To assist in law enforcement purposes and prevent/restrict the occurrences of potentially illegal or prohibited activities.</li></ol><h4>Disclosure of information</h4><p>We may share information with governmental agencies or other companies assisting us in fraud prevention or investigation. We may do so when:</p><ol><li>permitted or required by law; or,</li><li>trying to protect against or prevent actual or potential fraud or unauthorized transactions; or,</li><li>investigating fraud which has already taken place.The information is not provided to these companies for marketing purposes.</li></ol><h4>Usage of Cookies</h4><p>Cookies are small files placed on your computers hard drives. We use Cookies to analyse our apps usage, and also to maintain your signed in status when you login to our app.</p><h4>Commitment to Data Security</h4><p>Your personally identifiable information is kept secure. Only authorized employees, agents and contractors (who have agreed to keep information secure and confidential) have access to this information. All emails and newsletters from this site allow you to opt out of further mailings.</p><h4>Changes to Policies</h4><p>We reserved the rights to amend this Privacy Policy at any time. Any policy changes will take immediate effect. We may notify you in the event of any major changes to our policies.</p>');
});

$("button.TR").click(function() {
	var a = this;
	if ( $(a).hasClass('btn-danger') == true ) {
		$(a).addClass('btn-success').removeClass('btn-danger');
		TR.push($(this).attr('data-timerange'));
	} else {
		$(a).addClass('btn-danger').removeClass('btn-success');
		TR = jQuery.grep(TR, function(value) {
		  return value != $(this).attr('data-timerange');
		});
	};
});

$('button.inviteMates').on('mousedown',function() {
	meetingName = $('input#inputEvent').val();
	meetingVenue = $('input#inputLocation').val();
});

$('button.inviteMates').on('mouseup',function() {
	$('.form-horizontal').fadeOut().empty().fadeIn().append('<span class="matesEmails"><div class="form-group"><label for="mate1" class="col-lg-2 control-label">Member #1 email?</label><div class="col-lg-10"><input type="email" class="form-control" id="mate1" placeholder="Enter email.."></div></div></span><div class="addMatesbtn center"><button type="button" class="addMates btn btn-success btn-lg"><b>+</b></button></div>');
	googleLogin();
	$('span.googlelogin').empty().append('<span id="signinButton"><span class="g-signin" data-approvalprompt="force" data-callback="signinCallback" data-clientid="875376181351.apps.googleusercontent.com" data-cookiepolicy="single_host_origin" data-requestvisibleactions="http://schemas.google.com/AddActivity" data-scope="https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/plus.me https://www.googleapis.com/auth/calendar.readonly"></span></span>');
	addMates();
});

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

};

});