// Small client-side enhancement: dismiss status messages after a few seconds.
document.querySelectorAll(".flash").forEach((message) => {
  window.setTimeout(() => {
    message.classList.add("fade-out");
    window.setTimeout(() => message.remove(), 400);
  }, 4000);
});
