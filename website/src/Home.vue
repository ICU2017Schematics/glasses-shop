<template>
  <div id = "home">
    <div id="carousel-example-generic" class="carousel slide" data-ride="carousel">
      <!-- Indicators -->
      <ol class="carousel-indicators">
        <li data-target="#carousel-example-generic" data-slide-to="0" class="active"></li>
        <li data-target="#carousel-example-generic" data-slide-to="1"></li>
        <li data-target="#carousel-example-generic" data-slide-to="2"></li>
        <li data-target="#carousel-example-generic" data-slide-to="3"></li>
      </ol>

      <!-- Wrapper for slides -->
      <div class="carousel-inner" role="listbox">
        <div class="item active">
          <img src="/shop/images/141020_category_banners_glasses_women.jpg" alt="...">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="item">
          <img src="/shop/images/141020_category_banners_glasses_men.jpg" alt="...">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="item">
          <img src="/shop/images/140925_category_banners_rimless_glasses.jpg" alt="...">
          <div class="carousel-caption">
          </div>
        </div>
        <div class="item">
          <img src="/shop/images/141020_category_banners_glasses_kids.jpg" alt="...">
          <div class="carousel-caption">
          </div>
        </div>
      </div>

      <!-- Controls -->
      <a class="left carousel-control" href="#carousel-example-generic" role="button" data-slide="prev">
        <span class="glyphicon glyphicon-chevron-left" aria-hidden="true"></span>
        <span class="sr-only">Previous</span>
      </a>
      <a class="right carousel-control" href="#carousel-example-generic" role="button" data-slide="next">
        <span class="glyphicon glyphicon-chevron-right" aria-hidden="true"></span>
        <span class="sr-only">Next</span>
      </a>
    </div>

    <h1>Gender</h1>
    <div class="row">
      <div class="col-xs-6 col-md-3" v-for="cat in filter('gender')">
          <div class="thumbnail">
              <router-link :to="`/products?gender=${cat.name}`">
                  <img :src="cat.image" :alt="cat.name">
              </router-link>

              <div class="caption">
                  <h3>{{ cat['name']}}</h3>
                  <p>{{ cat['description'] }}</p>
                  <p><router-link :to="`/products?gender=${cat.name}`" class="btn btn-primary" role="button">Browse</router-link></p>
              </div>
          </div>
      </div>
    </div>

    <h1>Rim Type</h1>
    <div class="row">
      <div class="col-xs-6 col-md-3" v-for="cat in filter('rim')">
          <div class="thumbnail">
              <router-link :to="`/products?rim=${cat.name}`">
                  <img :src="cat.image" :alt="cat.name">
              </router-link>

              <div class="caption">
                  <h3>{{ cat['name']}}</h3>
                  <p>{{ cat['description'] }}</p>
                  <p><router-link :to="`/products?rim=${cat.name}`" class="btn btn-primary" role="button">Browse</router-link></p>
              </div>
          </div>
      </div>
    </div>

    <h1>Shape</h1>
    <div class="row">
      <div class="col-xs-6 col-md-3" v-for="cat in filter('shape')">
          <div class="thumbnail">
              <router-link :to="`/products?shape=${cat.name}`">
                  <img :src="cat.image" :alt="cat.name">
              </router-link>

              <div class="caption">
                  <h3>{{ cat['name']}}</h3>
                  <p>{{ cat['description'] }}</p>
                  <p><router-link :to="`/products?shape=${cat.name}`" class="btn btn-primary" role="button">Browse</router-link></p>
              </div>
          </div>
      </div>
    </div>

    <h1>Material</h1>
    <div class="row">
      <div class="col-xs-6 col-md-3" v-for="cat in filter('material')">
          <div class="thumbnail">
              <router-link :to="`/products?material=${cat.name}`">
                  <img :src="cat.image" :alt="cat.name">
              </router-link>

              <div class="caption">
                  <h3>{{ cat['name']}}</h3>
                  <p>{{ cat['description'] }}</p>
                  <p><router-link :to="`/products?material=${cat.name}`" class="btn btn-primary" role="button">Browse</router-link></p>
              </div>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'hello',
  data () {
    return {
      data: []
    }
  },
  methods: {
    filter(by) {
      const filtered = this.data.filter(cat => cat.segment == by)
      return filtered
    }
  },
  created() {
    const axios = require('axios')
    const self = this
    const config = {
      headers: {
        'Accept': 'application/json'
      }
    }
    axios.get(this.API_ENDPOINT, config).then(res => {
      self.data = res.data
    })
  }
}
</script>

<style>
</style>
