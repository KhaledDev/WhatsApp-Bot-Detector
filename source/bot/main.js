// imports
const { Client, LocalAuth } = require("whatsapp-web.js");
const qrcode = require("qrcode-terminal");

// variables
const group_whitelist = [
  "120363377880499372@g.us",
  "120363379096537975@g.us",
  "120363370702829195@g.us",
];

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
  }
});

// start the client
client.initialize();
