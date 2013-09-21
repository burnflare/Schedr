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
	$('span.addDates').append('<button data-daterange="'+data+'" class="DR btn btn-xs btn-danger">'+dayofweek+'<h1 class="datesec">'+date+'</h1>'+month+' '+year+'</button>');
	};
	noofTimes = ++noofTimes;
	activateButtons();
};

$('button.PLUS').click(function() {
updateDates();
});

function activateButtons() {
$("button.TR,button.DR").click(function() {
	var a = this;
	if ( $(a).hasClass('btn-danger') == true ) {
		$(a).addClass('btn-success').removeClass('btn-danger');
	} else {
		$(a).addClass('btn-danger').removeClass('btn-success');
	};
});
};

});