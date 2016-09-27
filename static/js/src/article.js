/**
 * Created by RaPoSpectre on 4/28/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vArticle',
    data: {
        comment: {
            content: '',
            reply: 0,
            cid: 0,
            tid: 0
        },
        title: '留下评论',
        aid: 0,
        no_comments: true,
        submit: false
    },
    methods: {
        replyMethod: function (cid, tid, nick) {
            this.comment.cid = cid;
            this.comment.tid = tid;
            this.comment.reply = 1;
            this.title = '@' + nick + ':'
        },
        createComment: function () {
            if(this.submit){
                return 1;
            }
            if(this.comment.content==''){
                $.scojs_message('请输入评论内容', $.scojs_message.TYPE_ERROR);
                return 1;
            }
            this.submit = true;
            url = generateUrl('api/v1/article/' + this.aid + '/comment');
            this.$http.post(url, this.comment, function (data) {
                if (data.status == 1) {
                    $.scojs_message('评论成功', $.scojs_message.TYPE_OK);
                    this.getComment();
                    this.clearComment();
                    this.submit = false;
                } else if (data.status == 3) {
                    window.location = data.body.url;
                } else {
                    $.scojs_message(data.msg, $.scojs_message.TYPE_ERROR);
                    this.submit = false;
                    this.clearComment();
                }
            })
        },
        clearComment: function () {
            this.comment.cid = 0;
            this.comment.tid = 0;
            this.comment.reply = 0;
            this.comment.content = '';
            this.title = '留下评论';
        },
        getData: function () {
            this.$set('article', null);
            url = generateUrl('api/v1/article/' + this.aid);
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('article', data.body.article);
                    var testEditormdView = editormd.markdownToHTML("article", {
                        markdown: this.article.content,//+ "\r\n" + $("#append-test").text(),
                        htmlDecode: "style,script,iframe",  // you can filter tags decode
                        tocm: true,    // Using [TOCM]
                        emoji: true,
                        taskList: true,
                        tex: true,  // 默认不解析
                        flowChart: true,  // 默认不解析
                        sequenceDiagram: true  // 默认不解析

                    });
                }
            })
        },
        getComment: function () {
            url = generateUrl('api/v1/article/' + this.aid + '/comments');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('comments', data.body.comment_list);
                    if(data.body.comment_list.length != 0){
                        this.no_comments = false;
                    }
                }
            })
        },
        getUserInfo: function () {
            url = generateUrl('api/v1/user/info');
            this.$http.get(url, function (data) {
                if (data.status == 1 || data.status == 3) {
                    this.$set('avatar', data.body.avatar);
                }
            })
        }
    },
    ready: function () {
        this.getData();
        this.getComment();
        this.getUserInfo();
    },
    computed: {
        noData: function () {
            return this.article == null;
        }
    }
});

