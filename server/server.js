var redis = require("redis"),
    client = redis.createClient();

client.on("error", function (err) {
    console.log("error event - " + client.host + ":" + client.port + " - " + err);
});

client.select(10);
client.set("string key", "string val", redis.print);
client.hset("hash key", "hashtest 1", "some value", redis.print);
/*
client.hset(["hash key", "hashtest 2", "some other value"], redis.print);
client.hkeys("hash key", function (err, replies) {
    console.log(replies.length + " replies:");
    replies.forEach(function (reply, i) {
        console.log("    " + i + ": " + reply);
    });
    client.quit();
});*/


var gameState = {}

var dgram = require("dgram");

var server = dgram.createSocket("udp4");
server.on("message", function (msg, rinfo) {
    console.log("server got: " + msg + " from " +
        rinfo.address + ":" + rinfo.port);
    var request = JSON.parse(msg);
    
    console.log("USER: " + request.user + " REQUESTING: " + request.event);

    client.select(10);

    // add the player to the game
    if (request.event == "login"){
        gameState[request.user] = {};
        gameState[request.user]["pos"] = [0,0];
        console.log("Player logged in");
    }

    if (request.event == "up"){
        gameState[request.user]["pos"][1] -= 10;
    }

    if (request.event == "down"){
        gameState[request.user]["pos"][1] += 10;
    }

    if (request.event == "left"){
        gameState[request.user]["pos"][0] -= 10;
    }

    if (request.event == "right"){
        gameState[request.user]["pos"][0] += 10;
    }

    client.set(request.user, JSON.stringify(gameState[request.user]), redis.print);
        
    var message = new Buffer(JSON.stringify(gameState));

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