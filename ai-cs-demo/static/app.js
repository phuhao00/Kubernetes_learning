const chatMessages = document.getElementById("chatMessages");
const chatForm = document.getElementById("chatForm");
const chatInput = document.getElementById("chatInput");
const faqList = document.getElementById("faqList");
const faqForm = document.getElementById("faqForm");
const humanQueue = document.getElementById("humanQueue");
const modeBadge = document.getElementById("modeBadge");

function appendMessage(role, content, meta = "") {
  const div = document.createElement("div");
  div.className = `msg ${role}${meta.includes("转人工") ? " escalated" : ""}`;
  div.innerHTML = `<div>${escapeHtml(content)}</div>${meta ? `<div class="msg-meta">${meta}</div>` : ""}`;
  chatMessages.appendChild(div);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function escapeHtml(text) {
  const d = document.createElement("div");
  d.textContent = text;
  return d.innerHTML;
}

async function sendMessage(text) {
  const message = text.trim();
  if (!message) return;
  appendMessage("user", message);
  chatInput.value = "";

  const res = await fetch("/api/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message }),
  });
  const data = await res.json();
  const meta = data.matched
    ? `✓ 知识库命中 · ${data.source === "llm" ? "LLM 润色" : "检索直答"}`
    : "⚠ 未命中 · 已转人工";
  appendMessage("assistant", data.reply, meta);
  loadHumanQueue();
}

chatForm.addEventListener("submit", (e) => {
  e.preventDefault();
  sendMessage(chatInput.value);
});

document.querySelectorAll("[data-prompt]").forEach((btn) => {
  btn.addEventListener("click", () => sendMessage(btn.dataset.prompt));
});

async function loadFaqs() {
  const res = await fetch("/api/admin/faq");
  const faqs = await res.json();
  document.getElementById("faqCount").textContent = faqs.length;
  faqList.innerHTML = faqs
    .map(
      (f) => `
    <div class="faq-item ${f.enabled ? "" : "disabled"}">
      <div class="q">${escapeHtml(f.question)}</div>
      <div class="a">${escapeHtml(f.answer)}</div>
      <div class="faq-actions">
        <button class="small" onclick="editFaq(${f.id})">编辑</button>
        <button class="small secondary" onclick="toggleFaq(${f.id}, ${!f.enabled})">${f.enabled ? "禁用" : "启用"}</button>
        <button class="small danger" onclick="deleteFaq(${f.id})">删除</button>
      </div>
    </div>`
    )
    .join("");
}

window.editFaq = async (id) => {
  const res = await fetch("/api/admin/faq");
  const faq = (await res.json()).find((f) => f.id === id);
  if (!faq) return;
  document.getElementById("faqId").value = faq.id;
  document.getElementById("faqQuestion").value = faq.question;
  document.getElementById("faqAnswer").value = faq.answer;
  document.getElementById("faqKeywords").value = faq.keywords;
  document.getElementById("faqEnabled").checked = faq.enabled;
};

window.toggleFaq = async (id, enabled) => {
  await fetch(`/api/admin/faq/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ enabled }),
  });
  loadFaqs();
};

window.deleteFaq = async (id) => {
  if (!confirm("确认删除该 FAQ？")) return;
  await fetch(`/api/admin/faq/${id}`, { method: "DELETE" });
  loadFaqs();
};

faqForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const id = document.getElementById("faqId").value;
  const body = {
    question: document.getElementById("faqQuestion").value,
    answer: document.getElementById("faqAnswer").value,
    keywords: document.getElementById("faqKeywords").value,
    enabled: document.getElementById("faqEnabled").checked,
  };
  if (id) {
    await fetch(`/api/admin/faq/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  } else {
    await fetch("/api/admin/faq", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
  }
  faqForm.reset();
  document.getElementById("faqId").value = "";
  loadFaqs();
});

document.getElementById("resetFormBtn").addEventListener("click", () => {
  faqForm.reset();
  document.getElementById("faqId").value = "";
});

document.getElementById("uploadCsvBtn").addEventListener("click", async () => {
  const file = document.getElementById("csvFile").files[0];
  if (!file) return alert("请选择 CSV 文件");
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/admin/faq/import-csv", { method: "POST", body: form });
  const data = await res.json();
  alert(`成功导入 ${data.imported} 条`);
  loadFaqs();
});

document.getElementById("pasteImportBtn").addEventListener("click", async () => {
  const text = document.getElementById("pasteArea").value;
  if (!text.trim()) return alert("请粘贴 CSV 内容");
  const res = await fetch("/api/admin/faq/import-text", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text }),
  });
  const data = await res.json();
  alert(`成功导入 ${data.imported} 条`);
  document.getElementById("pasteArea").value = "";
  loadFaqs();
});

async function loadHumanQueue() {
  const res = await fetch("/api/chat/human-queue");
  const items = await res.json();
  document.getElementById("humanCount").textContent = items.length;
  humanQueue.innerHTML = items.length
    ? items
        .map(
          (h) => `<div class="human-item"><strong>#${h.id}</strong> ${escapeHtml(h.user_message)}<br><span class="msg-meta">${h.created_at}</span></div>`
        )
        .join("")
    : "<p class='msg-meta'>暂无待处理</p>";
}

async function checkMode() {
  const res = await fetch("/api/health");
  await res.json();
  modeBadge.textContent = "检索模式（可配置 LLM）";
}

appendMessage("assistant", "您好！我是智能客服助手，请问有什么可以帮您？");
loadFaqs();
loadHumanQueue();
checkMode();
