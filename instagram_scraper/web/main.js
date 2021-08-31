console.log("Hello World")

var socket = io();

socket.on('connection', (socket) => {
    console.log('a user connected');
    socket.on('disconnect', () => {
        console.log('user disconnected');
    });
});

socket.on('new_image', (data) => {
    var element = document.getElementById("carousel_images");
    element.innerHTML += '<div class="carousel-item" id="' + data + '"><img src=/"' + data + '.jpeg" class="d-block w-100"></div>'
    new Notification("New image found!");
})


socket.emit('get_settings', (data) => {
    for (const key in data['app']) {
        var element = document.getElementById(key);
        element.value = data['app'][key];
    }
    for (const key in data['instagram']) {
        var element = document.getElementById(key);
        element.value = data['instagram'][key];
    }
    for (const key in data['users']) {
        var element = document.getElementById("user_list");
        var inner = "<li>" + key;
        if (data['users'][key].length > 0) {
            inner += "<ul>";
            for (const user in data['users'][key]) {
                inner += "<li>" + user + "</li>";
            }
            inner += "</ul>";
        }
        element += inner + "</li>";
    }
});

function save_settings() {
    socket.emit('set_settings', {
        "app": {
            "time_between_scans": document.getElementById("time_between_scans").value,
            "time_between_follower_checks": document.getElementById("time_between_follower_checks").value,
            "degrees_of_separation": document.getElementById("degrees_of_separation").value
        },
        "instagram": {
            "username": document.getElementById("username").value,
            "password": document.getElementById("password").value,
            "totp": document.getElementById("totp").value
        }
    })
}

function hide() {
    var element = document.getElementsByClassName('carousel-item active');
    element.remove()
}


function false_positive() {
    var element = document.getElementsByClassName('carousel-item active');
    socket.emit('false_positive', element.id)
    element.remove()
}


if (!("Notification" in window)) {
    console.log("This browser does not support desktop notification");
}
if (Notification.permission !== 'denied') {
    Notification.requestPermission();
}

