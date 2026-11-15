/**
 * MediResearch AI Frontend Client Logic
 * Multi-Agent Medical Researcher Interface
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const form = document.getElementById("medicalForm") || document.getElementById("legalForm");
  const questionInput = document.getElementById("questionInput");
  const charCount = document.getElementById("charCount");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const copyBtn = document.getElementById("copyBtn");

  const systemStatus = document.getElementById("systemStatus");
  const statusLabel = document.getElementById("statusLabel");
  const modelTag = document.getElementById("modelTag");

  const emptyView = document.getElementById("emptyView");
  const loadingView = document.getElementById("loadingView");
  const loadingLabel = document.getElementById("loadingLabel");
  const loadingCaption = document.getElementById("loadingCaption");

  const errorView = document.getElementById("errorView");
  const errorMsg = document.getElementById("errorMsg");

  const responseView = document.getElementById("responseView");
  const sourcesBlock = document.getElementById("sourcesBlock");
  const sourcesTags = document.getElementById("sourcesTags");
  const answerArticle = document.getElementById("answerArticle");
  const disclaimerNotice = document.getElementById("disclaimerNotice");

  const pipe1 = document.getElementById("pipe1");
  const pipe2 = document.getElementById("pipe2");
  const pipe3 = document.getElementById("pipe3");

  const printBtn = document.getElementById("printBtn");
  const memoTimestamp = document.getElementById("memoTimestamp");

  let latestAnswerRaw = "";
  let pipelineTimer = null;

  // Initialize
  verifyBackendStatus();

  // Character counter
  if (questionInput && charCount) {
    questionInput.addEventListener("input", () => {
      charCount.textContent = questionInput.value.length;
    });
  }

  // Suggestion chips
  document.querySelectorAll(".suggestion-chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (questionInput) {
        questionInput.value = btn.getAttribute("data-query");
        if (charCount) charCount.textContent = questionInput.value.length;
        questionInput.focus();
      }
    });
  });

  // Clear button
  if (clearBtn) {
    clearBtn.addEventListener("click", () => {
      if (questionInput) questionInput.value = "";
      if (charCount) charCount.textContent = "0";
      resetPipelineSteps();
      hideError();
      if (responseView) responseView.style.display = "none";
      if (copyBtn) copyBtn.style.display = "none";
      if (printBtn) printBtn.style.display = "none";
      if (emptyView) emptyView.style.display = "flex";
      if (questionInput) questionInput.focus();
    });
  }

  // Print button
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  // Copy button
  if (copyBtn) {
    copyBtn.addEventListener("click", async () => {
      if (!latestAnswerRaw) return;
      try {
        await navigator.clipboard.writeText(latestAnswerRaw);
        const span = copyBtn.querySelector("span");
        const prev = span.textContent;
        span.textContent = "Copied!";
        setTimeout(() => {
          span.textContent = prev;
        }, 1800);
      } catch (e) {
        console.error("Copy failed", e);
      }
    });
  }

  // Form submission
  if (form) {
    form.addEventListener("submit", async (e) => {
      e.preventDefault();
      const query = questionInput ? questionInput.value.trim() : "";

      if (!query || query.length < 5) {
        showError("Please enter a clinical question or scenario with at least 5 characters.");
        return;
      }

      startSubmission();

      try {
        const response = await fetch("/ask", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ question: query }),
        });

        const data = await response.json();

        if (!response.ok) {
          throw new Error(data.detail || `Server error (${response.status})`);
        }

        renderResponse(data);
      } catch (err) {
        showError(err.message || "An unexpected error occurred during medical analysis.");
      } finally {
        endSubmission();
      }
    });
  }

  // Backend Health Verification
  async function verifyBackendStatus() {
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error("Health check failed");
      const data = await res.json();

      if (data.status === "healthy") {
        if (systemStatus) systemStatus.classList.add("online");
        if (statusLabel) statusLabel.textContent = "Multi-Agent System Ready";
        if (modelTag) modelTag.textContent = data.model || "Connected";
      } else {
        throw new Error("Service degraded");
      }
    } catch {
      if (systemStatus) systemStatus.classList.add("offline");
      if (statusLabel) statusLabel.textContent = "Backend Disconnected";
      if (modelTag) modelTag.textContent = "Offline";
    }
  }

  // Submission Flow
  function startSubmission() {
    hideError();
    if (submitBtn) submitBtn.disabled = true;
    if (emptyView) emptyView.style.display = "none";
    if (responseView) responseView.style.display = "none";
    if (loadingView) loadingView.style.display = "flex";

    startPipelineSimulation();
  }

  function endSubmission() {
    if (submitBtn) submitBtn.disabled = false;
    if (loadingView) loadingView.style.display = "none";
    stopPipelineSimulation();
  }

  function startPipelineSimulation() {
    resetPipelineSteps();
    setStepActive(pipe1);
    if (loadingCaption) loadingCaption.textContent = "Step 1/3: Analyzing clinical parameters, vitals, and pathology...";

    pipelineTimer = setTimeout(() => {
      setStepCompleted(pipe1);
      setStepActive(pipe2);
      if (loadingCaption) loadingCaption.textContent = "Step 2/3: Searching clinical practice guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO)...";

      pipelineTimer = setTimeout(() => {
        setStepCompleted(pipe2);
        setStepActive(pipe3);
        if (loadingCaption) loadingCaption.textContent = "Step 3/3: Clinical Reviewer auditing drug interactions & contraindications...";
      }, 4000);
    }, 3000);
  }

  function stopPipelineSimulation() {
    if (pipelineTimer) clearTimeout(pipelineTimer);
  }

  function resetPipelineSteps() {
    [pipe1, pipe2, pipe3].forEach((p) => {
      if (!p) return;
      p.classList.remove("active", "completed");
    });
  }

  function setStepActive(stepEl) {
    if (!stepEl) return;
    stepEl.classList.remove("completed");
    stepEl.classList.add("active");
  }

  function setStepCompleted(stepEl) {
    if (!stepEl) return;
    stepEl.classList.remove("active");
    stepEl.classList.add("completed");
  }

  function markAllCompleted() {
    [pipe1, pipe2, pipe3].forEach((p) => {
      if (!p) return;
      p.classList.remove("active");
      p.classList.add("completed");
    });
  }

  // Render Response
  function renderResponse(data) {
    markAllCompleted();
    latestAnswerRaw = data.answer || "";

    if (memoTimestamp) {
      const now = new Date();
      memoTimestamp.textContent = `Generated: ${now.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    // Sources
    if (data.sources && data.sources.length > 0) {
      if (sourcesTags) {
        sourcesTags.innerHTML = data.sources
          .map((s) => `<span class="source-tag">${escapeHtml(s)}</span>`)
          .join("");
      }
      if (sourcesBlock) sourcesBlock.style.display = "block";
    } else {
      if (sourcesBlock) sourcesBlock.style.display = "none";
    }

    // Markdown formatted article
    if (answerArticle) {
      answerArticle.innerHTML = formatMarkdown(data.answer);
    }

    // Disclaimer
    if (disclaimerNotice) {
      disclaimerNotice.textContent = data.disclaimer || "";
    }

    if (responseView) responseView.style.display = "block";
    if (copyBtn) copyBtn.style.display = "inline-flex";
    if (printBtn) printBtn.style.display = "inline-flex";
  }

  // Error Banner
  function showError(msg) {
    if (errorMsg) errorMsg.textContent = msg;
    if (errorView) errorView.style.display = "flex";
    resetPipelineSteps();
  }

  function hideError() {
    if (errorView) errorView.style.display = "none";
    if (errorMsg) errorMsg.textContent = "";
  }

  // Simple Markdown Formatter
  function formatMarkdown(raw) {
    if (!raw) return "";

    let text = raw;

    // Bold section headers
    text = text.replace(/### (.*?)\n/g, '<h4 class="memo-subheading">$1</h4>');
    text = text.replace(/## (.*?)\n/g, '<h3 class="memo-heading">$1</h3>');

    // Bold text
    text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');

    // Bullet points
    text = text.replace(/^\s*-\s+(.*)$/gm, '<li class="memo-bullet">$1</li>');
    text = text.replace(/^\s*\*\s+(.*)$/gm, '<li class="memo-bullet">$1</li>');
    text = text.replace(/(<li class="memo-bullet">.*<\/li>\n?)+/g, '<ul class="memo-list">$&</ul>');

    // Numbered lists
    text = text.replace(/^\s*\d+\.\s+(.*)$/gm, '<li class="memo-numbered">$1</li>');

    // Paragraph breaks
    const paragraphs = text.split(/\n\s*\n/);
    const html = paragraphs
      .map((p) => {
        p = p.trim();
        if (!p) return "";
        if (p.startsWith("<h") || p.startsWith("<ul") || p.startsWith("<li")) {
          return p;
        }
        return `<p class="memo-p">${p.replace(/\n/g, "<br>")}</p>`;
      })
      .join("");

    return html;
  }

  function escapeHtml(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }
});
