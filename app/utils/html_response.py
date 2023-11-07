html = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TraderBot Assistant</title>
<style>
	body {
		font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
		margin: 0;
		padding: 0;
		background-color: #f4f7f6;
		display: flex;
		flex-direction: column;
		align-items: center;
		height: 100vh;
	}
	#chat-container {
		width: 100%;
		max-width: 800px; /* Maximum width of the chat interface */
		display: flex;
		flex-direction: column;
		margin-top: 20px; /* Added margin to the top */
		box-shadow: 0 0 10px 0 rgba(0,0,0,0.1);
		overflow: hidden; /* Prevents child elements from overflowing */
	}
	#header {
		/* background-color: #10a37f; */
		background-color: #4db6ac; 
		color: white;
		padding: 5px 20px;
		font-size: 0.8em;
		text-align: center;
	}
	#message-container {
		flex-grow: 1;
		overflow-y: auto;
		padding: 20px;
		background: #fff;
		height: calc(100vh - 60px);
	}
	ul {
		list-style-type: none;
		padding: 0;
		margin: 0;
	}
	li {
		margin-bottom: 10px;
		/* background: #e9e9e9; */
		padding: 10px;
		border-radius: 5px;
	}
	img {
		width:700px;
	}
	#input-container {
		padding: 10px;
		background: #eee;
		display: flex;
	}
	#message-form {
		display: flex;
		flex-grow: 1; /* Ensures the form fills the container */
	}
	textarea {
		flex-grow: 1;
		padding: 10px;
		border: 1px solid #ddd;
		border-radius: 4px;
		resize: vertical;
		margin-right: 10px; /* Space between textarea and button */
	}
	#send-button {
		padding: 10px 20px;
		background-color: #10a37f;
		border: none;
		border-radius: 4px;
		color: white;
		cursor: pointer;
		transition: background-color 0.3s;
	}
	#send-button:hover {
		background-color: #1a7f64;
	}
</style>
</head>
<body>
	<div id="chat-container">
		<div id="header">
			<h1>TraderBot</h1>
		</div>
		<div id="message-container">
			<ul id="message-list">
				<!-- List items will be added here by JavaScript -->
			</ul>
		</div>
		<div id="input-container">
			<form id="message-form" action="#" method="post">
				<textarea id="message-input" placeholder="Ask me about your trading history..." aria-label="Ask me about your trading history"></textarea>
				<button type="submit" id="send-button">Send</button>
			</form>
		</div>
	</div>

	<script>
		// WebSocket Connection and handler
		let ws = new WebSocket("ws://localhost:8000/ws");
		ws.onmessage = function(event) {
			let messages = document.getElementById("message-list")
			let message = document.createElement('li')
			url_content_validator = event.data.trim();
            // Regular expression pattern for matching URLs
            var urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
			if (!urlPattern.test(url_content_validator)) {
                console.log("Not URL");
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
			}
			else {
				console.log("Valid URL");
                var img = document.createElement('img')
                img.src = url_content_validator
                message.appendChild(img)
                messages.appendChild(message)
			}
		}


    	// JavaScript code to handle the form submission
		document.getElementById('message-form').addEventListener('submit', function(event) {
			event.preventDefault();
			const messageInput = document.getElementById('message-input');
			const messageText = messageInput.value.trim();
			if (messageText) {
				var user_id = "4359"
				let json_input = '{"user_id": "' + user_id + '",' +
				'"question": "' + messageText + '"}';
				question_obj = JSON.stringify(json_input)
				console.log(json_input);
				console.log(question_obj);
				ws.send(question_obj)
				messageInput.value = ''
			}
		});
		// const messageList = document.getElementById('message-list');
    	// for (let i = 0; i < 10; i++) { // Generates 1000 list items
		// 	const li = document.createElement('li');
		// 	li.textContent = `Message ${i + 1}`;
		// 	messageList.appendChild(li);
		// }
	</script>
</body>
</html>
"""