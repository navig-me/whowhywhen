<script>
    import { createEventDispatcher } from 'svelte';

    export let apiLogs = [];
    export let currentPage = 1;
    export let totalPages = 1;
    export let isTableLoading = false;
    const dispatch = createEventDispatcher();
    let showModal = false;
    let modalContent = [];
    let modalTitle = "";
    let showBlockModal = false;
    let blockContent = "";

    function handleCellClick(field, value) {
        dispatch('cellClick', { field, value });
    }

    function changePage(newPage) {
        if (newPage > 0 && newPage <= totalPages) {
            dispatch('changePage', { page: newPage });
        }
    }

    function showModalContent(title, content) {
        modalTitle = title;
        if (!content) {
            content = "No data available";
        }
        modalContent = content;
        showModal = true;
    }

    function closeModal() {
        showModal = false;
        modalContent = [];
        modalTitle = "";
    }

    function showBlockUserAgentModal(userAgent) {
        blockContent = `User-agent: ${userAgent}\nDisallow: /`;
        showBlockModal = true;
    }

    function closeBlockModal() {
        showBlockModal = false;
        blockContent = "";
    }

    function getDeviceIcon(log) {
        if (log.is_bot) {
            return "fa-robot";
        } else if (log.is_mobile || log.is_tablet) {
            return "fa-mobile";
        } else if (log.is_pc) {
            return "fa-desktop";
        }
        return "";
    }

    function handleFilterClick(field, value) {
        dispatch('addFilter', { field, value });
    }

    function getStatusColor(responseCode) {
        if (responseCode >= 200 && responseCode < 300) {
            return 'status-green';
        } else if (responseCode >= 300 && responseCode < 400) {
            return 'status-blue';
        } else if (responseCode >= 400 && responseCode < 500) {
            return 'status-orange';
        } else if (responseCode >= 500) {
            return 'status-red';
        }
        return '';
    }
</script>

<div class="logs-table">
    <h3>API Logs</h3>
    <div class="table-container">
        {#if isTableLoading}
            <div class="loading">Loading...</div>
        {:else}
            <table>
                <thead>
                    <tr>
                        <th></th>
                        <th>Path</th>
                        <th>IP Address</th>
                        <th>User Agent</th>
                        <th>Response Code</th>
                        <th>Response Time</th>
                        <th>Datetime</th>
                        <th>Query Parameters</th>
                    </tr>
                </thead>
                <tbody>
                    {#if apiLogs.length === 0}
                        <tr>
                            <td colspan="8">No logs available</td>
                        </tr>
                    {:else}
                        {#each apiLogs as log}
                            <tr>
                                <td class={getStatusColor(log.response_code)}></td>
                                <td>
                                    {log.path}
                                    <i class="fa fa-filter filter-icon" aria-hidden="true" on:click={() => handleFilterClick('path', log.path)}></i>
                                </td>
                                <td>
                                    {log.ip_address}
                                    <i class="fa fa-info-circle info-icon" aria-hidden="true" on:click={() => showModalContent("Location", log.location)}></i>
                                    <i class="fa fa-filter filter-icon" aria-hidden="true" on:click={() => handleFilterClick('ip_address', log.ip_address)}></i>
                                </td>
                                <td>
                                    <i class={`fa ${getDeviceIcon(log)} device-icon`} aria-hidden="true"></i>
                                    {log.user_agent}
                                    <i class="fa fa-info-circle info-icon" aria-hidden="true" on:click={() => showModalContent("User Agent Details", [
                                        { key: "Browser Family", value: log.user_agent_browser_family },
                                        { key: "Browser Version", value: log.user_agent_browser_version },
                                        { key: "OS Family", value: log.user_agent_os_family },
                                        { key: "OS Version", value: log.user_agent_os_version },
                                        { key: "Device Family", value: log.user_agent_device_family },
                                        { key: "Device Brand", value: log.user_agent_device_brand },
                                        { key: "Device Model", value: log.user_agent_device_model },
                                        { key: "Is Mobile", value: log.is_mobile },
                                        { key: "Is Tablet", value: log.is_tablet },
                                        { key: "Is PC", value: log.is_pc },
                                        { key: "Is Touch Capable", value: log.is_touch_capable },
                                        { key: "Is Bot", value: log.is_bot },
                                    ])}></i>
                                    <i class="fa fa-filter filter-icon" aria-hidden="true" on:click={() => handleFilterClick('user_agent', log.user_agent)}></i>
                                    <i class="fa fa-ban block-icon" aria-hidden="true" on:click={() => showBlockUserAgentModal(log.user_agent)}></i>
                                </td>
                                <td>
                                    {log.response_code}
                                    <i class="fa fa-info-circle info-icon" aria-hidden="true" on:click={() => showModalContent("Response Code", log.response_code_text)}></i>
                                    <i class="fa fa-filter filter-icon" aria-hidden="true" on:click={() => handleFilterClick('response_code', log.response_code)}></i>
                                </td>
                                <td>{log.response_time}</td>
                                <td>{new Date(log.created_at).toLocaleString()}</td>
                                <td>
                                    {log.query_params.length}
                                    <i class="fa fa-info-circle info-icon" aria-hidden="true" on:click={() => showModalContent("Query Parameters", log.query_params)}></i>
                                </td>
                            </tr>
                        {/each}
                    {/if}
                </tbody>
            </table>
        {/if}
    </div>
    <div class="pagination">
        <button on:click={() => changePage(1)} disabled={currentPage === 1}>First</button>
        <button on:click={() => changePage(currentPage - 1)} disabled={currentPage === 1}>Previous</button>
        <button disabled>{currentPage}</button>
        <button on:click={() => changePage(currentPage + 1)} disabled={currentPage === totalPages}>Next</button>
        <button on:click={() => changePage(totalPages)} disabled={currentPage === totalPages}>Last</button>
    </div>
</div>

{#if showModal}
    <div class="modal">
        <div class="modal-content">
            <span class="close" on:click={closeModal}>&times;</span>
            <h3>{modalTitle}</h3>
            {#if modalTitle === "Query Parameters"}
                {#if modalContent.length === 0}
                    <p>No query parameters available</p>
                {:else}
                    <table>
                        <thead>
                            <tr>
                                <th>Key</th>
                                <th>Value</th>
                            </tr>
                        </thead>
                        <tbody>
                            {#each modalContent as param}
                                <tr>
                                    <td>{param.key}</td>
                                    <td>{param.value}</td>
                                </tr>
                            {/each}
                        </tbody>
                    </table>
                {/if}
            {:else if modalTitle === "User Agent Details"}
                <div class="user-agent-details">
                    <div class="section">
                        <h4>Browser</h4>
                        <table>
                            <tbody>
                                <tr>
                                    <td>Family</td>
                                    <td>{modalContent.find(item => item.key === "Browser Family").value}</td>
                                </tr>
                                <tr>
                                    <td>Version</td>
                                    <td>{modalContent.find(item => item.key === "Browser Version").value}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="section">
                        <h4>OS</h4>
                        <table>
                            <tbody>
                                <tr>
                                    <td>Family</td>
                                    <td>{modalContent.find(item => item.key === "OS Family").value}</td>
                                </tr>
                                <tr>
                                    <td>Version</td>
                                    <td>{modalContent.find(item => item.key === "OS Version").value}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="section">
                        <h4>Device</h4>
                        <table>
                            <tbody>
                                <tr>
                                    <td>Family</td>
                                    <td>{modalContent.find(item => item.key === "Device Family").value}</td>
                                </tr>
                                <tr>
                                    <td>Brand</td>
                                    <td>{modalContent.find(item => item.key === "Device Brand").value}</td>
                                </tr>
                                <tr>
                                    <td>Model</td>
                                    <td>{modalContent.find(item => item.key === "Device Model").value}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="section">
                        <h4>Capabilities</h4>
                        <div class="capabilities">
                            {#if modalContent.find(item => item.key === "Is Mobile").value}
                                <i class="fa fa-mobile mobile" aria-hidden="true" title="Mobile"></i>
                            {/if}
                            {#if modalContent.find(item => item.key === "Is Tablet").value}
                                <i class="fa fa-tablet tablet" aria-hidden="true" title="Tablet"></i>
                            {/if}
                            {#if modalContent.find(item => item.key === "Is PC").value}
                                <i class="fa fa-desktop pc" aria-hidden="true" title="PC"></i>
                            {/if}
                            {#if modalContent.find(item => item.key === "Is Touch Capable").value}
                                <i class="fa fa-hand-pointer-o touch" aria-hidden="true" title="Touch Capable"></i>
                            {/if}
                            {#if modalContent.find(item => item.key === "Is Bot").value}
                                <i class="fa fa-robot bot" aria-hidden="true" title="Bot"></i>
                            {/if}
                        </div>
                    </div>
                </div>
            {:else}
                <p>{modalContent}</p>
            {/if}
        </div>
    </div>
{/if}

{#if showBlockModal}
    <div class="modal">
        <div class="modal-content">
            <span class="close" on:click={closeBlockModal}>&times;</span>
            <h3>Block User Agent</h3>
            <p>To block the user agent, add the following line to your robots.txt file:</p>
            <pre>{blockContent.split('\n')[0]}<br/>Disallow: /</pre>
        </div>
    </div>
{/if}

<style>
    .logs-table {
        flex: 1;
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        max-width: 100%;
        overflow-x: auto;
    }

    .table-container {
        height: 400px;
        overflow-y: auto;
    }

    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.8em;
        cursor: pointer;
        margin-bottom: 10px;
    }

    th, td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    th {
        background-color: #663399;
        color: white;
        font-size: 1.1em;
    }

    tr:hover {
        background-color: #f1f1f1;
    }

    .pagination {
        display: flex;
        justify-content: center;
        gap: 5px;
        margin-top: 20px;
    }

    .pagination button {
        padding: 5px 10px;
        border: 1px solid #663399;
        background-color: #fff;
        color: #663399;
        cursor: pointer;
        border-radius: 5px;
    }

    .pagination button.active {
        background-color: #663399;
        color: #fff;
    }

    .pagination button:disabled {
        background-color: #ddd;
        color: #666;
        cursor: not-allowed;
    }

    .loading {
        text-align: center;
        padding: 20px;
        font-size: 1.2em;
        color: #663399;
    }

    .modal {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(0, 0, 0, 0.5);
    }

    .modal-content {
        background: #fff;
        padding: 20px;
        border-radius: 10px;
        width: 50%;
        max-height: 80%;
        overflow-y: auto;
        text-align: left;
    }

    .close {
        float: right;
        font-size: 1.5em;
        cursor: pointer;
    }

    .info-icon {
        margin-left: 5px;
        cursor: pointer;
        color: #663399;
    }

    .device-icon {
        margin-right: 5px;
    }

    .filter-icon {
        margin-left: 5px;
        cursor: pointer;
        color: #666;
    }

    .filter-icon:hover {
        color: #333;
    }

    .block-icon {
        margin-left: 5px;
        cursor: pointer;
        color: #ff0000; /* Red color */
    }

    .block-icon:hover {
        color: #cc0000; /* Darker red on hover */
    }

    .query-params table,
    .user-agent-details table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9em;
    }

    .query-params th, .query-params td,
    .user-agent-details th, .user-agent-details td {
        border: 1px solid #ddd;
        padding: 8px;
        text-align: left;
    }

    .query-params th, .user-agent-details th {
        background-color: #663399;
        color: white;
    }

    .query-params tr:hover, .user-agent-details tr:hover {
        background-color: #f1f1f1;
    }

    .user-agent-details .section {
        margin-bottom: 20px;
    }

    .user-agent-details h4 {
        margin-bottom: 10px;
        color: #663399;
    }

    .capabilities i {
        margin-right: 10px;
        font-size: 1.5em;
    }

    .mobile { color: #4caf50; }
    .tablet { color: #ff9800; }
    .pc { color: #2196f3; }
    .touch { color: #9c27b0; }
    .bot { color: #f44336; }

    pre {
        background: #f5f5f5;
        padding: 10px;
        border-radius: 5px;
        white-space: pre-wrap;
        word-wrap: break-word;
        margin: 10px 0;
    }

    .status-green {
        background-color: #4caf50;
        width: 4px;
    }

    .status-blue {
        background-color: #2196f3;
        width: 4px;
    }

    .status-orange {
        background-color: #ff9800;
        width: 4px;
    }

    .status-red {
        background-color: #f44336;
        width: 4px;
    }
</style>

<!-- Font Awesome CDN for icons -->
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
