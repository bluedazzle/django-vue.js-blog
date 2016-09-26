/**
 * Created by RaPoSpectre on 5/26/16.
 */

$('.ui.accordion')
    .accordion()
;
$('.dropdown').dropdown({
    on: 'hover'
});

var editor;

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vModifyArticle',
    data: {
        article: {
            id: -1,
            content: '',
            title: '',
            slug: '',
            classification: -1,
            tags: []
        }
    },
    methods: {
        getData: function () {
            if (this.article.id != '') {
                var url = generateUrl('api/v1/article/' + this.article.id);
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        var blog = data.body.article;
                        this.article.content = blog.content;
                        this.article.title = blog.title;
                        this.article.slug = blog.slug;
                        this.article.classification = blog.classification_id;
                        var arr = [];
                        for (var i in blog.tag_list) {
                            arr.push(blog.tag_list[i].id.toString());
                        }
                        this.article.tags = arr;
                        editor = editormd("mdEditor", {
                            height: 740,
                            path: '/s/lib/',
                            markdown: this.article.content,
                            codeFold: true,
                            //syncScrolling : false,
                            saveHTMLToTextarea: true,    // 保存 HTML 到 Textarea
                            searchReplace: true,
                            //watch : false,                // 关闭实时预览
                            htmlDecode: "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启
                            //toolbar  : false,             //关闭工具栏
                            //previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
                            emoji: true,
                            taskList: true,
                            tocm: true,         // Using [TOCM]
                            tex: true,                   // 开启科学公式TeX语言支持，默认关闭
                            flowChart: true,             // 开启流程图支持，默认关闭
                            sequenceDiagram: true,       // 开启时序/序列图支持，默认关闭,
                            //dialogLockScreen : false,   // 设置弹出层对话框不锁屏，全局通用，默认为true
                            //dialogShowMask : false,     // 设置弹出层对话框显示透明遮罩层，全局通用，默认为true
                            //dialogDraggable : false,    // 设置弹出层对话框不可拖动，全局通用，默认为true
                            //dialogMaskOpacity : 0.4,    // 设置透明遮罩层的透明度，全局通用，默认值为0.1
                            //dialogMaskBgColor : "#000", // 设置透明遮罩层的背景颜色，全局通用，默认为#fff
                            imageUpload: true,
                            imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
                            imageUploadURL: "/api/v1/upload"
                        });
                    }
                    $('#tag').dropdown('set exactly', arr);
                    $('#classification').dropdown('set selected', this.article.classification);
                })
            } else {
                editor = editormd("mdEditor", {
                    height: 740,
                    path: '/s/lib/',
                    markdown: '',
                    codeFold: true,
                    //syncScrolling : false,
                    saveHTMLToTextarea: true,    // 保存 HTML 到 Textarea
                    searchReplace: true,
                    //watch : false,                // 关闭实时预览
                    htmlDecode: "style,script,iframe|on*",            // 开启 HTML 标签解析，为了安全性，默认不开启
                    //toolbar  : false,             //关闭工具栏
                    //previewCodeHighlight : false, // 关闭预览 HTML 的代码块高亮，默认开启
                    emoji: true,
                    taskList: true,
                    tocm: true,         // Using [TOCM]
                    tex: true,                   // 开启科学公式TeX语言支持，默认关闭
                    flowChart: true,             // 开启流程图支持，默认关闭
                    sequenceDiagram: true,       // 开启时序/序列图支持，默认关闭,
                    //dialogLockScreen : false,   // 设置弹出层对话框不锁屏，全局通用，默认为true
                    //dialogShowMask : false,     // 设置弹出层对话框显示透明遮罩层，全局通用，默认为true
                    //dialogDraggable : false,    // 设置弹出层对话框不可拖动，全局通用，默认为true
                    //dialogMaskOpacity : 0.4,    // 设置透明遮罩层的透明度，全局通用，默认值为0.1
                    //dialogMaskBgColor : "#000", // 设置透明遮罩层的背景颜色，全局通用，默认为#fff
                    imageUpload: true,
                    imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
                    imageUploadURL: "/api/v1/upload"
                });
            }
        },
        getClassification: function () {
            var url = generateUrl('api/v1/classifications');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('classifications', data.body.classification_list);
                }
            })
        },
        getTags: function () {
            var url = generateUrl('api/v1/tags');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('tags', data.body.tag_list);
                }
            })
        },
        submitArticle: function () {
            var url = generateUrl('admin/api/article');
            this.article.content = editor.getMarkdown();
            this.$http.post(url, this.article, function (data) {
                if (data.status == 1) {
                    window.location = '/admin/article';
                }
            })
        }
    },
    ready: function () {
        this.getClassification();
        this.getTags();
        this.getData(1);
    },
    computed: {
        noData: function () {
            return this.articles == null;
        }
    }
});

