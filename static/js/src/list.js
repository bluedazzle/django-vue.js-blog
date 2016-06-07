/**
 * Created by RaPoSpectre on 5/24/16.
 */

Vue.config.delimiters = ['${', '}}'];
var vm = new Vue({
    el: '#vList',
    data: {
        cid: -1,
        tag: -1,
        is_paginated: false
    },
    methods: {
        getData: function (page) {
            if (page != undefined) {
                this.$set('articles', null);
                this.$set('pageObj', null);
                url = '';
                if (this.cid != -1) {
                    url = generateUrl('api/v1/articles') + '&page=' + page + '&cid=' + this.cid;
                }
                if (this.tag != -1) {
                    url = generateUrl('api/v1/articles') + '&page=' + page + '&tag=' + this.tag;
                }
                if (this.cid == -1 && this.tag == -1) {
                    url = generateUrl('api/v1/articles') + '&page=' + page;
                }
                this.$http.get(url, function (data) {
                    if (data.status == 1) {
                        this.$set('articles', data.body.article_list);
                        this.$set('pageObj', data.body.page_obj);
                        this.is_paginated = data.body.is_paginated;
                    }
                })
            }
        },
        setCid: function (cid) {
            this.cid = cid;
            this.tag = -1;
            this.getData(1);
        },
        setTag: function (tag) {
            this.tag = tag;
            this.cid = -1;
            this.getData(1);
        }

    },
    ready: function () {
        this.getData(1);
    },
    computed: {
        noData: function () {
            return this.articles == null;
        }
    }
});

