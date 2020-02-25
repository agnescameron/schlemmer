    var ws = new WebSocket('ws://localhost:8765');
    // event emmited when connected
    ws.onopen = function () {
        console.log('websocket 1 is connected ...')
        // sending a send event to websocket server
        ws.send('connected')
    }
    // event emmited when receiving message 
    ws.onmessage = function (ev) {
        console.log(ev.data);
        document.body.style.backgroundColor = ev.data;
    }
