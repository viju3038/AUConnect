var edit_prof = document.querySelector("#profile-edit");
var main_prof = document.querySelector(".edit-overlay");
var close_prof = document.querySelector(".close-prof");

edit_prof.addEventListener("click", function () {
	main_prof.classList.add("bg-active");
});

close_prof.addEventListener("click", function () {
	main_prof.classList.remove("bg-active");
});

const profile_photo = document.querySelector(".profile-photo");
const imag = document.querySelector("#profile-img");

profile_photo.addEventListener("change", function () {
	const chosed_file = this.files[0];
	console.log(chosed_file);
	if (chosed_file) {
		const reader = new FileReader();
		reader.addEventListener("load", function () {
			imag.setAttribute("src", reader.result);
		});
		reader.readAsDataURL(chosed_file);
	}
});

const cover_photo = document.querySelector(".cov-photo");
const file_select = document.querySelector("#choose-cover-photo");
const cover_img = document.querySelector("#cover-img");

file_select.addEventListener("click", function () {
	if (cover_photo) {
		cover_photo.click();
	}
});

cover_photo.addEventListener("change", function () {
	console.log("Here");
	const chosed_file = this.files[0];
	console.log(chosed_file);
	if (chosed_file) {
		const reader = new FileReader();
		reader.addEventListener("load", function () {
			cover_img.setAttribute("src", reader.result);
		});
		reader.readAsDataURL(chosed_file);
	}
});

$("form#edit-prof").submit(function (e) {
	console.log("Ajax Call Made!");
	e.preventDefault();
	let formData = new FormData(this);
	$.ajax({
		type: "POST",
		url: "/profile/about/edit",
		dataType: "json",
		cache: false,
		data: formData,
		contentType: false,
		processData: false,
		success: function (data) {
			alert("Profile updated successfully!");
			main_prof.classList.remove("bg-active");
			location.reload();
		},
		error: function ($xhr) {
			data = $xhr.responseJSON;
			alert(data.error);
		},
	});
});

[].forEach.call(document.getElementsByClassName("tags-input edit-profile"), function (el) {
	let hiddenInput = document.createElement("input"),
		mainInput = document.createElement("input"),
		tags = [];

	hiddenInput.setAttribute("type", "hidden");
	hiddenInput.setAttribute("name", el.getAttribute("data-name"));

	mainInput.setAttribute("type", "text");
	mainInput.classList.add("main-input");
	mainInput.addEventListener("input", function () {
		let enteredTags = mainInput.value.split(",");
		if (enteredTags.length > 1) {
			enteredTags.forEach(function (t) {
				let filteredTag = filterTag(t);
				if (filteredTag.length > 0) addTag(filteredTag);
			});
			mainInput.value = "";
		}
	});

	mainInput.addEventListener("keydown", function (e) {
		let keyCode = e.which || e.keyCode;
		if (keyCode === 8 && mainInput.value.length === 0 && tags.length > 0) {
			removeTag(tags.length - 1);
		}
	});

	el.appendChild(mainInput);
	el.appendChild(hiddenInput);

	// addTag('hello!');

	function addTag(text) {
		let tag = {
			text: text,
			element: document.createElement("span"),
		};

		tag.element.classList.add("tag");
		tag.element.textContent = tag.text;

		let closeBtn = document.createElement("span");
		closeBtn.classList.add("close");
		closeBtn.addEventListener("click", function () {
			removeTag(tags.indexOf(tag));
		});
		tag.element.appendChild(closeBtn);

		tags.push(tag);

		el.insertBefore(tag.element, mainInput);

		refreshTags();
	}

	function removeTag(index) {
		let tag = tags[index];
		tags.splice(index, 1);
		el.removeChild(tag.element);
		refreshTags();
	}

	function refreshTags() {
		let tagsList = [];
		tags.forEach(function (t) {
			tagsList.push(t.text);
		});
		hiddenInput.value = tagsList.join(",");
	}

	function filterTag(tag) {
		return tag
			.replace(/[^\w -]/g, "")
			.trim()
			.replace(/\W+/g, "-");
	}

	el.getAttribute("data-value")
		.slice(1, -1)
		.split(",")
		.map(function (n) {
			addTag(n.trim().slice(1, -1));
		});
});
