<script>
    import { onMount } from 'svelte';
    import { Link, navigate } from 'svelte-routing';
    import { selectedProjectIdStore, clearToken } from '../stores/userStore';
    import { createEventDispatcher } from 'svelte';
    import Toast from '../components/Toast.svelte';
    import IntegrationSnippet from '../components/IntegrationSnippet.svelte';
    import { API_BASE_URL, DASH_API_BASE_URL } from '../config';

    let projects = [];
    let apiKeys = [];
    let newProjectName = '';
    let newApiKeyName = '';
    let showApiKeysModal = false;
    let selectedProjectId = null;
    let selectedProjectName = '';
    let toastMessage = '';
    let toastType = '';
    let showToast = false;
    let clientIp = '';
    let userAgent = navigator.userAgent;
    let clientLocation = {};
    let showIntegrationSnippet = false;
    let selectedApiKey = '';
    let showCurlModal = false;
    let curlCommand = '';
    let showDeleteConfirm = false;
    let apiKeyToDelete = null;
    let showNewProjectModal = false;
    let showNewApiKeyModal = false;

    const dispatch = createEventDispatcher();

    onMount(async () => {
        await fetchProjects();
        await fetchIpLocation();
    });

    async function fetchProjects() {
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me/projects`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            projects = await response.json();
        } else {
            showToastMessage('Failed to fetch projects', 'error');
        }
    }

    async function fetchIpLocation() {
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/ip-location`);
        if (response.ok) {
            const data = await response.json();
            clientIp = data.ip;
        } else {
            showToastMessage('Failed to fetch IP and location info', 'error');
        }
    }

    async function createProject() {
        if (projects.length >= 10) {
            showToastMessage('You have reached the maximum number of projects', 'error');
            return;
        }
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashauth/users/me/projects?project_name=${newProjectName}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            const project = await response.json();
            newProjectName = '';
            await fetchProjects();
            showToastMessage('Project created successfully', 'success');
            fetchApiKeys(project.id, project.name);  // Automatically open API keys popup
        } else {
            const errorData = await response.json();
            showToastMessage(errorData.detail || 'Failed to create project', 'error');
        }
        showNewProjectModal = false;  // Close the new project modal
    }

    async function fetchApiKeys(projectId, projectName) {
        selectedProjectId = projectId;
        selectedProjectName = projectName;
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/apikeys?user_project_id=${projectId}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            apiKeys = await response.json();
            showApiKeysModal = true;
        } else {
            showToastMessage('Failed to fetch API keys', 'error');
        }
    }

    async function createApiKey() {
        if (apiKeys.length >= 3) {
            showToastMessage('You have reached the maximum number of API keys for this project', 'error');
            return;
        }
        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/apikeys?user_project_id=${selectedProjectId}&name=${newApiKeyName}`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        if (response.ok) {
            newApiKeyName = '';
            await fetchApiKeys(selectedProjectId, selectedProjectName);
            showToastMessage('API key created successfully', 'success');
        } else {
            const errorData = await response.json();
            showToastMessage(errorData.detail || 'Failed to create API key', 'error');
        }
        showNewApiKeyModal = false;  // Close the new API key modal
    }

    function confirmDeleteApiKey(keyId) {
        apiKeyToDelete = keyId;
        showDeleteConfirm = true;
    }

    async function deleteApiKey() {
        if (!apiKeyToDelete) return;

        const token = localStorage.getItem('token');
        const response = await fetch(`${DASH_API_BASE_URL}/dashapi/apikeys/${apiKeyToDelete}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        if (response.ok) {
            await fetchApiKeys(selectedProjectId, selectedProjectName);
            showToastMessage('API key deleted successfully', 'success');
        } else {
            showToastMessage('Failed to delete API key', 'error');
        }
        apiKeyToDelete = null;
        showDeleteConfirm = false;
    }

    async function testApiKey(apiKey) {
        const response = await fetch(`${API_BASE_URL}/api/log`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-API-KEY': apiKey
            },
            body: JSON.stringify({
                url: 'www.whowhywhen.com/whowhywhen-test?q=test',
                ip_address: clientIp,
                user_agent: userAgent,
                response_code: 200
            })
        });
        if (response.ok) {
            showToastMessage('Test request successful', 'success');
        } else {
            showToastMessage('Test request failed', 'error');
        }

        // Generate the curl command
        openCurlModal(apiKey, clientIp, userAgent);
    }

    async function openCurlModal(apiKey, clientIp, userAgent) {
        curlCommand = `curl -X POST ${API_BASE_URL}/api/log \\
-H "Content-Type: application/json" \\
-H "X-API-KEY: ${apiKey}" \\
-d '{
  "url": "www.whowhywhen.com/whowhywhen-test?q=test",
  "ip_address": "${clientIp}",
  "user_agent": "${userAgent}",
  "response_code": 200
}'`;

        // Show the modal with the curl command
        showCurlModal = true;
    }

    function blurApiKey(apiKey, show) {
        return show ? apiKey : apiKey.slice(0, -4).replace(/./g, '*') + apiKey.slice(-4);
    }

    function logout() {
        clearToken();
        navigate('/');
    }

    function showToastMessage(message, type) {
        toastMessage = message;
        toastType = type;
        showToast = false; // Reset the toast visibility to force re-render
        setTimeout(() => {
            showToast = true;
        }, 0);
    }

    function handleProjectSelection(projectId, path) {
        selectedProjectIdStore.set(projectId); // Update the store with the selected project ID
    }

    function showIntegrationSnippetModal(apiKey) {
        selectedApiKey = apiKey;
        showIntegrationSnippet = true;
    }

    function closeIntegrationSnippetModal() {
        showIntegrationSnippet = false;
    }

    function closeCurlModal() {
        showCurlModal = false;
    }
</script>

<div class="projects-container">
    <h2>Your Projects</h2>
    {#if projects.length === 0}
        <p>No projects found. Create your first project to get started.</p>
    {/if}
    <div class="project-grid">
        {#each projects as project}
            <div class="project-card">
                <div class="project-header">
                    <span class="project-name">{project.name}</span>
                    {#if project.is_default}
                        <span class="default-star">★</span>
                    {/if}
                </div>
                <div class="project-actions">
                    <button class="btn-action" on:click={() => fetchApiKeys(project.id, project.name)}><i class="fas fa-key"></i> API Keys</button>
                    <Link to="/dashboard" class="btn-action" on:click={() => handleProjectSelection(project.id)}><i class="fas fa-tachometer-alt"></i> Dashboard</Link>
                    <Link to="/bots" class="btn-action" on:click={() => handleProjectSelection(project.id)}><i class="fas fa-robot"></i> Bot Requests</Link>
                </div>
            </div>
        {/each}
    </div>
    <button class="btn-new-project" on:click={() => showNewProjectModal = true}><i class="fas fa-plus"></i> New Project</button>

    {#if showNewProjectModal}
        <div class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => showNewProjectModal = false}>&times;</span>
                <h3>Create New Project</h3>
                <input type="text" bind:value={newProjectName} placeholder="Project Name" class="input-field" />
                <button class="btn-primary" on:click={createProject}><i class="fas fa-check"></i> Create Project</button>
            </div>
        </div>
    {/if}

    {#if showApiKeysModal}
        <div class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => showApiKeysModal = false}>&times;</span>
                <h3>API Keys for {selectedProjectName}</h3>
                <ul class="api-keys-list">
                    {#each apiKeys as key}
                        <li class="api-key-item">
                            <div class="api-key-details">
                                <span class="api-key-name">{key.name}</span>
                                <span class={key.show ? 'unblurred' : 'blurred'}>{blurApiKey(key.key, key.show)}</span>
                            </div>
                            <div class="api-key-actions">
                                <button class="btn-secondary" on:click={() => key.show = !key.show}>{key.show ? 'Hide' : 'Show'}</button>
                                <button class="btn-secondary" on:click={() => openCurlModal(key.key, clientIp, userAgent)}>cURL Command</button>
                                <button class="btn-secondary" on:click={() => showIntegrationSnippetModal(key.key)}>Integrate</button>
                                <button class="btn-secondary" on:click={() => testApiKey(key.key)}>Test API</button>
                                <button class="btn-secondary" on:click={() => confirmDeleteApiKey(key.id)}>Delete</button>
                            </div>
                        </li>
                    {/each}
                </ul>
                {#if apiKeys.length >= 3}
                    <p>You have reached the maximum number of API keys for this project. Delete an existing API key to create a new one.</p>
                {/if}
                <button class="btn-new-api-key" on:click={() => showNewApiKeyModal = true}>+ API Key</button>
            </div>
        </div>
    {/if}

    {#if showNewApiKeyModal}
        <div class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => showNewApiKeyModal = false}>&times;</span>
                <h3>Create New API Key</h3>
                <input type="text" bind:value={newApiKeyName} placeholder="API Key Name" class="input-field" />
                <button class="btn-primary" on:click={createApiKey}><i class="fas fa-check"></i> Create API Key</button>
            </div>
        </div>
    {/if}

    {#if showIntegrationSnippet}
        <IntegrationSnippet {selectedApiKey} clientIp={clientIp} userAgent={navigator.userAgent} close={closeIntegrationSnippetModal} />
    {/if}

    {#if showCurlModal}
        <div class="modal">
            <div class="modal-content wide">
                <span class="close" on:click={closeCurlModal}>&times;</span>
                <h3>cURL Command</h3>
                <pre>{curlCommand}</pre>
                <button class="btn-primary" on:click={closeCurlModal}><i class="fas fa-check"></i> Close</button>
            </div>
        </div>
    {/if}

    {#if showDeleteConfirm}
        <div class="modal">
            <div class="modal-content">
                <span class="close" on:click={() => showDeleteConfirm = false}>&times;</span>
                <h3>Confirm Deletion</h3>
                <p>Are you sure you want to delete this API key?</p>
                <button class="btn-secondary" on:click={deleteApiKey}><i class="fas fa-trash"></i> Yes, Delete</button>
                <button class="btn-primary" on:click={() => showDeleteConfirm = false}><i class="fas fa-times"></i> Cancel</button>
            </div>
        </div>
    {/if}
</div>

{#if showToast}
    <Toast message={toastMessage} type={toastType} />
{/if}

<style>
.projects-container {
    padding: 40px 20px;
    max-width: 1200px;
    margin: 0 auto;
    background-color: #f9f9f9;
    border-radius: 10px;
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.1);
    text-align: center;
}

h2, h3 {
    color: #663399;
    margin-bottom: 20px;
}

.project-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.project-card {
    background-color: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.project-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 6px 15px rgba(0, 0, 0, 0.2);
}

.project-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.project-name {
    font-weight: bold;
    font-size: 1.2rem;
    margin-right: 10px;
}

.default-star {
    color: #ff4000;
    font-size: 1.2rem;
}

.project-actions {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 20px;
}

.btn-action {
    background-color: #663399;
    color: #fff;
    padding: 10px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 5px;
    text-decoration: none;
    font-size: 0.9rem;
}

.btn-action:hover {
    background-color: #552288;
}

.input-field {
    width: calc(100% - 22px);
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 5px;
    margin-bottom: 20px;
}

.btn-new-project {
    background-color: #ff4000;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 20px;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 1rem;
}

.btn-new-project:hover {
    background-color: #e63900;
}

.btn-new-api-key {
    background-color: #ff4000;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-top: 20px;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 1rem;
}

.btn-new-api-key:hover {
    background-color: #e63900;
}

.modal {
    display: block;
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.5);
}

.modal-content {
    background-color: #fff;
    margin: 10% auto;
    padding: 30px;
    border: 1px solid #888;
    width: 80%;
    max-width: 800px;
    border-radius: 10px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.2);
    position: relative;
}

.modal-content.wide {
    width: 80%;
    max-width: 1000px;
}

.close {
    color: #aaa;
    position: absolute;
    top: 15px;
    right: 20px;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
}

.close:hover, .close:focus {
    color: black;
    text-decoration: none;
}

.blurred {
    filter: blur(4px);
}

.unblurred {
    filter: none;
}

.api-key-details {
    display: flex;
    align-items: center;
    justify-content: space-between;
    width: 100%;
}

.api-key-actions {
    display: flex;
    justify-content: space-between;
    width: 100%;
    margin-top: 10px;
}
.api-key-name {
    margin-right: 10px;
    font-weight: bold;
}

.create-api-key {
    margin-top: 20px;
}

pre {
    background-color: #f4f4f4;
    padding: 20px;
    border-radius: 5px;
    white-space: pre-wrap;
    word-wrap: break-word;
    text-align: left;
}

.btn-primary {
    background-color: #663399;
    color: #fff;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    margin-bottom: 20px;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 1rem;
}

.btn-primary:hover {
    background-color: #552288;
}

.btn-secondary {
    background-color: #ddd;
    color: #333;
    padding: 10px 20px;
    border: none;
    border-radius: 5px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    display: flex;
    align-items: center;
    gap: 5px;
    font-size: 1rem;
}

.btn-secondary:hover {
    background-color: #ccc;
}
</style>
