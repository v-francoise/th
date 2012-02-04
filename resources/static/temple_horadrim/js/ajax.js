function callback_function(data){
//	alert(data.value);
	(function($) {
		$("#myid").html(data.value);
	})(django.jQuery);
}

function get_children(id){
	Dajaxice.temple_horadrim.get_children(callback_function,{'id': id});
}

function get_children_dajax(id){
	Dajaxice.temple_horadrim.get_children_dajax(Dajax.process,{'id': id});
}

(function($) {
	$(document).ready(function() {
		$('tr.row1, tr.row2').hover(function(){
		 row = $(this).children().children()
		 id_tab = $(row).attr("value");
		 alert("test");
		 get_children_dajax(id_tab);
		});
	});
})(django.jQuery);