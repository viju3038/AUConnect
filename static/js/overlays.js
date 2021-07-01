var add_opp = document.querySelector("#opportunity-add");
var main_opp = document.querySelector(".opp-overlay");
var close = document.querySelector(".close-opp");

add_opp.addEventListener("click", function () {
	$('#opp_form')[0].reset();
	main_opp.classList.add("bg-active");
});

close.addEventListener("click", function () {
	main_opp.classList.remove("bg-active");
});

var add_res = document.querySelector("#resource-add");
var main_res = document.querySelector(".resource-overlay");
var close_res = document.querySelector(".close-res");

add_res.addEventListener("click", function () {
	$('#res_form')[0].reset();
	main_res.classList.add("bg-active");
});

close_res.addEventListener("click", function () {
	main_res.classList.remove("bg-active");
});

var add_post = document.querySelector("#post-add");
var main_post = document.querySelector(".post-overlay");
var close_post = document.querySelector(".close-post");

add_post.addEventListener("click", function () {
	$('#post_form')[0].reset();
	main_post.classList.add("bg-active");
});

close_post.addEventListener("click", function () {
	main_post.classList.remove("bg-active");
});

$("form#opp_form").submit(function (e) {

	console.log("Ajax Call Made!");
	e.preventDefault();
	let formData = new FormData(this);
	$.ajax({
		type: "POST",
		url: "/add-opportunity/",
		dataType: "json",
		cache: false,
		data: formData,
		contentType: false,
		processData: false,
		success: function (data) {
			alert("Opportunity added successfully!");
			$('#opp_form')[0].reset();
			main_opp.classList.remove("bg-active");
			location.reload();
		},
		error: function ($xhr) {
			data = $xhr.responseJSON;
			alert(data.error);
		},
	});
});

$("form#post_form").submit(function (e) {
	
	console.log("Ajax Call Made!");
	e.preventDefault();
	let formData = new FormData(this);
	$.ajax({
		type: "POST",
		url: "/add-post/",
		dataType: "json",
		cache: false,
		data: formData,
		contentType: false,
		processData: false,
		success: function (data) {
			alert("Post added successfully!");
			$('#post_form')[0].reset();
			main_post.classList.remove("bg-active");
			location.reload();
		},
		error: function ($xhr) {
			
			data = $xhr.responseJSON;
			alert(data.error);
		},
	});
});

$("form#res_form").submit(function (e) {
	console.log("Ajax Call Made!");
	e.preventDefault();
	let formData = new FormData(this);
	$.ajax({
		type: "POST",
		url: "/add-resource/",
		dataType: "json",
		cache: false,
		data: formData,
		contentType: false,
		processData: false,
		success: function (data) {
			alert("Resource added successfully!");
			$('#res_form')[0].reset();
			main_res.classList.remove("bg-active");
			location.reload();
		},
		error: function ($xhr) {
			data = $xhr.responseJSON;
			alert(data.error);
		},
	});
});

[].forEach.call(document.getElementsByClassName("tags-input add"), function (el) {
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
});
