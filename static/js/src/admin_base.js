/**
 * Created by RaPoSpectre on 5/24/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vBase',
    data: {},
    methods: {
        getData: function () {
            var url = generateUrl('admin/api/info');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('admin', data.body);
                }
            });
        },
        logout: function () {
            var url = generateUrl('admin/api/logout');
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    window.location = '/admin/login';
                }
            });
        }
    },
    ready: function () {
        this.getData();
    }
});

