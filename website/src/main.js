import Vue from 'vue'
import VueRouter from 'vue-router'
import CartController from './cart.js'
import Home from './Home.vue'
import Products from './Products.vue'
import Product from './Product.vue'
import Cart from './Cart.vue'
import CartButton from './Cart-Button.vue'
import ThankYou from './ThankYou.vue'

const API_ENDPOINT = process.env.GATEWAY_ENDPOINT || "http://localhost:5000"
let _cart = new CartController(API_ENDPOINT)

Vue.use(VueRouter)
Vue.component('cart-button', CartButton)
Vue.mixin({
  data() {
    return {
      get API_ENDPOINT() { return API_ENDPOINT },
      get cart() { return _cart }
    }
  }
})

// install global filters
const filters = {
  capitalize: function (value) {
    if (!value) return ''
    value = value.toString()
    return value.charAt(0).toUpperCase() + value.slice(1)
  },
  round: function(value) {
    return Math.round(value)
  }
}

for (const f in filters) {
  Vue.filter(f, filters[f])
}

const router = new VueRouter({
  mode: 'history',
  routes: [
    {path: '/', component: Home},
    {path: '/products', component: Products, props: (route) => ({ query: route.query })},
    {path: '/products/:id', component: Product, props: true},
    {path: '/cart', component: Cart},
    {path: '/thankyou/:id', component: ThankYou, props: true}
  ]
})

new Vue({
  router,
}).$mount('#app')
