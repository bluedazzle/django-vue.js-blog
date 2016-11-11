/**
 * Created by RaPoSpectre on 11/8/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vCollections',
    data: {},
    methods: {
        getData: function (page) {
            var url = generateUrl('api/v1/collections') + '&page=' + page;
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('collections', data.body.collection_list);
                    this.$set('pageObj', data.body.page_obj);
                }
            });
        },
        publishArticle: function (id) {
            var url = generateUrl('admin/api/knowledge/' + id + '/publish');
            this.$http.get(url, function (data) {
                if(data.status == 1){
                    $.scojs_message('姿势状态更改成功', $.scojs_message.TYPE_OK);
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
            return this.collections == null;
        }
    }
});
