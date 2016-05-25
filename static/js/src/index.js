/**
 * Created by RaPoSpectre on 5/25/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vIndex',
    data: {},
    methods: {
        getData: function () {
            this.$set('articles', null);
            url = generateUrl('api/v1/articles') + '&all=1';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('articles', data.body.article_list);
                }
            })
        }

    },
    ready: function () {
        this.getData();
    },
    computed: {
        noData: function () {
            return this.articles == null;
        }
    }
});
