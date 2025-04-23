document.addEventListener("htmx:afterSwap", (event) => {
    if (event.detail.target.id === "payment-response") {
        const modal = document.querySelector("#bitcoinModal");
        if (modal) {
            const bootstrapModal = new bootstrap.Modal(modal);
            bootstrapModal.show();
        }
    }
});