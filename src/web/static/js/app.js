async function createWebhook() {
  const res = await fetch(API.webhooks, {
    method: "POST",
  });

  const data = await res.json();
  const webhook_id = data.webhook_url.split("/").pop();

  document.getElementById("result").innerHTML = `
        <div>
            <h3 class="fs-4">Webhook Created</h3>
            <div class="p-1 mx-auto mt-4 text-primary bg-primary-subtle border border-primary rounded-3">
                ${data.webhook_url}
            </div>
            <br/>
            <hr/>
            <div class="mt-3 text-center">
                <a href="/webhooks/${webhook_id}"
                    class="text-decoration-none p-2 mx-auto bg-outline-primary text-center border border-primary rounded-3 d-inline-block">
                    View Requests
                </a>
            </div>
        </div>
    `;
}
