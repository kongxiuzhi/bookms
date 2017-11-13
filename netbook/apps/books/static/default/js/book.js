/**
 * Created by PyCharm.
 * User: netcharm
 * Date: 13-3-16
 * Time: 下午7:22
 * To change this template use File | Settings | File Templates.
 * @return {boolean}
 */

//function filter_expand(filter_name)
//{
//    var filter = $(filter_name);
//    filter.toggle();
//    return false;
//}

jQuery.fn.log = function (msg) {
    console.log("%s: %o", msg, this);
    return this;
};

function ConfirmEX( options )
{
    var popup_options = {
        autoOpen: true,
        closeOnEscape: true,
        maxWidth: 400,
        minHeight: 100,
        minWidth: 200,
        //dialogClass: "alert",
        modal: true
    };

    //var dlgHeader = $('#confirm_header');
    var dlgContent = $('#confirm_content');

    var dlgOkText = $('#confirm_btnOkText');
    //var dlgCancelText = $('#confirm_btnCancelText');

    var dlgOk = $('#confirm_btnOk');
    var dlgCancel = $('#confirm_btnCancel');

    dlgContent.html(options.contents);
    dlgOkText.html(options.value);

    var popup_dialog = $('#popup_confirm');
    popup_dialog.dialog(popup_options);
    popup_dialog.dialog('open');

    dlgOk.bind('click', {}, options.callback);
    dlgCancel.bind('click', function(){popup_dialog.dialog('close');});


    return false;
}

function change_one(urlpath, label, value, callback_after)
{
    var formmulti = $('#form_multi');
    var url = encodeURI(urlpath);
    var callback = function(){jQuery.get(url, formmulti.serialize(), function(){window.location.reload();});};
    if(callback_after)
    {
        last_ref = document.referrer;
        //callback = function(){jQuery.get(url, formmulti.serialize(), function(){eval(callback_after)});};
        callback = function(){jQuery.get(url, formmulti.serialize(), function(){window.location.replace(last_ref);});};
    }
    var options = { header:'', contents:label, ok:'', cancel:'', value:value, callback:callback };
    ConfirmEX( options );

    return false;
}

function change_multi(urlpath, value, callback_after)
{
    var books = $("td.books_list_isbn.ui-state-highlight");
    var book_ids = '';
    if(books.length <= 0){ return false; }
    books.each(
        function()
        {
            book_ids = book_ids.concat($(this).html().toString().concat(','));
        }
    );

    var booktitles = $("td.books_list_label.ui-state-highlight");
    var book_titles = '';
    booktitles.each(
        function()
        {
            book_titles = book_titles.concat($(this).text().toString().concat('<br/>\n'));
        }
    );

    var formmulti = $('#form_multi');
    var url = encodeURI(urlpath.concat('?id=', book_ids, '&v=', value));
    var callback = function(){jQuery.get(url, formmulti.serialize(), function(){window.location.reload();});};
    if(callback_after)
    {
        callback = function(){eval(callback_after);};
        //callback = function(){jQuery.get(url, formmulti.serialize(), function(){eval(callback_after);});};
    }
    var options = { header:'', contents:book_titles, ok:'', cancel:'', value:value, callback:callback };
    ConfirmEX( options );

    return false;
}

function popup_list(id)
{
    var books = $("td.books_list_isbn.ui-state-highlight");
    if(books.length <= 0)
    {
        return false;
    }

    var popup_options = {
        autoOpen: false,
        closeOnEscape: true,
        modal: true,
        maxHeight: 400,
        maxWidth: 400,
        minHeight: 200,
        minWidth: 200,
        width: "auto",
        height: "auto"
    };

    var popup_dialog = $(id);
    popup_dialog.dialog(popup_options);
    popup_dialog.on(
        'click',
        '.action',
        function(){
            $(this).closest(id).dialog('destroy');
        });
    popup_dialog.dialog('open');

    return false;
}

function change_tag_multi(tag)
{
    var new_tag = tag.replace(/[:|;|\/| |；|，|：|、]/g, ',');
    alert(new_tag);
    return change_multi('/books/change-tag-multi/', new_tag);
}

function change_media_multi(media)
{
    return change_multi('/books/change-media-multi/', media);
}

function change_state_multi(state)
{
    return change_multi('/books/change-state-multi/', state);
}

function change_location_multi(location)
{
    return change_multi('/books/change-location-multi/', location);
}

function change_category_multi(category)
{
    return change_multi('/books/change-category-multi/', category);
}

function export_multi(value)
{
    return change_multi('/books/export/', value, 'window.location.replace(url);$("#confirm_btnCancel").click();');
}

function remove_multi(value)
{
    return change_multi('/books/remove-multi/', value);
}

function remove_one(urlpath, book_title, value, callback_after)
{
    change_one(urlpath, book_title, value, callback_after);
    return false;
}

function popup_export_list()
{
    return popup_list('#popup_export');
}

function popup_tag_list()
{
    return popup_list('#popup_tag');
}

function popup_state_list()
{
    return popup_list('#popup_state');
}

function popup_media_list()
{
    return popup_list('#popup_media');
}

function popup_location_list()
{
    return popup_list('#popup_location');
}

function popup_category_list()
{
    return popup_list('#popup_category');
}

function rgbcolorToHex(color)
{
    if (color.substr(0, 1) === '#') {
        return color;
    }
    var digits = /(.*?)rgb\((\d+), (\d+), (\d+)\)/.exec(color);

    var red = parseInt(digits[2]);
    var green = parseInt(digits[3]);
    var blue = parseInt(digits[4]);

    var rgb = blue | (green << 8) | (red << 16);
    return digits[1] + '#' + rgb.toString(16);
}

function fit_ui_bgcolor()
{
    //
    // Init background to jQuery-UI theme
    //
    //var bgcolor = $(".ui-widget-header:first").css("background-color");
    //var bgcolor = "black"; // works fine when uncommented
    //$("body").css("background-color", bgcolor);

    var border = $(".ui-widget-content:first").css("border");
    $("input").each(function(){
        $(this).addClass("ui-widget-content");
    });
    $("select").each(function(){
        $(this).addClass("ui-widget-content");
    });
    $("textarea").each(function(){
        $(this).addClass("ui-widget-content");
        //$(this).css("background-image", "none");
    });
    $("button").each(function(){
        $(this).addClass("ui-widget-content");
    });
}

function fit_ui_table_style()
{
    //
    // Init Table Style to jQuery UI
    //
    var th = $("th");
    var tr = $("tr");
    var td = $("td");

    th.each(function(){ $(this).addClass("ui-state-default"); });
    td.each(function(){ $(this).addClass("ui-widget-content"); });
    if($('.books_list_isbn').length)
    {
        tr.hover(
            function(){ $(this).children("td").addClass("ui-state-hover");    },
            function(){ $(this).children("td").removeClass("ui-state-hover"); }
        );
        tr.click(function(){ $(this).children("td").toggleClass("ui-state-highlight"); });
    }
//    else
//    {
//        tr.hover(
//            function(){ return false; },
//            function(){ return false; }
//        );
//        //tr.click(function(){ });
//    }
}

function fit_ui_side_left()
{
    //
    // Init left side Accordion
    //
    var query_key = $('#query_key').val();
    var ac_filter_kp = {'':0, 'state':1, 'pubdate':2, 'buydate': 3, 'category':4, 'tag':5, 'location':6, 'media':7 };
    $( "#filter_accordion" ).accordion({ heightStyle: "content", active: ac_filter_kp[query_key] });
    $( "#media_accordion" ).accordion({ heightStyle: "content" });
    $( "#list_accordion" ).accordion({ heightStyle: "content" });
    $( "#tools_accordion" ).accordion({ heightStyle: "content" });
}

function fit_ui_action_button()
{
    //
    // Init Action Button
    //
    $(".action").each( function(){ $(this).button(); } );
}

function fit_ui_theme_switcher(cssname)
{
    if(!cssname)
    {
        cssname = 'ui-lightness';
    }
    $("#ui-theme-switcher").jui_theme_switch({
        stylesheet_link_id: 'css_theme',                     // REQUIRED
        datasource_url: '/static/js/jQuery/json_data/user/netcharm.json',  // REQUIRED
        project_url: '/',                                // url relative to web server document root (required only for locally hosted themes)

        // DEFAULTS
        switcher_label: "",
        default_theme: cssname,
        list_size: "1",
        use_groups: "yes",
        show_all: "no", // default is show items having "active": "yes"

        containerClass: "ui-accordion-content ui-widget-content",
        labelClass: "ui-widget",
        listClass: "ui-widget-content",

//        onDisplay: function() {
//            // your code here
//            return false;
//        },
        onChangeTheme: function(event, theme) {
            $.cookie('css_theme', theme.theme_name, { path: '/books' }) ;
            var formmulti = $('#form_multi');
            var url = encodeURI('/books/config/set/?name=theme&value='.concat(theme.theme_name));
            jQuery.get(url, formmulti.serialize());
        }
    });
}

function changecss(cssname)
{
    if($.cookie("css_theme")!=null)
    {
        //定义变量
        var css_old, css_new;
        var css_theme = $("#css_theme");

        //取得skin的css链接
        css_old = css_theme.attr("href");
        //把原来路径的ui-lightness替换成我们自己的str
        css_new = css_old.replace(/css\/\S+\//g, 'css'.concat('/', cssname, '/'));
        if(css_new != css_old)
        {
            //改变href属性其实这里已经完成
            css_theme.attr("href", css_new);
            //记录cookie,防止刷新就回到原来的css路径
            $.cookie('css_theme', cssname, { path: '/books' }) ;
        }
    }
}

$().ready(function InitUI()
{
    fit_ui_theme_switcher($('#theme_name').val());
    //changecss($.cookie("css_theme"));

    fit_ui_table_style();

    fit_ui_side_left();

    fit_ui_action_button();

    fit_ui_bgcolor();

    //$.cookie('previousUrl', window.location.href, {path:'/books'});

});



