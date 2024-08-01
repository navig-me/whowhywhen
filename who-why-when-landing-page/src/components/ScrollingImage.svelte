<script>
	export let gifUrl;
</script>

<div class="gif-frame-wrapper">
	<div class="gif-frame">
		<img src={gifUrl} alt="Demo GIF" />
	</div>
</div>

<style>
	.gif-frame-wrapper {
		display: flex;
		justify-content: center;
		align-items: center;
		width: 100%;
	}

	.gif-frame {
		width: 70%;
		height: auto;
		position: relative;
		background: #000; /* Optional: background color for the frame */
		margin-top: -100px; /* Adjust to overlap the Hero section */
		margin-bottom: -50px; /* Adjust to overlap the Feature section */
		z-index: 2;
		box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
		border-radius: 10px;
		overflow: hidden;
	}

	.gif-frame img {
		width: 100%;
		height: auto;
		border-radius: 10px;
	}
</style>
