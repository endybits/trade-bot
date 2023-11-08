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
	.loading-box {
		height: 10vh;
		display: flex;
		justify-content: center;
		align-items: center;
		/* background: FFF; */
	}
	.wave {
		width: 2px;
		height: 30px;
		background: linear-gradient(45deg, #4db6ac, cyan);
		margin: 5px;
		animation: wave 1s linear infinite;
		border-radius: 20px;
	}
	.wave:nth-child(2) {
		animation-delay: 0.1s;
	}
	.wave:nth-child(3) {
		animation-delay: 0.2s;
	}
	.wave:nth-child(3) {
		animation-delay: 0.2s;
	}
	.wave:nth-child(4) {
		animation-delay: 0.3s;
	}
	.wave:nth-child(5) {
		animation-delay: 0.4s;
	}
	.wave:nth-child(6) {
		animation-delay: 0.5s;
	}
	.wave:nth-child(7) {
		animation-delay: 0.6s;
	}
	.wave:nth-child(8) {
		animation-delay: 0.7s;
	}
	.wave:nth-child(9) {
		animation-delay: 0.8s;
	}
	.wave:nth-child(10) {
		animation-delay: 0.9s;
	}
	@keyframes wave {
		0% {
			transform: scale(0);
		}
		50% {
			transform: scale(1);
		}
		100% {
			transform: scale(0);
		}
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
				<!-- <li>
					<div class="loading-box">
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
						<div class="wave"></div>
					</div>
				</li> -->
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
		// Loading Animation
		function waitingMessage() {
			console.log("Waiting...");
			let messages = document.getElementById("message-list")
			let loadingMessage = document.createElement('li')
			loadingMessage.setAttribute('id', 'loading-item')
			let loadingBox = document.createElement('div')
			loadingBox.setAttribute('class', 'loading-box')
			for (let i = 0; i < 10; i++) {
				let wave = document.createElement('div')
				wave.setAttribute('class', 'wave')
				loadingBox.appendChild(wave);
			}
			loadingMessage.appendChild(loadingBox)
			messages.appendChild(loadingMessage)
		}
		function destroyItem(item){
			let messages = document.getElementById("message-list")
			messages.removeChild(item)
			// console.log('Item removed successfully!')
		}

		// WebSocket Connection and handler
		let ws = new WebSocket("ws://localhost:8000/ws");
		ws.onmessage = function(event) {
			let messages = document.getElementById("message-list")
			let message = document.createElement('li')
			response_value = event.data.trim();
            // Regular expression pattern for matching URLs
            let urlPattern = /^(https?|ftp):\/\/[^\s/$.?#].[^\s]*$/i;
			
			if (response_value == 'loading') {
				waitingMessage();
			}else {
				console.log("Message received");
				item = document.getElementById('loading-item')
				if (item) {
					destroyItem(item)
				}
				if (!urlPattern.test(response_value)) {
					let content = document.createTextNode(event.data)
					message.appendChild(content)
					messages.appendChild(message)
				}
				else {
					console.log("Valid URL");
					let img = document.createElement('img')
					img.src = response_value
					message.appendChild(img)
					messages.appendChild(message)
				}
			}
		}

    	// JavaScript code to handle the form submission
		document.getElementById('message-form').addEventListener('submit', function(event) {
			event.preventDefault();
			const messageInput = document.getElementById('message-input');
			const messageText = messageInput.value.trim();
			if (messageText) {
				let user_id = "4359"
				let json_input = '{"user_id": "' + user_id + '",' +
				'"question": "' + messageText + '"}';
				question_obj = JSON.stringify(json_input)
				ws.send(question_obj)
				messageInput.value = ''
			}
		});
	</script>
</body>
</html>
"""