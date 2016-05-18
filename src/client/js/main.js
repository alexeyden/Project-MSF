init();

algorithm = {
    is_new: false
}

model_reload = false;

/*!
 * Draggabilly PACKAGED v2.1.0
 * Make that shiz draggable
 * http://draggabilly.desandro.com
 * MIT license
 */

!function(t,i){"function"==typeof define&&define.amd?define("jquery-bridget/jquery-bridget",["jquery"],function(e){i(t,e)}):"object"==typeof module&&module.exports?module.exports=i(t,require("jquery")):t.jQueryBridget=i(t,t.jQuery)}(window,function(t,i){function e(e,r,a){function h(t,i,n){var o,r="$()."+e+'("'+i+'")';return t.each(function(t,h){var d=a.data(h,e);if(!d)return void s(e+" not initialized. Cannot call methods, i.e. "+r);var u=d[i];if(!u||"_"==i.charAt(0))return void s(r+" is not a valid method");var p=u.apply(d,n);o=void 0===o?p:o}),void 0!==o?o:t}function d(t,i){t.each(function(t,n){var o=a.data(n,e);o?(o.option(i),o._init()):(o=new r(n,i),a.data(n,e,o))})}a=a||i||t.jQuery,a&&(r.prototype.option||(r.prototype.option=function(t){a.isPlainObject(t)&&(this.options=a.extend(!0,this.options,t))}),a.fn[e]=function(t){if("string"==typeof t){var i=o.call(arguments,1);return h(this,t,i)}return d(this,t),this},n(a))}function n(t){!t||t&&t.bridget||(t.bridget=e)}var o=Array.prototype.slice,r=t.console,s="undefined"==typeof r?function(){}:function(t){r.error(t)};return n(i||t.jQuery),e}),function(t,i){"function"==typeof define&&define.amd?define("get-size/get-size",[],function(){return i()}):"object"==typeof module&&module.exports?module.exports=i():t.getSize=i()}(window,function(){function t(t){var i=parseFloat(t),e=-1==t.indexOf("%")&&!isNaN(i);return e&&i}function i(){}function e(){for(var t={width:0,height:0,innerWidth:0,innerHeight:0,outerWidth:0,outerHeight:0},i=0;d>i;i++){var e=h[i];t[e]=0}return t}function n(t){var i=getComputedStyle(t);return i||a("Style returned "+i+". Are you running this code in a hidden iframe on Firefox? See http://bit.ly/getsizebug1"),i}function o(){if(!u){u=!0;var i=document.createElement("div");i.style.width="200px",i.style.padding="1px 2px 3px 4px",i.style.borderStyle="solid",i.style.borderWidth="1px 2px 3px 4px",i.style.boxSizing="border-box";var e=document.body||document.documentElement;e.appendChild(i);var o=n(i);r.isBoxSizeOuter=s=200==t(o.width),e.removeChild(i)}}function r(i){if(o(),"string"==typeof i&&(i=document.querySelector(i)),i&&"object"==typeof i&&i.nodeType){var r=n(i);if("none"==r.display)return e();var a={};a.width=i.offsetWidth,a.height=i.offsetHeight;for(var u=a.isBorderBox="border-box"==r.boxSizing,p=0;d>p;p++){var c=h[p],f=r[c],g=parseFloat(f);a[c]=isNaN(g)?0:g}var l=a.paddingLeft+a.paddingRight,v=a.paddingTop+a.paddingBottom,m=a.marginLeft+a.marginRight,y=a.marginTop+a.marginBottom,b=a.borderLeftWidth+a.borderRightWidth,P=a.borderTopWidth+a.borderBottomWidth,E=u&&s,_=t(r.width);_!==!1&&(a.width=_+(E?0:l+b));var x=t(r.height);return x!==!1&&(a.height=x+(E?0:v+P)),a.innerWidth=a.width-(l+b),a.innerHeight=a.height-(v+P),a.outerWidth=a.width+m,a.outerHeight=a.height+y,a}}var s,a="undefined"==typeof console?i:function(t){console.error(t)},h=["paddingLeft","paddingRight","paddingTop","paddingBottom","marginLeft","marginRight","marginTop","marginBottom","borderLeftWidth","borderRightWidth","borderTopWidth","borderBottomWidth"],d=h.length,u=!1;return r}),function(t,i){"function"==typeof define&&define.amd?define("ev-emitter/ev-emitter",i):"object"==typeof module&&module.exports?module.exports=i():t.EvEmitter=i()}(this,function(){function t(){}var i=t.prototype;return i.on=function(t,i){if(t&&i){var e=this._events=this._events||{},n=e[t]=e[t]||[];return-1==n.indexOf(i)&&n.push(i),this}},i.once=function(t,i){if(t&&i){this.on(t,i);var e=this._onceEvents=this._onceEvents||{},n=e[t]=e[t]||[];return n[i]=!0,this}},i.off=function(t,i){var e=this._events&&this._events[t];if(e&&e.length){var n=e.indexOf(i);return-1!=n&&e.splice(n,1),this}},i.emitEvent=function(t,i){var e=this._events&&this._events[t];if(e&&e.length){var n=0,o=e[n];i=i||[];for(var r=this._onceEvents&&this._onceEvents[t];o;){var s=r&&r[o];s&&(this.off(t,o),delete r[o]),o.apply(this,i),n+=s?0:1,o=e[n]}return this}},t}),function(t,i){"function"==typeof define&&define.amd?define("unipointer/unipointer",["ev-emitter/ev-emitter"],function(e){return i(t,e)}):"object"==typeof module&&module.exports?module.exports=i(t,require("ev-emitter")):t.Unipointer=i(t,t.EvEmitter)}(window,function(t,i){function e(){}function n(){}var o=n.prototype=Object.create(i.prototype);o.bindStartEvent=function(t){this._bindStartEvent(t,!0)},o.unbindStartEvent=function(t){this._bindStartEvent(t,!1)},o._bindStartEvent=function(i,e){e=void 0===e?!0:!!e;var n=e?"addEventListener":"removeEventListener";t.navigator.pointerEnabled?i[n]("pointerdown",this):t.navigator.msPointerEnabled?i[n]("MSPointerDown",this):(i[n]("mousedown",this),i[n]("touchstart",this))},o.handleEvent=function(t){var i="on"+t.type;this[i]&&this[i](t)},o.getTouch=function(t){for(var i=0;i<t.length;i++){var e=t[i];if(e.identifier==this.pointerIdentifier)return e}},o.onmousedown=function(t){var i=t.button;i&&0!==i&&1!==i||this._pointerDown(t,t)},o.ontouchstart=function(t){this._pointerDown(t,t.changedTouches[0])},o.onMSPointerDown=o.onpointerdown=function(t){this._pointerDown(t,t)},o._pointerDown=function(t,i){this.isPointerDown||(this.isPointerDown=!0,this.pointerIdentifier=void 0!==i.pointerId?i.pointerId:i.identifier,this.pointerDown(t,i))},o.pointerDown=function(t,i){this._bindPostStartEvents(t),this.emitEvent("pointerDown",[t,i])};var r={mousedown:["mousemove","mouseup"],touchstart:["touchmove","touchend","touchcancel"],pointerdown:["pointermove","pointerup","pointercancel"],MSPointerDown:["MSPointerMove","MSPointerUp","MSPointerCancel"]};return o._bindPostStartEvents=function(i){if(i){var e=r[i.type];e.forEach(function(i){t.addEventListener(i,this)},this),this._boundPointerEvents=e}},o._unbindPostStartEvents=function(){this._boundPointerEvents&&(this._boundPointerEvents.forEach(function(i){t.removeEventListener(i,this)},this),delete this._boundPointerEvents)},o.onmousemove=function(t){this._pointerMove(t,t)},o.onMSPointerMove=o.onpointermove=function(t){t.pointerId==this.pointerIdentifier&&this._pointerMove(t,t)},o.ontouchmove=function(t){var i=this.getTouch(t.changedTouches);i&&this._pointerMove(t,i)},o._pointerMove=function(t,i){this.pointerMove(t,i)},o.pointerMove=function(t,i){this.emitEvent("pointerMove",[t,i])},o.onmouseup=function(t){this._pointerUp(t,t)},o.onMSPointerUp=o.onpointerup=function(t){t.pointerId==this.pointerIdentifier&&this._pointerUp(t,t)},o.ontouchend=function(t){var i=this.getTouch(t.changedTouches);i&&this._pointerUp(t,i)},o._pointerUp=function(t,i){this._pointerDone(),this.pointerUp(t,i)},o.pointerUp=function(t,i){this.emitEvent("pointerUp",[t,i])},o._pointerDone=function(){this.isPointerDown=!1,delete this.pointerIdentifier,this._unbindPostStartEvents(),this.pointerDone()},o.pointerDone=e,o.onMSPointerCancel=o.onpointercancel=function(t){t.pointerId==this.pointerIdentifier&&this._pointerCancel(t,t)},o.ontouchcancel=function(t){var i=this.getTouch(t.changedTouches);i&&this._pointerCancel(t,i)},o._pointerCancel=function(t,i){this._pointerDone(),this.pointerCancel(t,i)},o.pointerCancel=function(t,i){this.emitEvent("pointerCancel",[t,i])},n.getPointerPoint=function(t){return{x:t.pageX,y:t.pageY}},n}),function(t,i){"function"==typeof define&&define.amd?define("unidragger/unidragger",["unipointer/unipointer"],function(e){return i(t,e)}):"object"==typeof module&&module.exports?module.exports=i(t,require("unipointer")):t.Unidragger=i(t,t.Unipointer)}(window,function(t,i){function e(){}function n(){}var o=n.prototype=Object.create(i.prototype);o.bindHandles=function(){this._bindHandles(!0)},o.unbindHandles=function(){this._bindHandles(!1)};var r=t.navigator;return o._bindHandles=function(t){t=void 0===t?!0:!!t;var i;i=r.pointerEnabled?function(i){i.style.touchAction=t?"none":""}:r.msPointerEnabled?function(i){i.style.msTouchAction=t?"none":""}:e;for(var n=t?"addEventListener":"removeEventListener",o=0;o<this.handles.length;o++){var s=this.handles[o];this._bindStartEvent(s,t),i(s),s[n]("click",this)}},o.pointerDown=function(t,i){if("INPUT"==t.target.nodeName&&"range"==t.target.type)return this.isPointerDown=!1,void delete this.pointerIdentifier;this._dragPointerDown(t,i);var e=document.activeElement;e&&e.blur&&e.blur(),this._bindPostStartEvents(t),this.emitEvent("pointerDown",[t,i])},o._dragPointerDown=function(t,e){this.pointerDownPoint=i.getPointerPoint(e);var n=this.canPreventDefaultOnPointerDown(t,e);n&&t.preventDefault()},o.canPreventDefaultOnPointerDown=function(t){return"SELECT"!=t.target.nodeName},o.pointerMove=function(t,i){var e=this._dragPointerMove(t,i);this.emitEvent("pointerMove",[t,i,e]),this._dragMove(t,i,e)},o._dragPointerMove=function(t,e){var n=i.getPointerPoint(e),o={x:n.x-this.pointerDownPoint.x,y:n.y-this.pointerDownPoint.y};return!this.isDragging&&this.hasDragStarted(o)&&this._dragStart(t,e),o},o.hasDragStarted=function(t){return Math.abs(t.x)>3||Math.abs(t.y)>3},o.pointerUp=function(t,i){this.emitEvent("pointerUp",[t,i]),this._dragPointerUp(t,i)},o._dragPointerUp=function(t,i){this.isDragging?this._dragEnd(t,i):this._staticClick(t,i)},o._dragStart=function(t,e){this.isDragging=!0,this.dragStartPoint=i.getPointerPoint(e),this.isPreventingClicks=!0,this.dragStart(t,e)},o.dragStart=function(t,i){this.emitEvent("dragStart",[t,i])},o._dragMove=function(t,i,e){this.isDragging&&this.dragMove(t,i,e)},o.dragMove=function(t,i,e){t.preventDefault(),this.emitEvent("dragMove",[t,i,e])},o._dragEnd=function(t,i){this.isDragging=!1,setTimeout(function(){delete this.isPreventingClicks}.bind(this)),this.dragEnd(t,i)},o.dragEnd=function(t,i){this.emitEvent("dragEnd",[t,i])},o.onclick=function(t){this.isPreventingClicks&&t.preventDefault()},o._staticClick=function(t,i){if(!this.isIgnoringMouseUp||"mouseup"!=t.type){var e=t.target.nodeName;("INPUT"==e||"TEXTAREA"==e)&&t.target.focus(),this.staticClick(t,i),"mouseup"!=t.type&&(this.isIgnoringMouseUp=!0,setTimeout(function(){delete this.isIgnoringMouseUp}.bind(this),400))}},o.staticClick=function(t,i){this.emitEvent("staticClick",[t,i])},n.getPointerPoint=i.getPointerPoint,n}),function(t,i){"function"==typeof define&&define.amd?define(["get-size/get-size","unidragger/unidragger"],function(e,n){return i(t,e,n)}):"object"==typeof module&&module.exports?module.exports=i(t,require("get-size"),require("unidragger")):t.Draggabilly=i(t,t.getSize,t.Unidragger)}(window,function(t,i,e){function n(){}function o(t,i){for(var e in i)t[e]=i[e];return t}function r(t){return t instanceof HTMLElement}function s(t,i){this.element="string"==typeof t?h.querySelector(t):t,f&&(this.$element=f(this.element)),this.options=o({},this.constructor.defaults),this.option(i),this._create()}function a(t,i,e){return e=e||"round",i?Math[e](t/i)*i:t}var h=t.document,d=t.requestAnimationFrame||t.webkitRequestAnimationFrame||t.mozRequestAnimationFrame,u=0;d||(d=function(t){var i=(new Date).getTime(),e=Math.max(0,16-(i-u)),n=setTimeout(t,e);return u=i+e,n});var p=h.documentElement,c="string"==typeof p.style.transform?"transform":"WebkitTransform",f=t.jQuery,g=s.prototype=Object.create(e.prototype);return s.defaults={},g.option=function(t){o(this.options,t)},g._create=function(){this.position={},this._getPosition(),this.startPoint={x:0,y:0},this.dragPoint={x:0,y:0},this.startPosition=o({},this.position);var t=getComputedStyle(this.element);"relative"!=t.position&&"absolute"!=t.position&&(this.element.style.position="relative"),this.enable(),this.setHandles()},g.setHandles=function(){this.handles=this.options.handle?this.element.querySelectorAll(this.options.handle):[this.element],this.bindHandles()},g.dispatchEvent=function(i,e,n){var o=[e].concat(n);this.emitEvent(i,o);var r=t.jQuery;if(r&&this.$element)if(e){var s=r.Event(e);s.type=i,this.$element.trigger(s,n)}else this.$element.trigger(i,n)},s.prototype._getPosition=function(){var t=getComputedStyle(this.element),i=this._getPositionCoord(t.left,"width"),e=this._getPositionCoord(t.top,"height");this.position.x=isNaN(i)?0:i,this.position.y=isNaN(e)?0:e,this._addTransformPosition(t)},s.prototype._getPositionCoord=function(t,e){if(-1!=t.indexOf("%")){var n=i(this.element.parentNode);return parseFloat(t)/100*n[e]}return parseInt(t,10)},g._addTransformPosition=function(t){var i=t[c];if(0===i.indexOf("matrix")){var e=i.split(","),n=0===i.indexOf("matrix3d")?12:4,o=parseInt(e[n],10),r=parseInt(e[n+1],10);this.position.x+=o,this.position.y+=r}},g.pointerDown=function(t,i){this._dragPointerDown(t,i);var e=h.activeElement;e&&e.blur&&e!=h.body&&e.blur(),this._bindPostStartEvents(t),this.element.classList.add("is-pointer-down"),this.dispatchEvent("pointerDown",t,[i])},g.pointerMove=function(t,i){var e=this._dragPointerMove(t,i);this.dispatchEvent("pointerMove",t,[i,e]),this._dragMove(t,i,e)},g.dragStart=function(t,i){this.isEnabled&&(this._getPosition(),this.measureContainment(),this.startPosition.x=this.position.x,this.startPosition.y=this.position.y,this.setLeftTop(),this.dragPoint.x=0,this.dragPoint.y=0,this.element.classList.add("is-dragging"),this.dispatchEvent("dragStart",t,[i]),this.animate())},g.measureContainment=function(){var t=this.options.containment;if(t){var e=r(t)?t:"string"==typeof t?h.querySelector(t):this.element.parentNode,n=i(this.element),o=i(e),s=this.element.getBoundingClientRect(),a=e.getBoundingClientRect(),d=o.borderLeftWidth+o.borderRightWidth,u=o.borderTopWidth+o.borderBottomWidth,p=this.relativeStartPosition={x:s.left-(a.left+o.borderLeftWidth),y:s.top-(a.top+o.borderTopWidth)};this.containSize={width:o.width-d-p.x-n.width,height:o.height-u-p.y-n.height}}},g.dragMove=function(t,i,e){if(this.isEnabled){var n=e.x,o=e.y,r=this.options.grid,s=r&&r[0],h=r&&r[1];n=a(n,s),o=a(o,h),n=this.containDrag("x",n,s),o=this.containDrag("y",o,h),n="y"==this.options.axis?0:n,o="x"==this.options.axis?0:o,this.position.x=this.startPosition.x+n,this.position.y=this.startPosition.y+o,this.dragPoint.x=n,this.dragPoint.y=o,this.dispatchEvent("dragMove",t,[i,e])}},g.containDrag=function(t,i,e){if(!this.options.containment)return i;var n="x"==t?"width":"height",o=this.relativeStartPosition[t],r=a(-o,e,"ceil"),s=this.containSize[n];return s=a(s,e,"floor"),Math.min(s,Math.max(r,i))},g.pointerUp=function(t,i){this.element.classList.remove("is-pointer-down"),this.dispatchEvent("pointerUp",t,[i]),this._dragPointerUp(t,i)},g.dragEnd=function(t,i){this.isEnabled&&(c&&(this.element.style[c]="",this.setLeftTop()),this.element.classList.remove("is-dragging"),this.dispatchEvent("dragEnd",t,[i]))},g.animate=function(){if(this.isDragging){this.positionDrag();var t=this;d(function(){t.animate()})}},g.setLeftTop=function(){this.element.style.left=this.position.x+"px",this.element.style.top=this.position.y+"px"},g.positionDrag=function(){this.element.style[c]="translate3d( "+this.dragPoint.x+"px, "+this.dragPoint.y+"px, 0)"},g.staticClick=function(t,i){this.dispatchEvent("staticClick",t,[i])},g.enable=function(){this.isEnabled=!0},g.disable=function(){this.isEnabled=!1,this.isDragging&&this.dragEnd()},g.destroy=function(){this.disable(),this.element.style[c]="",this.element.style.left="",this.element.style.top="",this.element.style.position="",this.unbindHandles(),this.$element&&this.$element.removeData("draggabilly")},g._init=n,f&&f.bridget&&f.bridget("draggabilly",s),s});

$('#algorithm_info').keyup(function () {
    $("#edit-but a").removeClass("disabled");
});

function make_dir() {
    if(!$('#add-dir a').hasClass("disabled")) {
        var sel = tree_view.selected();

        show_msg_yesno_id({
            id: "#popup-msg-create-dir",
            onYes: function() {
                $.jsonRPC.request('path_create', {
                        params: [
                            sel.path + '/' + $('#popup-msg-create-dir-name').val()
                        ],
                        id: server.token,

                        success: function(result) {
                            tree_view.update()
                        },
                        error: function(result) {
                            if(result.error.code == 2) {
                                show_msg_ok_id({
                                    title : "Ошибка",
                                    text : "Некорректное имя",
                                    onOk : function() {}
                                });
                            } else {
                                alert(JSON.stringify(result.error))
                            }
                        }
                })
            },
            onNo: function() { }
        });
        $('#popup-msg-create-dir-path').html(sel.path + '/');
        $('#popup-msg-create-dir-name').val('Новая папка');
    }
}

function del_path() {
    if($('#del-but a').hasClass("disabled"))
        return true;

    var sel = tree_view.selected();

    $("#popup-msg-yesno-title").html("Удаление");
    $("#popup-msg-yesno-text").html("Удалить выбранный путь: " + sel.path + "?");

    show_msg_yesno_id({
        id : "#popup-msg-yesno",
        onYes : function() {
            $.jsonRPC.request("path_remove", {
                params: [sel.path],
                id: server.token,
                success: function(result) {
                    tree_view.update();

                    $('#edit-dir a').addClass('disabled');
                    $("#run-but a").addClass("disabled");
                    $("#del-but a").addClass("disabled");
                    $("#add-but a").addClass("disabled");
                    $("#add-dir-but a").addClass("disabled");
                },
                error: function(result) {
                    show_msg_ok_id({
                        title : "Ошибка",
                        text : "Невозможно удалить этот ресурс!",
                        onOk : function() {}
                    });
                }
            });
        },
        onNo : function() {
        }
    });
}

function load(src) {
    myDiagram.model.linkFromPortIdProperty = "fromPort";
    myDiagram.model.linkToPortIdProperty = "toPort";
    myDiagram.model = go.Model.fromJson(src);
    myPalette.layoutDiagram(true);

    $('#panel_message').css("display", "none");
    $('#panel_flowchart').css("display", "block");
}

function create() {
    if($('#add-but a').hasClass("disabled"))
        return true;

    $("#popup-msg-yesno-title").html("Сохранение");
    $("#popup-msg-yesno-text").html("Текущий алгоритм не сохранен, изменения будут потеряны. Все равно продолжить?");

    var do_create = function() {
        var template = '    { "class": "go.GraphLinksModel",       ' +
        '      "linkFromPortIdProperty": "fromPort",' +
        '      "linkToPortIdProperty": "toPort",    ' +
        '      "nodeDataArray": [                   ' +
        ' {"category":"Start", "text":"Начало", "key":-1, "loc":"-27.76666259765625 -339"}, ' +
        ' {"category":"End", "text":"Конец", "key":-4, "loc":"-0.76666259765625 97"} ' +
        '     ],                                    ' +
        '      "linkDataArray": [                   ' +
        '    ]}                                     ';

        load(template);

        var source = myDiagram.model.toJson();
        algorithm.source = source;
        algorithm.name = "Новый алгоритм";
        algorithm.path = tree_view.selected().path + '/' + algorithm.name;
        algorithm.is_new = true;
        $('#algorithm_info').val(algorithm.name);

        model_reload = true;
    }

    if(!$('#edit-but a').hasClass("disabled")) {
        show_msg_yesno_id({
                id : "#popup-msg-yesno",
                onYes : function() {
                    do_create();
                },
                onNo : function() {
                }
            });
    } else {
        do_create();
    }
}

function save() {
   if($('#edit-but a').hasClass("disabled"))
    return true;

    var source = myDiagram.model.toJson();
    algorithm.source = source;

    var new_name = $('#algorithm_info').val();
    var new_path = algorithm.path.substr(0, algorithm.path.length - algorithm.name.length) + new_name;

    var do_save = function() {
        var cmd = !algorithm.is_new ? 'algorithm_update' : 'algorithm_create';
        $.jsonRPC.request(cmd, {
            params: [new_path, algorithm],
            id: server.token,
            success: function(result) {},
            error: function(result) {
                show_msg_ok_id({
                    title : "Ошибка",
                    text : "Невозможно сохранить алгоритм по этому пути!",
                    onOk : function() {}
                });
            }
        });
        if(algorithm.is_new)
            tree_view.update();
    }

    if(new_name != algorithm.name && !algorithm.is_new) {
        $.jsonRPC.request('path_move', {
            params: [
                algorithm.path, new_path
            ],
            id: server.token,

            success: function(result) {
                tree_view.update();
                do_save();
                algorithm.name = new_name;
                algorithm.path = new_path;
            },
            error: function(result) {
                if(result.error.code == 2) {
                    show_msg_ok_id({
                        title : "Ошибка",
                        text : "Невозможно сохранить алгоритм: новое имя некорректно",
                        onOk : function() {}
                    });
                } else {
                    alert(JSON.stringify(result.error));
                }

                return false;
            }
        })
    } else {
        do_save();
    }

    myDiagram.isModified = false;
    $('#edit-but a').addClass("disabled")

    return true;
}

function exec() {
   if($('#run-but a').hasClass("disabled"))
    return;

    var variables = {};
    var output_spec = {};

    var filterFloat = function (value) {
        if(/^(\-|\+)?([0-9]+(\.[0-9]+)?|Infinity)$/g
          .test(value))
          return Number(value);
      return NaN;
    }

    var filterName = function (value) {
        return /[a-zA-Z_]+[0-9]*/g.test(value);
    }

    var filterNameList = function(value) {
        return /[a-zA-Z_]+[0-9]*(,[\s]*[a-zA-Z_]+[0-9]*)*/g.test(value);
    }

    var nodes = myDiagram.model.nodeDataArray;
    nodes.forEach(function(n) {
        if(n.category == "Act") {
            var lines = n.text.split('\n');

            lines.forEach(function(l) {
                if(l.indexOf(":=") != -1) {
                    var parts = l.split(':=');

                    if(parts.length == 2 && filterName(parts[0].trim()) && !isNaN(filterFloat(parts[1].trim())))
                        variables[parts[0].trim()] = filterFloat(parts[1].trim());
                }
            });
        }
        if(n.category == 'Out') {
            if(filterNameList(n.text.trim())) {
                var parts = n.text.trim().split(',');
                parts.forEach(function(p) {
                    output_spec[p.trim()] = 0;
                });
            }
        }
    });

    var template = '<tr>' +
                    '<td>{name} =</td>' +
                    '<td><input id="run_var_{name}" type="text" class="form_input" value="{value}"/>' +
                    '</td></tr>';
    var html = "";

    for(var v in variables) {
        var html_item = template;
        html_item = html_item.replace(/\{name\}/g, v);
        html_item = html_item.replace("{value}", variables[v]);
        html += html_item;
    }

    var has_output = Object.keys(output_spec).length > 0;

    if(!has_output) {
        show_msg_ok_id({title : "Ошибка",
            text : "Отсутствуют выходные переменные! " +
                    "Используйте блок \"Вывод\", чтобы указать выходные переменные.", onOk : function() {}
         });
        return;
    }

    $('#popup-start-text').html(html);

    $("#popup-start .popup-preloader").hide();
    $("#popup-start .popup-modal-yes").removeClass("disabled");
    $("#popup-start .popup-modal-no").removeClass("disabled");

    $("#popup-start-result").hide();

    var popup = show_msg_yesno_id({
        id : "#popup-start",
        onYes: function() {
            $("#popup-start .popup-preloader").show();
            $("#popup-start .popup-modal-yes").addClass("disabled");
            $("#popup-start .popup-modal-no").addClass("disabled");

            for (var v in variables) {
                variables[v] = filterFloat($('#run_var_' + v).val());

                if(isNaN(variables[v])) {
                    popup.close();

                    show_msg_ok_id({
                        title : "Ошибка",
                        text : "Некорректное значение переменной " + v,
                        onOk : function() {}
                    });

                    return;
                }
            }

            $.jsonRPC.request('algorithm_exec', {
                params: [
                    { input_spec: [], output_spec: Object.keys(output_spec), source:  myDiagram.model.toJson() },
                    variables
                ],
                id: server.token,

                success: function(result) {
                    var html = '';

                    for(var v in result.result)
                        html += v + " = " + result.result[v] + " <br/>";

                    $("#popup-start-result").show();
                    $("#popup-start-result-text").html(html);
                    $("#popup-start .popup-preloader").hide();
                    $("#popup-start .popup-modal-yes").removeClass("disabled");
                    $("#popup-start .popup-modal-no").removeClass("disabled");
                },
                error: function(result) {
                    popup.close();

                    show_msg_ok_id({
                        title : "Ошибка исполнения",
                        text : result.error.message.replace('\n', '<br/>'),
                        onOk : function() {}
                    });
                }
            });
        },
        dontClose : true,
        onNo: function() {}
    });
}

function rename_dir() {
    if(!$('#edit-dir a').hasClass("disabled")) {
        var sel = tree_view.selected();

        show_msg_yesno_id({
            id: "#popup-msg-rename",
            onYes: function() {
                $.jsonRPC.request('path_move', {
                        params: [
                            sel.path,
                            sel.path.substr(0, sel.path.length - sel.name.length) + $('#popup-msg-rename-name').val()
                        ],
                        id: server.token,

                        success: function(result) {
                            tree_view.update()
                        },
                        error: function(result) {
                            if(result.error.code == 2) {
                                show_msg_ok_id({
                                    title : "Ошибка",
                                    text : "Переименование невозможно.",
                                    onOk : function() {}
                                });
                            } else {
                                alert(JSON.stringify(result.error))
                            }
                        }
                });
            },
            onNo: function() { }
        });
        $('#popup-msg-rename-path').html(sel.path);
        $('#popup-msg-rename-name').val(sel.name);
    }
}

function show_msg_yesno_id(params) {
    $.magnificPopup.open({
        items: {
            type: 'inline',
            src: params.id
        },
        closeOnBgClick: false,
        showCloseBtn: false,
        enableEscapeKey: false
    });

    var $draggable = $(params.id).draggabilly({
      containment: 'body',
      handle: '.popup-title'
    })

    $(document).off('click', params.id + ' .popup-modal-yes');
    $(document).off('click', params.id + ' .popup-modal-no');

    $(document).on('click', params.id + ' .popup-modal-yes', function (e) {
        e.preventDefault();

        if($(params.id + ' .popup-modal-yes').hasClass("disabled"))
            return;

        if(!('dontClose' in params)) {
            $.magnificPopup.close();
            $draggable.draggabilly('destroy');
        }

        params.onYes();
    });
    $(document).on('click', params.id + ' .popup-modal-no', function (e) {
        e.preventDefault();

        if($(params.id + ' .popup-modal-no').hasClass("disabled"))
            return;

        $.magnificPopup.close();
        $draggable.draggabilly('destroy');

        params.onNo();
    });

    return {
        close: function() {
            $.magnificPopup.close();
            $draggable.draggabilly('destroy');
        }
    }
}

function show_msg_ok_id(params) {
    if(!('id' in params))
        params.id = "#popup-msg-ok";

    $.magnificPopup.open({
        items: {
            type: 'inline',
            src: params.id
        }
    });

    var $draggable = $(params.id).draggabilly({
      containment: 'body',
      handle: '.popup-title'
    })

    if(params.id == '#popup-msg-ok') {
        $("#popup-msg-ok-title").html(params.title);
        $("#popup-msg-ok-text").html(params.text);
    }

    $(document).off('click', params.id + ' .popup-modal-ok');
    $(document).on('click', params.id + ' .popup-modal-ok', function (e) {
        e.preventDefault();
        $.magnificPopup.close();
        $draggable.draggabilly('destroy');

        params.onOk();
    });
}