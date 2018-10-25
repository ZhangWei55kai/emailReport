/*
* @Author: zhangwei
* @Date:   2016-12-14 21:06:42
* @Last Modified by:   zhangwei
* @Last Modified time: 2016-12-14 21:08:15
*/

'use strict';
function getCookie(name){
	var cookieValue = null;
	if(document.cookie != ''){
		var cookieF =''
		var cookies = document.cookie.split(';');
		for (var i = 0;cookies.length>i;i++) {
			cookieF = $.trim(cookies[i]);
			if (cookieF.substring(0,name.length+1)===(name+'=')){
				cookieValue = decodeURIComponent(cookieF.substring(name.length+1));
				break;
			}
		}
	}
	return cookieValue
};
function csrfSafeMethod(method) {
	 // these HTTP methods do not require CSRF protection
	 return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
var csrftoken = getCookie('csrftoken')

var ssajax = {
	'ajax':function(args){
		this._ajaxSetup();
		$.ajax(args);

	},
	'_ajaxSetup':function(){
		$.ajaxSetup({
			'beforeSend':function(xhr,settings){
				if (!csrfSafeMethod(settings.type)&& sameOrigin(settings.url)){
					xhr.setRequestHeader("X-CSRFToken", csrftoken);
				}}

		})
	}
}