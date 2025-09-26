const startBtn = document.getElementById("start-btn");
const userSpeech = document.getElementById("user-speech");
const robotResponse = document.getElementById("robot-response");
const pandaAvatar = document.getElementById("panda-avatar");
const teaServed = document.getElementById("tea-served");

const socket = new WebSocket("ws://localhost:8000/api/chat");

const pandaImages = {
	happy: "/frontend/img/panda_smiling.jpeg",
	sad: "/frontend/img/panda_crying.jpeg",
	calm: "/frontend/img/panda_calm.jpeg",
	neutral: "/frontend/img/panda_neutral.jpeg",
	angry: "/frontend/img/panda_angry.jpeg",
	clapping: "/frontend/img/panda_clapping.jpeg",
	dancing: "/frontend/img/panda_dancing.jpeg",
	surprised: "/frontend/img/panda_surprised.jpeg",
	thinking: "/frontend/img/panda_thinking.jpeg",
	thumbsup: "/frontend/img/panda_thubsup.jpeg",
	uhhuh: "/frontend/img/panda_uhhuh.jpeg",
};

socket.onmessage = (event) => {
	// Check if the message from the server is a button press event.
	if (event.data === "button_pressed") {
		// If so, simulate a click on the start button to begin speech recognition.
		startBtn.click();
		return;
	}

	const data = JSON.parse(event.data);
	robotResponse.textContent = `Robot: ${data.response}`;
	pandaAvatar.src = pandaImages[data.emotion] || pandaImages.neutral;

	const sugarAmount = document.getElementById("sugar-amount");
	const milkAmount = document.getElementById("milk-amount");

	if (data.tea) {
		teaServed.textContent = `Serving: ${data.tea}`;
		sugarAmount.textContent = `Sugar: ${data.sugar}`;
		milkAmount.textContent = `Milk: ${data.milk}`;
	} else {
		teaServed.textContent = "";
		sugarAmount.textContent = "";
		milkAmount.textContent = "";
	}

	const utterance = new SpeechSynthesisUtterance(data.response);
	utterance.lang = "ja-JP";
	utterance.rate = 2;
	window.speechSynthesis.speak(utterance);
};

startBtn.addEventListener("click", () => {
	userSpeech.textContent = "Listening...";
	teaServed.textContent = "";

	const recognition = new (
		window.SpeechRecognition || window.webkitSpeechRecognition
	)();
	recognition.lang = "ja-JP";
	recognition.onresult = (event) => {
		const transcript = event.results[0][0].transcript;
		userSpeech.textContent = `You: ${transcript}`;
		socket.send(transcript);
	};
	recognition.start();
});
