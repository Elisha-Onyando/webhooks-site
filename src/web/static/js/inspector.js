// ── Tab switching ──────────────────────────────────────────
function switchTab(name, btn) {
    currentTab = name;
    document.querySelectorAll('#detail-tabs .nav-link').forEach(b => b.classList.remove('active'));
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('tab-' + name).classList.add('active');
}

// ── Select request ─────────────────────────────────────────
function selectRequest(id, el) {

    // Update sidebar active state
    document.querySelectorAll('.request-item').forEach(item => {
        item.classList.remove('active', 'bg-dark-subtle');
        item.style.borderLeftColor = 'transparent';
    });
    el.classList.add('active', 'bg-dark-subtle');
    el.style.borderLeftColor = 'bg-primary';

    // Show detail panel
    document.getElementById('no-selection').style.setProperty('display', 'none', 'important');
    document.getElementById('detail-view').style.setProperty('display', 'flex', 'important');

    // Populate from local data — no fetch needed
    populateRequestDetails(requests[id]);

    // Re-enforce active tab
    document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
    document.getElementById('tab-' + currentTab).classList.add('active');
}

function populateRequestDetails(requestData){
    // Header row
    document.getElementById('d-method').textContent = requestData.method;
    document.getElementById('d-method').className   = `badge border font-monospace method-${requestData.method}`;
    document.getElementById('d-id').textContent     = `Request Id: ${requestData.id}`;
    document.getElementById('d-type').textContent   = `Body Type: ${requestData.type || '_'}`;
    document.getElementById('d-time').textContent   = requestData.time;
    document.getElementById('d-ip').textContent     = requestData.ip;
    document.getElementById('d-size').textContent   = `${requestData.size} B`;

    // Headers table
    const headersTable = document.getElementById('headers-table');
    headersTable.innerHTML = Object.entries(requestData.headers)
        .map(([k, v]) => `<tr>
            <td class="text-secondary" style="width:35%;">${k}</td>
            <td class="text-light">${v}</td>
        </tr>`).join('');
    document.getElementById('badge-headers').textContent = Object.keys(requestData.headers).length;

    // Body
    document.getElementById('body-content').textContent = requestData.body
        ? JSON.stringify(requestData.body, null, 2) : '— No body content —';

    // Query params
    const queryTable = document.getElementById('query-table');
    const queryEntries = Object.entries(requestData.query);
    queryTable.innerHTML = queryEntries.length
        ? queryEntries.map(([k, v]) => `<tr>
            <td class="text-secondary" style="width:35%;">${k}</td>
            <td class="text-light">${v}</td>
        </tr>`).join('')
        : `<tr><td colspan="2" class="text-secondary text-center fst-italic py-3">No query parameters</td></tr>`;
    document.getElementById('badge-query').textContent = queryEntries.length;

    // Raw
    document.getElementById('raw-content').textContent = requestData.raw || '';
}

document.addEventListener('DOMContentLoaded', () => {
    const firstItem = document.querySelector('.request-item');
    if (firstItem) {
        selectRequest(firstItem.dataset.id, firstItem);
    }
});

// ── Copy endpoint URL ──────────────────────────────────────────
function copyEndpoint(){
    const url = document.getElementById('endpoint-url').textContent.trim();
    const icon = document.getElementById('copy-icon');
    const buttonText = document.getElementById('button-text');

    const markSuccess = () => {
        const originalText = buttonText.textContent;
        icon.className = 'bi bi-check2-circle text-success';
        buttonText.textContent = 'Copied';

        setTimeout(() => {
            icon.className = 'bi bi-clipboard';
            buttonText.textContent = originalText;
        }, 1800);
    };

    const markFail = () => {
        icon.className = 'bi bi-x-circle text-danger';
        setTimeout(() => icon.className = 'bi bi-clipboard', 1800);
    }

    if (navigator.clipboard && window.isSecureContext){
        navigator.clipboard.writeText(url).then(markSuccess).catch(markFail);
    } else {
        const textarea = document.createElement('textarea');
        textarea.value = url;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        try {
            document.execCommand('copy');
            markSuccess();
        } catch (e) {
            markFail();
        } finally {
            document.body.removeChild(textarea);
        }
    }
}

// ── Send test request ──────────────────────────────────────────
function sendTestRequest(btn){
    const webhookId = btn.dataset.webhookId;
    fetch(`/webhooks/${webhookId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            identifier: `UIREQ${Math.floor(10000 + Math.random() * 90000)}`,
            message: 'Testing the url from the UI',
            name: 'Lee Solutions'
        })
    }).then(() => location.reload());
}

// ── Delete request ──────────────────────────────────────────
function deleteRequest(btn){
    const webhookId = btn.dataset.webhookId;
    const requestId = btn.dataset.requestId;

    fetch(`${API.webhooks}/${webhookId}/requests/${requestId}`, {
        method: 'DELETE'
    }).then(() => location.reload());
}

// ── Clear webhook requests ──────────────────────────────────────────
function clearRequests(btn){
    const webhookId = btn.dataset.webhookId;
    fetch(`${API.webhooks}/${webhookId}/requests/clear`, {
        method: 'DELETE'
    }).then(() => location.reload());
}

// ── Filter sidebar ─────────────────────────────────────────
function filterRequests(query) {
    const q = query.toLowerCase();
    document.querySelectorAll('.request-item').forEach(item => {
        const text = (item.dataset.method + item.dataset.path + item.dataset.ip + item.dataset.id).toLowerCase();
        item.style.display = text.includes(q) ? '' : 'none';
    });
}
