var redis = require("redis"),
    client = redis.createClient();

client.on("error", function (err) {
    console.log("error event - " + client.host + ":" + client.port + " - " + err);
});

client.select(10);
client.set("string key", "string val", redis.print);
client.hset("hash key", "hashtest 1", "some value", redis.print);
client.hset(["hash key", "hashtest 2", "some other value"], redis.print);
client.hkeys("hash key", function (err, replies) {
    console.log(replies.length + " replies:");
    replies.forEach(function (reply, i) {
        console.log("    " + i + ": " + reply);
    });
    client.quit();
});


var dgram = require("dgram");

var server = dgram.createSocket("udp4");
server.on("message", function (msg, rinfo) {
    console.log("server got: " + msg + " from " +
        rinfo.address + ":" + rinfo.port);
    var request = JSON.parse(msg);
    var message = new Buffer("Got it!");
    console.log("USER: " + request.user + " REQUESTING: " + request.event);
    server.send(message, 0, message.length, rinfo.port, rinfo.address, function(err, bytes) {
        // server.close();
    });
});

server.on("listening", function () {
    var address = server.address();
    console.log("server listening " +
        address.address + ":" + address.port);
});

server.bind(43278);