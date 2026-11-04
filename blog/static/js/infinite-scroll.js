(() => {
    const grid = document.querySelector("[data-post-grid]");
    const controls = document.querySelector("[data-scroll-controls]");
    const nextLink = controls?.querySelector("[data-next-page]");
    if (!grid || !nextLink || !("IntersectionObserver" in window)) return;

    const status = controls.querySelector("[data-scroll-status]");
    let loading = false;
    let failed = false;

    async function loadMore() {
        if (loading || nextLink.hidden) return;
        loading = true;
        grid.setAttribute("aria-busy", "true");
        nextLink.setAttribute("aria-disabled", "true");
        status.textContent = "Loading more posts…";

        try {
            const response = await fetch(nextLink.href);
            if (!response.ok) throw new Error(`Could not load posts (${response.status})`);
            const page = new DOMParser().parseFromString(await response.text(), "text/html");
            const cards = page.querySelectorAll("[data-post-grid] > [data-post-card]");
            if (!cards.length) throw new Error("The next page contained no posts");

            grid.append(...cards);
            failed = false;
            const nextPage = page.querySelector("[data-next-page]");
            if (nextPage) {
                nextLink.href = nextPage.href;
                status.textContent = `${cards.length} more posts loaded.`;
            } else {
                nextLink.hidden = true;
                observer.disconnect();
                status.textContent = "You've reached the end of the blog.";
            }
        } catch (error) {
            failed = true;
            console.error("Failed to load more blog posts:", error);
            status.textContent = "Could not load more posts. Select Load more posts to retry.";
        } finally {
            loading = false;
            grid.removeAttribute("aria-busy");
            nextLink.removeAttribute("aria-disabled");
        }
    }

    const observer = new IntersectionObserver(entries => {
        if (entries.some(entry => entry.isIntersecting) && !failed) loadMore();
    }, { rootMargin: "300px" });

    nextLink.addEventListener("click", event => {
        event.preventDefault();
        loadMore();
    });
    document.querySelector("[data-pagination]").hidden = true;
    observer.observe(controls);
})();
