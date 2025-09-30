// imports
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");
var http = require("http");
const fs = require("fs");

// variables
const group_whitelist = JSON.parse(
  fs.readFileSync("source/Config/Groups.json", "utf8"),
);
const links_whitelist = JSON.parse(
  fs.readFileSync("source/Config/Links.json", "utf8"),
);
console.log(group_whitelist);
console.log(links_whitelist);

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
  //console.log(message.from);
  if (group_whitelist.groups.includes(message.from)) {
    console.log(
      `Message from whitelisted group ${message.from}: ${message.body}`,
    );
    // add the message to the queue
    msg_queue.push(message);
  }
});

function convert_text_to_one_line(text) {
  if (!text) {
    return "";
  }
  return text.replace(/\n/g, " ").replace(/\r/g, " ").trim();
}

function removeEmojis(text) {
  if (!text) {
    return "";
  }
  return text.replace(
    /(\u00a9|\u00ae|[\u2000-\u3300]|\ud83c[\ud000-\udfff]|\ud83d[\ud000-\udfff]|\ud83e[\ud000-\udfff])/g,
    "",
  );
}

function isLink(text) {
  const urlRegex =
    /^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$/i;
  return urlRegex.test(text);
}

function is_whitelisted_link(text) {
  var is_link = isLink(text);
  if (is_link) {
    // Check if any of the whitelisted groups/domains are contained in the URL
    return links_whitelist.links.some((domain) => text.includes(domain));
  }
  return false;
}

function processQueue() {
  if (msg_queue.length > 0 && !awaiting_response) {
    const message = msg_queue.shift();
    awaiting_response = true;

    const cleaned_message = removeEmojis(
      convert_text_to_one_line(message.body),
    );

    if (is_whitelisted_link(cleaned_message)) {
      // dont send the message for inference if its a whitelisted link.
      awaiting_response = false;
      console.log(`Whitelisted link, skipping inference: ${message.body}`);
      return;
    }

    if (cleaned_message.length === 0 || cleaned_message == "") {
      awaiting_response = false;
      console.log("Empty message after cleaning, skipping.");
      return;
    }

    const final_link = `http://127.0.0.1:8000/inference`;

    fetch(final_link, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: cleaned_message,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // 0 = not spam
        // 1 = spam

        if (data.result === 0) {
          console.log(`Not spam: ${message.body}`);
        } else if (data.result === 1) {
          console.log(`Spam detected and message deleted: ${message.body}`);
          message.delete(true);
        }
        awaiting_response = false;
      })
      .catch((error) => {
        console.error("Error during inference:", error);
        awaiting_response = false;
      });
  }
}

queue_interval = setInterval(processQueue, 100); // process the queue every 100ms

fs.readFile("source/bot/index.html", function (err, html) {
  if (err) {
    throw err;
  }
  var server = http
    .createServer(function (request, response) {
      response.writeHeader(200, { "Content-Type": "text/html" });
      response.write(html);
      response.end();
    })
    .listen(6969);

  if (server.listening) {
    console.log("web server started at http://localhost:6969");
  }
});

// start the client
client.initialize();
