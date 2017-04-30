home_prefix = 'http://cs-sys-1.uis.georgetown.edu/~jw1498/test/';

function getCount(){
    $.ajax({
        url: "countHandler.cgi",
        data:{
            topic_id: tid
        },
        success: function(response){
            $("#total_count").html(response);
        }
    })
}

function lockscreen(){
    $screen_lock = $("<div class='screen-cover'></div>");
    $screen_lock.css({
        "position" : "absolute",
        "z-index" : 10000,
        "background-color" : "#000",
        "opacity" : 0.15,
        "cursor": "wait"
    });
    $screen_lock.width($("body").width());
    $screen_lock.height($("body").height());
    $screen_lock.prependTo($("body"));
}

function moodFeedback(m){
    r = window.prompt("Are you " +m +" at this moment? It is about which document/query/subtopic? What do you want to search? Tell us why:");
    if (r != null){
        $.ajax({
            method: "post",
            url: "./moodFeedback.cgi",
            data:{
                mood: m,
                reason: r,
                topic_id: tid,
                source: mode
            }
        })
    }   
}

function runQuery(){
    mode = "N" //search from query box is normal search
    url = dict["domains"][1]
    level = 'L';
    para = "T=" + tid + "&Mode="+mode+"&q=" + encodeURIComponent($("#querybox").val());
    thequery = $("#querybox").val();
    search_signal = 1;
    // ?? set mode or level ??
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();

    $.ajax({
        method: "post",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            query: thequery,
            flag: 'query'
        },
        success:function(response) {
            $("#lemurbox").attr("src", home_prefix + url + "?" + para);
        }
    })
    
    // if parent.tname == '' #lemurdiscard.hide()
}

function structureQuery(field){ //format of structure query:  fieldName:value;   ex.  phone:2021234567
    mode = "S" //abbreviation for structured query
    q = "" //query
    if (field == "phone") {
        if ($("#phoneInput").val()) {
            q = "phone:"+$("#phoneInput").val()+";";
        }
    } else if (field == "email") {
        if ($("#emailInput").val()) {
            q = "email:"+$("#emailInput").val()+";"
        }
    } else if (field == "name") {
        if ($("#nameInput").val()) {
            q = "name:"+$("#nameInput").val()+";"
        }
    } else if (field == "socialMedia") {
        if (("#socialMediaInput").val() && $("#socialMediaInput").val() != "-- select an social media --") {
            q += "socialMedia:"+$("#socialMediaInput").val()+";";
        }
        if ($("#socialMediaIDInput").val())  {
            q += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
        }
    } else if (field == "reviewSite") {
        if ($("#reviewSiteInput").val() &&  $("#reviewSiteInput").val() != "-- select a review site --")  {
            q += "reviewSite:"+$("#reviewSiteInput").val()+";";
        }
        if ($("#reviewSiteIDInput").val())  {
            q += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
        }
    }
    if (q) {
        para = "T=" + tid + "Mode="+ mode+ "&q="+encodeURIComponent(q)
        search_signal = 1;
        $("#control_panel_2").hide();
        $("#highlight input", parent.documenqt).val("");
        lockscreen();
        $.ajax({
            method: "post",
            url: home_prefix + "otherlog.cgi",
            data:{
                source: mode,
                topic_id: tid,
                query: q,
                flag: 'query'
            },
            success:function(response) {
                $("#lemurbox").attr("src", home_prefix + url + "?" + para);
            }
        })
    }
}

function phoneSearch(){
    mode = "S";
    para = "T=" + tid + "Mode="+ mode+ "&q=" + encodeURIComponent("phone:"+$("#phoneInput").val()+";");
    search_signal = 1;
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function emailSearch() {
    mode = "T";
    query = "email:"+$("#emailInput").val()+";"
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);	

}

function nameSearch() {
    mode = "T";
    query = "name:"+$("#nameInput").val()+";"
    para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
    search_signal = 1;
    url = dict["domains"][1].replace("search","elasticsearch");
    $("#control_panel_2").hide();
    $("#highlight input", parent.document).val("");
    lockscreen();
    $("#lemurbox").attr("src", home_prefix + url + "?" + para);
}

function socialMediaSearch() {
    mode = "T";
    query = "";
    if (("#socialMediaInput").val() && $("#socialMediaInput").val() != "-- select an social media --")  {
        query += "socialMedia:"+$("#socialMediaInput").val()+";";
    }
    if ($("#socialMediaIDInput").val())  {
        query += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
    }
    if (query) {
        para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
        search_signal = 1;
        url = dict["domains"][1].replace("search","elasticsearch");
        $("#control_panel_2").hide();
        $("#highlight input", parent.document).val("");
        lockscreen();
        $("#lemurbox").attr("src", home_prefix + url + "?" + para);
    }
}

function reviewSiteSearch() {
    mode = "T";
    query = ""
    if ($("#reviewSiteInput").val() &&  $("#reviewSiteInput").val() != "-- select a review site --")  {
        query += "reviewSite:"+$("#reviewSiteInput").val()+";";
    }
    if ($("#reviewSiteIDInput").val())  {
        query += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
    }
    if (query) {
        para = "T=" + tid + "&q=" + "" + encodeURIComponent(query);
        search_signal = 1;
        url = dict["domains"][1].replace("search","elasticsearch");
        $("#control_panel_2").hide();
        $("#highlight input", parent.document).val("");
        lockscreen();
        $("#lemurbox").attr("src", home_prefix + url + "?" + para);
    }
}

function refineSearch() {
    mode = "S";
    query = ""
    if ($age == 1) {
	    query += "age:"+$( "#ageSlider" ).slider( "values", 0 )+$( "#ageSlider" ).slider( "values", 1 )+";";
    }
    if ($height== 1) {
	    query += "height:"+$( "#heightSlider" ).slider( "values", 0 )+$( "#heightSlider" ).slider( "values", 1 )+";";
    }
    if ($("#nameInput").val()) {
        query += "name:"+$("#nameInput").val()+";";
    }
    if ($("#stateInput").val() &&  $("#stateInput").val() != "-- select a state --") {
        query += "state:"+$("#stateInput").val()+";";
    }
    if ($("#cityInput").val())  {
        query += "city:"+$("#cityInput").val()+";";
    }
    if ($("#whiteHairBox").is(":checked"))  {
        query += "hairColor:"+$("#whiteHairBox").val()+";";
    }
    if ($("#blackHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blackHairBox").val()+";";
    }
    if ($("#brownHairBox").is(":checked"))  {
        query += "hairColor:"+$("#brownHairBox").val()+";";
    }
    if ($("#blondeHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blondeHairBox").val()+";";
    }
    if ($("#redHairBox").is(":checked"))  {
        query += "hairColor:"+$("#redHairBox").val()+";";
    }
    if ($("#blueHairBox").is(":checked"))  {
        query += "hairColor:"+$("#blueHairBox").val()+";";
    }
    if ($("#brownEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#brownEyeBox").val()+";";
    }
    if ($("#blackEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#blackEyeBox").val()+";";
    }
    if ($("#blueEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#blueEyeBox").val()+";";
    }
    if ($("#amberEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#amberEyeBox").val()+";";
    }
    if ($("#greyEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#greyEyeBox").val()+";";
    }
    if ($("#greenEyeBox").is(":checked"))  {
        query += "eyeColor:"+$("#greenEyeBox").val()+";";
    }
    if ($("#ethnicityInput").val() &&  $("#ethnicityInput").val() != "-- select an ethnicity --") {
	query += "ethnicity:"+$("#ethnicityInput").val()+";"
    }
    if ($("#nationalityInput").val() && $("#nationalityInput").val()!="-- select a country --")  {
        query += "nationality:"+$("#nationalityInput").val()+";";
    }
    if ($("#socialMediaInput").val() && $("#socialMediaInput").val() != "-- select an social media --")  {
        query += "socialMedia:"+$("#socialMediaInput").val()+";";
    }
    if ($("#socialMediaIDInput").val())  {
        query += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
    }
    if ($("#reviewSiteInput").val() && $("#reviewSiteInput").val() != "-- select a review site --")  {
        query += "reviewSite:"+$("#reviewSiteInput").val()+";";
    }
    if ($("#reviewSiteIDInput").val())  {
        query += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
    }
    if (query) {
        para = "T=" + tid + "Mode=" + mode+ "&q=" + "" + encodeURIComponent(query);
        search_signal = 1;
        $("#control_panel_2").hide();
        $("#highlight input", parent.document).val("");
        lockscreen();
        $.ajax({
            method: "post",
            url: home_prefix + "otherlog.cgi",
            data:{
                source: mode,
                topic_id: tid,
                query: q,
                flag: 'query'
            },
            success:function(response) {
                $("#lemurbox").attr("src", home_prefix + url + "?" + para);
            }
        })
    }
}

function move(opnum){
    if ((opnum == 'd' || opnum =='r')&& tname ==''){
        alertdialog(1);
        return;
    }
    if (opnum == 'd' || opnum =='r') {lockscreen();}
    $.ajax({
        method: "post",
        url: "http://cs-sys-1.uis.georgetown.edu/~jw1498/test/moveHandler.cgi",
	    data: {
            topic_id: tid,
            docno: doc_id, // ?? make sure set doc_id ??
            signal: opnum,
        },
        success: function(response){
            response = response.trim();
		    $(".screen-cover").remove();
                if (response == "-1"){
                    if (opnum == 'r') alertdialog(11);
                    if (opnum == 'd') alertdialog(13);
                }
                else if (response == "0"){
                    goback();
                }
                else{
                    doc_id = response.trim();
                    $("#lemurbox").attr("src", home_prefix+url+'?e='+response)
                }
                //    if (opnum == 'd') {
			    //alertdialog(15);
		//    } else {
		//	alertdialog(16);
		//    }
                //}
            }
            // what about 0 response ??
        });
};

function switchDoc(op) {
    if (op != "p" &&  op != "n") {
        alertdialog(1);
        return;
    }
    $.ajax({
        method: "post",
        url: "http://cs-sys-1.uis.georgetown.edu/~jw1498/test/switchDocHandler.cgi",
	    data:{
            topic_id: tid,
            docno: doc_id, // ?? make sure set doc_id ??
            signal: op,
        },
        success: function(response){
            response = response.trim();
            if (response == "-1"){
                $(".screen-cover").remove();
            }
            else if (response == "0"){
                //do nothing
            }
            else{
                doc_id = response.trim();
                $("#lemurbox").attr("src", home_prefix+url+'?e='+response)
            }
        }
        // what about 0 response ??
   });
}

function goback(){
    level = 'L';
    lockscreen();
    $.ajax({
        method: "get",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            docno: doc_id,
            flag: 'goback',
        }
    })
    $("#lemurbox").attr("src", home_prefix+url+'?'+para);
}

function prepareTopbar(){
    $("#control_panel .search_button").click(runQuery);
    $("#docback").click(goback);
    $("#docdiscard").click(function(){
        move('r');
    });
    $("#docdup").click(function(){
        move('d');
    });
    $("#docnext").click(function(){
        move('n');
    });
    $("#docprev").click(function(){
        move('p');
    });

    $("#assesshappy").tooltip();

    $("#assesssad").tooltip();
    
    $("#highlightText").bind("input",function(){
	$("#lemurbox")[0].contentWindow.highlighting(1);
     }
    );
    $("#highlight button").click(function(){
	$("#lemurbox")[0].contentWindow.highlighting(1);    
})
}
