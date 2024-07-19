<script>
	export let questions = [];

	let rows = [
		questions.slice(0, 10),
		questions.slice(10, 20),
		questions.slice(20, 30),
		questions.slice(30, 40)
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
		background: linear-gradient(to bottom, #e0e0e0, #f0f0f0);
		padding: 50px 0;
		overflow: hidden;
	}

	.question-row {
		display: flex;
		white-space: nowrap;
		animation: scroll 60s linear infinite;
		gap: 40px;
	}

	.question-row:nth-child(1) { color: #ff6f61; font-size: 1.4em; animation-duration: 35s; }
	.question-row:nth-child(2) { color: #6b5b95; font-size: 1.6em; animation-duration: 45s; }
	.question-row:nth-child(3) { color: #88b04b; font-size: 1.8em; animation-duration: 55s; }
	.question-row:nth-child(4) { color: #1f09e5; font-size: 2em; animation-duration: 65s; }

	.question {
		font-family: 'Helvetica Neue', sans-serif;
		font-weight: 500;
		text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
		transition: transform 0.3s, text-shadow 0.3s;
	}

	.question:hover {
		transform: scale(1.05);
		text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
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
