// var review = document.querySelector("#opportunity-add");
var main = document.querySelector(".review-overlay");
var cancel = document.querySelector(".cancel-review");

// add_opp.addEventListener("click", function () {
// 	main.classList.add("bg-active");
// });

cancel.addEventListener("click", function () {
	main.classList.remove("bg-active");
});

var review_id ='';
var review_type = '';

const send_review = (id,type) => {
    document.getElementById('review').value = '';
    console.log(id);
    main.classList.add("bg-active");
    review_id = id
    review_type = type;
}

$("form#review_form").submit(function (e) {
    e.preventDefault();
    let formData = new FormData(this);
    formData.append('type', review_type);
    let url = "/send-review/"+review_id
    $.ajax({
        type: "POST",
        url: url,
        dataType: "json",
        cache: false,
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            alert("Review sent successfully!");
            main.classList.remove("bg-active");
            document.getElementById('review').value = '';
            location.reload();
        },
        error: function ($xhr) {
            data = $xhr.responseJSON;
            alert(data.error);
        },
    });
});