// imports
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
const fs = require("fs");

// variables
const group_whitelist = JSON.parse(
  fs.readFileSync("source/Config/Groups.json", "utf8"),
);

var msg_queue = []; // message queue so keep track of each message
var awaiting_response = false; // flag to indicate if waiting for a response
var queue_interval = null; // interval for processing the message queue

// client setup
const client = new Client({
  authStrategy: new LocalAuth({
    dataPath: "./session",
  }),
});

// event handlers
client.on("ready", () => {
  console.log("Client is ready!");
});

client.on("qr", (qr) => {
  qrcode.generate(qr, { small: true });
});

client.on("message_create", (message) => {
  console.log(message.from);
  if (group_whitelist.includes(message.from)) {
    console.log(
      `Message from whitelisted group ${message.from}: ${message.body}`,
    );
    // add the message to the queue
    msg_queue.push(message);
  }
});

function processQueue() {
  if (msg_queue.length > 0 && !awaiting_response) {
    const message = msg_queue.shift();
    awaiting_response = true;

    const final_link = `http://127.0.0.1:8000/inference/${message.body}`;

    fetch(final_link)
      .then((response) => response.json())
      .then((data) => {
        // 0 = not spam
        // 1 = spam

        if (data.result === 0) {
          console.log(`Not spam: ${message.body}`);
        } else if (data.result === 1) {
          message.delete(true);
        }
      });
    awaiting_response = false;
  }
}

queue_interval = setInterval(processQueue, 100); // process the queue every 100ms

// start the client
client.initialize();
