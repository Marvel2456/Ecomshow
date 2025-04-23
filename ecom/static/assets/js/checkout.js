document.addEventListener("htmx:afterRequest", (event) => {
    if (event.detail.xhr.status === 200) {
        const response = JSON.parse(event.detail.xhr.responseText);
        if (response.success) {
            // Close the modal
            const modal = document.querySelector("#bitcoinModal");
            if (modal) {
                const bootstrapModal = bootstrap.Modal.getInstance(modal);
                if (bootstrapModal) {
                    bootstrapModal.hide(); // Close the modal
                }
            }

            // Redirect to the products page
            window.location.href = "/products"; // Ensure this matches your Django URL pattern
        }
    } else if (event.detail.xhr.status === 400) {
        const response = JSON.parse(event.detail.xhr.responseText);
        alert("Error: " + JSON.stringify(response.errors)); // Show form errors
    }
});

// Optional: Redirect immediately when the button is clicked
document.querySelector(".btn-success").addEventListener("click", () => {
    const modal = document.querySelector("#bitcoinModal");
    if (modal) {
        const bootstrapModal = bootstrap.Modal.getInstance(modal);
        if (bootstrapModal) {
            bootstrapModal.hide(); // Close the modal
        }
    }
    window.location.href = "/products"; // Redirect to the products page
});