<script>
    let activeTab = 'JavaScript';
  
    const tabs = [
      { name: 'JavaScript', code: '/* JavaScript Code */' },
      { name: 'Python', code: '/* Python Code */' },
      { name: 'Ruby', code: '/* Ruby Code */' },
      // Add more tabs here as needed
    ];
  
    function setActiveTab(tab) {
      activeTab = tab.name;
    }
  
    function copyToClipboard(code) {
      navigator.clipboard.writeText(code).then(() => {
        alert('Code copied to clipboard');
      }, (err) => {
        alert('Failed to copy code: ', err);
      });
    }
  </script>
  
  <section class="snippet-section">
    <div class="container">
      <h2>Integration Code Snippets</h2>
      <div class="tabs">
        {#each tabs as tab}
          <button
            class:active={activeTab === tab.name}
            on:click={() => setActiveTab(tab)}
          >
            {tab.name}
          </button>
        {/each}
      </div>
      <div class="snippets">
        {#each tabs as tab}
          {#if activeTab === tab.name}
            <div class="snippet">
              <h3>{tab.name}</h3>
              <button class="copy-btn" on:click={() => copyToClipboard(tab.code)}>Copy</button>
              <pre><code>{tab.code}</code></pre>
            </div>
          {/if}
        {/each}
      </div>
    </div>
  </section>
  
  <style>
    .snippet-section {
      padding: 60px 0;
      text-align: center;
      background: #663399;
      color: #fff;
    }
  
    .tabs {
      margin-bottom: 20px;
      display: flex;
      justify-content: center;
      flex-wrap: wrap;
    }
  
    .tabs button {
      background-color: #fff;
      border: 1px solid #fff;
      color: #663399;
      padding: 10px 20px;
      margin: 5px;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s, color 0.3s;
    }
  
    .tabs button.active {
      background-color: #fff;
      color: #663399;
    }
  
    .tabs button:hover:not(.active) {
      background-color: #ddd;
    }
  
    .snippets {
      display: flex;
      justify-content: center;
      margin-top: 20px;
    }
  
    .snippet {
      width: 100%;
      max-width: 600px;
      background: #fff;
      padding: 20px;
      border-radius: 10px;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
      transition: transform 0.3s, box-shadow 0.3s;
      position: relative;
    }
  
    .snippet:hover {
      transform: translateY(-10px);
      box-shadow: 0 6px 30px rgba(0, 0, 0, 0.2);
    }
  
    .snippet h3 {
      color: #663399;
    }
  
    .copy-btn {
      position: absolute;
      top: 10px;
      right: 10px;
      background: #663399;
      color: #fff;
      border: none;
      padding: 5px 10px;
      border-radius: 5px;
      cursor: pointer;
      transition: background-color 0.3s;
    }
  
    .copy-btn:hover {
      background: #552288;
    }
  
    pre {
      background: #f0f0f0;
      padding: 15px;
      border-radius: 5px;
      text-align: left;
      white-space: pre-wrap;
      word-wrap: break-word;
      margin-top: 20px;
    }
  
    pre code {
      display: block;
      padding: 10px;
      border-radius: 5px;
      background: #fff;
      color: #333;
    }
  </style>
  