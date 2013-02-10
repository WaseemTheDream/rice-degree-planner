$(function() {
	$(".classes").append('<button class="add-class-button">Add Class</button>');
	$(".add-class-button").click(function(){
		openAddClassPopup();
	});
});

function openAddClassPopup(){
	$html = '<div id="add-class-popup"><span class="popup-title">Enter Class Name</span><div id="search-container"><input type="text" name="search" id="search" /><input type="hidden" name="class_id" id="class_id" /><div class="note">Ex: COMP 140, PHIL 103, CAAM 335...</div></div><button id="submit-add-class" class="button">Add Class</button></div>';
	$.fancybox($html);
	$("#submit-add-class").click(function(){
		submitAddClass();
	});
	$("#search").autocomplete({
		source:"GetClasses.html",
		select:function(event, ui){
			$("#class_id").val(ui.item.class_id);
		}
	}).keypress(function(event) {
		if ( event.which == 13 ) {
			submitAddClass();
		}else{
			$("#class_id").val("");
		}
   });
}

function submitAddClass(){
	if(!$("#class_id").val()){
		$("#search").css("border-color","#F33");
		$("#search-container").effect("shake", { times:2, distance:5 }, 500);
	}else{
		alert("I should be telling the server that you want to add course \""+$("#class_id").val()+"\"");
		$.fancybox.close();
	}
}