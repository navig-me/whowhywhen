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
		padding: 20px 0;
		overflow: hidden;
		text-align: center;
	}

	.question-row {
		display: flex;
		white-space: nowrap;
		animation: scroll 180s linear infinite;
		gap: 40px;
	}

	.question-row:nth-child(odd) {
		animation-duration: 60s;
	}

	.question-row:nth-child(even) {
		animation-duration: 80s;
	}

	.question {
		font-family: 'Helvetica Neue', sans-serif;
		font-size: 0.8rem;
		font-weight: 700;
		color: #333;
		padding: 5px 10px;
		transition: transform 0.3s, background-color 0.3s;
		display: inline-block;
	}

	.question:hover {
		transform: scale(1.05);
		/* background-color: #e0e0e0; */
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
