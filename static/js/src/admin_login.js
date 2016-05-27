/**
 * Created by RaPoSpectre on 5/26/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vLogin',
    data: {
        loginData: {
            username: '',
            password: ''
        }
    },
    methods: {
        login: function () {
            var url = generateUrl('admin/api/login');
            this.$http.post(url, this.loginData, function (data) {
                if (data.status == 1) {
                    window.location = '/admin/index';
                }
            });
        }


    },
    ready: function () {
    }
});
