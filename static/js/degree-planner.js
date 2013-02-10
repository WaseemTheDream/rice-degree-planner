var needsReload = false;

$(function() {
	$(".classes").append('<button class="add-class-button">+</button>');
	$(".add-class-button").click(function(){
		openAddClassPopup($(this).parents(".semester").data("term"));
	});
	$("#user-button").click(function(){
		openEditUserPopup();
	});
	$(".class .delete").click(function(){
		deleteClass($(this).parents(".class"));
	});
	$(".degree .delete").click(function(){
		deleteDegree($(this).parents(".degree"));
	});
	
	
	processBubbles();
	
});

function processBubbles(){
	$(".satified-by li").each(function(){		
		courseId = $(this).data('courseId');
		if(courseId){
			groupClasses = $(this).parents(".group").find(".progress").attr('class').split(' ');
			for(i in groupClasses){
				if(groupClasses[i].indexOf("group") > -1){
					groupClass = groupClasses[i]
				}
			}
			hours = "?";
			$("#schedule .class[data-course-id=\""+courseId+"\"]").find(".group-icons").append('<span class="group-icon '+groupClass+'">'+hours+'</span>');
		}
	});
}

function openAddClassPopup(term){
	html = '<div id="add-class-popup"><span class="popup-title">Enter Class Name</span><div id="search-container"><input type="text" name="search" id="search" /><input type="hidden" name="class_id" id="class_id" /><div class="note">Ex: COMP 140, PHIL 103, CAAM 335...</div></div><button id="submit-add-class" class="button">Add Class</button></div>';
	needsReload = false;
	$.fancybox(html, {
		afterClose : function() {
			if(needsReload){
				location.reload();
			}
			return;
		}
	});
	$("#submit-add-class").click(function(){
		submitAddClass($("#search").val(), term);
	});
	$("#search").keypress(function(event) {
		if ( event.which == 13) {
			submitAddClass($("#search").val(), term);
		}
   });
}

function submitAddClass(course, term){
	if(!$("#search").val()){
		$("#search").css("border-color","#F33");
		$("#search-container").effect("shake", { times:2, distance:5 }, 500);
	}else{
		data = {'term': term, 'course': course};		
		$.ajax({
			type: "POST",
			url: "/addCourse",
			data: {'json': JSON.stringify(data)},
			dataType: "json",
			success: function(data){
				if(data.success){
					needsReload = true;
					$.fancybox.close();
				}else{
					$("#search").css("border-color","#F33");
					$("#search-container").effect("shake", { times:2, distance:5 }, 500);
				}
			},
			error: function(data){
				$("#search").css("border-color","#F33");
				$("#search-container").effect("shake", { times:2, distance:5 }, 500);
			}
		});
		
		
	}
}

function openEditUserPopup(){
	$html = '<div id="edit-user-popup"><div class="info-table"><div class="info-row"><label for="name">Student Name</label><input type="text" name="name" id="name" /></div><div class="info-row"><label for="matricutlation_year">Matriculation Year</label><input type="text" name="matricutlation_year" id="matricutlation_year" /></div><div class="info-row"><label for="graduation_year">Expected Graduation Year</label><input type="text" name="graduation_year" id="graduation_year" /></div></div><button id="submit-edit-user" class="button">Save Changes</button></div>';
	$.fancybox($html);
	$("#submit-edit-user").click(function(){
		submitEditUser();
	});
}

function submitEditUser(){
	alert("I should be telling the server that you want to update info");
}

function deleteClass(x){
	data = {'id':x.data('courseTakenId')}
	$.post("/deleteCourse", {'json': JSON.stringify(data)});
	x.fadeOut();
}