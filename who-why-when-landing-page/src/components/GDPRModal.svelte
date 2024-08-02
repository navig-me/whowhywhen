<script>
    import { onMount } from 'svelte';
  
    export let isVisible = false;
    const cookieName = 'gdpr_accepted';
    
    function acceptGDPR() {
      document.cookie = `${cookieName}=true;path=/;max-age=31536000`;
      isVisible = false;
    }
  
    function checkGDPR() {
      const cookies = document.cookie.split(';').map(cookie => cookie.trim());
      isVisible = !cookies.some(cookie => cookie.startsWith(`${cookieName}=`));
    }
  
    onMount(() => {
      checkGDPR();
    });
  </script>
  
  {#if isVisible}
    <div class="gdpr-modal">
      <div class="gdpr-content">
        <p>We use cookies to ensure that we give you the best experience on our website. By continuing to use our site, you accept our use of cookies.</p>
        <button on:click={acceptGDPR}>Accept</button>
      </div>
    </div>
  {/if}
  
  <style>
    .gdpr-modal {
      position: fixed;
      bottom: 20px;
      right: 20px;
      width: 250px;
      background: rgba(0, 0, 0, 0.8);
      color: #fff;
      padding: 10px;
      box-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
      z-index: 1000;
      border-radius: 5px;
    }
  
    .gdpr-content {
      text-align: center;
      font-size: 0.9rem;
    }
  
    .gdpr-content p {
      margin: 0 0 10px;
    }
  
    .gdpr-content button {
      background-color: #ff4000;
      color: #fff;
      border: none;
      padding: 5px 10px;
      cursor: pointer;
      font-size: 0.8rem;
      border-radius: 3px;
      transition: background-color 0.3s ease;
    }
  
    .gdpr-content button:hover {
      background-color: #e63600;
    }
  </style>
  