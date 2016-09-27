/**
 * Created by RaPoSpectre on 5/24/16.
 */

jQuery(function ($) {
        $(document).ready(function () {
            //enabling stickUp on the '.navbar-wrapper' class
            $('#myNav').stickUp();
        });
    });

    // Initialize collapse button
    $(".button-collapse").sideNav();
    // Initialize collapsible (uncomment the line below if you use the dropdown variation)
    //$('.collapsible').collapsible();


Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vBase',
    data: {},
    methods: {
        getData: function () {
            var url = generateUrl('api/v1/articles') + '&query=latest';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('latest', data.body.article_list);
                }
            });
            url = generateUrl('api/v1/articles') + '&query=popular';
            this.$http.get(url, function (data) {
                if (data.status == 1) {
                    this.$set('popular', data.body.article_list);
                }
            });
        }

    },
    ready: function () {
        this.getData();
    },
    computed: {
        noLatest: function () {
            return this.latest == null;
        },
        noPopular: function () {
            return this.popular == null;
        }
    }
});

