document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("form");

    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const name = form.querySelector("input[name='name']").value.trim();
        const email = form.querySelector("input[name='email']").value.trim();
        const mobile = form.querySelector("input[name='mobile']").value.trim();

        if (!name || !email || !mobile) {
            alert("Please fill all required fields!");
            return;
        }

        if (!/^\d{10}$/.test(mobile)) {
            alert("Enter a valid 10-digit mobile number");
            return;
        }

        alert("Form submitted successfully! 🚀");
        form.reset();
    });
});