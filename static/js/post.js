document.querySelectorAll(".post-card").forEach((ele) => {
	const carouselImages = ele.querySelector(".post-items");
	const carouselButtons = ele.querySelectorAll("#carousel-button");
	const numberOfImages = ele.querySelectorAll(".post-items .post-item").length;
	let imageIndex = 0;
	let translateX = 0;

	carouselButtons.forEach((button) => {
		button.addEventListener("click", (event) => {
			if (event.target.className === "prev") {
				if (imageIndex !== 0) {
					imageIndex--;
					translateX += 100 / numberOfImages;
				}
			} else {
				if (imageIndex !== numberOfImages - 1) {
					imageIndex++;
					translateX -= 100 / numberOfImages;
				}
			}

			carouselImages.style.transform = `translateX(${translateX}%)`;
		});
	});
});
