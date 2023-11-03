html1 = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TraderBot</title>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <form action="" onsubmit="sendQuestion(event)">
        <label>Token: 
            <input type="text" name="" id="token" autocomplete="off" value="kt-som3_V4lu3">
        </label>
        <button onclick="connect(event)">Connect</button>
        <label>Question: 
            <input type="text" name="" id="questionText" autocomplete="off">
        </label>
        <button>Send</button>
    </form>
    <ul id="messages"></ul>
    <script>
        var ws = null;
        function connect(event) {
            var token = document.getElementById("token")
            var ws = new WebSocket("ws://localhost:8000/ws?token=" + token.value);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            event.preventDefault()
        }
        function sendQuestion(event) {
            var input = document.getElementById("questionText")
            ws.send(input.value)
            input.value = ''
            event.preventDefault()
        }
    </script>
</body>
</html>
"""

html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TraderBot</title>
</head>
<body>
    <h1>WebSocket Chat</h1>
    <form action="" onsubmit="sendQuestion(event)">
        <!-- <label>Question:  -->
            <input type="text" name="" id="questionText" autocomplete="off">
        <!-- </label> -->
        <!-- <button onclick="connect(event)">Connect</button>
        -->
        <button>Send</button>
    </form>
    <ul id="messages"></ul>
    <script>
        // var ws = null;
        // function connect(event) {
        var ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            var content = document.createTextNode(event.data)
            message.appendChild(content)
            messages.appendChild(message)
        };
            //event.preventDefault()
        // }
        function sendQuestion(event) {
            var input = document.getElementById("questionText")
            ws.send(input.value)
            input.value = ''
            event.preventDefault()
        }
    </script>
</body>
</html>"""