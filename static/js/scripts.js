console.log("im here!!");

var xhttp = new XMLHttpRequest();

xhttp.onreadystatechange = function() {
  if (this.readyState == 4 && this.status == 200) {
    document.getElementById("result").innerHTML = this.responseText;
  }
};
xhttp.open("GET", "/get_history", true);
xhttp.send();

var socket = io("http://" + document.domain + ":" + location.port);
socket.on("connect", function() {
  socket.emit("post_message", { data: "Sending data." }, data => {
    console.log("Received!");
    console.log(data);
  });
});
