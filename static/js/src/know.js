/**
 * Created by RaPoSpectre on 6/24/16.
 */


Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vKnow',
    data: {
        is_paginated: false,
        query: ''
    },
    methods: {
        getData: function (page) {
            if (page != undefined) {
                this.$set('articles', null);
                this.$set('pageObj', null);
                var url = '';
                if (this.query != ''){
                    url = generateUrl('api/v1/knowledge') + '&page=' + page + '&query=' + this.query;
                }else {
                    url = generateUrl('api/v1/knowledge') + '&page=' + page;
                }

                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('knows', data.body.knowledge_list);
                        this.$set('pageObj', data.body.page_obj);
                        this.is_paginated = data.body.is_paginated;
                    }
                })
            }
        },
        showBody: function (index, id) {
            var know = this.knows[index];
            var coll = 'coll' + id.toString();
            $("#" + coll).empty();
            var testEditormdView = editormd.markdownToHTML(coll, {
                        markdown: know.answer,//+ "\r\n" + $("#append-test").text(),
                        htmlDecode: "style,script,iframe",  // you can filter tags decode
                        tocm: true,    // Using [TOCM]
                        emoji: true,
                        taskList: true,
                        tex: true,  // 默认不解析
                        flowChart: true,  // 默认不解析
                        sequenceDiagram: true  // 默认不解析

                    });
        }

    },
    ready: function () {
        this.getData(1);
    },
    computed: {
        noData: function () {
            return this.knows == null;
        }
    }
});

$(document).ready(function () {
    $('.collapsible').collapsible({
        accordion: false // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
});