console.log("im here!!");

var chatbox = document.getElementById("chatbox");
reloadMessages();
var socket = io("http://" + document.domain + ":" + location.port);

var submit = document.getElementById("submit");
var reload = document.getElementById("reload");
var messageInput = document.getElementById("messageInput");

socket.on("server_message", data => {
  console.log(data);
});

function appendMessage(element, text) {
  let row = document.createElement("div");
  row.classList = "row";
  let col = document.createElement("div");
  col.classList = "col-12";
  col.innerText = text;
  row.appendChild(col);
  element.appendChild(row);
}

reload.addEventListener("click", reloadMessages);
submit.addEventListener("click", sendMessage);

function sendMessage() {
  socket.emit("post_message", { text: messageInput.value }, ack => {
    if (ack == 0) {
      messageInput.value = "";
      reloadMessages();
    }
  });
}

function reloadMessages() {
  chatbox.innerHTML = "";
  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      let response = JSON.parse(this.responseText);
      for (let i = 0; i < response.length; i++) {
        appendMessage(chatbox, response[i]);
      }
    }
  };
  xhttp.open("GET", "/get_history", true);
  xhttp.send();
}
