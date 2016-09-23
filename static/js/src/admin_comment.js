/**
 * Created by RaPoSpectre on 6/24/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vComment',
    data: {},
    methods: {
        getData: function (page) {
            var url = generateUrl('admin/api/comments') + '&page=' + page;
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('comments', data.body.comment_list);
                    this.$set('pageObj', data.body.page_obj);
                }
            });
        },
        publishArticle: function (id) {
            var url = generateUrl('admin/api/comment/' + id + '/review');
            this.$http.get(url, function (data) {
                if(data.status == 1){
                    $.scojs_message('留言状态更改成功', $.scojs_message.TYPE_OK);
                    this.getData(1);
                }else{
                    $.scojs_message(data.msg, $.scojs_message.TYPE_ERROR);
                }
            })
        }


    },
    ready: function () {
        this.getData(1);
    },
    computed: {
        noData: function () {
            return this.comments == null;
        }
    }
});
