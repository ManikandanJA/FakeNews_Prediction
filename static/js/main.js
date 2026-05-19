// main.js - FakeNewsDetector
// Built by: Manikandan J.A.

document.addEventListener("DOMContentLoaded", function () {

  // Animate confidence bar
  const bar = document.querySelector(".conf-bar-fill");
  if (bar) {
    const targetWidth = bar.style.width;
    bar.style.width = "0%";
    setTimeout(() => { bar.style.width = targetWidth; }, 300);
  }

  // Auto-dismiss flash alerts after 4 seconds
  const alerts = document.querySelectorAll(".alert");
  alerts.forEach(a => {
    setTimeout(() => {
      a.style.transition = "opacity 0.6s";
      a.style.opacity = "0";
      setTimeout(() => a.remove(), 700);
    }, 4000);
  });

  // Textarea character counter
  const textarea = document.querySelector("textarea[name='news_text']");
  if (textarea) {
    textarea.addEventListener("input", function() {
      const len = this.value.length;
      let counter = document.getElementById("char-count");
      if (!counter) {
        counter = document.createElement("small");
        counter.id = "char-count";
        counter.style.cssText = "color:#718096;float:right;margin-top:4px;";
        this.parentNode.appendChild(counter);
      }
      counter.textContent = len + " characters";
    });
  }

});

// Quick test fill function (called from HTML)
function fillText(text) {
  const ta = document.querySelector("textarea[name='news_text']");
  if (ta) {
    ta.value = text;
    ta.dispatchEvent(new Event("input"));
    ta.focus();
  }
}

// Show loading state on form submit
document.addEventListener("DOMContentLoaded", function() {
  const form = document.querySelector("form[method='POST']");
  const btn  = document.getElementById("analyseBtn");
  if (form && btn) {
    form.addEventListener("submit", function() {
      btn.textContent = "⏳ Analysing... Please wait";
      btn.classList.add("btn-loading");
      btn.disabled = true;
    });
  }
});
