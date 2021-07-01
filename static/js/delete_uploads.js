const delete_item = (type, id) => {
	console.log(type,id)
	$.ajax({
	    type: "DELETE",
	    url: "/" + type + "/delete/" + id,
	    success: function (data) {
	        alert(type + " deleted successfully!");
	        location.reload();
	    },
	    error: function ($xhr) {
	        data = $xhr.responseJSON;
	        alert(data.error);
	    },
	});
};
