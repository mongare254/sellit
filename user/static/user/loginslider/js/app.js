const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const containers = document.querySelector(".containers");

sign_up_btn.addEventListener("click", () => {
    containers.classList.add("sign-up-mode");
});

sign_in_btn.addEventListener("click", () => {
    containers.classList.remove("sign-up-mode");
});