html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        /* Style for the unordered list */
        ul {
        list-style-type: disc; /* Use a bullet point as the list marker */
        padding: 0; /* Remove default padding */
        margin: 20px 0; /* Add margin to create spacing around the list */
        }

        /* Style for list items */
        li {
        margin: 5px 0; /* Add margin to create vertical spacing between list items */
        padding-left: 20px; /* Add padding to create indentation for sublists */
        line-height: 1.4; /* Adjust line height for better readability */
        }
        /* Style for nested lists (sublists) */
        ul ul {
        list-style-type: circle; /* Use a different marker for nested lists */
        }
        li img {
            width:600px;
            
        }
    </style>
    <title>TraderBot</title>
</head>
<body>
    <div class="container mt-3">
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendQuestion(event)">
            <label>User: 
                <input type="text" name="" id="user_id" autocomplete="off" value="4359">
            </label>
            <label>Question: 
                <input type="text" name="" id="question" autocomplete="off">
            </label>
            <button>Send</button>
        </form>
        <ul id="messages" class="list-group list-group-flush" style="list-style: none;"></ul>
    </div>
    <script>
        var ws = new WebSocket("ws://localhost:8000/ws");
        ws.onmessage = function(event) {
            var messages = document.getElementById('messages')
            var message = document.createElement('li')
            message.classList.add('list-group-item')
            
            url_content_validator = event.data.trim();
            // Regular expression pattern for matching URLs
            var urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;

            if (!urlPattern.test(url_content_validator)) {
                console.log("Not URL");
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
                // You can do something with the valid URL here
            } else {
                console.log("Valid URL");
                var img = document.createElement('img')
                img.src = url_content_validator
                message.appendChild(img)
                messages.appendChild(message)
            }
        };
        function sendQuestion(event) {
            var question = document.getElementById("question")
            var user_id = document.getElementById("user_id")
            let json_input = '{"user_id": "' + user_id.value + '",' +
            '"question": "' + question.value + '"}';
            question_obj = JSON.stringify(json_input)
            console.log(json_input);
            console.log(question_obj);
            ws.send(question_obj)
            question.value = ''
            event.preventDefault()
        }
    </script>
</body>
</html>"""