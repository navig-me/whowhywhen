  <script>
    export let message = '';
    export let type = 'info'; // Can be 'info', 'success', 'error'

    let show = true;

    $: {
      show = true;
      setTimeout(() => {
        show = false;
      }, 3000);
    }
  </script>

  {#if show}
    <div class="toast {type}">
      {message}
    </div>
  {/if}

  <style>
    .toast {
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      padding: 10px 20px;
      border-radius: 5px;
      box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
      color: white;
      font-weight: bold;
      z-index: 1000;
    }

    .toast.info {
      background-color: #663399;
    }

    .toast.success {
      background-color: #28a745;
    }

    .toast.error {
      background-color: #dc3545;
    }
  </style>
