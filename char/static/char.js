if (window.s) {
    window.s.close()
}
var socket = new WebSocket("ws://" + window.location.host + "/echo");
socket.onopen = function () {
    console.log('WebSocket open');
    };
if (socket.readyState == WebSocket.OPEN) socket.onopen();
socket.onmessage = function(e){
    obj = eval("("+e.data+")");
    for (j=0;j<obj.length;j++){
        fmsg = obj[j];
        var fd_msg_ele = "<div class='msg-item'>" +
            "<span>"+ fmsg.from +"</span>" +
            "<span>"+new Date().setTime(fmsg.timestamp) +"</span>" +
            "<div class='msg-text'>" + fmsg.msg + "</div>" +
            "</div>";
            $(".chat-box-window").append(fd_msg_ele);
            $(".chat-box-window").animate({scrollTop:$('.chat-box-window').height()},500)
            }
    };

