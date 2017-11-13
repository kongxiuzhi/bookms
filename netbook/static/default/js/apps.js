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

function remove_one(urlpath, book_title, value, callback_after)
{
    change_one(urlpath, book_title, value, callback_after);
    return false;
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
    var border = $(".ui-widget-content:first").css("border");
    $("input").each(function(){
        $(this).addClass("ui-widget-content");
    });
    $("select").each(function(){
        $(this).addClass("ui-widget-content");
    });
    $("textarea").each(function(){
        $(this).addClass("ui-widget-content");
    });
    $("button").each(function(){
        $(this).addClass("ui-widget-content");
    });
}

function fit_ui_side_left()
{
    //
    // Init left side Accordion
    //
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
            $.cookie('css_theme', theme.theme_name, { path: '/' }) ;
            var formmulti = $('#form_multi');
            var url = encodeURI('/config/set/?key=theme&value='.concat(theme.theme_name));
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
            $.cookie('css_theme', cssname, { path: '/' }) ;
        }
    }
}

$().ready(function InitUI()
{
    fit_ui_theme_switcher($('#theme_name').val());
    //changecss($.cookie("css_theme"));

    fit_ui_side_left();

    fit_ui_action_button();

    fit_ui_bgcolor();

    //$( document ).tooltip("option", "track", true);
    $( document ).tooltip({
        content: function() {
            return $(this).attr('title');
        }
    });

});



