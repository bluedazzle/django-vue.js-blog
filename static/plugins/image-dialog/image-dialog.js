/*!
 * Image (upload) dialog plugin for Editor.md
 *
 * @file        image-dialog.js
 * @author      pandao
 * @version     1.3.4
 * @updateTime  2015-06-09
 * {@link       https://github.com/pandao/editor.md}
 * @license     MIT
 */

(function () {

    var factory = function (exports) {

        var pluginName = "image-dialog";

        exports.fn.imageDialog = function () {

            var _this = this;
            var cm = this.cm;
            var lang = this.lang;
            var editor = this.editor;
            var settings = this.settings;
            var cursor = cm.getCursor();
            var selection = cm.getSelection();
            var imageLang = lang.dialog.image;
            var classPrefix = this.classPrefix;
            var iframeName = classPrefix + "image-iframe";
            var dialogName = classPrefix + pluginName, dialog;

            cm.focus();

            var loading = function (show) {
                var _loading = dialog.find("." + classPrefix + "dialog-mask");
                _loading[(show) ? "show" : "hide"]();
            };

            if (editor.find("." + dialogName).length < 1) {
                var guid = (new Date).getTime();
                var action = settings.imageUploadURL + (settings.imageUploadURL.indexOf("?") >= 0 ? "&" : "?") + "guid=" + guid;

                if (settings.crossDomainUpload) {
                    action += "&callback=" + settings.uploadCallbackURL + "&dialog_id=editormd-image-dialog-" + guid;
                }

                var dialogContent = ( (settings.imageUpload) ? "<form action=\"" + action + "\" target=\"" + iframeName + "\" method=\"post\" enctype=\"multipart/form-data\" class=\"" + classPrefix + "form\">" : "<div class=\"" + classPrefix + "form\">" ) +
                    ( (settings.imageUpload) ? "<iframe name=\"" + iframeName + "\" id=\"" + iframeName + "\" guid=\"" + guid + "\"></iframe>" : "" ) +
                    "<label>" + imageLang.url + "</label>" +
                    "<input type=\"text\" data-url />" + (function () {
                        return (settings.imageUpload) ? "<div class=\"" + classPrefix + "file-input\">" +
                        "<input type=\"file\" name=\"" + classPrefix + "image-file\" accept=\"image/*\" />" +
                        "<input type=\"submit\" value=\"" + imageLang.uploadButton + "\" />" +
                        "</div>" +
                        "<div class=\"" + classPrefix + "file-input\">" +
                        "<input type=\"file\" name=\"qiniu-image-file\" accept=\"image/*\" />" +
                        "<input type=\"button\" id=\"qn\" value=\"七牛云传\" />" +
                        "</div>" : "";
                    })() +
                    "<br/>" +
                    "<label>" + imageLang.alt + "</label>" +
                    "<input type=\"text\" value=\"" + selection + "\" data-alt />" +
                    "<br/>" +
                    "<label>" + imageLang.link + "</label>" +
                    "<input type=\"text\" value=\"http://\" data-link />" +
                    "<br/>" +
                    ( (settings.imageUpload) ? "</form>" : "</div>");

                //var imageFooterHTML = "<button class=\"" + classPrefix + "btn " + classPrefix + "image-manager-btn\" style=\"float:left;\">" + imageLang.managerButton + "</button>";

                dialog = this.createDialog({
                    title: imageLang.title,
                    width: (settings.imageUpload) ? 465 : 380,
                    height: 454,
                    name: dialogName,
                    content: dialogContent,
                    mask: settings.dialogShowMask,
                    drag: settings.dialogDraggable,
                    lockScreen: settings.dialogLockScreen,
                    maskStyle: {
                        opacity: settings.dialogMaskOpacity,
                        backgroundColor: settings.dialogMaskBgColor
                    },
                    buttons: {
                        enter: [lang.buttons.enter, function () {
                            var url = this.find("[data-url]").val();
                            var alt = this.find("[data-alt]").val();
                            var link = this.find("[data-link]").val();

                            if (url === "") {
                                alert(imageLang.imageURLEmpty);
                                return false;
                            }

                            var altAttr = (alt !== "") ? " \"" + alt + "\"" : "";

                            if (link === "" || link === "http://") {
                                cm.replaceSelection("![" + alt + "](" + url + altAttr + ")");
                            }
                            else {
                                cm.replaceSelection("[![" + alt + "](" + url + altAttr + ")](" + link + altAttr + ")");
                            }

                            if (alt === "") {
                                cm.setCursor(cursor.line, cursor.ch + 2);
                            }

                            this.hide().lockScreen(false).hideMask();

                            return false;
                        }],

                        cancel: [lang.buttons.cancel, function () {
                            this.hide().lockScreen(false).hideMask();

                            return false;
                        }]
                    }
                });

                dialog.attr("id", classPrefix + "image-dialog-" + guid);

                if (!settings.imageUpload) {
                    return;
                }

                var fileInput = dialog.find("[name=\"" + classPrefix + "image-file\"]");

                fileInput.bind("change", function () {
                    var fileName = fileInput.val();
                    var isImage = new RegExp("(\\.(" + settings.imageFormats.join("|") + "))$"); // /(\.(webp|jpg|jpeg|gif|bmp|png))$/

                    if (fileName === "") {
                        alert(imageLang.uploadFileEmpty);

                        return false;
                    }

                    if (!isImage.test(fileName)) {
                        alert(imageLang.formatNotAllowed + settings.imageFormats.join(", "));

                        return false;
                    }

                    loading(true);

                    var submitHandler = function () {

                        var uploadIframe = document.getElementById(iframeName);

                        uploadIframe.onload = function () {

                            loading(false);

                            var body = (uploadIframe.contentWindow ? uploadIframe.contentWindow : uploadIframe.contentDocument).document.body;
                            var json = (body.innerText) ? body.innerText : ( (body.textContent) ? body.textContent : null);

                            json = (typeof JSON.parse !== "undefined") ? JSON.parse(json) : eval("(" + json + ")");

                            if (!settings.crossDomainUpload) {
                                if (json.success === 1) {
                                    dialog.find("[data-url]").val(json.url);
                                }
                                else {
                                    alert(json.message);
                                }
                            }

                            return false;
                        };
                    };

                    dialog.find("[type=\"submit\"]").bind("click", submitHandler).trigger("click");
                });

                var qiniuInput = dialog.find("[name=\"qiniu-image-file\"]");

                qiniuInput.bind("change", function () {
                    var fileName = qiniuInput.val();
                    var isImage = new RegExp("(\\.(" + settings.imageFormats.join("|") + "))$"); // /(\.(webp|jpg|jpeg|gif|bmp|png))$/

                    if (fileName === "") {
                        alert(imageLang.uploadFileEmpty);

                        return false;
                    }

                    if (!isImage.test(fileName)) {
                        alert(imageLang.formatNotAllowed + settings.imageFormats.join(", "));

                        return false;
                    }

                    loading(true);

                    var submitHandler = function () {
                        var url = generateUrl('/api/v1/upload');
                        var uploader = Qiniu.uploader({
                            runtimes: 'html5,flash,html4',      // 上传模式，依次退化
                            browse_button: 'qn',         // 上传选择的点选按钮，必需
                            // 在初始化时，uptoken，uptoken_url，uptoken_func三个参数中必须有一个被设置
                            // 切如果提供了多个，其优先级为uptoken > uptoken_url > uptoken_func
                            // 其中uptoken是直接提供上传凭证，uptoken_url是提供了获取上传凭证的地址，如果需要定制获取uptoken的过程则可以设置uptoken_func
                            // uptoken : '<Your upload token>', // uptoken是上传凭证，由其他程序生成
                             uptoken_url: url,         // Ajax请求uptoken的Url，强烈建议设置（服务端提供）
                            // uptoken_func: function(file){    // 在需要获取uptoken时，该方法会被调用
                            //    // do something
                            //    return uptoken;
                            // },
                            get_new_uptoken: true,             // 设置上传文件的时候是否每次都重新获取新的uptoken
                            // downtoken_url: '/downtoken',
                            // Ajax请求downToken的Url，私有空间时使用，JS-SDK将向该地址POST文件的key和domain，服务端返回的JSON必须包含url字段，url值为该文件的下载地址
                            // unique_names: true,              // 默认false，key为文件名。若开启该选项，JS-SDK会为每个文件自动生成key（文件名）
                            // save_key: true,                  // 默认false。若在服务端生成uptoken的上传策略中指定了sava_key，则开启，SDK在前端将不对key进行任何处理
                            domain: 'http://ocpgdokmz.bkt.clouddn.com/',     // bucket域名，下载资源时用到，必需
                            container: 'container',             // 上传区域DOM ID，默认是browser_button的父元素
                            max_file_size: '100mb',             // 最大文件体积限制
                            flash_swf_url: 'http://cdn.staticfile.org/Plupload/2.1.1/Moxie.swf',  //引入flash，相对路径
                            max_retries: 3,                     // 上传失败最大重试次数
                            dragdrop: true,                     // 开启可拖曳上传
                            drop_element: 'container',          // 拖曳上传区域元素的ID，拖曳文件或文件夹后可触发上传
                            chunk_size: '4mb',                  // 分块上传时，每块的体积
                            log_level: 5,
                            auto_start: true,                   // 选择文件后自动上传，若关闭需要自己绑定事件触发上传
                            //x_vars : {
                            //    查看自定义变量
                            //    'time' : function(up,file) {
                            //        var time = (new Date()).getTime();
                            // do something with 'time'
                            //        return time;
                            //    },
                            //    'size' : function(up,file) {
                            //        var size = file.size;
                            // do something with 'size'
                            //        return size;
                            //    }
                            //},
                            init: {
                                'FilesAdded': function (up, files) {
                                    plupload.each(files, function (file) {
                                        // 文件添加进队列后，处理相关的事情
                                    });
                                },
                                'BeforeUpload': function (up, file) {
                                    // 每个文件上传前，处理相关的事情
                                },
                                'UploadProgress': function (up, file) {
                                    // 每个文件上传时，处理相关的事情
                                },
                                'FileUploaded': function (up, file, info) {
                                    // 每个文件上传成功后，处理相关的事情
                                    // 其中info是文件上传成功后，服务端返回的json，形式如：
                                    // {
                                    //    "hash": "Fh8xVqod2MQ1mocfI4S4KpRL6D98",
                                    //    "key": "gogopher.jpg"
                                    //  }
                                    // 查看简单反馈
                                     var domain = up.getOption('domain');
                                     var res = parseJSON(info);
                                     var sourceLink = domain + res.key;
                                    dialog.find("[data-url]").val(sourceLink);
                                },
                                'Error': function (up, err, errTip) {
                                    //上传出错时，处理相关的事情
                                },
                                'UploadComplete': function () {
                                    //队列文件处理完毕后，处理相关的事情
                                },
                                'Key': function (up, file) {
                                    // 若想在前端对每个文件的key进行个性化处理，可以配置该函数
                                    // 该配置必须要在unique_names: false，save_key: false时才生效

                                    var key = "";
                                    // do something with key here
                                    return key
                                }
                            }
                        });


                        //      if (json.success === 1)
                        //      {
                        //          dialog.find("[data-url]").val(json.url);
                        //      }
                        //      else
                        //      {
                        //          alert(json.message);
                        //      }
                        //    }
                        //
                        //    return false;
                        //};
                    };

                    dialog.find("[id=\"qn\"]").bind("click", submitHandler).trigger("click");
                });
            }

            dialog = editor.find("." + dialogName);
            dialog.find("[type=\"text\"]").val("");
            dialog.find("[type=\"file\"]").val("");
            dialog.find("[data-link]").val("http://");

            this.dialogShowMask(dialog);
            this.dialogLockScreen();
            dialog.show();

        };

    };

    // CommonJS/Node.js
    if (typeof require === "function" && typeof exports === "object" && typeof module === "object") {
        module.exports = factory;
    }
    else if (typeof define === "function")  // AMD/CMD/Sea.js
    {
        if (define.amd) { // for Require.js

            define(["editormd"], function (editormd) {
                factory(editormd);
            });

        } else { // for Sea.js
            define(function (require) {
                var editormd = require("./../../editormd");
                factory(editormd);
            });
        }
    }
    else {
        factory(window.editormd);
    }

})();
