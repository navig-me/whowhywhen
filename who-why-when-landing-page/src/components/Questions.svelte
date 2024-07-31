<script>
	export let questions = [];

	let rows = [
		questions.slice(0, 5),
		questions.slice(5, 10),
		questions.slice(10, 15),
		questions.slice(15, 20)
	];
</script>

<div class="scrolling-questions">
	{#each rows as row, index}
		<div class="question-row row-{index + 1}">
			{#each row.concat(row) as question}
				<div class="question">{question}</div>
			{/each}
		</div>
	{/each}
</div>

<style>
	.scrolling-questions {
		background: linear-gradient(to bottom, #f0f0f0, #e0e0e0);
		padding: 30px 0;
		overflow: hidden;
	}

	.question-row {
		display: flex;
		white-space: nowrap;
		animation: scroll 180s linear infinite;
		gap: 40px;
	}

	.question-row:nth-child(1) { 
		color: #ff4000; 
		font-size: 1em; 
		font-weight: bold;
		animation-duration: 35s; 
	}
	.question-row:nth-child(2) { 
		color: #ff7300; 
		font-size: 1.2em; 
		font-weight: bold;
		animation-duration: 45s; 
	}
	.question-row:nth-child(3) { 
		color: #7700ff; 
		font-size: 1.4em; 
		font-weight: bold;
		animation-duration: 55s; 
	}
	.question-row:nth-child(4) { 
		color: #663399; 
		font-size: 1.6em; 
		font-weight: bold;
		animation-duration: 65s; 
	}

	.question {
		font-family: 'Helvetica Neue', sans-serif;
		font-weight: 700;
		transition: transform 0.3s;
	}

	.question:hover {
		transform: scale(1.05);
	}

	@keyframes scroll {
		0% { transform: translateX(0); }
		100% { transform: translateX(-50%); }
	}

	@media (max-width: 768px) {
		.question-row {
			font-size: 0.8em;
		}
	}

	@media (max-width: 480px) {
		.question-row {
			font-size: 0.6em;
		}
	}
</style>
