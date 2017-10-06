<template>
<div id="products">
    <h1>{{ category|capitalize}} Glasses</h1>
    <div class="row">
        <div class="col-xs-6 col-md-3" v-for="product in products">
            <div class="thumbnail">
                <router-link :to="`/products/${product.product_id}`">
                    <img :src="product.image" :alt="product.name">
                </router-link>

                <div class="caption">
                    <h3>{{product.name}}</h3>
                    <p>
                        <span class="sale-price">${{product.sale_price}}</span><br>
                        List Price: <s>${{product.retail_price}}</s><br>
                        Save: {{ product.percent_savings|round}}%
                    </p>
                    <p><router-link :to="`/products/${product.product_id}`" class="btn btn-primary" role="button">Learn More</router-link></p>
                </div>
            </div>
        </div>
    </div>
</div>
</template>

<script>
export default {
  name: 'products',
  data () {
    return {
        category: "",
        products: []
    }
  },
  methods: {
      init() {
        const url = this.API_ENDPOINT + window.location.pathname + window.location.search
        const axios = require('axios')
        const self = this
        const config = {
            headers: {
                'Accept': 'application/json'
            }
        }

        axios.get(url, config).then(res => {
            // get the category query. Unfortunately, the current API does not have a regular structure for search
            // so the query can be ?shape=Wayfarer, ?gender=Male, etc.
            //
            // Get the $route.query KV pair and use the value. ASSUMES only one query parameter on the URL
            self.category = Object.values(self.$route.query)[0]
            self.products = res.data
        })
      }
  },
  created() {
      this.init()
  },
  watch: {
      '$route' (to, from) {
          this.init()
      }
  }
}
</script>

