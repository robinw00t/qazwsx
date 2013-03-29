matrix_x = 12;
matrix_y = 12;
matrixAmount = matrix_x * matrix_y;



function set_pixel(x, y, col) {
	//console.log("X="+y+" Y="+y);
	//console.log(col);
	$('#box-'+y+'-'+x)[0].style.backgroundColor = 'rgb('+col[0]+', '+col[1]+', '+col[2]+')';
}

for(y = 0; y < matrix_y; y++) {
	for(x = 0; x < matrix_x; x++) {
	    $('.boxcontainer').append("<div class='box' id='box-"+y+"-"+x+"'><div class='led'></div></div>");
	}
}

function getBrowserHeight(){
  var  myHeight = 0;
  if( typeof( window.innerWidth ) == 'number' ) {
    //Non-IE
    myHeight = window.innerHeight;
  } else if( document.documentElement && ( document.documentElement.clientWidth || document.documentElement.clientHeight ) ) {
    //IE 6+ in 'standards compliant mode'
    myHeight = document.documentElement.clientHeight;
  } else if( document.body && ( document.body.clientWidth || document.body.clientHeight ) ) {
    //IE 4 compatible
    myHeight = document.body.clientHeight;
  }
  return myHeight;
}


var wsUri = "ws://localhost:1024";

function ws_init() {
	websocket = new WebSocket(wsUri);
	websocket.onopen = function(evt) {
		onOpen(evt);
	};

	websocket.onclose = function(evt) {
		onClose(evt);
	};

	websocket.onmessage = function(evt) {
		onMessage(evt);
	};

	websocket.onerror = function(evt) {
		onError(evt);
	};

	sizeMatrix();
}

function sizeMatrix(){
	matrix_size = Math.round(getBrowserHeight()/matrix_y);
	// sizing the boxes to the right values
	$('.boxcontainer').css("width", matrix_x * matrix_size + "px");
	$('.boxcontainer').css("height", matrix_y * matrix_size + "px");
	$('.box').css("height", matrix_size+'px');
	$('.box').css("width", matrix_size+'px');
}

$(window).resize(function() {
	sizeMatrix();
});

function json_encode(obj) {
	return JSON.stringify(obj);
}

function onOpen(evt) {
	console.log("CONNECTED");

	setInterval("get_screen()", 20);
}

function onClose(evt) {
	console.log("DISCONNECTED");
}

function onMessage(evt) {
	//console.log(evt.data);
	px = JSON.parse(evt.data);
	//console.log(px);

	for(y=0; y<matrix_y; y++) {
		for(x=0; x<matrix_x; x++) {
			idx=(y*matrix_x)+x;
			idx = idx*3;
			//console.log("X="+x+" Y="+y);
			set_pixel(x, y, [ px[idx+0], px[idx+1], px[idx+2] ]);
		}
	}
}

function get_screen() {
	console.log("DBG get_screen()");

	websocket.send(json_encode(
		{ 'action' : 'get_screen' }
	));
}

function onError(evt) {
	console.log("ERROR: "+evt.data);
}

ws_init();
