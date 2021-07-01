var add_workexp = document.querySelector('#work-exp');
var main_workexp = document.querySelector('.workexp-overlay');
var close_workexp = document.querySelector('.close-workexp');

add_workexp.addEventListener('click', function () {
    main_workexp.classList.add('bg-active');
});

close_workexp.addEventListener('click', function () {
    main_workexp.classList.remove('bg-active');
});

$("form#work_exp").submit(function (e) {
    console.log("Ajax Call Made!");
    e.preventDefault();
    let formData = new FormData(this);
    $.ajax({
        type: "POST",
        url: "/add-work-exp/",
        dataType: 'json',
        cache: false,
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
            alert("Congratulations on your new work experience!!");
            main_workexp.classList.remove("bg-active");
        },
        error: function ($xhr) {
            data = $xhr.responseJSON;
            alert(data.error);
		},
    });
});