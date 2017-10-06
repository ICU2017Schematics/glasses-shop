<template>
<div id="product">
    <h1>{{product.name}} Glasses</h1>
    <div class="row">
        <div class="col-md-6">
            <img class="img-responsive" :src="product.image" :alt="product.name">
            <div class="description-area">
                <h2>Description</h2>
                <p>{{product.description}}</p>
            </div>
        </div>
        <div class="dimensions col-md-2">
            <h4 class="text-center">Dimensions</h4>
            <p class="text-center">
                <img class="img-responsive center-block" src="http://www.globaleyeglasses.com/images/total_width.png" alt="">
                {{product.custom1}}
            </p>
            <p class="text-center">
                <img class="img-responsive center-block" src="http://www.globaleyeglasses.com/images/width_height.png" alt="">
                {{product.custom2}}
            </p>
            <p class="text-center">
                <img class="img-responsive center-block" src="http://www.globaleyeglasses.com/images/bridge.png" alt="">
                {{product.custom3}}
            </p>
            <p class="text-center">
                <img class="img-responsive center-block" src="http://www.globaleyeglasses.com/images/arm.png" alt="">
                {{product.custom4}}
            </p>
        </div>
        <div class="sellbox col-md-4">
            <h2>{{product.name}}</h2>
            <p>
                In Stock<br>
                <small>SKU: {{product.product_id}}</small>
            </p>
            <p>
                Gender: {{product.category1}}<br>
                Shape: {{product.category3}}<br>
                Material: {{product.category4}}<br>
                Rim Type: {{product.category2}}
            </p>
            </p>
            <p>
                <s>${{product.retail_price}}</s><br>
                <span class="sale-price">${{product.sale_price}}</span>
            </p>
            <p>
                <strong>INCLUDES:</strong><br>
                Case &amp; Cleaning Cloth<br>
                30 Day Returns
            </p>
            <button id="add-to-cart" type="button" class="btn btn-cart" v-on:click="addToCart"><i class="glyphicon glyphicon-shopping-cart"></i>Add To Cart</button>
        </div>
    </div>

</div>
</template>

<script>
export default {
    name: 'product',
    data() {
        return {
            product: {}
        }
    },
    created() {
        const url = this.API_ENDPOINT + window.location.pathname
        const axios = require('axios')
        const self = this
        const config = {
            headers: {
                'Accept': 'application/json'
            }
        }        
        axios.get(url, config).then(res => {
            self.product = res.data
        })
    },
    methods: {
        addToCart() { this.cart.addToCart(this.product) }
    }
  
}
</script>
