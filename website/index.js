document.score = 0;
document.AIScore = 0;
document.sliderValue = 170;
document.countdownLeft = 30;
document.AICheckInterval = 2000;
document.sliderTick = 117;

function sleep(ms) {
	return new Promise(resolve => setTimeout(resolve, ms));
}

function selectDifficulty(difficulty)
{
	if (difficulty=="easy") {document.AICheckInterval = 3000; document.sliderTick=177;}
	if (difficulty=="med")  {document.AICheckInterval = 2000; document.sliderTick=117;}
	if (difficulty=="hard") {document.AICheckInterval = 1500; document.sliderTick=88;}
	if (difficulty=="impossible") {document.AICheckInterval = 10; document.sliderTick=100000;}

	document.getElementById("selectDifficultyScreen").style.visibility = "hidden";
	document.getElementById("startScreen").style.visibility = "visible";
	startGameCountdown();
}

async function startGameCountdown()
{
	let i = 3;
	while(i > 0)
	{
		await sleep(1000);
		let timer = document.getElementById("startTimer");
		
		timer.innerHTML= --i;
	}

	document.getElementById("startScreen").style.visibility="hidden";
	await sleep(400);
	startGame();
	document.querySelector("input[name='captchaUser']").focus()
}

async function startGame()
{

	updateSlider();
	doCountdown();

	doFlash();

	while(true)
	{
		await sleep(document.AICheckInterval);
		checkAIAndResetClock();
	}
}

async function updateSlider()
{			
	await sleep(100);
	document.sliderBlocker = document.getElementById("blocker");
	
	while(true)
	{
		await sleep(document.sliderTick);
		document.sliderValue -= 10;
		console.log("updating sliderValue");
		document.sliderBlocker.style.width = "" + document.sliderValue + "px";
	}
}

async function doCountdown()
{	
	while(document.countdownLeft > 0)
	{
		await sleep(1000);
		let countdownElement = document.querySelector("p[name='countdown']");
		document.countdownLeft--;
		countdownElement.innerHTML = document.countdownLeft;
	}

	let winner = document.score > document.AIScore ? "User" : "AI";
	console.log(winner);
	
	if(winner == "User")
	{
		start();
		await sleep(1000);
		stop();
	}

	let endScreen = document.getElementById("endScreenWinner" + winner);
	console.log(endScreen);
	
	endScreen.style.visibility = "visible";

	document.getElementById("userScoreEndscreen" + winner).innerHTML = document.score;
	document.getElementById("AIScoreEndscreen" + winner).innerHTML = document.AIScore;

	document.AICheckInterval = 100000000;
	document.sliderTick = 1000000;
}

async function doFlash()
{
	let on = false;
	let flash = function(isOn)
	{
		if(!isOn)
		{
			document.querySelector("p[name='countdown']").style.color = "red";
			document.getElementById("zoningAgent").style.visibility="visible";	
		}
		else
		{
			document.querySelector("p[name='countdown']").style.color = "black";
			document.getElementById("zoningAgent").style.visibility="hidden";
		}
	}

	await sleep((document.countdownLeft - 8) * 1000);

	while(true)
	{
		let divisor = (3 - ((document.countdownLeft)/4));

		if(divisor == 0)
		{
			divisor = 1;
		}

		await sleep(Math.trunc(500 / divisor));
		console.log("slept for " + Math.trunc(500 / divisor) + "ms");
		on = !on;
		flash(on);
	}

}

async function checkAIAndResetClock()
{
	document.sliderValue = 170;
	let AIinput = document.querySelector("input[name='res']");
	handleInput(AIinput);
	await sleep(100);
}

async function handleInput(inputElement)
{
	console.log("input changed");
 	let input = inputElement.value;
 	if(input.length == 5 || input == "warming up...")
 	{
 		if(inputElement.name=="captchaUser")
 		{
 			res = await fetch("http://localhost:8080/submit/user?res=" + input);
 			response = await res.text();
 			console.log(response);
 		
 			document.score += response == "correct" ? 1 : -1;

 			document.getElementById("gameImage").src = "http://localhost:8080/user?" + new Date();

	 		document.getElementById("userText").innerHTML = document.score;

 			inputElement.value = "";
 		}
 		else
 		{
 			res = await fetch("http://localhost:8080/submit/AI?res=" + input);
 			response = await res.text();
 			console.log(response);
 		
 			document.AIScore += response == "correct" ? 1 : -1;

 			document.getElementById("gameImageAI").src = "http://localhost:8080/AI?" + new Date();

	 		document.getElementById("AIText").innerHTML = document.AIScore;

 			inputElement.value = "";
 		}
 	}
}

