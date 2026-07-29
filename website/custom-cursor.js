const cursor = document.createElement("div");
cursor.className = "custom-cursor";

const dot = document.createElement("div");
dot.className = "cursor-dot";

document.body.appendChild(cursor);
document.body.appendChild(dot);
document.addEventListener("mousemove", (e) => {
    cursor.style.left = e.clientX + "px";
    cursor.style.top = e.clientY + "px";

    dot.style.left = e.clientX + "px";
    dot.style.top = e.clientY + "px";
});
document.querySelectorAll("a, button").forEach((el) => {
    el.addEventListener("mouseenter", () => {
        cursor.classList.add("active");
    });

    el.addEventListener("mouseleave", () => {
        cursor.classList.remove("active");
    });
});