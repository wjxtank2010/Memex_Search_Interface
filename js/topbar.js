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

//function runQuery(){
//    mode = "N" //search from query box is normal search
//    url = dict["domains"][1]
//    level = 'L';
//    para = "T=" + tid + "&Mode="+mode+"&N=1"+"&q=" + "box:"+$("#querybox").val()+";";
//    thequery = $("#querybox").val();
//    search_signal = 1;
//    // ?? set mode or level ??
//    $("#control_panel_2").hide();
//    $("#highlight input", parent.document).val("");
//    lockscreen();
//
//    $.ajax({
//        method: "post",
//        url: home_prefix + "otherlog.cgi",
//        data:{
//            source: mode,
//            topic_id: tid,
//            query: para,
//            flag: 'query'
//        },
//        success:function(response) {
//            $("#lemurbox").attr("src", home_prefix + url + "?" + encodeURIComponent(para));
//        }
//    })
//
//    // if parent.tname == '' #lemurdiscard.hide()
//}

function singleFieldQuery(field){ //format of query:  fieldName:value;   ex.  phone:2021234567
    if (field == "box") {
        mode = "N";
    } else {
        mode = "S" //abbreviation for structured query
    }
    var q = "" //query
    var N = 0; //number of query parts
    url = dict["domains"][1];
    level = 'L';
    if (field == "phone") {
        if ($("#phoneInput").val()) {
            q = "phone:"+$("#phoneInput").val()+";";
            N += 1;
        }
    } else if (field == "email") {
        if ($("#emailInput").val()) {
            q = "email:"+$("#emailInput").val()+";"
            N += 1;
        }
    } else if (field == "name") {
        if ($("#nameInput").val()) {
            q = "name:"+$("#nameInput").val()+";"
            N += 1;
        }
    } else if (field == "socialMedia") {
        if (("#socialMediaInput").val() && $("#socialMediaInput").val() != "-- select an social media --") {
            q += "socialMedia:"+$("#socialMediaInput").val()+";";
            N += 1;
        }
        if ($("#socialMediaIDInput").val())  {
            q += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
            N += 1;
        }
    } else if (field == "reviewSite") {
        if ($("#reviewSiteInput").val() &&  $("#reviewSiteInput").val() != "-- select a review site --")  {
            q += "reviewSite:"+$("#reviewSiteInput").val()+";";
            N += 1;
        }
        if ($("#reviewSiteIDInput").val())  {
            q += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
            N = 1;
        }
    } else if (field == "box") {
        if ($("#querybox").val()) {
            q = "box:" + $("#querybox").val() + ";";
            N += 1;
        }
    }
    if (q) {
        para = "T=" + tid + "&Mode="+ mode+ "&N="+ N + "&q=";
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
                query: para+q,
                flag: 'query',
                lvl: level
            },
            success:function(response) {
                $("#lemurbox").attr("src", home_prefix + url + "?" + para + encodeURIComponent(q));
                para += encodeURIComponent(q);
            }
        })
    }
}

function refineSearch() {
    mode = "S";
    q = ""; //query
    var N = 0; //number of query parts
    url = dict["domains"][1];
    level = 'L';
    if ($age == 1) { //age slider value has been changed
	    q += "age:"+$("#ageSlider").slider("values",0)+$("#ageSlider").slider("values",1)+";";
	    N += 1;
    }
    if ($height== 1) { //height slider value has been changed
	    q += "height:"+$("#heightSlider").slider("values",0)+$("#heightSlider").slider("values",1)+";";
	    N += 1;
    }
    if ($("#nameInput").val()) {
        q += "name:"+$("#nameInput").val()+";";
        N += 1;
    }
    if ($("#stateInput").val() &&  $("#stateInput").val() != "-- select a state --") {
        q += "state:"+$("#stateInput").val()+";";
        N += 1;
    }
    if ($("#cityInput").val())  {
        q += "city:"+$("#cityInput").val()+";";
        N += 1;
    }

    var hairColors = [];
    var hairboxes = ["#WhiteHairBox","#BlackHairBox","#BrownHairBox","#BlondeHairBox","#RedHairBox","#BlueHairBox"];
    for (i=0;i<hairboxes.length;i++) {
        if ($(hairboxes[i]).is(":checked")) {
            hairColors.push($(hairboxes[i]).val());
        }
    }
    if (hairColors.length>0) {
        q += "hairColor:"+hairColors.join()+";";
        N += 1;
    }

    var eyeColors = [];
    var eyeBoxes = ["#BrownEyeBox","#BlackEyeBox","#BlueEyeBox","#AmberEyeBox","#GreyEyeBox","#GreenEyeBox"];
    for (i=0;i<eyeBoxes.length;i++) {
        if ($(eyeBoxes[i]).is(":checked")) {
            eyeColors.push($(eyeBoxes[i]).val());
        }
    }
    if (eyeColors.length>0) {
        q += "eyeColor:"+eyeColors.join()+";";
        N += 1;
    }

    if ($("#ethnicityInput").val() &&  $("#ethnicityInput").val() != "-- select an ethnicity --") {
	    q += "ethnicity:"+$("#ethnicityInput").val()+";"
	    N += 1;
    }
    if ($("#nationalityInput").val() && $("#nationalityInput").val()!="-- select a country --")  {
        q += "nationality:"+$("#nationalityInput").val()+";";
        N += 1;
    }
    if ($("#socialMediaInput").val() && $("#socialMediaInput").val() != "-- select an social media --")  {
        q += "socialMedia:"+$("#socialMediaInput").val()+";";
        N += 1;
    }
    if ($("#socialMediaIDInput").val())  {
        q += "socialMediaID:"+$("#socialMediaIDInput").val()+";";
        N += 1;
    }
    if ($("#reviewSiteInput").val() && $("#reviewSiteInput").val() != "-- select a review site --")  {
        q += "reviewSite:"+$("#reviewSiteInput").val()+";";
        N += 1;
    }
    if ($("#reviewSiteIDInput").val())  {
        q += "reviewSiteID:"+$("#reviewSiteIDInput").val()+";";
        N += 1;
    }

    //within current search
    if ($("#withinCurrentSearch").is(":checked")) {
        if ($("#phoneInput").val()) {
            q += "phone:"+$("#phoneInput").val()+";";
            N += 1;
        }
        if ($("#emailInput").val()) {
            q += "email:"+$("#emailInput").val()+";"
            N += 1;
        }
        if ($("#querybox").val()) {
            q += "box:"+$("#querybox").val()+";";
            N += 1;
        }
    }

    if (q) {
        para = "T=" + tid + "&Mode=" + mode+ "&N=" + N + "&q=";
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
                query: para+q,
                flag: 'query',
                lvl:level
            },
            success:function(response) {
                $("#lemurbox").attr("src", home_prefix + url + "?" + para+encodeURIComponent(q));
                para += encodeURIComponent(q);
            }
        });
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
                    //goback();
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
        method: "post",
        url: home_prefix + "otherlog.cgi",
        data:{
            source: mode,
            topic_id: tid,
            docno: doc_id,
            flag: 'goback',
            lvl:level
        }
    })
    $("#lemurbox").attr("src", home_prefix+url+'?'+para);
}

function prepareTopbar(){
    $("#control_panel .search_button").click(singleFieldQuery("box"));
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
    
    $("#highlightText").bind("input",function() {
        $("#lemurbox")[0].contentWindow.highlighting(1);
    });
    $("#highlight button").click(function() {
	    $("#lemurbox")[0].contentWindow.highlighting(1);
    });
}
